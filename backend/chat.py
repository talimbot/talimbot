import os
from datetime import datetime
from pathlib import Path

import requests
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1] / ".env.local")
load_dotenv(Path(__file__).parent / ".env")

default_db = "sqlite:///" + str(Path(__file__).parent / "data" / "chat.db")
url = os.getenv("DATABASE_URL", default_db).replace("postgres://", "postgresql://", 1)
engine = create_engine(url, pool_pre_ping=True)
Session = sessionmaker(engine)
Base = declarative_base()
signer = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "change-me"))


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    student_number = Column(String, index=True)
    student_name = Column(String, index=True)
    title = Column(String, default="New chat")
    updated_at = Column(DateTime, default=datetime.utcnow, index=True)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)
router = APIRouter(prefix="/api/chat")

SYSTEM_PROMPT = ("You are a friendly study assistant for 15-16 year old students. "
                 "Reply in the student's language (Persian by default). Be clear and concise. "
                 "Students know their teacher can read these chats.")


def auth(authorization, role):
    try:
        header = authorization or ""
        token = header[7:] if header.startswith("Bearer ") else header
        data = signer.loads(token, max_age=43200)
    except Exception as e:
        print("AUTH ERROR:", repr(e), "| authorization header present:", bool(authorization))
        raise HTTPException(401, "Not authenticated")
    if not isinstance(data, dict) or data.get("role") != role:
        raise HTTPException(403, "Forbidden")
    return data


class Msg(BaseModel):
    content: str


def conv_dict(c):
    return {"id": c.id, "title": c.title, "student_name": c.student_name,
            "student_number": c.student_number, "updated_at": c.updated_at.isoformat()}


def msgs(s, cid):
    return [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
            for m in s.query(Message).filter_by(conversation_id=cid).order_by(Message.id)]


@router.post("/conversations")
def new_conv(authorization: str = Header(None)):
    u = auth(authorization, "student")
    with Session() as s:
        c = Conversation(student_number=u["id"], student_name=u["name"])
        s.add(c)
        s.commit()
        return conv_dict(c)


@router.get("/conversations")
def my_convs(authorization: str = Header(None)):
    u = auth(authorization, "student")
    with Session() as s:
        q = s.query(Conversation).filter_by(student_number=u["id"]).order_by(
            Conversation.updated_at.desc())
        return [conv_dict(c) for c in q]


def owned(s, cid, u):
    c = s.get(Conversation, cid)
    if not c or c.student_number != u["id"]:
        raise HTTPException(404, "Not found")
    return c


@router.get("/conversations/{cid}/messages")
def my_msgs(cid: int, authorization: str = Header(None)):
    u = auth(authorization, "student")
    with Session() as s:
        owned(s, cid, u)
        return msgs(s, cid)


@router.delete("/conversations/{cid}")
def delete_conv(cid: int, authorization: str = Header(None)):
    u = auth(authorization, "student")
    with Session() as s:
        conversation = owned(s, cid, u)
        s.query(Message).filter_by(conversation_id=cid).delete(
            synchronize_session=False
        )
        s.delete(conversation)
        s.commit()
        return {"deleted": True, "id": cid}


@router.post("/conversations/{cid}/messages")
def send(cid: int, body: Msg, authorization: str = Header(None)):
    u = auth(authorization, "student")
    text = body.content.strip()[:2000]
    if not text:
        raise HTTPException(400, "Empty message")
    with Session() as s:
        c = owned(s, cid, u)
        s.add(Message(conversation_id=cid, role="user", content=text))
        if c.title == "New chat":
            c.title = text[:40]
        c.updated_at = datetime.utcnow()
        s.commit()
        history = msgs(s, cid)[-20:]
        payload = {
            "model": os.getenv("LLM_MODEL", "openai/gpt-4o-mini"),
            "max_tokens": 2000,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
                       + [{"role": m["role"], "content": m["content"]} for m in history],
        }
        try:
            api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
            if not api_key or api_key == "PASTE_YOUR_OPENROUTER_API_KEY_HERE":
                raise HTTPException(502, "OpenRouter API key is not configured.")
            openrouter = requests.Session()
            openrouter.trust_env = False
            response = openrouter.post(
                os.getenv("LLM_URL", "https://openrouter.ai/api/v1/chat/completions"),
                json=payload,
                timeout=60,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000"),
                    "X-Title": "TalimBot",
                },
            )
            if not response.ok:
                try:
                    provider_error = response.json().get("error", {}).get("message", "")
                except ValueError:
                    provider_error = ""
                detail = provider_error or f"OpenRouter returned HTTP {response.status_code}."
                print("LLM ERROR:", detail)
                raise HTTPException(502, detail)
            result = response.json()
            choice = result["choices"][0]
            if choice.get("finish_reason") == "length":
                print("LLM RESPONSE TRUNCATED: output token limit reached")
                raise HTTPException(
                    502,
                    "پاسخ طولانی بود و کامل نشد. لطفاً درخواست را به چند بخش تقسیم کنید.",
                )
            reply = choice["message"]["content"]
        except HTTPException:
            raise
        except requests.RequestException as e:
            print("LLM CONNECTION ERROR:", repr(e))
            raise HTTPException(502, "Could not connect to OpenRouter.")
        except (KeyError, IndexError, TypeError, ValueError) as e:
            print("LLM RESPONSE ERROR:", repr(e))
            raise HTTPException(502, "OpenRouter returned an unexpected response.")
        s.add(Message(conversation_id=cid, role="assistant", content=reply))
        c.updated_at = datetime.utcnow()
        s.commit()
        return {"role": "assistant", "content": reply}


@router.get("/teacher/conversations")
def t_list(q: str = "", authorization: str = Header(None)):
    auth(authorization, "teacher")
    with Session() as s:
        query = s.query(Conversation)
        if q:
            query = query.filter(Conversation.student_name.ilike(f"%{q}%"))
        return [conv_dict(c) for c in query.order_by(Conversation.updated_at.desc()).limit(100)]


@router.get("/teacher/conversations/{cid}/messages")
def t_msgs(cid: int, authorization: str = Header(None)):
    auth(authorization, "teacher")
    with Session() as s:
        return msgs(s, cid)

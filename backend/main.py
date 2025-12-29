from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

app = FastAPI()

# CORS configuration - allow all origins for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file path
DATA_FILE = Path(__file__).parent / "data" / "students.json"
DATA_FILE.parent.mkdir(exist_ok=True)

# Pydantic models
class Student(BaseModel):
    studentNumber: str
    name: str
    nationalCode: str = ""
    mbti: Optional[str] = None
    learningStyle: Optional[str] = None
    ams: Optional[str] = None
    cooperative: Optional[str] = None
    grade: float
    preferredStudents: List[str] = []
    group: Optional[int] = None

class StudentUpdate(BaseModel):
    mbti: Optional[str] = None
    learningStyle: Optional[str] = None
    ams: Optional[str] = None
    cooperative: Optional[str] = None
    preferredStudents: Optional[List[str]] = None

class GroupingRequest(BaseModel):
    courseName: str

class TeacherAuthRequest(BaseModel):
    password: str

class StudentAuthRequest(BaseModel):
    studentNumber: str
    nationalCode: str

class SystemData(BaseModel):
    students: List[Student]
    courseName: str = ""
    groupingComplete: bool = False
    groupingResults: Optional[Dict[str, Any]] = None
    resultsVisible: bool = False
    teacherPassword: str = "teacher123"

# Initialize data
def load_data() -> SystemData:
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return SystemData(**data)
    else:
        # Initialize with real 30 students from class data
        initial_students = [
            Student(studentNumber='S001', name='یاسمن آدینه پور', nationalCode='929986644', grade=18.77),
            Student(studentNumber='S002', name='پریا احمدزاده', nationalCode='980085330', grade=17.28),
            Student(studentNumber='S003', name='فاطمه اکبرزاده', nationalCode='970154550', grade=16.71),
            Student(studentNumber='S004', name='آناهیتا الهی مهر', nationalCode='26425955', grade=19.05),
            Student(studentNumber='S005', name='مریم امیری', nationalCode='980093341', grade=18.87),
            Student(studentNumber='S006', name='باران برادران رحیمی', nationalCode='960043985', grade=19.07),
            Student(studentNumber='S007', name='مایسا بصیری امین', nationalCode='960089446', grade=19.33),
            Student(studentNumber='S008', name='دلارام ثابت عهد', nationalCode='960125620', grade=19.55),
            Student(studentNumber='S009', name='شاینا جان محمدی', nationalCode='960068041', grade=19.47),
            Student(studentNumber='S010', name='آیدا جوان', nationalCode='95112313', grade=16.77),
            Student(studentNumber='S011', name='سارینا حاجی آبادی', nationalCode='999216751', grade=16.08),
            Student(studentNumber='S012', name='هستی حسن پور جوان', nationalCode='960074198', grade=19.55),
            Student(studentNumber='S013', name='فاطمه حسینی', nationalCode='2400410259', grade=19.07),
            Student(studentNumber='S014', name='غزل خسروی', nationalCode='929995767', grade=15.05),
            Student(studentNumber='S015', name='غزل ذباح', nationalCode='960110186', grade=19.25),
            Student(studentNumber='S016', name='نازنین زهرا راشکی', nationalCode='3661516087', grade=17.02),
            Student(studentNumber='S017', name='ویونا روح نواز', nationalCode='314458344', grade=18.70),
            Student(studentNumber='S018', name='روژینا سعادتی', nationalCode='960051023', grade=18.20),
            Student(studentNumber='S019', name='ترنم شعبانی', nationalCode='950083100', grade=19.37),
            Student(studentNumber='S020', name='ستایش شفابخش', nationalCode='960126899', grade=18.36),
            Student(studentNumber='S021', name='فاطمه شیرزادخان', nationalCode='980120756', grade=19.33),
            Student(studentNumber='S022', name='آرزو علی جوی', nationalCode='960054316', grade=17.98),
            Student(studentNumber='S023', name='آناهیتا قنادزاده', nationalCode='960089836', grade=18.84),
            Student(studentNumber='S024', name='نیایش کارگر', nationalCode='929956052', grade=17.74),
            Student(studentNumber='S025', name='باران کبریایی نسب', nationalCode='980119588', grade=18.82),
            Student(studentNumber='S026', name='زینب کیانوش', nationalCode='970072678', grade=18.58),
            Student(studentNumber='S027', name='ستایش محمودی', nationalCode='929904656', grade=19.33),
            Student(studentNumber='S028', name='ستایش مشتاقی', nationalCode='361282217', grade=17.67),
            Student(studentNumber='S029', name='مهتاب معلمی', nationalCode='960070265', grade=18.56),
            Student(studentNumber='S030', name='باران وحدتی', nationalCode='929916913', grade=15.02),
        ]
        
        data = SystemData(students=initial_students)
        save_data(data)
        return data

def save_data(data: SystemData):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data.dict(), f, ensure_ascii=False, indent=2)

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "TalimBot API is running"}

@app.get("/api/students")
def get_all_students():
    data = load_data()
    return {"students": data.students}

@app.get("/api/student/{student_number}")
def get_student(student_number: str):
    # Return demo account if requested
    if student_number == "DEMO":
        return Student(
            studentNumber="DEMO",
            name="پریناز عاکف",
            nationalCode="0921111111",
            grade=0.0,
            mbti=None,
            learningStyle=None,
            ams=None,
            cooperative=None,
            preferredStudents=[],
            group=None
        )
    
    data = load_data()
    student = next((s for s in data.students if s.studentNumber == student_number), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/api/student/{student_number}")
def update_student(student_number: str, updates: StudentUpdate):
    # Silently ignore updates to demo account (pretend it worked)
    if student_number == "DEMO":
        demo_student = Student(
            studentNumber="DEMO",
            name="پریناز عاکف",
            nationalCode="0921111111",
            grade=0.0,
            mbti=updates.mbti,
            learningStyle=updates.learningStyle,
            ams=updates.ams,
            cooperative=updates.cooperative,
            preferredStudents=updates.preferredStudents or [],
            group=None
        )
        return {"success": True, "student": demo_student}
    
    data = load_data()
    student = next((s for s in data.students if s.studentNumber == student_number), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update only provided fields
    update_dict = updates.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(student, key, value)
    
    save_data(data)
    return {"success": True, "student": student}

class GroupingRequest(BaseModel):
    courseName: str

@app.post("/api/grouping/perform")
async def perform_grouping(request: GroupingRequest):
    data = load_data()
    
    # Get API key from environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your environment variables or hosting platform settings"
        )
    
    # Get students with complete info (mbti and learningStyle required)
    students_with_info = [s for s in data.students if s.mbti and s.learningStyle]
    
    if len(students_with_info) == 0:
        raise HTTPException(status_code=400, detail="No students have completed their profiles yet")
    
    try:
        # Import grouping logic
        from grouping_logic import group_students_with_ai
        
        # group_students_with_ai is now synchronous (uses requests library)
        # Run it in a thread pool to avoid blocking
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            grouping_result = await loop.run_in_executor(
                executor,
                lambda: group_students_with_ai(students_with_info, request.courseName, api_key)
            )
        
        # Apply grouping to students
        for student in data.students:
            student.group = None
        
        for group in grouping_result["groups"]:
            for student_number in group["students"]:
                student = next((s for s in data.students if s.studentNumber == student_number), None)
                if student:
                    student.group = group["groupNumber"]
        
        data.courseName = request.courseName
        data.groupingComplete = True
        data.groupingResults = grouping_result
        data.resultsVisible = False  # Teacher must manually show results
        
        save_data(data)
        return {"success": True, "results": grouping_result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/grouping/status")
def get_grouping_status():
    data = load_data()
    students_with_info = [s for s in data.students if s.mbti and s.learningStyle]
    students_grouped = [s for s in data.students if s.group is not None]
    
    return {
        "totalStudents": len(data.students),
        "studentsWithCompleteInfo": len(students_with_info),
        "studentsGrouped": len(students_grouped),
        "groupingComplete": data.groupingComplete,
        "resultsVisible": data.resultsVisible,
        "courseName": data.courseName,
        "groups": data.groupingResults.get("groups", []) if data.groupingResults else []
    }

class PasswordRequest(BaseModel):
    password: str

@app.post("/api/grouping/toggle-visibility")
def toggle_results_visibility(request: PasswordRequest):
    data = load_data()
    if request.password != data.teacherPassword:
        raise HTTPException(status_code=403, detail="Invalid password")
    
    data.resultsVisible = not data.resultsVisible
    save_data(data)
    return {"success": True, "resultsVisible": data.resultsVisible}

@app.post("/api/grouping/reset")
def reset_grouping(request: PasswordRequest):
    data = load_data()
    if request.password != data.teacherPassword:
        raise HTTPException(status_code=403, detail="Invalid password")
    
    # Clear ONLY grouping-related data, keep student profiles intact
    for student in data.students:
        student.group = None
    
    data.groupingComplete = False
    data.groupingResults = None
    data.resultsVisible = False
    data.courseName = ""
    
    save_data(data)
    return {"success": True}

@app.post("/api/data/reset-all")
def reset_all_data(request: PasswordRequest):
    data = load_data()
    if request.password != data.teacherPassword:
        raise HTTPException(status_code=403, detail="Invalid password")
    
    # Clear ALL student data fields AND grouping
    for student in data.students:
        student.group = None
        student.mbti = None
        student.learningStyle = None
        student.ams = None
        student.cooperative = None
        student.preferredStudents = []
    
    data.groupingComplete = False
    data.groupingResults = None
    data.resultsVisible = False
    data.courseName = ""
    
    save_data(data)
    return {"success": True}

@app.post("/api/auth/teacher")
def check_teacher_password(request: TeacherAuthRequest):
    data = load_data()
    return {"valid": request.password == data.teacherPassword}

@app.post("/api/auth/student")
def authenticate_student(request: StudentAuthRequest):
    # Special demo account - not stored in database
    # Check for national code without leading zero (frontend strips it)
    if request.nationalCode == "921111111":
        demo_student = Student(
            studentNumber="DEMO",
            name="پریناز عاکف",
            nationalCode="921111111",
            grade=0.0,
            mbti=None,
            learningStyle=None,
            ams=None,
            cooperative=None,
            preferredStudents=[],
            group=None
        )
        return {"valid": True, "student": demo_student}
    
    data = load_data()
    student = next((s for s in data.students if s.studentNumber == request.studentNumber), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.nationalCode != request.nationalCode:
        raise HTTPException(status_code=401, detail="Invalid national code")
    
    return {"valid": True, "student": student}

class NationalCodeAuthRequest(BaseModel):
    nationalCode: str

@app.post("/api/auth/student-by-nationalcode")
def authenticate_student_by_nationalcode(request: NationalCodeAuthRequest):
    # Special demo account - not stored in database
    # Check for national code without leading zero (frontend strips it)
    if request.nationalCode == "921111111":
        demo_student = Student(
            studentNumber="DEMO",
            name="پریناز عاکف",
            nationalCode="921111111",
            grade=0.0,
            mbti=None,
            learningStyle=None,
            ams=None,
            cooperative=None,
            preferredStudents=[],
            group=None
        )
        return {"valid": True, "student": demo_student}
    
    data = load_data()
    # Find student by national code (without leading zero)
    student = next((s for s in data.students if s.nationalCode == request.nationalCode), None)
    if not student:
        raise HTTPException(status_code=404, detail="کد ملی در سیستم یافت نشد")
    
    return {"valid": True, "student": student}

@app.get("/api/student/{student_number}/group")
def get_student_group(student_number: str):
    # Demo account has no group
    if student_number == "DEMO":
        raise HTTPException(status_code=404, detail="Demo account is not part of any group")
    
    data = load_data()
    
    if not data.resultsVisible:
        raise HTTPException(status_code=403, detail="Results are not yet visible")
    
    student = next((s for s in data.students if s.studentNumber == student_number), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.group is None:
        raise HTTPException(status_code=404, detail="Student not assigned to a group yet")
    
    # Find all students in the same group
    group_members = [s for s in data.students if s.group == student.group]
    
    # Find the group details from results
    group_info = None
    if data.groupingResults:
        for g in data.groupingResults.get("groups", []):
            if g["groupNumber"] == student.group:
                group_info = g
                break
    
    return {
        "groupNumber": student.group,
        "members": group_members,
        "reasoning": group_info.get("reasoning", "") if group_info else "",
        "courseName": data.courseName
    }

@app.get("/api/data/backup")
def get_data_backup():
    """Download complete student data as JSON backup for safekeeping"""
    data = load_data()
    return data.dict()

# ============================================
# STATIC FILE SERVING (Frontend HTML/CSS/JS)
# ============================================

# Define static directory path
STATIC_DIR = Path(__file__).parent / "static"

# Mount static files FIRST - this handles all non-API routes
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import requests
import json
import os
from typing import List, Dict, Any, Optional

# API Configuration
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

def analyze_mbti(mbti: str) -> Dict[str, str]:
    """Helper to break down MBTI into explicit tags"""
    if not mbti or len(mbti) < 4:
        return {"type": "Unknown", "tags": []}
    
    m = mbti.upper()
    return {
        "energy": 'Introvert (درون‌گرا)' if m[0] == 'I' else 'Extrovert (برون‌گرا)',
        "info": 'Intuitive' if m[1] == 'N' else 'Sensing',
        "decision": 'Thinking' if m[2] == 'T' else 'Feeling',
        "structure": 'Judging' if m[3] == 'J' else 'Perceiving'
    }

def group_students_with_ai(students: List[Any], course_name: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Group students using OpenRouter API (ChatGPT)
    Args:
        students: List of student objects
        course_name: Name of the course
        api_key: OpenRouter API key (optional, falls back to env var)
    """
    # Get API key from parameter or environment variable
    openrouter_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
    
    # Clean the API key - remove any whitespace and newlines
    if openrouter_key:
        openrouter_key = openrouter_key.strip().replace('\n', '').replace('\r', '')
    
    print(f"🔍 DEBUG: API key exists: {bool(openrouter_key)}")
    print(f"🔍 DEBUG: API key length: {len(openrouter_key) if openrouter_key else 0}")
    print(f"🔍 DEBUG: API key starts with: {openrouter_key[:10] if openrouter_key and len(openrouter_key) > 10 else 'N/A'}")
    
    if not openrouter_key or openrouter_key == '':
        raise Exception(
            "OpenRouter API key not configured! "
            "Please add OPENROUTER_API_KEY in Railway Variables tab. "
            "Get your free key at: https://openrouter.ai/keys"
        )
    
    # Validate API key format
    if not openrouter_key.startswith('sk-or-v1-'):
        raise Exception(
            f"Invalid API key format. OpenRouter keys should start with 'sk-or-v1-'. "
            f"Current key starts with: {openrouter_key[:10]}... "
            f"Please check your OPENROUTER_API_KEY in Railway Variables."
        )
    
    # Sanitization & Data Enrichment
    valid_student_ids = set(s.studentNumber for s in students)
    
    student_data = []
    for s in students:
        mbti_details = analyze_mbti(s.mbti)
        student_data.append({
            "id": s.studentNumber,
            "name": s.name,
            "mbti": s.mbti,
            "mbti_analysis": mbti_details,
            "learningStyle": s.learningStyle,
            "grade": s.grade,
            "preferredStudents": [id for id in (s.preferredStudents or []) if id in valid_student_ids]
        })
    
    # Dynamic Group Size Logic
    total_students = len(students)
    if total_students < 4:
        size_guidance = "a single group"
    elif total_students < 8:
        size_guidance = "groups of 3-4 students"
    else:
        size_guidance = "groups of 4-5 students"
    
    # The Prompt
    prompt = f"""You are an expert educational AI consultant. Group these students for a "{course_name}" course.

INPUT DATA:
{json.dumps(student_data, ensure_ascii=False, indent=2)}

RULES:
1. **USE PROVIDED DATA**: Use the "mbti_analysis" fields provided in the input to determine Introvert/Extrovert counts. Do NOT guess.
2. **ALL INCLUDED**: Every student ID listed above must be assigned to a group.
3. **SIZE**: Create {size_guidance}.

CRITERIA WEIGHTS:
- 70% Effectiveness: Mix MBTI (E vs I, T vs F), Mix Learning Styles, Balance Grades.
- 30% Preferences: Keep friends together ONLY if it doesn't hurt the balance.

OUTPUT FORMAT (JSON):
{{
  "groups": [
    {{
      "groupNumber": 1,
      "students": ["S001", "S002"...],
      "reasoning": "Write a Detailed Persian (Farsi) explanation. Explicitly mention the count of Introverts and Extroverts based on the input data. Example: 'این گروه شامل ۲ درون‌گرا (S001, S002) و ۳ برون‌گرا (S003...) است...'"
    }}
  ]
}}"""

    # Make API call using requests library
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openrouter_key}',
        'HTTP-Referer': 'https://talimbot.up.railway.app',
        'X-Title': 'TalimBot'
    }
    
    payload = {
        'model': 'openai/gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a precise algorithmic grouping assistant. You MUST output ONLY valid JSON. You rely on the explicit "mbti_analysis" fields provided in the user prompt for your reasoning.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.1
    }
    
    print(f"🔍 DEBUG: Sending request to OpenRouter...")
    print(f"🔍 DEBUG: Using API key ending in: ...{openrouter_key[-8:]}")
    print(f"🔍 DEBUG: Model: {payload['model']}")
    
    response = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    
    print(f"🔍 DEBUG: Response status: {response.status_code}")
    
    if response.status_code == 401:
        error_data = response.json() if response.text else {}
        error_msg = error_data.get('error', {}).get('message', 'Unauthorized')
        raise Exception(
            f"Authentication failed (401): {error_msg}. "
            f"Please verify your OPENROUTER_API_KEY in Railway Variables tab is correct. "
            f"Get a valid key at: https://openrouter.ai/keys"
        )
    
    if not response.ok:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    data = response.json()
    content = data['choices'][0]['message']['content']
    print(f"🔍 DEBUG: Got response content, length: {len(content)}")
    
    # Parse Result
    try:
        grouping_result = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse API JSON response: {content}")
        raise Exception("Invalid JSON from API")
    
    # Failsafe: Add missing students if AI messed up
    assigned_students = set()
    for group in grouping_result['groups']:
        if 'students' in group:
            assigned_students.update(group['students'])
    
    all_ids = [s.studentNumber for s in students]
    missing = [id for id in all_ids if id not in assigned_students]
    
    if missing:
        print(f'AI missed students, adding to last group: {missing}')
        if grouping_result['groups']:
            grouping_result['groups'][-1]['students'].extend(missing)
            grouping_result['groups'][-1]['reasoning'] += f" (سیستم دانش‌آموزان {', '.join(missing)} را به این گروه اضافه کرد)"
        else:
            grouping_result['groups'].append({
                "groupNumber": 1,
                "students": missing,
                "reasoning": "گروه بازیابی شده توسط سیستم"
            })
    
    return grouping_result

async def random_grouping(students: List[Any]) -> Dict[str, Any]:
    """Fallback random grouping if API fails"""
    import random
    
    shuffled = students.copy()
    random.shuffle(shuffled)
    
    group_size = 5
    num_groups = (len(shuffled) + group_size - 1) // group_size
    
    groups = []
    for i in range(num_groups):
        group_students = shuffled[i * group_size:(i + 1) * group_size]
        groups.append({
            "groupNumber": i + 1,
            "students": [s.studentNumber for s in group_students],
            "reasoning": "گروه‌بندی تصادفی (API در دسترس نبود)"
        })
    
    return {"groups": groups}

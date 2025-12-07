import aiohttp
import json
from typing import List, Dict, Any

# API Configuration
OPENROUTER_API_KEY = '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'
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

async def group_students_with_ai(students: List[Any], course_name: str) -> Dict[str, Any]:
    """
    Group students using OpenRouter API (ChatGPT)
    """
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

    # Make API call
    async with aiohttp.ClientSession() as session:
        async with session.post(
            OPENROUTER_API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'HTTP-Referer': 'https://talimbot.github.io',
                'X-Title': 'TalimBot'
            },
            json={
                'model': 'openai/gpt-4o-mini',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a precise algorithmic grouping assistant. You output strictly valid JSON. You rely on the explicit "mbti_analysis" fields provided in the user prompt for your reasoning.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.1,
                'response_format': {'type': 'json_object'}
            }
        ) as response:
            if not response.ok:
                error_text = await response.text()
                raise Exception(f"API request failed: {response.status} - {error_text}")
            
            data = await response.json()
            content = data['choices'][0]['message']['content']
    
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

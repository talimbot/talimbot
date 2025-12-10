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
    Group students using OpenRouter API (ChatGPT) with advanced educational psychology principles
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
    
    if not openrouter_key or openrouter_key == '':
        raise Exception(
            "OpenRouter API key not configured! "
            "Please add OPENROUTER_API_KEY in Railway Variables tab. "
            "Get your free key at: https://openrouter.ai/keys"
        )
    
    # Validate API key format (but don't log the key)
    if not openrouter_key.startswith('sk-or-v1-'):
        raise Exception(
            f"Invalid API key format. OpenRouter keys should start with 'sk-or-v1-'. "
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
            "ams": s.ams if hasattr(s, 'ams') else None,
            "cooperative": s.cooperative if hasattr(s, 'cooperative') else None,
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
    
    # The Enhanced Prompt
    prompt = f"""You are an expert educational psychologist specializing in adolescent team formation and Vygotsky's Zone of Proximal Development (ZPD). Create optimal learning groups for "{course_name}" course with 15-16 year old students.

INPUT DATA:
{json.dumps(student_data, ensure_ascii=False, indent=2)}

STUDENT AGE CONTEXT (15-16 years - Adolescence):
- High need for peer acceptance and social belonging
- Developing abstract thinking and metacognition
- Identity formation through social interactions
- Sensitivity to feedback from peers
- Collaborative learning enhances engagement

GROUPING FRAMEWORK - PRIORITY ORDER:

1. **ZPD OPTIMIZATION (Zone of Proximal Development)** - 30%
   - Mix academic performance (grade field) to create ZPD scaffolding
   - Place high performers (معدل بالا) with medium performers for peer tutoring
   - Avoid grouping all high or all low performers together
   - Target: Each group should have grade variance of 1-2 points to maximize learning

2. **MBTI COMPLEMENTARITY (NOT Similarity)** - 25%
   Research-based MBTI pairings for adolescent teamwork:
   - ENFP + INTJ: Visionary creativity with strategic planning
   - ENTP + INFJ: Innovation meets deep insight and empathy
   - ENTJ + INFP: Leadership with values-driven creativity
   - ESTJ + ISFP: Organization with practical creativity
   - ESFJ + INTP: Social cohesion with analytical thinking
   - ESTP + ISFJ: Action-oriented with detail consciousness
   - ENFJ + ISTP: Motivational leadership with technical problem-solving
   - ESFP + ISTJ: Enthusiasm with reliability and structure
   
   KEY PRINCIPLES:
   - Balance E (Extrovert) and I (Introvert): 2-3 of each per group
   - Complement T (Thinking) with F (Feeling) for balanced decision-making
   - Mix N (Intuitive) with S (Sensing) for big-picture + detail focus
   - Combine J (Judging) with P (Perceiving) for structure + flexibility

3. **VARK DIVERSITY (Learning Styles)** - 20%
   - Include different learning styles in each group:
     * Visual (دیداری): Diagrams, charts, spatial understanding
     * Aural (شنیداری): Discussions, verbal explanations
     * Read/Write: Text-based learning, note-taking
     * Kinesthetic (حرکتی): Hands-on, experiential learning
   - Diversity ensures multiple teaching approaches within group
   - Adolescents learn best when exposed to varied learning methods

4. **ACADEMIC MOTIVATION (AMS Score)** - 15%
   - AMS field: Academic Motivation Scale (0-196)
   - Balance high and moderate motivation levels
   - High motivation students (>140) can inspire others
   - Avoid grouping all low-motivation (<100) students together
   - Target: Each group has at least one high-motivation member

5. **COOPERATIVE LEARNING SKILLS** - 10%
   - Cooperative field: Cooperation ability (0-125)
   - High cooperation students (>88) act as social facilitators
   - Mix cooperation levels for peer modeling
   - Students with strong cooperation skills help integrate introverts

6. **COURSE-SPECIFIC REQUIREMENTS** - Based on "{course_name}":
   - Math/Science: Prioritize T (Thinking) types, Visual/Kinesthetic learners
   - Literature/Humanities: Include F (Feeling) types, Read/Write learners
   - Projects/Labs: Need high Kinesthetic and ESTP/ISTP types
   - Discussion-based: Ensure Aural learners and E (Extrovert) types

7. **STUDENT PREFERENCES** - 5% (Secondary consideration)
   - Honor "preferredStudents" field ONLY if it doesn't compromise above criteria
   - Adolescents benefit from working outside comfort zones
   - Strategic separation can reduce cliques and expand social circles

CRITICAL RULES:
✓ ALL students MUST be assigned to a group
✓ Create {size_guidance}
✓ Each group needs MBTI balance: 2-3 Introverts + 2-3 Extroverts
✓ Each group needs grade diversity: Mix high (>18) with medium (16-18) performers
✓ Prioritize complementary MBTI types over similar types
✓ Use provided data fields - DO NOT invent values

OUTPUT FORMAT (Valid JSON Only):
{{
  "groups": [
    {{
      "groupNumber": 1,
      "students": ["S001", "S002", "S003", "S004"],
      "reasoning": "توضیحات کامل به فارسی - شامل: (1) تحلیل ZPD: معدل‌ها و چگونگی یادگیری همیاری (2) تکمیل MBTI: چرا این تیپ‌ها با هم سازگارند (3) تنوع VARK (4) سطح انگیزش و همکاری (5) مناسب بودن برای درس {course_name}. مثال: 'این گروه دارای ZPD مطلوب است: S001 (معدل 19.5) و S002 (معدل 17.2) به S003 (معدل 16) کمک می‌کنند. تکمیل MBTI: ENFP (S001) با خلاقیت و INTJ (S002) با برنامه‌ریزی استراتژیک همکاری می‌کنند. تنوع یادگیری: 2 Visual، 1 Aural، 1 Kinesthetic. انگیزش بالا (AMS>150) در S001 الهام‌بخش است.'"
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
        'model': 'openai/gpt-4o-mini', # 'openai/gpt-3.5-turbo',
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
    
    print(f"Sending request to OpenRouter API...")
    
    response = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response preview: {response.text[:200]}")
    
    if response.status_code == 401:
        try:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unauthorized')
        except:
            error_msg = response.text
        
        raise Exception(
            f"OpenRouter Authentication Error: {error_msg}. "
            f"Your API key is configured but invalid. Please:\n"
            f"1. Go to https://openrouter.ai/keys\n"
            f"2. Check if your key is active and has credits\n"
            f"3. Create a NEW key if needed\n"
            f"4. Update OPENROUTER_API_KEY in Railway Variables"
        )
    
    if response.status_code == 402:
        raise Exception(
            "OpenRouter Payment Required: Your account has no credits. "
            "Add credits at https://openrouter.ai/credits"
        )
    
    if not response.ok:
        try:
            error_data = response.json()
            error_detail = error_data.get('error', {}).get('message', response.text)
        except:
            error_detail = response.text
        raise Exception(f"API request failed ({response.status_code}): {error_detail}")
    
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

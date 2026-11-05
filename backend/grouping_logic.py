import requests
import json
import os
from typing import List, Dict, Any, Optional

# API Configuration
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

def analyze_mbti(mbti: str) -> Dict[str, str]:
    """Helper to break down MBTI into explicit tags"""
    if not mbti or len(str(mbti)) < 4:
        return {"type": "Unknown", "tags": []}
    
    m = str(mbti).upper()
    return {
        "energy": 'Introvert (درون‌گرا)' if m[0] == 'I' else 'Extrovert (برون‌گرا)',
        "info": 'Intuitive' if m[1] == 'N' else 'Sensing',
        "decision": 'Thinking' if m[2] == 'T' else 'Feeling',
        "structure": 'Judging' if m[3] == 'J' else 'Perceiving'
    }

def has_valid_data(student: Any) -> bool:
    """
    Strict validation: Returns True ONLY if all required fields are filled.
    """
    try:
        # Check all fields: MBTI, Learning Style, AMS, Cooperative, and Grade
        has_mbti = hasattr(student, 'mbti') and bool(student.mbti) and len(str(student.mbti).strip()) >= 4
        has_ls = hasattr(student, 'learningStyle') and bool(student.learningStyle)
        has_ams = hasattr(student, 'ams') and student.ams is not None
        has_coop = hasattr(student, 'cooperative') and student.cooperative is not None
        has_grade = hasattr(student, 'grade') and student.grade is not None
        
        return all([has_mbti, has_ls, has_ams, has_coop, has_grade])
    except Exception:
        return False
    # """
    # Evaluates if a student has actually filled out the required fields.
    # Adjust these checks based on how your system represents empty data (None, "", etc.)
    # """
    # try:
    #     has_mbti = hasattr(student, 'mbti') and bool(student.mbti) and len(str(student.mbti).strip()) >= 4
    #     has_grade = hasattr(student, 'grade') and student.grade is not None
    #     return has_mbti and has_grade
    # except Exception:
    #     return False

def group_students_with_ai(students: List[Any], course_name: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Group students using OpenRouter API (ChatGPT) with advanced educational psychology principles.
    """
    # Get API key from parameter or environment variable
    openrouter_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
    
    # Clean the API key
    if openrouter_key:
        openrouter_key = openrouter_key.strip().replace('\n', '').replace('\r', '')
    
    if not openrouter_key or openrouter_key == '':
        raise Exception(
            "OpenRouter API key not configured! "
            "Please add OPENROUTER_API_KEY in Railway Variables tab. "
            "Get your free key at: https://openrouter.ai/keys"
        )
    
    if not openrouter_key.startswith('sk-or-v1-'):
        raise Exception(
            "Invalid API key format. OpenRouter keys should start with 'sk-or-v1-'. "
            "Please check your OPENROUTER_API_KEY in Railway Variables."
        )

    
    # --- 1. FILTERING AND SORTING (For Repeatability) ---
    valid_students = [s for s in students if has_valid_data(s)]
    
    if not valid_students:
        return {"groups": [], "error": "No students with valid data found to group."}

    # Sort students by ID to ensure the LLM receives them in the exact same order every run
    valid_students.sort(key=lambda s: str(s.studentNumber))
    
    valid_student_ids = set(s.studentNumber for s in valid_students)
    total_students = len(valid_students)

    # --- 2. DATA ENRICHMENT ---
    student_data = []
    for s in valid_students:
        mbti_details = analyze_mbti(s.mbti)
        student_data.append({
            "id": s.studentNumber,
            "name": s.name,
            "mbti": s.mbti,
            "mbti_analysis": mbti_details,
            "learningStyle": s.learningStyle if hasattr(s, 'learningStyle') else None,
            "ams": s.ams if hasattr(s, 'ams') else None,
            "cooperative": s.cooperative if hasattr(s, 'cooperative') else None,
            "grade": s.grade,
            "preferredStudents": [id for id in (getattr(s, 'preferredStudents', []) or []) if id in valid_student_ids]
        })
    
    # --- 3. DYNAMIC GROUP SIZE LOGIC ---
    if total_students < 4:
        size_guidance = "a single group"
    elif total_students < 8:
        size_guidance = "groups of 3-4 students"
    else:
        remainder = total_students % 5
        if remainder == 1:
            size_guidance = "groups of 5 students, with some groups of 3-4 if needed to avoid groups smaller than 3"
        elif remainder == 2:
            size_guidance = "groups of 5 students, with some groups of 4 if needed to avoid groups of 2"
        else:
            size_guidance = "groups of 5 students"
    
    # --- 4. PROMPT ASSEMBLY ---
    prompt = f"""You are an expert educational psychologist specializing in adolescent team formation and Vygotsky's Zone of Proximal Development (ZPD). Create optimal learning groups for "{course_name}" course with 15-16 year old students.

INPUT DATA (ONLY GROUP THESE STUDENTS):
{json.dumps(student_data, ensure_ascii=False, indent=2)}

TOTAL STUDENTS TO GROUP: {total_students}
GROUPING STRATEGY: Prefer {size_guidance}. IMPORTANT: Avoid creating groups with only 1-2 students. If the math doesn't work out evenly with groups of 5, adjust by creating some groups of 4 to balance the numbers.

STUDENT AGE CONTEXT (15-16 years - Adolescence):
- High need for peer acceptance and social belonging
- Developing abstract thinking and metacognition
- Identity formation through social interactions
- Sensitivity to feedback from peers
- Collaborative learning enhances engagement

GROUPING FRAMEWORK - HIERARCHY OF IMPORTANCE:

1. **PRIMARY DRIVER: ZPD OPTIMIZATION (Zone of Proximal Development)**
   - Mix academic performance (grade field) to create ZPD scaffolding
   - Place high performers (معدل بالا) with medium performers for peer tutoring
   - Avoid grouping all high or all low performers together
   - Target: Each group should have grade variance of 1-2 points to maximize learning

2. **SECONDARY DRIVER: MBTI COMPLEMENTARITY (NOT Similarity)**
   - Balance E (Extrovert) and I (Introvert): 2-3 of each per group
   - Complement T (Thinking) with F (Feeling) for balanced decision-making
   - Mix N (Intuitive) with S (Sensing) for big-picture + detail focus
   - Combine J (Judging) with P (Perceiving) for structure + flexibility

3. **TERTIARY DRIVER: VARK DIVERSITY (Learning Styles)**
   - Include different learning styles in each group (Visual, Aural, Read/Write, Kinesthetic)
   - Diversity ensures multiple teaching approaches within group

4. **BALANCING FACTOR: ACADEMIC MOTIVATION (AMS Score)**
   - Balance high and moderate motivation levels
   - Target: Each group has at least one high-motivation member

5. **SOCIAL GLUE: COOPERATIVE LEARNING SKILLS**
   - High cooperation students act as social facilitators
   - Mix cooperation levels for peer modeling

6. **CONTEXTUAL ADAPTATION: COURSE-SPECIFIC REQUIREMENTS**
   Based on "{course_name}": Adapt MBTI/VARK priorities to fit the subject matter.

7. **TIE-BREAKER: STUDENT PREFERENCES**
   - Honor "preferredStudents" field ONLY if it doesn't compromise above criteria

CRITICAL RULES:
✓ ALL {total_students} students MUST be assigned to a group
✓ Adjust group sizes (use groups of 4) to avoid creating groups with only 1-2 students
✓ Each group needs MBTI balance and grade diversity
✓ Use ONLY provided data fields - DO NOT invent values or add missing students

🚨 MANDATORY DUPLICATE PREVENTION (HIGHEST PRIORITY) 🚨
✓ Each student ID can appear in EXACTLY ONE group
✓ Before outputting, verify EVERY student ID appears exactly once
✓ Total students in all groups MUST equal {total_students}

OUTPUT FORMAT (Valid JSON Only):
{{
  "groups": [
    {{
      "groupNumber": 1,
      "students": ["S001", "S002", "S003", "S004"],
      "reasoning": "توضیحات کامل به فارسی بر اساس ZPD، MBTI، و سبک‌های یادگیری"
    }}
  ]
}}"""

    # --- 5. API CALL ---
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openrouter_key}',
        'HTTP-Referer': 'https://talimbot-talimbot.hf.space',
        'X-Title': 'TalimBot'
    }
    
    payload = {
        'model': 'openai/gpt-4o',
        'messages': [
            {
                'role': 'system',
                'content': '''You are a precise algorithmic grouping assistant. You MUST output ONLY valid JSON - no markdown, no code blocks, no extra text. Start directly with { and end with }.

🚨 CRITICAL DUPLICATE PREVENTION RULE 🚨
• Each student ID can appear in EXACTLY ONE group
• NO DUPLICATES ALLOWED
• Total students in all groups MUST equal the TOTAL STUDENTS number exactly.
• Only use the IDs provided in the INPUT DATA.'''
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.0,  # Set to 0.0 for maximum determinism (repeatability)
        'seed': 42           # Locks the randomness seed on supported models
    }
    
    print(f"Sending request to OpenRouter API for {total_students} valid students...")
    
    response = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code == 401:
        raise Exception("OpenRouter Authentication Error. API Key invalid or expired.")
    if response.status_code == 402:
        raise Exception("OpenRouter Payment Required: Your account has no credits.")
    if not response.ok:
        raise Exception(f"API request failed ({response.status_code}): {response.text}")
    
#     data = response.json()
#     content = data['choices'][0]['message']['content']
    
#     # --- 6. PARSE AND CLEANUP ---
#     try:
#         grouping_result = json.loads(content)
#     except json.JSONDecodeError:
#         import re
#         json_match = re.search(r'
# http://googleusercontent.com/immersive_entry_chip/0
    
    data = response.json()
    content = data['choices'][0]['message']['content']
    print(f"🔍 DEBUG: Got response content, length: {len(content)}")
    
    # Parse Result - Extract JSON from markdown code blocks if present
    try:
        # Try direct JSON parse first
        grouping_result = json.loads(content)
    except json.JSONDecodeError as e:
        # Try to extract JSON from markdown code blocks
        import re
        
        # Look for JSON in ```json ... ``` or ``` ... ``` blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            try:
                grouping_result = json.loads(json_match.group(1))
                print(f"✅ Extracted JSON from markdown code block")
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from code block: {json_match.group(1)[:200]}")
                raise Exception("Invalid JSON from API (even after markdown extraction)")
        else:
            # Try to find JSON object in the content
            json_match = re.search(r'\{.*"groups".*\}', content, re.DOTALL)
            if json_match:
                try:
                    grouping_result = json.loads(json_match.group(0))
                    print(f"✅ Extracted JSON object from response")
                except json.JSONDecodeError:
                    print(f"Failed to parse extracted JSON: {json_match.group(0)[:200]}")
                    raise Exception("Invalid JSON from API (extraction failed)")
            else:
                print(f"❌ No JSON found in response. Full content:\n{content}")
                raise Exception("Invalid JSON from API - no valid JSON structure found")
    
    # Failsafe: Detect and remove duplicates, then add missing students
    assigned_students = set()
    duplicate_students = set()
    
    # First pass: detect duplicates
    for group in grouping_result['groups']:
        if 'students' in group:
            for student_id in group['students']:
                if student_id in assigned_students:
                    duplicate_students.add(student_id)
                    print(f'⚠️ DUPLICATE DETECTED: {student_id} appears in multiple groups!')
                else:
                    assigned_students.add(student_id)
    
    # Second pass: remove duplicates (keep first occurrence only)
    if duplicate_students:
        print(f'🔧 Removing duplicates: {duplicate_students}')
        first_occurrence = {}
        for i, group in enumerate(grouping_result['groups']):
            if 'students' in group:
                cleaned_students = []
                for student_id in group['students']:
                    if student_id in duplicate_students:
                        if student_id not in first_occurrence:
                            # Keep first occurrence
                            first_occurrence[student_id] = i
                            cleaned_students.append(student_id)
                        else:
                            # Remove duplicate
                            print(f'  Removing {student_id} from group {group["groupNumber"]}')
                    else:
                        cleaned_students.append(student_id)
                group['students'] = cleaned_students
        
        # Rebuild assigned_students set after cleaning
        assigned_students = set()
        for group in grouping_result['groups']:
            if 'students' in group:
                assigned_students.update(group['students'])
    
    # Third pass: add missing students
    # all_ids = [s.studentNumber for s in students]
    # missing = [id for id in all_ids if id not in assigned_students]
    
    # if missing:
    #     print(f'⚠️ AI missed students, adding to last group: {missing}')
    #     if grouping_result['groups']:
    #         grouping_result['groups'][-1]['students'].extend(missing)
    #         grouping_result['groups'][-1]['reasoning'] += f" (سیستم دانش‌آموزان {', '.join(missing)} را به این گروه اضافه کرد)"
    #     else:
    #         grouping_result['groups'].append({
    #             "groupNumber": 1,
    #             "students": missing,
    #             "reasoning": "گروه بازیابی شده توسط سیستم"
    #         })
    
    # Final verification
    final_assigned = set()
    for group in grouping_result['groups']:
        if 'students' in group:
            final_assigned.update(group['students'])
    
    if len(final_assigned) != len(students):
        print(f'❌ ERROR: Final count mismatch! Expected {len(students)}, got {len(final_assigned)}')
    else:
        print(f'✅ Verification passed: All {len(students)} students assigned exactly once')
    
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

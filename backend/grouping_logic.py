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
        # Prefer groups of 5, but use groups of 4 if needed to avoid very small groups
        # Examples: 30 students = 6 groups of 5
        #          27 students = 5 groups of 5 + 1 group of 2 (bad) → instead: 3 groups of 5 + 3 groups of 4 (good)
        #          25 students = 5 groups of 5
        #          22 students = 4 groups of 5 + 1 group of 2 (bad) → instead: 2 groups of 5 + 3 groups of 4 (good)
        remainder = total_students % 5
        if remainder == 1:
            # e.g., 21 students: would be 4 groups of 5 + 1 of 1 → instead make 3 groups of 5 + 2 groups of 3
            size_guidance = "groups of 5 students, with some groups of 3-4 if needed to avoid groups smaller than 3"
        elif remainder == 2:
            # e.g., 22 students: would be 4 groups of 5 + 1 of 2 → instead make 2 groups of 5 + 3 groups of 4
            size_guidance = "groups of 5 students, with some groups of 4 if needed to avoid groups of 2"
        else:
            size_guidance = "groups of 5 students"
    
    # The Enhanced Prompt
    prompt = f"""You are an expert educational psychologist specializing in adolescent team formation and Vygotsky's Zone of Proximal Development (ZPD). Create optimal learning groups for "{course_name}" course with 15-16 year old students.

INPUT DATA:
{json.dumps(student_data, ensure_ascii=False, indent=2)}

TOTAL STUDENTS: {total_students}
GROUPING STRATEGY: Prefer {size_guidance}. IMPORTANT: Avoid creating groups with only 1-2 students. If the math doesn't work out evenly with groups of 5, adjust by creating some groups of 4 to balance the numbers. For example:
- 30 students = 6 groups of 5 ✓
- 27 students = 3 groups of 5 + 3 groups of 4 ✓ (NOT 5 groups of 5 + 1 group of 2 ✗)
- 25 students = 5 groups of 5 ✓
- 22 students = 2 groups of 5 + 3 groups of 4 ✓ (NOT 4 groups of 5 + 1 group of 2 ✗)

STUDENT AGE CONTEXT (15-16 years - Adolescence):
- High need for peer acceptance and social belonging
- Developing abstract thinking and metacognition
- Identity formation through social interactions
- Sensitivity to feedback from peers
- Collaborative learning enhances engagement

GROUPING FRAMEWORK - HIERARCHY OF IMPORTANCE:

1. **PRIMARY DRIVER: ZPD OPTIMIZATION (Zone of Proximal Development)**
   *This is the most critical psychological factor.*
   - Mix academic performance (grade field) to create ZPD scaffolding
   - Place high performers (معدل بالا) with medium performers for peer tutoring
   - Avoid grouping all high or all low performers together
   - Target: Each group should have grade variance of 1-2 points to maximize learning

2. **SECONDARY DRIVER: MBTI COMPLEMENTARITY (NOT Similarity)**
   *Use this to refine the groups created by ZPD.*
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

3. **TERTIARY DRIVER: VARK DIVERSITY (Learning Styles)**
   *Ensure the group has "Full Coverage" of capabilities.*
   - Include different learning styles in each group:
     * Visual (دیداری): Diagrams, charts, spatial understanding
     * Aural (شنیداری): Discussions, verbal explanations
     * Read/Write: Text-based learning, note-taking
     * Kinesthetic (حرکتی): Hands-on, experiential learning
   - Diversity ensures multiple teaching approaches within group
   - Adolescents learn best when exposed to varied learning methods

4. **BALANCING FACTOR: ACADEMIC MOTIVATION (AMS Score)**
   - AMS field: Academic Motivation Scale (0-196)
   - Balance high and moderate motivation levels
   - High motivation students (>140) can inspire others
   - Avoid grouping all low-motivation (<100) students together
   - Target: Each group has at least one high-motivation member

5. **SOCIAL GLUE: COOPERATIVE LEARNING SKILLS**
   - Cooperative field: Cooperation ability (0-125)
   - High cooperation students (>88) act as social facilitators
   - Mix cooperation levels for peer modeling
   - Students with strong cooperation skills help integrate introverts

6. **CONTEXTUAL ADAPTATION: COURSE-SPECIFIC REQUIREMENTS**
   Based on "{course_name}":
   - Math/Science: Prioritize T (Thinking) types, Visual/Kinesthetic learners
   - Literature/Humanities: Include F (Feeling) types, Read/Write learners
   - Projects/Labs: Need high Kinesthetic and ESTP/ISTP types
   - Discussion-based: Ensure Aural learners and E (Extrovert) types

7. **TIE-BREAKER: STUDENT PREFERENCES**
   *Only use this if it does not violate the drivers above.*
   - Honor "preferredStudents" field ONLY if it doesn't compromise above criteria
   - Adolescents benefit from working outside comfort zones
   - Strategic separation can reduce cliques and expand social circles

CRITICAL RULES:
✓ ALL students MUST be assigned to a group
✓ PREFER groups of 5 students to minimize total number of groups
✓ Adjust group sizes (use groups of 4) to avoid creating groups with only 1-2 students
✓ Each group should have 3-5 students (never 1-2 students alone)
✓ Each group needs MBTI balance: 2-3 Introverts + 2-3 Extroverts
✓ Each group needs grade diversity: Mix high (>18) with medium (16-18) performers
✓ Prioritize complementary MBTI types over similar types
✓ Use provided data fields - DO NOT invent values

🚨 MANDATORY DUPLICATE PREVENTION (HIGHEST PRIORITY) 🚨
This is a HARD CONSTRAINT, not a guideline:
✓ Each student ID (S001, S002, etc.) can appear in EXACTLY ONE group
✓ NO student can be in multiple groups - this would be a CRITICAL ERROR
✓ Before outputting, verify EVERY student ID appears exactly once
✓ If you find a duplicate, STOP and fix it immediately
✓ Total students in all groups MUST equal {total_students}

VALIDATION CHECKLIST (complete this mentally before responding):
□ Step 1: List all student IDs used across all groups
□ Step 2: Check if any ID appears more than once → if YES, remove duplicates
□ Step 3: Count total students in groups → must equal {total_students}
□ Step 4: Check for missing students → add them to appropriate groups
□ Step 5: Verify no duplicates exist → if duplicates found, START OVER

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
        'HTTP-Referer': 'https://talimbot-talimbot.hf.space',
        'X-Title': 'TalimBot'
    }
    
    payload = {
        'model': 'openai/gpt-4o',  # Using GPT-4o for better accuracy and reasoning
        'messages': [
            {
                'role': 'system',
                'content': '''You are a precise algorithmic grouping assistant. You MUST output ONLY valid JSON - no markdown, no code blocks, no extra text. Start directly with { and end with }.

🚨 CRITICAL DUPLICATE PREVENTION RULE 🚨
This is the MOST IMPORTANT rule - violating this makes your output INVALID:
• Each student ID (e.g., S001, S002) can appear in EXACTLY ONE group
• NO DUPLICATES ALLOWED - putting a student in multiple groups is a CRITICAL ERROR
• Before you output, you MUST verify: count how many times each student ID appears across ALL groups
• If ANY student ID appears more than once, your output is REJECTED
• If the total count of students in all groups ≠ total input students, your output is REJECTED

VALIDATION STEPS (do this before outputting):
1. Make a list of ALL student IDs from all groups you created
2. Check if any ID appears 2 or more times → if YES, remove duplicates
3. Count total students: sum of all group sizes must equal the TOTAL STUDENTS number
4. Verify each input student ID appears exactly once

You rely on the explicit "mbti_analysis" fields provided in the user prompt for your reasoning.'''
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.2  # Lower temperature for more consistent, logical grouping
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
    all_ids = [s.studentNumber for s in students]
    missing = [id for id in all_ids if id not in assigned_students]
    
    if missing:
        print(f'⚠️ AI missed students, adding to last group: {missing}')
        if grouping_result['groups']:
            grouping_result['groups'][-1]['students'].extend(missing)
            grouping_result['groups'][-1]['reasoning'] += f" (سیستم دانش‌آموزان {', '.join(missing)} را به این گروه اضافه کرد)"
        else:
            grouping_result['groups'].append({
                "groupNumber": 1,
                "students": missing,
                "reasoning": "گروه بازیابی شده توسط سیستم"
            })
    
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

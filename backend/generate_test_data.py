"""
Test Data Generator for TalimBot Grouping System
=================================================
This script generates complete test data for all 30 students with random but realistic values.
Run this script to test the grouping algorithm, then delete it when done.

Usage:
1. Run: python generate_test_data.py
2. This creates a backup of current data and generates test data
3. Test the grouping in the teacher dashboard
4. Run: python generate_test_data.py --restore
5. Delete this file when done

The script will:
- Backup your current students.json to students.json.backup
- Generate random but realistic MBTI, VARK, AMS, Cooperative scores
- Add random preferred students (2-4 per student)
- Preserve student names and numbers
"""

import json
import random
import sys
import os
from pathlib import Path

# Get the data directory
DATA_DIR = Path(__file__).parent / 'data'
STUDENTS_FILE = DATA_DIR / 'students.json'
BACKUP_FILE = DATA_DIR / 'students.json.backup'

# MBTI types (all 16 types)
MBTI_TYPES = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
]

# VARK learning styles
VARK_STYLES = ['Visual', 'Aural', 'Read/Write', 'Kinesthetic']

# Persian names for students
PERSIAN_NAMES = [
    'علی احمدی', 'زهرا محمدی', 'محمد رضایی', 'فاطمه کریمی', 'حسین نوری',
    'مریم صادقی', 'رضا حسینی', 'سارا عباسی', 'امیر کاظمی', 'نرگس رحمانی',
    'مهدی ملکی', 'نازنین امینی', 'سعید باقری', 'مینا جعفری', 'حامد اکبری',
    'پریسا موسوی', 'احمد فتحی', 'لیلا شریفی', 'مصطفی سلیمی', 'ندا قاسمی',
    'جواد تقوی', 'سمیرا صفری', 'مجید حیدری', 'شیدا عسگری', 'کامران صالحی',
    'الهام یوسفی', 'بهنام ناصری', 'سمانه رستمی', 'آرش مرادی', 'شقایق فروغی'
]

def generate_test_student(student_number, index, all_student_numbers):
    """Generate complete test data for one student"""
    # Random MBTI
    mbti = random.choice(MBTI_TYPES)
    
    # Random VARK
    learning_style = random.choice(VARK_STYLES)
    
    # Random AMS score (50-196, with bias towards higher scores)
    # Using beta distribution for more realistic spread
    ams_normalized = random.betavariate(5, 2)  # Skewed towards higher values
    ams = str(int(50 + ams_normalized * 146))
    
    # Random Cooperative score (40-125, also biased higher)
    coop_normalized = random.betavariate(4, 2)
    cooperative = str(int(40 + coop_normalized * 85))
    
    # Random grade (14.0-20.0, with realistic distribution)
    grade_normalized = random.betavariate(3, 2)
    grade = round(14.0 + grade_normalized * 6.0, 2)
    
    # Random preferred students (2-4 students)
    num_preferred = random.randint(2, 4)
    other_students = [s for s in all_student_numbers if s != student_number]
    preferred = random.sample(other_students, num_preferred)
    
    return {
        "studentNumber": student_number,
        "name": PERSIAN_NAMES[index],
        "nationalCode": f"{929986644 + index}",
        "mbti": mbti,
        "learningStyle": learning_style,
        "ams": ams,
        "cooperative": cooperative,
        "grade": grade,
        "preferredStudents": preferred,
        "group": None
    }

def backup_current_data():
    """Backup current students.json"""
    if STUDENTS_FILE.exists():
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backed up current data to: {BACKUP_FILE}")
        return True
    else:
        print(f"❌ Error: {STUDENTS_FILE} not found!")
        return False

def restore_backup():
    """Restore from backup"""
    if BACKUP_FILE.exists():
        with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Restored data from backup: {BACKUP_FILE}")
        print(f"💡 You can now delete the backup file: {BACKUP_FILE}")
        return True
    else:
        print(f"❌ Error: Backup file not found at {BACKUP_FILE}")
        return False

def generate_complete_test_data():
    """Generate complete test data for all 30 students"""
    # Backup first
    if not backup_current_data():
        return False
    
    # Load current structure
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate student numbers
    all_student_numbers = [f"S{i:03d}" for i in range(1, 31)]
    
    # Generate test students
    test_students = []
    for i, student_num in enumerate(all_student_numbers):
        test_students.append(generate_test_student(student_num, i, all_student_numbers))
    
    # Update data
    data['students'] = test_students
    data['groupingComplete'] = False
    data['groupingResults'] = None
    data['resultsVisible'] = False
    
    # Save test data
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generated complete test data for all 30 students!")
    print(f"\n📊 Test Data Summary:")
    
    # Show statistics
    mbti_counts = {}
    vark_counts = {}
    for student in test_students:
        mbti_counts[student['mbti']] = mbti_counts.get(student['mbti'], 0) + 1
        vark_counts[student['learningStyle']] = vark_counts.get(student['learningStyle'], 0) + 1
    
    print(f"\n🧠 MBTI Distribution:")
    for mbti, count in sorted(mbti_counts.items()):
        print(f"  {mbti}: {count} students")
    
    print(f"\n📚 VARK Distribution:")
    for vark, count in sorted(vark_counts.items()):
        print(f"  {vark}: {count} students")
    
    avg_ams = sum(int(s['ams']) for s in test_students) / len(test_students)
    avg_coop = sum(int(s['cooperative']) for s in test_students) / len(test_students)
    avg_grade = sum(s['grade'] for s in test_students) / len(test_students)
    
    print(f"\n📈 Average Scores:")
    print(f"  AMS: {avg_ams:.1f}/196")
    print(f"  Cooperative: {avg_coop:.1f}/125")
    print(f"  Grade: {avg_grade:.2f}/20")
    
    print(f"\n🎯 Next Steps:")
    print(f"  1. Go to teacher dashboard")
    print(f"  2. Test the grouping algorithm")
    print(f"  3. When done, run: python generate_test_data.py --restore")
    print(f"  4. Delete this file and the backup")
    
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--restore':
        # Restore mode
        print("🔄 Restoring original data...")
        if restore_backup():
            print("\n✅ Done! Original data restored.")
            print(f"💡 You can now delete:")
            print(f"  - {BACKUP_FILE}")
            print(f"  - {__file__}")
    else:
        # Generate mode
        print("🎲 Generating complete test data for all 30 students...")
        print("=" * 60)
        if generate_complete_test_data():
            print("\n✅ Test data generation complete!")
            print(f"\n⚠️  IMPORTANT: This is TEST DATA!")
            print(f"    Run 'python generate_test_data.py --restore' to restore original data")

if __name__ == '__main__':
    main()

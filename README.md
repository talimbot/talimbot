---
title: TalimBot
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# TalimBot - AI-Powered Student Grouping System

An intelligent educational platform that uses advanced psychology principles and AI to create optimal learning groups for adolescent students (ages 15-16).

## Overview

TalimBot is a comprehensive web-based system designed to help teachers form balanced, effective study groups by analyzing student personalities, learning styles, academic motivation, and cooperative skills. The system uses OpenAI's GPT-4o to create groups that maximize learning potential through Zone of Proximal Development (ZPD) theory and complementary personality matching.

## Key Features

### For Teachers
- **AI-Powered Grouping**: Automated group formation using educational psychology principles
- **Multi-Factor Analysis**: Considers 7 key criteria with weighted priorities:
  - ZPD Optimization (30%) - Grade-based peer tutoring scaffolding
  - MBTI Complementarity (25%) - Personality type balance
  - VARK Diversity (20%) - Learning style variety
  - Academic Motivation (15%) - AMS score distribution
  - Cooperative Skills (10%) - Teamwork ability balance
  - Course-Specific Requirements
  - Student Preferences (5%)
- **Real-time Dashboard**: Monitor student profile completion and grouping status
- **Data Management**: Import/export student data via JSON, fill test data
- **Result Control**: Show/hide grouping results to students
- **Flexible Reset Options**: 
  - Reset grouping only (preserve student data)
  - Reset all data (complete system reset)

### For Students
- **Profile Management**: Complete personality and learning assessments
- **Integrated Tests**: 
  - MBTI personality test (16 types)
  - VARK learning style questionnaire (Visual, Aural, Read/Write, Kinesthetic)
  - AMS academic motivation scale (28 questions, 0-196 score)
  - Cooperative learning skills assessment (25 questions, 0-125 score)
- **Peer Preferences**: Select up to 4 preferred groupmates
- **Group View**: See assigned group members and AI reasoning (when visible)
- **Progress Tracking**: Monitor test completion status

## Technical Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: JSON file-based storage (students.json)
- **AI Integration**: OpenRouter API with GPT-4o model
- **Authentication**: Password-based teacher authentication, national code verification for students

### Frontend
- **UI Framework**: Tailwind CSS
- **Language Support**: Persian (RTL layout) with Vazirmatn font
- **Pages**:
  - Login page (student/teacher authentication)
  - Student dashboard (profile management, tests)
  - Teacher dashboard (grouping management, analytics)
  - Group view (display assigned groups)
  - AMS questionnaire (academic motivation assessment)
  - Cooperative questionnaire (teamwork skills assessment)

### Deployment
- **Platform**: Railway.app
- **Server**: Uvicorn ASGI server
- **Static Files**: Served via FastAPI StaticFiles
- **Environment Variables**: OPENROUTER_API_KEY

## Project Structure

```
talimbot/
├── backend/
│   ├── main.py                 # FastAPI application and API endpoints
│   ├── grouping_logic.py       # AI grouping algorithm
│   ├── data/
│   │   ├── students.json       # Student data (gitignored)
│   │   └── students.json.backup # Clean backup template
│   └── static/
│       ├── pages/              # HTML pages
│       │   ├── login.html
│       │   ├── student-dashboard.html
│       │   ├── teacher-dashboard.html
│       │   ├── group-view.html
│       │   ├── ams-questionnaire.html
│       │   ├── cooperative-questionnaire.html
│       │   └── student-data.html
│       ├── assets/
│       │   ├── js/
│       │   │   ├── data.js     # API client functions
│       │   │   └── grouping.js # Grouping utilities
│       │   └── css/
│       │       └── styles.css  # Custom styles
│       └── index.html          # Landing page
├── resources_references/        # Documentation and reference files
│   ├── RAILWAY_DEPLOYMENT.md   # Deployment guide
│   ├── TEST_RESULTS_AND_SOLUTION.md
│   ├── angizesh_tahsili.txt    # AMS questionnaire source
│   ├── cooperative.txt         # Cooperative questionnaire source
│   ├── students_class_notebook.txt # Original student data
│   └── sample-student-data.json # JSON import example
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for Railway
├── Procfile                    # Railway start command
└── .gitignore                  # Git ignore rules

```

## Installation and Setup

### Prerequisites
- Python 3.11+
- OpenRouter API key (get from https://openrouter.ai/keys)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/talimbot/talimbot.git
cd talimbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variable:
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key-here"

# Linux/Mac
export OPENROUTER_API_KEY="your-api-key-here"
```

4. Run the server:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Access the application:
```
http://localhost:8000
```

### Railway Deployment

1. Fork this repository to your GitHub account

2. Create a new project on Railway.app

3. Connect your GitHub repository

4. Add environment variable in Railway dashboard:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key

5. Railway will auto-deploy using the Procfile

## Usage Guide

### Teacher Workflow

1. **Login**: Access teacher dashboard with password (default: teacher123)

2. **Monitor Students**: View student profile completion status

3. **Fill Test Data** (Optional): Use the test data generator to fill 10 sample students for testing

4. **Import Data** (Optional): Upload JSON file with student information

5. **Perform Grouping**:
   - Enter course name
   - Click "Start Grouping" button
   - Wait for AI processing (30-60 seconds)
   - Review generated groups with detailed reasoning

6. **Show Results**: Toggle result visibility to allow students to view their groups

7. **Reset Options**:
   - Reset Grouping: Clear groups, keep student data
   - Reset All Data: Complete system wipe

### Student Workflow

1. **Login**: Enter student number (S001-S030) and national code

2. **Complete Profile**:
   - Take MBTI personality test (external link)
   - Complete VARK learning style questionnaire
   - Fill AMS academic motivation scale (28 questions)
   - Complete cooperative skills assessment (25 questions)
   - Select up to 4 preferred groupmates (optional)

3. **Save Information**: Click "Save All Information" button

4. **View Group**: Access group view page to see assigned group (when teacher makes it visible)

## Grouping Algorithm

The AI grouping system follows a sophisticated 7-tier priority framework:

1. **ZPD Optimization (30%)**: Mixes high and medium performers for peer tutoring
2. **MBTI Complementarity (25%)**: Pairs complementary personality types (e.g., ENFP+INTJ)
3. **VARK Diversity (20%)**: Ensures multiple learning styles in each group
4. **Academic Motivation (15%)**: Distributes high-motivation students across groups
5. **Cooperative Skills (10%)**: Balances teamwork abilities
6. **Course-Specific Requirements**: Adapts to subject matter needs
7. **Student Preferences (5%)**: Honors preferences when they don't compromise other criteria

Groups are typically 5 students each, with some groups of 4 to avoid very small groups.

## Data Structure

### Student Object
```json
{
  "studentNumber": "S001",
  "name": "Student Name",
  "nationalCode": "1234567890",
  "mbti": "INTJ",
  "learningStyle": "Visual",
  "ams": "150",
  "cooperative": "95",
  "grade": 18.5,
  "preferredStudents": ["S002", "S003"],
  "group": 1
}
```

## API Endpoints

- `GET /api/students` - Get all students
- `GET /api/student/{student_number}` - Get specific student
- `PUT /api/student/{student_number}` - Update student data
- `POST /api/grouping/perform` - Execute AI grouping
- `GET /api/grouping/status` - Get grouping statistics
- `POST /api/grouping/reset` - Reset grouping only
- `POST /api/data/reset-all` - Reset all data
- `POST /api/grouping/toggle-visibility` - Show/hide results
- `POST /api/auth/teacher` - Verify teacher password
- `POST /api/auth/student` - Authenticate student
- `GET /api/student/{student_number}/group` - Get student's group

## Security Notes

- Student data stored in students.json (excluded from version control)
- Teacher password: "teacher123" (change in production)
- National codes used for student authentication
- API key required for AI grouping functionality

## Educational Foundation

This system is based on:
- **Vygotsky's Zone of Proximal Development (ZPD)**: Optimal learning occurs when students work slightly above their current level with peer support
- **MBTI Complementarity Research**: Diverse personality types enhance team creativity and problem-solving
- **VARK Learning Theory**: Multiple learning styles improve knowledge retention
- **Academic Motivation Scale (AMS)**: Measures intrinsic and extrinsic motivation factors
- **Cooperative Learning Principles**: Teamwork skills are essential for collaborative success

## License

This project is for educational purposes.

## Contributors

Developed for educational psychology research and classroom implementation.

## Support

For issues or questions, please refer to the documentation in the `resources_references/` folder.

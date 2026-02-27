# TalimBot

An intelligent educational platform for creating optimal student learning groups based on psychological principles and educational research.

## Overview

TalimBot is a web-based application designed to help teachers create effective learning groups by analyzing student characteristics including personality types (MBTI), learning styles (VARK), academic motivation, and cooperative learning tendencies. The system uses AI to generate balanced groups that promote collaborative learning.

## Features

**Teacher Dashboard**
- Manage student data and grouping criteria
- View and analyze group compositions
- Control visibility of grouping results

**Student Dashboard**
- Complete personality assessments (MBTI)
- Identify learning style preferences (VARK)
- Answer motivation and cooperation questionnaires
- View assigned groups and group members

**AI-Powered Grouping**
- Analyzes multiple factors: personality types, learning styles, academic performance
- Creates balanced groups based on educational psychology principles
- Provides reasoning for each group composition

## Technology Stack

**Backend**
- FastAPI (Python 3.11)
- JSON-based data storage
- OpenRouter API integration

**Frontend**
- Vanilla JavaScript
- Tailwind CSS for styling
- Fully responsive design with RTL support

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── grouping_logic.py    # AI grouping algorithms
├── data/                # Student data storage
├── static/              # Web interface files
├── liara.json           # Liara deployment config
└── requirements.txt     # Python dependencies
```

## Setup

### Prerequisites
- Python 3.11+
- OpenRouter API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Parinaz11/talimbot.git
cd talimbot/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

4. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

5. Open your browser:
```
http://localhost:8000
```

## Deployment

The application is configured for deployment on Liara (Iranian cloud platform). Upon pushing to the main branch, GitHub Actions automatically deploys the application.

## License

MIT

## Author

Developed for educational purposes.

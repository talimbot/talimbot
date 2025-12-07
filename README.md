# TalimBot - سیستم گروه‌بندی هوشمند دانش‌آموزان

A full-stack intelligent student grouping system using AI-powered analysis with FastAPI backend and GitHub Pages frontend.

## 🎯 Overview

TalimBot groups 30 real students based on MBTI personality types, learning styles, math grades, and peer preferences using AI (GPT-4o-mini via OpenRouter). Teachers control when students can view their group assignments.

### Real Student Data
- **30 Students** from class 1061 (دهم تجربی)
- **Persian Names**: Full Persian names from actual class roster
- **National Code Authentication**: Students login with their national ID
- **Math Grades**: Real grades from student records

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+ installed
- Modern web browser
- Internet connection (for AI grouping)

### Step 1: Start Backend (30 seconds)

```powershell
# Navigate to backend folder
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
python main.py
```

**Server runs on:** `http://localhost:8000`

**Keep this terminal running!**

### Step 2: Open Frontend (10 seconds)

**Option A - Direct Open (Easiest):**
- Double-click `index.html` in File Explorer

**Option B - Local Server (Recommended):**
```powershell
# In a NEW terminal window
python -m http.server 3000
```
Then visit: `http://localhost:3000`

---

## 👥 Login Credentials

### Students (30 students available)
Login with:
- **Student Number:** S001, S002, ..., S030
- **National Code:** Each student's 10-digit national ID

**Example:**
- Student Number: `S001`
- National Code: `929986644`
- Name: آدینه پور - یاسمن

### Teacher
- **Password:** `teacher123`

---

## 📋 How It Works

### For Students:

1. **Login**
   - Enter student number (S001-S030)
   - Enter your 10-digit national code
   - System displays your Persian name

2. **Complete Profile**
   - Take MBTI test (link provided)
   - Take VARK learning style test (link provided)
   - Fill out AMS and Cooperative preferences
   - Select up to 4 preferred groupmates
   - Save your information

3. **View Group** (after teacher enables)
   - See your group number
   - View all group members
   - Read AI reasoning in Persian

### For Teachers:

1. **Monitor Progress**
   - View dashboard with statistics
   - See which students completed profiles
   - Check readiness for grouping

2. **Perform Grouping**
   - Enter course name
   - Click "Start Grouping"
   - AI analyzes all data (10-30 seconds)
   - Review generated groups with Persian reasoning

3. **Control Visibility**
   - Groups are hidden by default
   - Click "Show Results to Students"
   - Toggle visibility on/off anytime

4. **Manage Data**
   - View all student information
   - Edit student data if needed
   - Reset grouping when necessary

---

## 🌐 Deployment to GitHub Pages

### Part 1: Deploy Frontend to GitHub Pages

1. **Create GitHub Repository**
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial commit with real student data"
   
   # Create repo on GitHub and push
   git remote add origin https://github.com/talimbot/talimbot.git
   git branch -M main
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
   - Click Save

3. **Your site will be live at:**
   `https://talimbot.github.io/talimbot/`

### Part 2: Deploy Backend to Render.com (Free)

1. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name:** `talimbot-backend`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** Free

3. **Add Environment Variable**
   - In Render dashboard → Environment
   - Add: `OPENROUTER_API_KEY` = `your-api-key`
   - Optionally: `TEACHER_PASSWORD` = `your-password`

4. **Get Your Backend URL**
   - Copy the URL (e.g., `https://talimbot-backend.onrender.com`)

### Part 3: Update Frontend to Use Deployed Backend

Update `API_BASE_URL` in BOTH files:
- `assets/js/data.js`
- `assets/js/grouping.js`

```javascript
// Change from:
const API_BASE_URL = 'http://localhost:8000/api';

// To:
const API_BASE_URL = 'https://talimbot-backend.onrender.com/api';
```

Commit and push changes:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

GitHub Pages will auto-deploy in ~1 minute.

---

## 🔧 Configuration

### API Key (OpenRouter)
Located in `backend/grouping_logic.py`:
```python
OPENROUTER_API_KEY = 'sk-or-v1-...'
```

### Teacher Password
Located in `backend/main.py` (SystemData model):
```python
teacherPassword: str = "teacher123"
```

Change as needed for security.

### Student Data
Students are initialized in `backend/main.py` in the `load_data()` function.
All 30 real students with Persian names and national codes are pre-loaded.

---

## 📁 Project Structure

```
talimbot/
├── backend/
│   ├── main.py              # FastAPI server with real student data
│   ├── grouping_logic.py    # AI grouping with OpenRouter
│   ├── requirements.txt     # Python dependencies
│   ├── README.md            # Backend documentation
│   └── data/
│       └── students.json    # Auto-created data storage
│
├── assets/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── data.js          # API client for student data
│       └── grouping.js      # API client for grouping
│
├── pages/
│   ├── login.html           # Login with national code
│   ├── student-dashboard.html
│   ├── student-data.html
│   ├── teacher-dashboard.html
│   └── group-view.html
│
├── Icons/                   # UI icons
├── index.html              # Redirects to login
├── README.md               # This file
├── .gitignore              # Git ignore rules
└── start-backend.ps1       # Windows startup script
```

---

## 🎯 Features

### ✅ Implemented
- **Real Student Data**: 30 actual students with Persian names
- **National Code Authentication**: Secure login using national IDs  
- **Persistent Storage**: JSON database on backend
- **AI-Powered Grouping**: OpenRouter GPT-4o-mini integration
- **Persian Language**: Full RTL support with Persian reasoning
- **Teacher Controls**: Show/hide results, reset grouping
- **Math Grades**: Real grades from class records
- **MBTI & Learning Styles**: Comprehensive personality analysis
- **Peer Preferences**: Students select preferred groupmates

### 🎨 UI Features
- Modern, responsive design with Tailwind CSS
- Persian (RTL) interface
- Real-time validation
- Progress indicators

---

## 🐛 Troubleshooting

### "Failed to fetch" errors
**Problem:** Backend not running or wrong URL
**Solution:**
1. Check backend is running: Visit `http://localhost:8000`
2. Should see: `{"message":"TalimBot API is running"}`
3. Check `API_BASE_URL` in JS files matches backend

### Students can't login
**Problem:** Wrong national code
**Solution:**
- National code must be exactly 10 digits
- Must match the code in backend database
- Check `backend/main.py` for correct codes

### Students can't see groups
**Problem:** Teacher hasn't enabled visibility
**Solution:**
- Teacher must click "Show Results to Students"
- Button appears after grouping is complete

### Grouping fails
**Problem:** API error or no internet
**Solution:**
1. Check internet connection
2. Verify OpenRouter API key is valid
3. Check backend logs for errors
4. System has fallback random grouping if AI fails

---

## 📊 Student List (Sample)

| # | Student Number | Name | National Code | Math Grade |
|---|----------------|------|---------------|------------|
| 1 | S001 | آدینه پور - یاسمن | 929986644 | 16.0 |
| 2 | S002 | احمدزاده - پریا | 980085330 | 12.0 |
| 3 | S003 | اکبرزاده - فاطمه | 970154550 | 11.0 |
| 4 | S004 | الهی مهر - آناهیتا | 26425955 | 17.0 |
| 5 | S005 | امیری - مریم | 980093341 | 18.0 |
| ... | ... | ... | ... | ... |
| 30 | S030 | وحدتی - باران | 929916913 | 12.0 |

*Full list available in `backend/main.py`*

---

## 🔐 Security Notes

### Current (Demo/Development):
- ✅ Simple password authentication
- ✅ CORS allows all origins
- ✅ National codes as passwords

### Recommended for Production:
- 🔒 Use environment variables for secrets
- 🔒 Implement JWT token authentication
- 🔒 Enable HTTPS only
- 🔒 Add rate limiting
- 🔒 Use PostgreSQL instead of JSON
- 🔒 Hash national codes
- 🔒 Implement proper session management

---

## 📞 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/students` | GET | Get all students |
| `/api/student/{id}` | GET | Get one student |
| `/api/student/{id}` | PUT | Update student |
| `/api/auth/student` | POST | Authenticate student |
| `/api/auth/teacher` | POST | Authenticate teacher |
| `/api/grouping/perform` | POST | Run AI grouping |
| `/api/grouping/status` | GET | Get stats |
| `/api/grouping/toggle-visibility` | POST | Show/hide results |
| `/api/grouping/reset` | POST | Clear grouping |
| `/api/student/{id}/group` | GET | Get student's group |

---

## 🎓 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **aiohttp** - Async HTTP client
- **OpenRouter API** - AI integration

### Frontend
- **HTML5 / CSS3** - Structure and styling
- **Tailwind CSS** - Utility-first CSS
- **JavaScript (Async/Await)** - Modern JS
- **Fetch API** - HTTP requests

### Deployment
- **GitHub Pages** - Frontend hosting (free)
- **Render.com** - Backend hosting (free)

---

## 📝 License

This project is for educational purposes.

---

## 🙏 Credits

- Student data from class 1061 (دهم تجربی)
- AI grouping powered by OpenRouter (GPT-4o-mini)

---

## ✅ Pre-Launch Checklist

- [ ] Backend running locally
- [ ] Students can login with national codes
- [ ] Teacher can login with password
- [ ] Grouping works with AI
- [ ] Visibility toggle works
- [ ] All 30 students load correctly
- [ ] Persian names display properly
- [ ] Math grades show correctly
- [ ] Backend deployed to Render
- [ ] Frontend deployed to GitHub Pages
- [ ] API URLs updated for production

---

**Live URL:** `https://talimbot.github.io/talimbot/pages/login.html`

**Last Updated:** December 2025

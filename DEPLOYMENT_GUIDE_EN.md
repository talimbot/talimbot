# 📘 Complete TalimBot Deployment Guide (English)

This guide will help you deploy TalimBot to **https://talimbot.github.io/talimbot**

---

## 🎯 System Overview

**TalimBot** is an intelligent student grouping system featuring:
- ✅ 30 real students with Persian names
- ✅ Authentication via national ID (9 digits)
- ✅ Persistent storage in JSON file (on backend server)
- ✅ AI-powered grouping (GPT-4o-mini via OpenRouter)
- ✅ Teacher-controlled result visibility

---

## 📋 Prerequisites

### For Local Development (Today):
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge)
- Internet connection

### For Production Deployment (Tomorrow):
- GitHub account (free)
- Render.com account (free)
- Git installed on your computer

---

## 🚀 Part 1: Local Testing (For Today)

### Step 1: Start the Backend Server

1. **Open Terminal** (PowerShell on Windows):
   ```powershell
   cd C:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend
   ```

2. **Install Python dependencies** (first time only):
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```powershell
   python main.py
   ```

4. **Verify** - You should see:
   ```
   INFO: Uvicorn running on http://127.0.0.1:8000
   ```

**⚠️ Keep this terminal open! The server must run continuously.**

---

### Step 2: Open the Frontend

**Option A - Easiest:**
1. Navigate to: `C:\Users\Parinaz\Desktop\Talim_Project\talimbot`
2. Double-click `index.html`
3. Login page opens in browser

**Option B - With Local Server (Recommended):**
1. Open a NEW terminal
2. Run:
   ```powershell
   cd C:\Users\Parinaz\Desktop\Talim_Project\talimbot
   python -m http.server 3000
   ```
3. Open browser and go to: `http://localhost:3000`

---

### Step 3: Test the System

#### Login as Student:
1. Select "دانش آموز" (Student)
2. Student Number: `S001`
3. National Code: `929986644`
4. Expected Name: **یاسمن آدینه پور** (Yasaman Adinepour)
5. Expected Grade: **18.77**

#### Login as Teacher:
1. Select "معلم" (Teacher)
2. Password: `teacher123`

**✅ If login succeeds, your local system works!**

---

## 🌐 Part 2: Internet Deployment (For Tomorrow)

### Phase 1: Prepare Your Code

1. **Open Terminal**:
   ```powershell
   cd C:\Users\Parinaz\Desktop\Talim_Project\talimbot
   ```

2. **Check Git installation**:
   ```powershell
   git --version
   ```
   If not installed, download from: https://git-scm.com/download/win

3. **Initialize Git** (if you haven't already):
   ```powershell
   git init
   git add .
   git commit -m "Initial commit with 30 real students"
   ```

---

### Phase 2: Deploy Backend to Render.com

#### 2.1. Create Render Account
1. Go to: https://render.com
2. Sign up (using GitHub account is easier)

#### 2.2. Connect Repository to Render
1. In GitHub, create a new repository named `talimbot`
2. Push your code:
   ```powershell
   git remote add origin https://github.com/talimbot/talimbot.git
   git branch -M main
   git push -u origin main
   ```

#### 2.3. Create Web Service in Render
1. In Render, click **"New +"** → **"Web Service"**
2. Select repository: `talimbot/talimbot`
3. Configuration:
   - **Name**: `talimbot-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: `Free`

4. Click **"Create Web Service"**

#### 2.4. Wait for Deployment
- Time: 3-5 minutes
- When complete, your server URL will be:
  ```
  https://talimbot-backend.onrender.com
  ```

**⚠️ Save this URL! You'll need it.**

---

### Phase 3: Update Frontend API URLs

Edit TWO files to point to your production backend:

#### File 1: `assets/js/data.js`
Find line 5:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change to:
```javascript
const API_BASE_URL = 'https://talimbot-backend.onrender.com/api';
```

#### File 2: `assets/js/grouping.js`
Find line 5:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change to:
```javascript
const API_BASE_URL = 'https://talimbot-backend.onrender.com/api';
```

**Save and commit:**
```powershell
git add assets/js/data.js assets/js/grouping.js
git commit -m "Update API URL for production"
git push
```

---

### Phase 4: Deploy Frontend to GitHub Pages

1. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Settings → Pages
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

2. **Wait** (1-2 minutes)

3. **Test your site**:
   - Main URL: `https://talimbot.github.io/talimbot/`
   - Login page: `https://talimbot.github.io/talimbot/pages/login.html`

---

## ✅ Pre-Launch Checklist

Before using tomorrow, verify these items:

### Backend (Render):
- [ ] Render service is active (Status: Live)
- [ ] Backend URL works: `https://talimbot-backend.onrender.com`
- [ ] Test endpoint: Open in browser - should see:
  ```json
  {"message": "TalimBot API is running"}
  ```

### Frontend (GitHub Pages):
- [ ] Site opens: `https://talimbot.github.io/talimbot/`
- [ ] Login page displays correctly
- [ ] Student can login (S001 / 929986644)
- [ ] Teacher can login (teacher123)

### Functionality:
- [ ] Student can save profile
- [ ] After page refresh, data persists
- [ ] Teacher can perform grouping
- [ ] Teacher can show/hide results
- [ ] Students see groups only after teacher enables visibility

---

## 🔧 Common Issues & Solutions

### Issue 1: "Failed to fetch" in browser
**Cause:** Backend not running or wrong URL

**Solution:**
1. Check Render service is running
2. Verify URL in `data.js` and `grouping.js`
3. Check backend logs in Render dashboard

### Issue 2: Student cannot login
**Cause:** Wrong national code or backend data changed

**Solution:**
1. Verify national code: Must be 9 digits (without leading 0)
2. Correct example: S001 → 929986644

### Issue 3: Data not saving
**Cause:** Frontend connected to localStorage instead of backend

**Solution:**
1. Press F12 → Console → Check for errors
2. Ensure API_BASE_URL points to Render
3. Check Network tab for API requests

### Issue 4: Render service appears offline (Cold Start)
**Cause:** Free plan sleeps after 15 minutes of inactivity

**Solution:**
1. First visit: Wait 30-60 seconds
2. Server wakes up after first request
3. To prevent: Use paid plan or keep-alive service

---

## 🎓 Teacher Dashboard Visibility Control

The visibility toggle button appears **ONLY after grouping is complete**:

### Before Grouping:
- Button is hidden
- Only "Start Grouping" button shows

### After Grouping:
- "Toggle Visibility" button appears
- Default state: **Hidden** (students cannot see groups)
- Teacher must click "Show Results to Students" to enable visibility
- Button text changes based on state:
  - 🔵 "نمایش نتایج به دانش‌آموزان" (Show Results) - Currently hidden
  - 🟠 "مخفی کردن نتایج از دانش‌آموزان" (Hide Results) - Currently visible

### Student Experience:
- If visibility = OFF: Message "نتایج گروه‌بندی هنوز نمایش داده نشده" (Results not yet shown)
- If visibility = ON: Full group details visible

---

## 📊 Student Credentials

All 30 students with real data:

| # | Student Number | Name (Persian) | National Code | Grade (معدل) |
|---|----------------|----------------|---------------|--------------|
| 1 | S001 | یاسمن آدینه پور | 929986644 | 18.77 |
| 2 | S002 | پریا احمدزاده | 980085330 | 17.28 |
| 3 | S003 | فاطمه اکبرزاده | 970154550 | 16.71 |
| ... | ... | ... | ... | ... |
| 30 | S030 | باران وحدتی | 929916913 | 15.02 |

**📄 Complete list in:** `backend/main.py` lines 69-98

---

## 🔐 Security Considerations

### Current Setup (Testing/Demo):
- ✅ Simple teacher password: `teacher123`
- ✅ National codes as passwords
- ✅ CORS allows all origins

### Production Recommendations:
- 🔒 Change teacher password (environment variable)
- 🔒 Hash national codes (bcrypt or similar)
- 🔒 Implement JWT token authentication
- 🔒 Enforce HTTPS only
- 🔒 Add rate limiting
- 🔒 Use real database (PostgreSQL)
- 🔒 Restrict CORS to specific domain

---

## 📞 Support & Debugging

### If something goes wrong:

1. **Check Browser Console** (F12):
   - Note any red errors

2. **Check Render Logs**:
   - Render Dashboard → Your Service → Logs tab
   - Look for Python errors

3. **Test Backend Directly**:
   ```
   https://talimbot-backend.onrender.com/api/students
   ```
   Should return student list

4. **Compare Local vs Production**:
   - If Local works but Production doesn't → URL issue
   - If Local also fails → Code issue

---

## 💡 About the JSON File Question

**Your question:** "Isn't it better to have an initial .json file instead of hardcoding?"

**Answer:** You're absolutely right! Here are both approaches:

### Current Approach (Hardcoded in Python):
**Pros:**
- ✅ Simple deployment (one less file to manage)
- ✅ Data auto-creates on first run
- ✅ Easy to version control the "reset" state

**Cons:**
- ❌ Harder to update student data (must edit Python code)
- ❌ Mixing data with logic
- ❌ Need to restart server to change initial data

### Better Approach (Initial JSON file):
**Structure:**
```
backend/
├── main.py
├── requirements.txt
├── initial_data.json       ← Initial template
└── data/
    └── students.json       ← Active data (auto-created)
```

**Benefits:**
- ✅ Separate data from code
- ✅ Easy to update students (edit JSON)
- ✅ Can reset to initial state easily
- ✅ Non-programmers can modify data

**I can convert to this approach if you'd like!** Just say the word and I'll:
1. Create `backend/initial_data.json` with all 30 students
2. Update `main.py` to load from this file
3. Add a "reset to initial" function

---

## 🎉 Success Indicators

If all checks pass:

✅ **Your site is live at:**
```
https://talimbot.github.io/talimbot/pages/login.html
```

✅ **30 students can:**
- Login with national code
- Fill their profiles
- Data persists (even after refresh)
- View groups (when teacher allows)

✅ **Teacher can:**
- Monitor student progress
- Run AI-powered grouping
- Control result visibility
- Manage all data

---

## 📚 Important Files

```
talimbot/
├── backend/
│   ├── main.py                 # FastAPI server + 30 students
│   ├── grouping_logic.py       # AI grouping logic
│   ├── requirements.txt        # Python packages
│   └── data/
│       └── students.json       # Persistent storage (auto-created)
│
├── assets/js/
│   ├── data.js                 # API Client (UPDATE URL HERE!)
│   └── grouping.js             # API Client (UPDATE URL HERE!)
│
├── pages/
│   ├── login.html              # Login page
│   ├── student-dashboard.html  # Student dashboard
│   ├── teacher-dashboard.html  # Teacher dashboard
│   └── group-view.html         # Group view
│
├── index.html                  # Main page (redirects to login)
├── README.md                   # Project info
├── DEPLOYMENT_GUIDE.md         # Persian guide
└── DEPLOYMENT_GUIDE_EN.md      # This file!
```

---

## ⏰ Timeline for Tomorrow

### Morning (Before Class):
1. ✅ Check Render backend (should be Live)
2. ✅ Open GitHub Pages site
3. ✅ Test with one student (S001)
4. ✅ Test with teacher login (teacher123)

### During Class:
1. 👨‍🎓 Students login: `https://talimbot.github.io/talimbot/pages/login.html`
2. 📝 Fill their profiles (MBTI, VARK, AMS, preferences)
3. ⏳ Wait for teacher to complete grouping

### After Profiles Complete:
1. 🧑‍🏫 Teacher logs in
2. ▶️ Clicks "Start Grouping" button
3. ⏰ Waits 10-30 seconds (AI processing)
4. 👁️ Clicks "Show Results to Students" button
5. ✅ Students can now view their groups!

---

**🎯 You're ready for tomorrow!**

Good luck! 🚀

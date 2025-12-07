# 🚀 Backend Deployment Guide - Step by Step

## 🎯 Problem Overview

**Current Situation:**
- ✅ GitHub Pages works: `https://talimbot.github.io/talimbot/`
- ❌ Backend on laptop only: `http://localhost:8000` (not accessible from internet)
- ❌ Mobile/other devices can't connect to localhost

**Solution:**
Deploy backend to a cloud service so it has a real URL like:
`https://talimbot-api.onrender.com`

---

## 🌟 Option 1: Render.com (RECOMMENDED - FREE)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with **GitHub** (easiest - auto-connects your repo)

### Step 2: Create New Web Service
1. After login, click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Find and select your **talimbot** repository
4. Click **"Connect"**

### Step 3: Configure Service
Fill in these settings:

**Name:** `talimbot-api` (or any name you like)

**Region:** Choose closest to you (e.g., Frankfurt, Oregon)

**Branch:** `main`

**Root Directory:** Leave empty (or put `backend`)

**Runtime:** `Python 3`

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:** `Free` (select from dropdown)

### Step 4: Deploy
1. Click **"Create Web Service"** at the bottom
2. Wait 2-3 minutes for deployment (you'll see logs)
3. When you see "Live" with a green dot - it's ready! ✅

### Step 5: Get Your Backend URL
Look at the top of the page, you'll see:
```
https://talimbot-api.onrender.com
```
**Copy this URL!** You'll need it in the next step.

### Step 6: Update Frontend Configuration
Edit `assets/js/data.js` in your repository:

**Change this:**
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

**To this:**
```javascript
const API_BASE_URL = 'https://talimbot-api.onrender.com/api';
```
(Replace `talimbot-api` with your actual Render service name)

### Step 7: Push Changes to GitHub
```bash
git add assets/js/data.js
git commit -m "Update API URL to production backend"
git push origin main
```

### Step 8: Test Your Site
1. Wait 1-2 minutes for GitHub Pages to update
2. Open `https://talimbot.github.io/talimbot/`
3. Try logging in as S001
4. It should work! 🎉

---

## ⚠️ Important Notes for Render.com Free Tier

### Automatic Sleep
- Free tier services **sleep after 15 minutes of inactivity**
- First request after sleep takes **30-60 seconds** to wake up
- Subsequent requests are fast

### Solution for Sleep Issue:
Use a service like **UptimeRobot** (free) to ping your API every 14 minutes:
1. Sign up at https://uptimerobot.com
2. Add monitor: `https://talimbot-api.onrender.com/api/students`
3. Check interval: 5 minutes
4. This keeps your service awake during active hours

---

## 🌟 Option 2: Railway.app (Easy Alternative)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **talimbot** repository
4. Railway auto-detects Python and deploys!

### Step 3: Configure (if needed)
If it doesn't auto-start:
- Go to Settings
- Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Get URL
1. Go to your service
2. Click **"Settings"** → **"Domains"**
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `https://talimbot-api.up.railway.app`)

### Step 5: Update Frontend
Same as Render - edit `assets/js/data.js` with your Railway URL.

---

## 🌟 Option 3: PythonAnywhere (Manual but Stable)

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Create free "Beginner" account

### Step 2: Upload Files
1. Go to **"Files"** tab
2. Upload all files from `backend/` folder
3. Upload `requirements.txt`

### Step 3: Install Dependencies
1. Go to **"Consoles"** tab
2. Start a **Bash console**
3. Run:
```bash
pip install --user -r requirements.txt
```

### Step 4: Configure Web App
1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Choose **Python 3.10**
5. In WSGI configuration file, replace content with:
```python
from main import app as application
```

### Step 5: Set Working Directory
- Source code: `/home/yourusername/`
- Working directory: `/home/yourusername/`

### Step 6: Reload and Get URL
1. Click **"Reload"** at top
2. Your URL: `https://yourusername.pythonanywhere.com`

---

## 🧪 Testing Your Deployment

### Test 1: API is Alive
Visit in browser:
```
https://your-backend-url.onrender.com/api/students
```
Should return JSON with student data.

### Test 2: Login from Phone
1. Open `https://talimbot.github.io/talimbot/` on your phone
2. Try logging in as S001
3. Should work without errors!

### Test 3: Grouping Works
1. Login as teacher
2. Try creating groups
3. Enter your OpenRouter API key when prompted
4. Groups should be created successfully

---

## 🔧 Troubleshooting

### "CORS Error" in Browser Console
**Fix:** Your backend's CORS is already configured to allow all origins (`allow_origins=["*"]`). This should work.

For better security in production, edit `backend/main.py`:
```python
allow_origins=["https://talimbot.github.io"],
```

### "502 Bad Gateway" on Render
- Service might be starting (wait 30 seconds)
- Check Render logs for errors
- Verify Start Command is correct

### "Module not found" Error
- Check `requirements.txt` has all dependencies
- Redeploy with correct Build Command

### Students Data Resets After Deployment
- Free tier services may reset files on restart
- **Solution:** Download data regularly using the download button
- **Better Solution:** Use a database (MongoDB Atlas free tier) instead of JSON file

---

## 📊 Quick Comparison

| Service | Free Tier | Sleep | Setup | Speed |
|---------|-----------|-------|-------|-------|
| **Render** | ✅ Yes | 15 min | Easy | Fast |
| **Railway** | ✅ $5 credit | No | Easiest | Fastest |
| **PythonAnywhere** | ✅ Yes | No | Manual | Medium |

**Recommendation:** Start with **Render.com** - easiest setup, good performance.

---

## 🎯 Quick Start (TL;DR)

1. **Sign up** at https://render.com with GitHub
2. **New Web Service** → Connect your `talimbot` repo
3. **Configure:**
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** and copy your URL
5. **Update** `assets/js/data.js` with your URL
6. **Push** to GitHub
7. **Test** on phone - it works! 🎉

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **PythonAnywhere Docs:** https://help.pythonanywhere.com

---

**After deploying, your system will work from anywhere in the world!** 🌍

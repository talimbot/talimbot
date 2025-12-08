# 🚂 Railway Deployment Guide for TalimBot

## 📋 Overview
This guide will help you deploy your complete TalimBot application (Frontend + Backend) to Railway for free, making it accessible from anywhere.

## ✅ What We've Done (Preparation Complete!)

### 1. **Restructured the Project**
- ✅ Created `backend/static/` folder
- ✅ Moved all frontend files (HTML, CSS, JS, Icons) to `backend/static/`
- ✅ Updated `main.py` to serve static files
- ✅ Updated `data.js` to use relative API paths for Railway

### 2. **Updated FastAPI Configuration**
Your `backend/main.py` now:
- Serves static files from `backend/static/` folder
- Uses environment variable for OpenRouter API key
- Handles both frontend (HTML pages) and backend (API endpoints) from the same server
- Works seamlessly on Railway's deployment platform

### 3. **Project Structure**
```
talimbot/
├── .env                     # LOCAL ONLY - Contains your API key (NEVER commit this!)
├── .env.example             # Template for environment variables
├── .gitignore               # Ensures .env is not committed
├── Procfile                 # Tells Railway how to start the server
├── runtime.txt              # Specifies Python version
├── README.md                
├── RAILWAY_DEPLOYMENT.md    
├── backend/
│   ├── main.py              # ✅ UPDATED - Serves static files + API endpoints
│   ├── grouping_logic.py    
│   ├── requirements.txt     
│   ├── data/
│   │   └── students.json    
│   └── static/              # ✅ NEW - All frontend files
│       ├── index.html       
│       ├── assets/          # CSS and JS files
│       │   ├── css/
│       │   │   └── styles.css
│       │   └── js/
│       │       ├── data.js  # ✅ UPDATED - Uses relative API paths
│       │       └── grouping.js
│       ├── pages/           # All HTML pages
│       │   ├── login.html
│       │   ├── student-dashboard.html
│       │   ├── teacher-dashboard.html
│       │   ├── ams-questionnaire.html
│       │   ├── cooperative-questionnaire.html
│       │   └── group-view.html
│       └── Icons/           # Logo and icons
```

---

## 🚀 Deployment Steps

### **Step 1: Verify Local Setup**

1. **Create `.env` file** (if you haven't already):
   ```bash
   # In the project root (talimbot/) folder
   echo OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here > .env
   ```

2. **Test locally**:
   ```bash
   cd backend
   python main.py
   ```
   
3. **Open browser** to `http://localhost:8000`
   - You should see the index.html page
   - All pages should work (login, dashboards, questionnaires)
   - API calls should work (grouping, data saving)

---

### **Step 2: Commit Changes to GitHub**

⚠️ **IMPORTANT**: Make sure `.env` is in `.gitignore` (it already is!)

```bash
# From the talimbot/ directory
git add .
git status  # Verify .env is NOT listed (should only see modified files)

git commit -m "Restructure project for Railway deployment - serve frontend from backend"
git push origin main
```

---

### **Step 3: Deploy to Railway**

#### A. **Sign Up / Log In**
1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with your GitHub account

#### B. **Create New Project**
1. Click **"Deploy from GitHub repo"**
2. Select your `talimbot` repository
3. Railway will automatically detect it's a Python project

#### C. **Configure Environment Variables**
1. In the Railway dashboard, go to your project
2. Click on the **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   - **Key**: `OPENROUTER_API_KEY`
   - **Value**: `sk-or-v1-your-actual-openrouter-api-key`
5. Click **"Add"**

#### D. **Verify Deployment Settings**
Railway auto-detects settings from your files:
- ✅ **Build Command**: None needed (Python dependencies auto-installed)
- ✅ **Start Command**: From `Procfile` → `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ **Python Version**: From `runtime.txt` → `python-3.11.0`

#### E. **Deploy!**
1. Click **"Deploy"**
2. Wait 2-3 minutes for deployment
3. Railway will show deployment logs
4. When complete, you'll see: ✅ **"Deployment successful"**

#### F. **Get Your URL**
1. In Railway dashboard, click **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `https://talimbot-production-abc123.up.railway.app`)

---

### **Step 4: Test Your Deployed Application**

1. **Open your Railway URL** in a browser
2. **Test all features**:
   - ✅ Main page loads (`index.html`)
   - ✅ Login page works (`/pages/login.html`)
   - ✅ Student dashboard loads
   - ✅ Teacher dashboard loads
   - ✅ Questionnaires work (AMS, Cooperative)
   - ✅ Grouping functionality works
   - ✅ Data saves correctly

---

## 🔧 How It Works

### **Single Server Architecture**
Railway runs ONE server that handles BOTH:

1. **Frontend (Static Files)**:
   - `GET /` → Serves `index.html`
   - `GET /pages/login.html` → Serves login page
   - `GET /assets/css/styles.css` → Serves CSS
   - `GET /assets/js/data.js` → Serves JavaScript

2. **Backend (API Endpoints)**:
   - `POST /api/grouping` → AI grouping logic
   - `GET /api/students` → Get all students
   - `PUT /api/students/{id}` → Update student
   - All other API routes in `main.py`

### **How Requests Are Routed**

```
User Browser → Railway URL
              ↓
        FastAPI Server (main.py)
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  /api/*            Everything else
(API Endpoints)     (Static Files)
    ↓                   ↓
grouping_logic.py   backend/static/
OpenRouter API        (HTML/CSS/JS)
```

### **Environment Variable Flow**

```
Local Development:
.env file → load_dotenv() → os.getenv("OPENROUTER_API_KEY")

Railway Production:
Railway Variables → os.getenv("OPENROUTER_API_KEY")
```

---

## 📊 Monitoring & Management

### **View Logs**
1. Go to Railway dashboard
2. Click on your project
3. Click **"Deployments"** tab
4. Click on the latest deployment
5. View real-time logs

### **Check Usage**
- Railway free tier: **$5 credit/month**
- Your app should use: **~$2-3/month**
- Monitor usage in **"Usage"** tab

### **Redeploy (After Code Changes)**
1. Make changes locally
2. Test locally (`python main.py`)
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
4. Railway **auto-deploys** within 1-2 minutes!

---

## 🆘 Troubleshooting

### **Problem: API calls fail (404 errors)**
**Solution**: API routes must start with `/api/`
- ✅ Correct: `POST /api/grouping`
- ❌ Wrong: `POST /grouping`

### **Problem: Static files not loading (CSS/JS missing)**
**Solution**: 
1. Verify files are in `backend/static/` folder
2. Check browser console for 404 errors
3. Ensure paths in HTML are relative (e.g., `/assets/css/styles.css`)

### **Problem: OpenRouter API errors**
**Solution**:
1. Verify API key is correct in Railway Variables
2. Check you have credits in your OpenRouter account
3. View logs in Railway to see exact error message

### **Problem: Server won't start**
**Solution**:
1. Check Railway logs for error messages
2. Verify `requirements.txt` has all dependencies
3. Ensure `Procfile` command is correct

---

## 🎯 Success Checklist

After deployment, verify:

- [ ] Railway URL loads the main page
- [ ] All navigation links work
- [ ] Login system works (student/teacher)
- [ ] Student dashboard loads
- [ ] Teacher dashboard loads
- [ ] AMS questionnaire works and saves
- [ ] Cooperative questionnaire works and saves
- [ ] AI grouping creates groups successfully
- [ ] Student data persists after refresh
- [ ] API calls complete without errors
- [ ] No console errors in browser DevTools

---

## 💡 Next Steps

Once deployed successfully:

1. **Share the Railway URL** with your teacher
2. **Test from different devices** (phone, tablet)
3. **Monitor Railway dashboard** for any errors
4. **Keep your OpenRouter API key secure**
5. **Consider upgrading Railway plan** if you exceed free tier

---

## 📞 Support Resources

- **Railway Docs**: https://docs.railway.app
- **OpenRouter Docs**: https://openrouter.ai/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Your Deployment Guide**: `RAILWAY_DEPLOYMENT.md`

---

## 🎉 Congratulations!

Your TalimBot is now a **real, independent website** accessible from anywhere! 🚀

**Your app URL**: `https://your-project.up.railway.app`

Teachers and students can access it from:
- ✅ Home computers
- ✅ School computers
- ✅ Phones (any device with internet)
- ✅ Tablets

No need for localhost, no need for running Python locally - it's fully online! 🌐

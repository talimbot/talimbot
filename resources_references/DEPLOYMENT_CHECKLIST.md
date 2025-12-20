# ✅ Railway Deployment Checklist

## Pre-Deployment Verification

### ✅ Local Testing Complete
- [x] Project restructured with `backend/static/` folder
- [x] All frontend files copied to `backend/static/`
- [x] `main.py` updated to serve static files
- [x] `data.js` updated for Railway deployment
- [x] Local server tested and working (`http://localhost:8000`)
- [x] All pages accessible (index, login, dashboards, questionnaires)
- [x] API endpoints working (grouping, data saving)

### ✅ Git Repository Status
- [x] `.env` file in `.gitignore` (API key NOT committed)
- [x] All changes committed to Git
- [x] Changes pushed to GitHub main branch
- [x] Repository: `https://github.com/talimbot/talimbot`

---

## 🚂 Railway Deployment Steps

### Step 1: Create Railway Account
- [ ] Go to https://railway.app
- [ ] Click "Start a New Project"
- [ ] Sign in with GitHub account
- [ ] Authorize Railway to access your repositories

### Step 2: Deploy from GitHub
- [ ] Click "Deploy from GitHub repo"
- [ ] Select `talimbot/talimbot` repository
- [ ] Railway auto-detects Python project
- [ ] Deployment starts automatically

### Step 3: Configure Environment Variables
- [ ] Go to project dashboard
- [ ] Click "Variables" tab
- [ ] Click "+ New Variable"
- [ ] Add variable:
  - **Key**: `OPENROUTER_API_KEY`
  - **Value**: `sk-or-v1-your-actual-key-here`
- [ ] Click "Add"

### Step 4: Generate Public URL
- [ ] Go to "Settings" tab
- [ ] Scroll to "Networking" section
- [ ] Click "Generate Domain"
- [ ] Copy your URL: `https://talimbot-production-xxxx.up.railway.app`

### Step 5: Wait for Deployment
- [ ] Monitor deployment in "Deployments" tab
- [ ] Wait 2-3 minutes for build to complete
- [ ] Look for "✅ Deployment successful" message

---

## 🧪 Post-Deployment Testing

### Test All Features
Visit your Railway URL and verify:

#### Frontend Pages
- [ ] Main page loads (`/`)
- [ ] Login page works (`/pages/login.html`)
- [ ] Student dashboard loads and functions
- [ ] Teacher dashboard loads and functions
- [ ] AMS questionnaire page works
- [ ] Cooperative questionnaire page works
- [ ] Group view page displays correctly

#### Authentication & Navigation
- [ ] Can login as student (use student number from data)
- [ ] Can login as teacher (password: `teacher123`)
- [ ] Navigation between pages works
- [ ] Back buttons work correctly
- [ ] Logout functionality works

#### Student Features
- [ ] MBTI test can be filled and saved
- [ ] VARK test can be filled and saved
- [ ] AMS questionnaire completes and auto-saves score
- [ ] Cooperative questionnaire completes and auto-saves score
- [ ] Preferred students selection works (max 4)
- [ ] "Save All Data" button saves successfully
- [ ] Data persists after page refresh
- [ ] Can view assigned group

#### Teacher Features
- [ ] Can view all students in table
- [ ] Can edit student information
- [ ] Can add new students
- [ ] Can delete students
- [ ] Download data button works
- [ ] Toggle visibility for students works
- [ ] AI Grouping functionality works
  - [ ] Can select course (Riazi, Faravari, etc.)
  - [ ] Grouping completes successfully
  - [ ] Groups are created and saved
  - [ ] Students can see their groups
- [ ] AMS and Cooperation columns display correctly

#### API & Data Persistence
- [ ] API calls complete without errors (check browser console)
- [ ] Student data saves to backend
- [ ] Data persists between sessions
- [ ] Groups persist after creation
- [ ] No 404 errors for API endpoints
- [ ] No CORS errors in console

---

## 🔍 Troubleshooting Guide

### If pages don't load:
1. Check Railway deployment logs for errors
2. Verify `backend/static/` folder contains all files
3. Check browser console for 404 errors

### If API calls fail:
1. Verify environment variable `OPENROUTER_API_KEY` is set
2. Check Railway logs for API errors
3. Test API endpoints directly: `https://your-url.railway.app/api/students`

### If grouping doesn't work:
1. Verify OpenRouter API key is correct
2. Check you have credits in OpenRouter account
3. View Railway logs during grouping attempt
4. Ensure request is reaching `/api/grouping` endpoint

### If static files are missing:
1. Verify files exist in `backend/static/` folder locally
2. Ensure git committed and pushed all files
3. Trigger manual redeploy in Railway
4. Check file paths in HTML are correct (relative paths)

---

## 📊 Monitoring

### Check Deployment Status
- [ ] Railway dashboard shows "Active" status
- [ ] Latest deployment timestamp is recent
- [ ] No error messages in deployment logs

### Monitor Usage
- [ ] View usage in Railway "Usage" tab
- [ ] Verify you're within free tier ($5/month)
- [ ] Estimated usage: ~$2-3/month

### View Logs
- [ ] Real-time logs available in "Deployments" tab
- [ ] Check logs for any errors or warnings
- [ ] Monitor API request logs

---

## 🎯 Final Verification

### Complete Success Criteria
- [ ] Application is accessible from any device with internet
- [ ] All features work identically to localhost version
- [ ] No errors in browser console
- [ ] No errors in Railway logs
- [ ] Data persistence works correctly
- [ ] AI grouping creates groups successfully
- [ ] Teachers can manage students
- [ ] Students can complete questionnaires

### Share with Users
- [ ] Copy Railway URL
- [ ] Share URL with teacher
- [ ] Provide login instructions:
  - Teacher: Password is `teacher123`
  - Students: Use their student number
- [ ] Explain how to access from any device

---

## 🚀 You're Done!

Once all checkboxes are checked, your TalimBot is:
- ✅ **Fully deployed** on Railway
- ✅ **Accessible from anywhere** via the internet
- ✅ **Secure** (API key in environment variables)
- ✅ **Free** (within Railway's $5/month credit)
- ✅ **Professional** (real production website)

**Your Live URL**: `https://your-project.up.railway.app`

---

## 📝 Next Steps

1. **Bookmark your Railway dashboard** for monitoring
2. **Keep your OpenRouter API key safe** (never share it)
3. **Monitor Railway usage** to stay within free tier
4. **Test from multiple devices** (phone, tablet, different computers)
5. **Collect feedback** from teachers and students

---

## 🆘 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Review**: `RAILWAY_SETUP_GUIDE.md` for detailed instructions

# 🚂 Railway Deployment Guide for TalimBot

## Quick Deploy to Railway.app

### Step 1: Create Railway Account
1. Go to: **https://railway.app**
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your repositories

### Step 2: Deploy from GitHub
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **"talimbot"** repository
4. Railway will automatically detect it's a Python project!

### Step 3: Add Environment Variable (IMPORTANT!)
1. In your Railway project, click on your service
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Add:
   - **Name:** `OPENROUTER_API_KEY`
   - **Value:** `sk-or-v1-your-actual-key-here` (get from https://openrouter.ai)
5. Click **"Add"**

### Step 4: Configure Build (if needed)
Railway usually auto-detects, but if it doesn't:
1. Go to **"Settings"** tab
2. **Build Command:** `pip install -r backend/requirements.txt`
3. **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 5: Deploy!
1. Railway deploys automatically
2. Wait 2-3 minutes for build to complete
3. You'll see "Active" when ready

### Step 6: Get Your URL
1. Click **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. You'll get: `https://talimbot-production-xxxx.up.railway.app`
5. **Copy this URL!**

### Step 7: Update Frontend
Edit `assets/js/data.js` line 11:
```javascript
return 'https://talimbot-production-xxxx.up.railway.app/api';
```

### Step 8: Push to GitHub
```bash
git add assets/js/data.js
git commit -m "Configure Railway backend URL"
git push origin main
```

### Step 9: Test!
Visit: `https://talimbot.github.io/talimbot/`

---

## Environment Variables Explained

### Local Development (.env file)
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Railway (Variables tab in dashboard)
- **Variable Name:** OPENROUTER_API_KEY
- **Variable Value:** sk-or-v1-your-key-here

**Important:** NEVER commit your .env file to GitHub! It's already in .gitignore.

---

## Cost

Railway offers:
- **$5 free credit per month** (renews monthly)
- **$0.000463 per GB-hour** of RAM
- Usually enough for small projects like this
- Can upgrade to Developer plan ($5/month) for more resources

---

## Advantages over Render

✅ **No sleep** - stays online 24/7  
✅ **Faster deployments** - usually 1-2 minutes  
✅ **Better free tier** - $5 credit (vs Render's sleep after 15min)  
✅ **Auto-deploy** from GitHub on push  
✅ **Easy environment variables** - simple UI  

---

## Troubleshooting

### Build Fails
- Check Logs tab for error messages
- Verify `requirements.txt` has all dependencies
- Make sure `python-dotenv` is included

### "API key not configured" Error
- Go to Variables tab
- Verify OPENROUTER_API_KEY is set
- Make sure there are no extra spaces
- Redeploy after adding variable

### Can't Access Backend
- Check service is "Active" (not deploying/failed)
- Verify you generated a domain in Settings → Networking
- Try accessing: `https://your-url.up.railway.app/api/students`

---

## Next Steps

After deployment:
1. Test login from multiple devices
2. Test grouping functionality
3. Download JSON backup
4. Share link with students!

---

**Your website is now live and independent!** 🎉

# Hugging Face Spaces Deployment Guide for TalimBot

## Status: Ready to Deploy ✅

All necessary files have been created and committed. Follow the steps below to complete the deployment.

---

## Files Created

1. **Dockerfile** - Docker configuration for HF Spaces (port 7860)
2. **.dockerignore** - Excludes unnecessary files from Docker build
3. **README_HF.md** - Hugging Face Space description with metadata

---

## Step 1: Get Your Hugging Face Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name it: `TalimBot Deploy`
4. Type: **Write** (must have write permissions)
5. Click **"Generate a token"**
6. **COPY THE TOKEN** (you won't see it again!)

---

## Step 2: Push to Hugging Face

The git remote is already configured. Now push your code:

```powershell
git push huggingface main
```

When prompted:
- **Username**: `parinazAkef` (your HF username)
- **Password**: Paste your **access token** (not your actual password!)

---

## Step 3: Configure Environment Secret

1. Go to: https://huggingface.co/spaces/parinazAkef/talimbot
2. Click the **Settings** tab (top of page)
3. Scroll to **"Variables and secrets"**
4. Click **"New secret"**
5. Name: `OPENROUTER_API_KEY`
6. Value: Your OpenRouter API key (starts with `sk-or-v1-`)
7. Click **"Save"**

**✅ You've already done this step!**

---

## Step 4: Wait for Build

After pushing, Hugging Face will:
1. Show "Building" status (3-5 minutes)
2. Pull Docker image, install dependencies
3. Start your FastAPI app on port 7860
4. Show "Running" status when ready

---

## Step 5: Access Your Live App

Once status shows **"Running"** (green), your app will be available at:

**Primary URL:**
```
https://huggingface.co/spaces/parinazAkef/talimbot
```

**Direct URL (no HF frame):**
```
https://parinazakef-talimbot.hf.space
```

---

## Step 6: Test the Application

### Teacher Login
1. Go to your HF Space URL
2. Click on **"معلم"** (Teacher)
3. Password: `teacher123`
4. You should see the teacher dashboard

### Student Login
1. Click on **"دانش آموز"** (Student)
2. Enter national code: `0921111111` (demo account)
3. You should see: **پریناز عاکف** dashboard

### Test Grouping
1. Login as teacher
2. Use **"پر کردن داده‌های تست"** to generate 10 sample students
3. Click **"شروع گروه‌بندی"**
4. Enter course name (e.g., "ریاضی")
5. Wait 30-60 seconds for AI grouping
6. Check results!

---

## Troubleshooting

### If Build Fails

**Error: "Port 7860 not listening"**
- Fixed! Our Dockerfile uses `--port 7860`

**Error: "OPENROUTER_API_KEY not found"**
- Go to Space Settings → Add secret `OPENROUTER_API_KEY`

**Error: "File not found: main.py"**
- Fixed! Dockerfile copies `backend/` folder and sets working directory

### If Push Fails

**Error: "Authentication failed"**
- Make sure you're using an **access token**, not your password
- Generate new token with **Write** permissions

**Error: "Repository not found"**
- Check space URL: https://huggingface.co/spaces/parinazAkef/talimbot
- Make sure space exists and is public

---

## File Structure (Docker Container)

```
/app/
  ├── requirements.txt
  ├── backend/
  │   ├── main.py                    # FastAPI app (runs on port 7860)
  │   ├── grouping_logic.py         # AI grouping algorithm
  │   ├── data/
  │   │   └── students.json.backup  # Initial data template
  │   └── static/
  │       ├── pages/                # HTML pages
  │       ├── assets/               # CSS, JS files
  │       └── Icons/                # Images
  └── resources_references/         # Documentation
```

---

## Environment Variables

The Space automatically provides:
- `OPENROUTER_API_KEY` (from Secrets)
- `PORT=7860` (HF Spaces requirement)

Your FastAPI app reads `OPENROUTER_API_KEY` via:
```python
api_key = os.getenv("OPENROUTER_API_KEY")
```

---

## Next Steps After Deployment

1. **Update GitHub README** - Add HF Space badge and link
2. **Share URL** - Send to users/colleagues
3. **Monitor Usage** - Check Logs tab in HF Space
4. **Add to Profile** - Pin Space to your HF profile

---

## Updating Your App

To push changes:

```powershell
# Make your code changes
git add .
git commit -m "Your update description"

# Push to GitHub (optional)
git push fork main

# Push to Hugging Face (triggers rebuild)
git push huggingface main
```

HF will automatically rebuild and redeploy!

---

## Comparison: Railway vs Hugging Face

| Feature | Railway | Hugging Face |
|---------|---------|--------------|
| Free Tier | 500 hours/month | Unlimited (24/7) |
| Sleep Mode | No | No |
| Cold Start | No | No |
| Iran Access | Sometimes blocked | More accessible |
| Custom Domain | Yes (paid) | Yes (subdomain free) |
| Secrets | Environment variables | Secrets (encrypted) |
| Logs | Real-time | Real-time |
| Auto-deploy | Git push | Git push |

---

## Contact & Support

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Your Space**: https://huggingface.co/spaces/parinazAkef/talimbot
- **OpenRouter Docs**: https://openrouter.ai/docs

---

## Summary

✅ **Completed:**
- Created Dockerfile (port 7860)
- Created .dockerignore
- Created README_HF.md
- Committed files to git
- Added HF remote

🔄 **Your Action Required:**
1. Get HF access token from https://huggingface.co/settings/tokens
2. Run: `git push huggingface main`
3. Enter username + token when prompted
4. Wait for "Running" status
5. Test at: https://parinazakef-talimbot.hf.space

---

Good luck! 🚀

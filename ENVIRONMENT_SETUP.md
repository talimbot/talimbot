# 🔐 Environment Setup Guide

## For Local Development

### Step 1: Create .env File
In the **root folder** of your project (same level as `backend/` folder), create a file named exactly:
```
.env
```

### Step 2: Add Your API Key
Open the `.env` file and add:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

**Get your API key:**
1. Go to https://openrouter.ai
2. Sign up/Login (free!)
3. Go to Keys → Create Key
4. Copy the key (starts with `sk-or-v1-`)
5. Paste it in your `.env` file

### Step 3: Verify .gitignore
Make sure `.gitignore` contains `.env` (it already does!) so you never accidentally commit your secret key.

### Step 4: Run the Server
```powershell
cd backend
python main.py
```

The backend will automatically load your API key from the `.env` file!

---

## For Railway Deployment

### Step 1: Deploy to Railway
Follow the guide in `RAILWAY_DEPLOYMENT.md`

### Step 2: Add Environment Variable
In Railway dashboard:
1. Click your service
2. Go to **"Variables"** tab
3. Add variable:
   - Name: `OPENROUTER_API_KEY`
   - Value: `sk-or-v1-your-actual-key-here`

Railway will inject this environment variable into your application automatically!

---

## Security Best Practices

✅ **DO:**
- Keep `.env` file in your root folder locally
- Add `.env` to `.gitignore` (already done)
- Use Railway Variables for production
- Never share your API key publicly

❌ **DON'T:**
- Commit `.env` to GitHub
- Hardcode API keys in your code
- Share `.env` file with others
- Post your key in Discord/forums

---

## How It Works

### Local Development:
```
.env file (your laptop)
    ↓
python-dotenv loads it
    ↓
os.getenv("OPENROUTER_API_KEY")
    ↓
Backend uses key for AI grouping
```

### Production (Railway):
```
Railway Variables (cloud dashboard)
    ↓
Injected as environment variable
    ↓
os.getenv("OPENROUTER_API_KEY")
    ↓
Backend uses key for AI grouping
```

**Same code, different sources!** ✨

---

## Testing Your Setup

### Test 1: Check .env file exists
```powershell
Test-Path .env
```
Should return: `True`

### Test 2: Start backend and check logs
```powershell
cd backend
python main.py
```
Look for: "INFO: Application startup complete" (no API key errors)

### Test 3: Try grouping
1. Open `http://localhost:8000` in browser
2. Login as teacher (password: teacher123)
3. Try creating groups
4. Should work without asking for API key!

---

## Troubleshooting

### "API key not configured" Error
**Local:**
- Check `.env` file exists in root folder (not backend folder!)
- Verify the key starts with `sk-or-v1-`
- No spaces or quotes around the key

**Railway:**
- Go to Variables tab
- Verify OPENROUTER_API_KEY is set
- Redeploy after adding variable

### .env file not being read
- Make sure it's in the **root** folder, not `backend/` folder
- File name must be exactly `.env` (not `.env.txt`)
- Restart the backend server after creating/editing `.env`

---

## File Structure

```
talimbot/
├── .env                    ← Your API key here (local only)
├── .gitignore              ← Already includes .env
├── backend/
│   ├── main.py             ← Loads from .env automatically
│   ├── grouping_logic.py
│   └── requirements.txt    ← Includes python-dotenv
└── ...
```

---

**Your API key is now secure and ready for both local and production use!** 🔒✨

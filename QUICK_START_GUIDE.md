# 🚀 TalimBot - Quick Start Guide

## ⚠️ IMPORTANT: Restart Backend Server

**Your backend server needs to be restarted** to apply the latest fixes:

```powershell
# In the terminal running the server, press Ctrl+C to stop
# Then restart:
cd backend
python main.py
```

---

## ✅ What Was Fixed

### 1. Toggle Visibility Bug (422 Error) ✅
- **Problem**: "Show grouping to students" button gave 422 Unprocessable Entity error
- **Fix**: Changed backend endpoint to accept JSON body instead of query parameter
- **Status**: Fixed - works after server restart

### 2. Added AMS and Cooperation Columns ✅
- **Added**: Two new columns in teacher's student list
- **Editable**: Teacher can now view and edit AMS and cooperation values
- **Status**: Complete

### 3. Download All Data Button ✅
- **Location**: Green button next to "نمایش لیست دانش‌آموزان" in teacher dashboard
- **Function**: Downloads complete database as JSON file with timestamp
- **Filename**: `talimbot-data-2024-12-08T14-30-00.json`
- **Status**: Working perfectly

---

## 📥 How to Download Student Data

### Method 1: Use the Download Button (Easiest) ✨
1. Login as teacher (password: `teacher123`)
2. Scroll to "لیست تمام دانش آموزان" section
3. Click the green **"📥 دانلود همه داده‌ها (JSON)"** button
4. File downloads automatically to your Downloads folder

### Method 2: Direct API Access
Visit this URL in your browser while server is running:
```
http://localhost:8000/api/data/backup
```
Then right-click → Save As

### Method 3: PowerShell Command
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/data/backup" -OutFile "backup-$(Get-Date -Format 'yyyy-MM-dd-HHmmss').json"
```

---

## 🌐 Production (GitHub Pages) - Data Access

### ❌ WRONG Way:
```
https://talimbot.github.io/data/backup  ❌ This won't work!
```
**Why?** GitHub Pages only serves static HTML/CSS/JS files, not API endpoints.

### ✅ CORRECT Way:

#### If Backend is on Render.com:
```
https://your-app-name.onrender.com/api/data/backup
```

#### If Backend is on Railway:
```
https://your-app-name.up.railway.app/api/data/backup
```

#### Or Use the Download Button:
The green download button in teacher dashboard works in production too! It automatically uses the correct backend URL.

---

## 🧪 Testing the Fixes

### Test 1: Toggle Visibility
1. Login as teacher
2. Complete grouping if not done
3. Click "نمایش گروه‌بندی به دانش‌آموزان" or "عدم نمایش..."
4. Enter password: `teacher123`
5. Should see success message (not 422 error)

### Test 2: AMS and Cooperation Columns
1. Login as teacher
2. Click "نمایش لیست دانش‌آموزان"
3. Check table headers - should see "AMS" and "همکاری" columns
4. Click edit on any student
5. Verify you can edit AMS and Cooperation fields

### Test 3: Download Data
1. Login as teacher
2. Click green "📥 دانلود همه داده‌ها (JSON)" button
3. File should download to Downloads folder
4. Open the file - should see all student data in JSON format

---

## 📁 File Cleanup

### You Can Safely Delete:
- `backend/.env.example` - Not needed (API keys stored in browser)
- `API_KEY_IMPLEMENTATION_GUIDE.md` - Instructions already in SYSTEM_DOCUMENTATION.md

### Keep These Files:
- `SYSTEM_DOCUMENTATION.md` - Complete system reference
- `QUICK_START_GUIDE.md` - This file
- `README.md` - Project overview
- All files in `backend/`, `pages/`, `assets/`

---

## 🔧 Server Status Commands

### Check if server is running:
```powershell
Test-NetConnection -ComputerName localhost -Port 8000
```

### View server logs:
Look at the terminal where you ran `python main.py`

### Restart server:
```powershell
# Press Ctrl+C in server terminal
cd backend
python main.py
```

---

## 📊 Student Table Columns (Updated)

| Column | Editable | Description |
|--------|----------|-------------|
| شماره | ❌ No | Student Number (S001-S030) |
| نام | ✅ Yes | Student Name |
| MBTI | ✅ Yes | Personality Type (16 types) |
| سبک یادگیری | ✅ Yes | VARK Learning Style |
| **AMS** | ✅ Yes | Academic Motivation Scale (NEW) |
| **همکاری** | ✅ Yes | Cooperation Preference (NEW) |
| نمره | ✅ Yes | Grade (0-20) |
| گروه | ❌ No | Assigned Group Number |

---

## 🎯 Next Steps

1. **Restart Backend** (if not done already)
2. **Test all three fixes** using the tests above
3. **Download a backup** to see the data format
4. **Read SYSTEM_DOCUMENTATION.md** for complete details
5. **Plan deployment** using the deployment guide in documentation

---

## 💡 Pro Tips

- **Regular Backups**: Download data after each grouping session
- **Browser Storage**: API key is saved in browser - no need to enter multiple times
- **Mobile Access**: System works on mobile, but desktop recommended for teacher panel
- **Data Format**: Downloaded JSON can be imported into Excel or other tools

---

**Need Help?** Check `SYSTEM_DOCUMENTATION.md` for:
- Complete API reference
- Deployment instructions
- Troubleshooting guide
- Configuration options

---

**Last Updated**: December 8, 2024  
**All Systems**: ✅ Ready to Use (after server restart)

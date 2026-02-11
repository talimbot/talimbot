# 🔧 URGENT FIX: Read-Only File System Issue

## ❌ Problem
```
OSError: [Errno 30] Read-only file system: '/usr/src/app/data/students.json'
```

Your app can't save data because Liara containers are **read-only by default**.

---

## ✅ Solution: Add Persistent Disk

### Method 1: Via Liara Dashboard (EASIER) ⭐

1. **Go to Liara Console**: https://console.liara.ir
2. **Select your app** (`talimbot`)
3. **Click on "دیسک‌ها" (Disks)** in the right sidebar
4. **Click "ایجاد دیسک" (Create Disk)**
5. **Fill in**:
   - **Name**: `data-disk`
   - **Mount Path**: `/usr/src/app/data`
   - **Size**: `1GB` (more than enough for JSON files)
6. **Click "ایجاد" (Create)**
7. **Restart your app**: Go to تنظیمات → راه‌اندازی مجدد

### Method 2: Via CLI

```powershell
cd c:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend
liara disk:create --app talimbot --name data-disk --size 1
liara deploy --app talimbot --platform python
```

---

## 🚀 Git Auto-Deployment Setup

### Step 1: Get Liara API Token

1. Go to https://console.liara.ir/api
2. Click **"ایجاد توکن API" (Create API Token)**
3. Give it a name: `github-actions`
4. **Copy the token** (you'll only see it once!)

### Step 2: Add Token to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `LIARA_TOKEN`
5. Value: Paste the token you copied
6. Click **"Add secret"**

### Step 3: Deploy!

Now, every time you push to `main` or `master` branch:
```powershell
git add .
git commit -m "your changes"
git push
```

GitHub Actions will automatically deploy to Liara! 🎉

---

## ⚡ Quick Fix Right Now

Run these commands to fix immediately:

```powershell
cd c:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend

# Commit the new configuration
git add liara.json .github/workflows/liara-deploy.yml
git commit -m "Add persistent disk and auto-deployment"

# Deploy with new configuration
liara deploy --app talimbot --platform python
```

Then go to Liara dashboard and create the disk as shown in Method 1 above.

---

## 🧪 Test After Fix

After creating the disk and redeploying:

1. Go to: `https://talimbot.liara.run/api/students`
2. Try updating a student (via your frontend)
3. Refresh - changes should persist! ✅

---

## 📊 Check Deployment Status

### Via GitHub:
- Go to your repo → **Actions** tab
- See deployment status in real-time

### Via Liara:
```powershell
liara logs --app talimbot --follow
```

---

## 🎯 Summary

**What we fixed:**
1. ✅ Added persistent disk configuration in `liara.json`
2. ✅ Created GitHub Actions workflow for auto-deployment
3. ✅ Set up automatic deployments on every push

**What you need to do:**
1. ⚠️ Create the disk in Liara (Method 1 is easiest)
2. ⚠️ Get Liara API token and add to GitHub secrets
3. ⚠️ Push to GitHub to trigger auto-deployment

---

**Need help?** Just ask! 😊

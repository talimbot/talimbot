# 🚀 راهنمای استقرار پروژه روی لیارا (Liara Deployment Guide)

## ✅ آماده‌سازی کامل شده (Already Done)

تمام فایل‌های زیر توسط Copilot ایجاد شده‌اند و commit شده‌اند:
- ✅ `liara.json` - تنظیمات لیارا
- ✅ `Procfile` - دستور اجرای سرور
- ✅ `.gitignore` - فایل‌های قابل نادیده گرفتن
- ✅ `.env.example` - نمونه متغیرهای محیطی
- ✅ `requirements.txt` - وابستگی‌های Python

---

## 📋 مراحل استقرار (Deployment Steps)

### مرحله 1️⃣: ثبت‌نام در لیارا

1. به سایت https://liara.ir بروید
2. روی **ثبت‌نام** کلیک کنید
3. اطلاعات خود را وارد کنید (ایمیل + رمز عبور)
4. حساب خود را تأیید کنید

---

### مرحله 2️⃣: نصب Node.js (برای CLI لیارا)

لیارا از طریق CLI (Command Line Interface) کار می‌کند که به Node.js نیاز دارد.

**نصب Node.js در ویندوز:**
1. به https://nodejs.org بروید
2. نسخه **LTS** را دانلود کنید (کلید سبز)
3. فایل نصبی (.msi) را اجرا کنید
4. تمام گزینه‌های پیش‌فرض را بپذیرید و نصب کنید
5. پنجره PowerShell را **ببندید و دوباره باز کنید**

تست کنید:
```powershell
node --version
npm --version
```

اگر هر دو شماره نسخه را نشان دادند، موفق بوده‌اید! ✅

---

### مرحله 3️⃣: نصب Liara CLI

در PowerShell اجرا کنید:
```powershell
npm install -g @liara/cli
```

تست کنید:
```powershell
liara --version
```

---

### مرحله 4️⃣: ورود به حساب لیارا

```powershell
liara login
```

این دستور یک لینک می‌دهد - روی آن کلیک کنید و در مرورگر وارد شوید.

---

### مرحله 5️⃣: ساخت برنامه (App) در لیارا

**دو روش دارید:**

#### 🅰️ روش 1: از طریق وب‌سایت لیارا (راحت‌تر)
1. وارد پنل لیارا شوید (https://console.liara.ir)
2. روی **ایجاد برنامه** کلیک کنید
3. نام برنامه: `talimbot` (یا هر نام دلخواه)
4. پلتفرم: **Python** را انتخاب کنید
5. پلن: **رایگان** یا **ارزان‌ترین** را انتخاب کنید (۵۰-۱۰۰ هزار تومان/ماه)
6. روی **ایجاد برنامه** کلیک کنید

#### 🅱️ روش 2: از طریق CLI
```powershell
cd c:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend
liara create --name talimbot --platform python
```

---

### مرحله 6️⃣: ایجاد دیسک ذخیره‌سازی دائمی (CRITICAL!) ⚠️

**این مرحله الزامی است - بدون آن برنامه کار نمی‌کند!**

**از طریق وب (توصیه می‌شود):**
1. در پنل لیارا به برنامه `talimbot` بروید
2. از منوی سمت راست **دیسک‌ها** را انتخاب کنید
3. روی **ایجاد دیسک** کلیک کنید
4. **نام دیسک**: `data-disk`
5. **مسیر mount**: `/usr/src/app/data`
6. **فضا**: `1GB` (کافی است)
7. روی **ایجاد** کلیک کنید

**یا از طریق CLI:**
```powershell
liara disk:create --app talimbot --name data-disk --size 1
```

---

### مرحله 7️⃣: تنظیم متغیر محیطی (API Key)

**از طریق وب (ساده‌تر):**
1. در پنل لیارا رد شوید به برنامه `talimbot`
2. از منوی سمت راست **تنظیمات** → **متغیرهای محیطی** را انتخاب کنید
3. روی **افزودن متغیر** کلیک کنید
4. کلید: `OPENROUTER_API_KEY`
5. مقدار: کلید API خود را بگذارید (مثلاً: `sk-or-v1-...`)
6. **ذخیره** کنید

**یا از طریق CLI:**
```powershell
liara env:set OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here --app=talimbot
```

⚠️ **مهم:** کلید API خود را از https://openrouter.ai/keys بگیرید

---

### مرحله 8️⃣: استقرار (Deploy)!

```powershell
cd c:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend
liara deploy --app talimbot --platform python
```

این دستور:
- تمام فایل‌ها را آپلود می‌کند
- وابستگی‌ها را از `requirements.txt` نصب می‌کند
- سرور FastAPI را راه‌اندازی می‌کند

منتظر بمانید تا پیام **برنامه شما با موفقیت مستقر شد** را ببینید! 🎉

---

### مرحله 9️⃣: تنظیم استقرار خودکار از GitHub 🤖

**این قابلیت اجازه می‌دهد هر بار که کد را push می‌کنید، خودکار روی لیارا deploy شود!**

#### گام 1: دریافت API Token از لیارا
1. به https://console.liara.ir/api بروید
2. روی **ایجاد توکن API** کلیک کنید
3. نام: `github-actions`
4. توکن را **کپی کنید** (فقط یک بار نمایش داده می‌شود!)

#### گام 2: افزودن Token به GitHub
1. به مخزن GitHub خود بروید
2. **Settings** → **Secrets and variables** → **Actions**
3. روی **New repository secret** کلیک کنید
4. Name: `LIARA_TOKEN`
5. Value: توکنی که کپی کردید را paste کنید
6. **Add secret** را بزنید

#### گام 3: Push کردن workflow
```powershell
cd c:\Users\Parinaz\Desktop\Talim_Project\talimbot\backend
git add .
git commit -m "Add Liara auto-deployment"
git push
```

**🎉 تمام! حالا هر بار که push می‌کنید، خودکار deploy می‌شود!**

برای مشاهده وضعیت deployment: به repo خود در GitHub → تب **Actions** بروید

---

### مرحله 🔟: مشاهده سایت

لیارا یک آدرس به شما می‌دهد:
```
https://talimbot.liara.run
```

سایت شما آماده است! 🌐

---

## 🔍 تست و بررسی

### تست API:
```
https://talimbot.liara.run/api/students
```

### تست صفحه اصلی:
```
https://talimbot.liara.run/
```

---

## 📦 مدیریت داده‌ها (Data Persistence)

فایل `students.json` شما در پوشه `/data` ذخیره می‌شود و لیارا به طور خودکار آن را نگه می‌دارد.

**⚠️ توصیه مهم:** هر از چند گاهی از داده‌ها backup بگیرید:
1. به API endpoint زیر بروید:
   ```
   https://talimbot.liara.run/api/data/backup
   ```
2. فایل JSON را ذخیره کنید

---

## 🔄 به‌روزرسانی پروژه (Updates)

هر بار که کد را تغییر دادید:

```powershell
# 1. Commit کردن تغییرات
git add .
git commit -m "توضیحات تغییرات"

# 2. استقرار مجدد
liara deploy --app talimbot --platform python
```

---

## 💰 هزینه‌ها (Pricing)

برای پروژه شما:
- **CPU:** خیلی کم (~100 هزار تومان/ماه)
- **حافظه:** 512MB کافی است
- **ترافیک:** برای 30 نفر رایگان است
- **Storage:** JSON فایل کوچک - هزینه‌ای ندارد

**تخمین:** حدود **50-100 هزار تومان در ماه** 💵

---

## 🆘 عیب‌یابی (Troubleshooting)

### خطا: "Module not found"
```powershell
# بررسی requirements.txt
liara deploy --app talimbot --platform python --no-cache
```

### دیدن لاگ‌ها:
```powershell
liara logs --app talimbot
```

یا از پنل وب: **برنامه** → **لاگ‌ها**

### خطا: API Key کار نمی‌کند
1. بروید به **تنظیمات** → **متغیرهای محیطی**
2. بررسی کنید `OPENROUTER_API_KEY` درست تنظیم شده
3. فضای خالی اضافی نداشته باشد
4. برنامه را restart کنید: **تنظیمات** → **راه‌اندازی مجدد**

---

## 📞 پشتیبانی لیارا

- وب‌سایت: https://liara.ir
- مستندات: https://docs.liara.ir
- تلگرام: @liara_ir
- ایمیل: support@liara.ir

---

## ✨ مزایای لیارا برای پروژه شما

✅ **سرویس ایرانی** - بدون مشکل تحریم  
✅ **استقرار آسان** - فقط یک دستور  
✅ **هزینه پایین** - پرداخت بر اساس مصرف  
✅ **JSON Persistence** - داده‌ها حفظ می‌شوند  
✅ **SSL رایگان** - HTTPS خودکار  
✅ **پشتیبانی فارسی** - راحت‌تر برای شما  

---

## 🎓 دستورات مهم CLI

```powershell
# ورود به لیارا
liara login

# لیست برنامه‌ها
liara app:list

# دیدن وضعیت برنامه
liara app:info --app talimbot

# دیدن لاگ‌ها
liara logs --app talimbot --follow

# راه‌اندازی مجدد
liara app:restart --app talimbot

# دیدن متغیرهای محیطی
liara env:list --app talimbot

# حذف برنامه (احتیاط!)
liara app:remove --app talimbot
```

---

**موفق باشید! 🚀**

اگر مشکلی داشتید، از من بپرسید - من اینجا هستم تا کمک کنم! 😊

# Deployment Guide

## Pushing Code Changes to GitHub

When you've made changes to the code and want to push them to GitHub:

```powershell
# Check what files have changed
git status

# Add all changes
git add .

# Commit with a message describing your changes
git commit -m "Your change description"

# Push to your GitHub repository
git push fork main
```

**Note:** If the push is rejected, you may need to force push (be careful, this overwrites remote):
```powershell
git push fork main --force
```

## Updating Students.json Data on Liara

When you've made changes to `backend/data/students.json` and want them reflected on your live website:

### Step 1: Delete old data from persistent disk

```powershell
# Navigate to backend folder
cd backend

# Open Liara shell
liara shell --app talimbot

# Inside the Liara shell, delete the old file
rm /usr/src/app/data/students.json

# Exit the shell
exit
```

### Step 2: Restart the app to load new data

```powershell
# Restart the app (this will initialize with your latest code)
liara restart --app talimbot

# Wait 10 seconds for app to restart
Start-Sleep -Seconds 10
```

### Step 3: Verify the changes

Visit your website: https://talimbot.liara.run/api/students

## Important Notes

**Code vs Data:**
- Code changes are automatically deployed when you push to GitHub (via GitHub Actions)
- Data changes require manual update on the persistent disk (follow steps above)
- The persistent disk preserves data across deployments to prevent data loss

**GitHub Remotes:**
- `fork` - Your personal repository (Parinaz11/talimbot)
- `origin` - Original repository (talimbot/talimbot)
- Always push to `fork` for your changes

## Quick Reference

**Push code:**
```powershell
git add .; git commit -m "Description"; git push fork main
```

**Update students.json:**
```powershell
cd backend; liara shell --app talimbot
# Then in shell: rm /usr/src/app/data/students.json; exit
liara restart --app talimbot
```

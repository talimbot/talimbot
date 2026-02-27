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
rm -f /usr/src/app/data/students.json

# Exit the shell
exit
```

### Step 2: Deploy to reinitialize with new data

```powershell
# Deploy the app (this will create new students.json from your code)
liara deploy --app talimbot --platform python --no-app-logs
```

### Step 3: Verify the changes

Visit your website: https://talimbot.liara.run/api/students

## Important Notes

**Code vs Data:**
- Code changes are automatically deployed when you push to GitHub (via Liara dashboard connection)
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
# Then in shell: rm -f /usr/src/app/data/students.json; exit
liara deploy --app talimbot --platform python --no-app-logs
```

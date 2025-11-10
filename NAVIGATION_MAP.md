# 🗺️ TalimBot Navigation Map

## 🚀 Quick Start

### For Development/Testing:
1. Open `login.html` in your browser
2. Select role:
   - **Student**: Enter `S001` to `S030`
   - **Teacher**: Password `teacher123`

---

## 📱 Page Navigation Flow

### 🎓 Student Journey

```
login.html
    ↓
    [Enter S001-S030]
    ↓
student-dashboard-new.html ←─── [Auto-redirect from student-dashboard.html]
    │
    ├─→ [Complete Tests]
    │   ├─ MBTI Test (External Link)
    │   ├─ VARK Test (External Link)
    │   ├─ AMS Test (External Link)
    │   └─ Cooperative Test (Coming Soon)
    │
    ├─→ [Select Preferences] (Max 4 classmates)
    ├─→ [Save All Results]
    │
    └─→ Bottom Navigation:
        ├─ Home (Current)
        ├─ Chat → teacher-chat.html
        ├─ Group → group-view.html
        └─ Logout → login.html
```

---

### 👨‍🏫 Teacher Journey

```
login.html
    ↓
    [Enter password: teacher123]
    ↓
teacher-dashboard-new.html ←─── [Auto-redirect from teacher-dashboard.html]
    │
    ├─→ View Stats:
    │   ├─ Total Students: 30
    │   ├─ Completed Profiles: X
    │   └─ Grouped Students: Y
    │
    ├─→ Set Course Name
    │   └─ [Save Course]
    │
    ├─→ Grouping Operations:
    │   ├─ [Start Grouping] → Creates groups
    │   ├─ [View Results] → Shows group assignments
    │   └─ [Reset Grouping] → Clears all groups
    │
    ├─→ Manage Students:
    │   ├─ [Show/Hide Table]
    │   ├─ View all student data
    │   └─ [Edit Student] (Individual)
    │
    └─→ Bottom Navigation:
        ├─ Home (Current)
        ├─ Chat → teacher-chat.html
        ├─ Data → student-data.html
        └─ Logout → login.html
```

---

## 🔗 File Relationships

### Core Files (Redesigned):
```
login.html .......................... Main entry point (REDESIGNED ✅)
student-dashboard-new.html .......... Student main page (NEW ✅)
teacher-dashboard-new.html .......... Teacher main page (NEW ✅)
```

### Redirect Files:
```
student-dashboard.html .............. → Redirects to student-dashboard-new.html
teacher-dashboard.html .............. → Redirects to teacher-dashboard-new.html
```

### Data Files (Unchanged):
```
data.js ............................. Student data management (LocalStorage)
grouping.js ......................... Grouping algorithm logic
```

### Legacy Files (To be redesigned):
```
teacher.html ........................ Old teacher menu
student.html ........................ Old student menu
teacher-chat.html ................... Chat interface (TODO)
group-view.html ..................... Group display (TODO)
student-data.html ................... Data entry (TODO)
classroom.html ...................... Main classroom (TODO)
```

---

## 🎯 Bottom Navigation Links

### Student Dashboard Bottom Nav:
| Icon | Label | Link | Description |
|------|-------|------|-------------|
| 🏠 | خانه | `#` | Current page (active) |
| 💬 | چت | `teacher-chat.html` | Chat with teacher |
| 👥 | گروه | `group-view.html` | View assigned group |
| 🚪 | خروج | `login.html` | Logout |

### Teacher Dashboard Bottom Nav:
| Icon | Label | Link | Description |
|------|-------|------|-------------|
| 🏠 | خانه | `#` | Current page (active) |
| 💬 | چت | `teacher-chat.html` | Chat interface |
| 📄 | داده‌ها | `student-data.html` | Student data entry |
| 🚪 | خروج | `login.html` | Logout |

---

## 🔐 Authentication System

### Session Storage Keys:
```javascript
// For Students:
sessionStorage.setItem('currentStudent', 'S001');  // Student ID

// For Teachers:
sessionStorage.setItem('isTeacher', 'true');       // Teacher flag
```

### Auth Check Example:
```javascript
// In student pages:
const studentNumber = sessionStorage.getItem('currentStudent');
if (!studentNumber) {
    window.location.href = 'login.html';
}

// In teacher pages:
const isTeacher = sessionStorage.getItem('isTeacher');
if (!isTeacher) {
    window.location.href = 'login.html';
}
```

---

## 📊 Data Flow

### Student Data Update:
```
Student Dashboard
    ↓
    [Fill Test Results]
    ↓
    [Click Save Button]
    ↓
data.js → updateStudent(studentNumber, {
    mbti: "INTJ",
    learningStyle: "Visual",
    ams: 85,
    cooperative: 8,
    preferredStudents: ["S002", "S005", "S012"]
})
    ↓
localStorage.setItem('studentGroupingData', JSON.stringify(data))
```

### Grouping Process:
```
Teacher Dashboard
    ↓
    [Set Course Name]
    ↓
    [Click Start Grouping]
    ↓
grouping.js → performGrouping(courseName)
    ↓
    [Algorithm runs]
    ↓
    [Groups created]
    ↓
applyGrouping(groupingResult, courseName)
    ↓
data.js → Updates each student's group field
    ↓
localStorage updated
    ↓
    [Display Group Results]
```

---

## 🌐 External Links

### Test Links (In Student Dashboard):
1. **MBTI Test**:
   - English: https://www.16personalities.com/
   - Persian: https://www.16personalities.com/fa

2. **VARK Test**:
   - Official: https://vark-learn.com/the-vark-questionnaire/
   - Persian: http://maktabestan.ir/

3. **AMS Test**:
   - English: https://idrlabs.com/academic-motivation/test.php
   - Persian: (To be built)

4. **Cooperative Learning**:
   - Status: To be built (offline questionnaire)

---

## 📱 Page-Specific Features

### Login Page Features:
- ✅ Role selection (Student/Teacher)
- ✅ Student ID validation (S001-S030)
- ✅ Teacher password validation
- ✅ Password visibility toggle
- ✅ Error messages
- ✅ Split layout (desktop)

### Student Dashboard Features:
- ✅ Profile display (name, ID, grade)
- ✅ Stats card (tests completed, grade, group)
- ✅ 4 test cards with external links
- ✅ Inline result inputs
- ✅ Preference selector (max 4)
- ✅ Save button with toast notification
- ✅ Bottom navigation
- ✅ Gradient background

### Teacher Dashboard Features:
- ✅ Stats grid (3 cards)
- ✅ Course name input/save
- ✅ Grouping status display
- ✅ Start grouping with progress animation
- ✅ Group results display (2-column grid)
- ✅ Student table (collapsible)
- ✅ Edit student data
- ✅ Reset grouping
- ✅ Bottom navigation

---

## 🎨 Color Coding by Role

### Student Pages:
- **Primary Color**: Purple (`#8B5CF6`)
- **Gradient**: Purple → Pink
- **Accent**: Purple-600
- **Active Nav**: Purple-500

### Teacher Pages:
- **Primary Color**: Blue (`#2563EB`)
- **Gradient**: Blue-600 → Blue-700
- **Accent**: Blue-600
- **Active Nav**: Blue-500

---

## 🔄 Redirect Logic

### Old → New Dashboard Redirects:

**student-dashboard.html**:
```html
<script>
    window.location.href = 'student-dashboard-new.html';
</script>
```

**teacher-dashboard.html**:
```html
<script>
    window.location.href = 'teacher-dashboard-new.html';
</script>
```

**Why?**
- Preserves existing links
- Seamless transition
- Can be removed later

---

## 🧪 Testing Scenarios

### Student Flow Test:
1. ✅ Open `login.html`
2. ✅ Click Student card
3. ✅ Enter `S001`
4. ✅ Click Login
5. ✅ See student dashboard with profile
6. ✅ Fill test results
7. ✅ Select 4 preferences
8. ✅ Click Save
9. ✅ See success toast
10. ✅ Navigate to Group view

### Teacher Flow Test:
1. ✅ Open `login.html`
2. ✅ Click Teacher card
3. ✅ Enter `teacher123`
4. ✅ Click Login
5. ✅ See teacher dashboard with stats
6. ✅ Enter course name "Mathematics"
7. ✅ Click Start Grouping
8. ✅ See progress animation
9. ✅ See group results
10. ✅ Toggle student list
11. ✅ Click Reset Grouping

---

## 🐛 Common Issues & Solutions

### Issue: Login redirects to itself
**Solution**: Clear browser cache and sessionStorage
```javascript
sessionStorage.clear();
```

### Issue: Stats show 0/0/0
**Solution**: Students need to complete their profiles first

### Issue: Grouping button disabled
**Solution**: 
1. Set course name first
2. Ensure at least 1 student has completed profile

### Issue: Bottom nav icons not showing
**Solution**: SVG icons are inline, check browser console for errors

### Issue: Tailwind classes not working
**Solution**: Ensure CDN is loaded:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

---

## 📞 Developer Quick Reference

### Add New Student Dashboard Tab:
1. Add link to bottom nav
2. Create new HTML file
3. Include auth check
4. Load student data from `data.js`

### Add New Teacher Dashboard Tab:
1. Add link to bottom nav
2. Create new HTML file
3. Include auth check
4. Load data from `data.js`

### Modify Student Data Structure:
1. Update `data.js` → `initialStudents` array
2. Update `updateStudent()` function
3. Update dashboard display logic

### Change Colors Globally:
Replace color classes in all files:
- `purple-X` → `blue-X` (for student pages)
- `blue-X` → `green-X` (for teacher pages)

---

**Quick Navigation Cheat Sheet**:
```
🎓 Student: login.html → S001 → student-dashboard-new.html
👨‍🏫 Teacher: login.html → teacher123 → teacher-dashboard-new.html
```

**Data Location**: Browser LocalStorage → Key: `studentGroupingData`

**Session Keys**: 
- `currentStudent` (Student ID)
- `isTeacher` (Boolean flag)

---

**Last Updated**: November 10, 2025  
**Version**: 2.0.5  
**Status**: ✅ Production Ready

# Student Grouping System

A modern web application for grouping students based on MBTI personality types, learning styles, grades, and peer preferences.

## Features

### For Students
- 🔐 Login with student number
- 🧠 Access to MBTI and Learning Style test links
- ✍️ Enter test results and preferences
- 👥 Select up to 4 preferred groupmates
- 📊 View assigned group members
- 💯 Display of current grade

### For Teachers
- 🔐 Secure login with password
- 📚 Set course name
- 📊 View student statistics
- 🎯 Automated grouping system
- 👀 View all groups and assignments
- 🔄 Reset and regroup students

## How to Use

### Starting the Application
1. Open `login.html` in your web browser
2. Select your role (Student or Teacher)

### For Students
1. **Login**: Enter your student number (S001-S030)
2. **Take Tests**: Click the links to complete MBTI and Learning Style tests
3. **Enter Results**: Input your MBTI type and learning style
4. **Select Preferences**: Choose up to 4 students you'd like to be grouped with (optional)
5. **Save**: Click "Save Information"
6. **View Group**: Once the teacher completes grouping, click "See My Group"

### For Teachers
1. **Login**: Use password: `teacher123`
2. **Enter Course Name**: Input the course name (e.g., "Mathematics")
3. **Review Statistics**: Check how many students have completed their profiles
4. **Start Grouping**: Click "Start Grouping Process" to create balanced groups
5. **View Results**: Review the generated groups and student assignments

## Student Data

The system includes 30 pre-configured students (S001-S030):
- Each has a name, student number, and grade
- Students can add their MBTI type and learning style
- Students can select preferred groupmates

## Grouping Algorithm

The system uses an intelligent algorithm that considers:
- ✅ MBTI compatibility (complementary personality types)
- ✅ Learning style diversity (mix of different learning preferences)
- ✅ Grade balance (mix of performance levels)
- ✅ Student preferences (attempts to honor preferred groupmates)

### ChatGPT API Integration (Optional)

The grouping logic includes commented code for ChatGPT API integration. To enable:

1. Open `grouping.js`
2. Add your OpenAI API key: Replace `YOUR_CHATGPT_API_KEY_HERE`
3. Uncomment the ChatGPT API section (lines 14-21)
4. Comment out the random grouping fallback (line 24)

**Current Behavior**: Without API configuration, the system uses random grouping.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Storage**: Browser localStorage
- **Styling**: Modern CSS with gradients and animations
- **Optional**: OpenAI ChatGPT API for intelligent grouping

## File Structure

```
├── login.html                  # Login page with role selection
├── student-dashboard.html      # Student profile and information entry
├── group-view.html            # View assigned group members
├── teacher-dashboard.html     # Teacher control panel
├── data.js                    # Data management and localStorage
├── grouping.js                # Grouping algorithm logic
├── styles.css                 # Modern UI styling
└── README.md                  # This file
```

## Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Requires localStorage support

## Demo Credentials

### Teacher Login
- Password: `teacher123`

### Student Login
- Any student number from S001 to S030
- Example: `S001` (Emma Johnson), `S015` (Amelia Taylor)

## Features Overview

### Modern UI
- 🎨 Beautiful gradient backgrounds
- 🎯 Smooth animations and transitions
- 📱 Responsive design for all devices
- 🎭 Intuitive role-based interfaces

### Data Persistence
- � All data stored in browser localStorage
- 🔄 Data persists across sessions
- 🗑️ Reset option available for teachers

### Smart Grouping
- 🤖 AI-ready with ChatGPT integration support
- 🎲 Random fallback when API unavailable
- ⚖️ Balanced group creation (5-6 students per group)
- 🤝 Considers student preferences

## Development Notes

- No backend server required
- Pure client-side application
- Easy to deploy (just upload files)
- Can be enhanced with real backend for production use

## Future Enhancements

- 🔐 Enhanced authentication system
- 💾 Backend database integration
- 📧 Email notifications for students
- 📊 Advanced analytics and reporting
- 📱 Mobile app version
- 🌐 Multi-language support

---

**Version**: 1.0  
**Last Updated**: November 2025

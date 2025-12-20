// Student Grouping System - Data Management
// This file handles all data operations using Backend API

// Backend API Configuration
// Auto-detects if running on Railway deployment or localhost
function getApiBaseUrl() {
    // When deployed to Railway, it will use the same domain
    // Railway serves both frontend and backend from the same URL
    // So we use relative paths for API calls
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        // PRODUCTION: Running on Railway - use relative paths
        return '/api';
    }
    
    // DEVELOPMENT: Running locally
    return 'http://localhost:8000/api';
}

const API_BASE_URL = getApiBaseUrl();

// Utility function for API calls
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Get all data (for backward compatibility)
async function getData() {
    const students = await getAllStudents();
    const status = await getGroupingStats();
    return {
        students: students,
        courseName: status.courseName,
        groupingComplete: status.groupingComplete,
        resultsVisible: status.resultsVisible,
        teacherPassword: 'teacher123'
    };
}

// Get student by student number
async function getStudent(studentNumber) {
    try {
        return await apiCall(`/student/${studentNumber}`);
    } catch (error) {
        return null;
    }
}

// Update student information
async function updateStudent(studentNumber, updates) {
    try {
        const result = await apiCall(`/student/${studentNumber}`, {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
        return result.success;
    } catch (error) {
        return false;
    }
}

// Get all students
async function getAllStudents() {
    const result = await apiCall('/students');
    return result.students;
}

// Check if a student number exists in the system
async function studentExists(studentNumber) {
    const student = await getStudent(studentNumber);
    return student !== null;
}

// Get students with complete information (REQUIRED fields only: MBTI and Learning Style)
async function getStudentsWithCompleteInfo() {
    const students = await getAllStudents();
    return students.filter(s => s.mbti && s.learningStyle);
}

// Check if a student has complete profile (all fields filled)
async function hasCompleteProfile(studentNumber) {
    const student = await getStudent(studentNumber);
    if (!student) return false;
    
    return !!(student.mbti && student.learningStyle && 
              student.ams !== null && student.cooperative !== null);
}

// Get completion percentage for a student
async function getProfileCompletion(studentNumber) {
    const student = await getStudent(studentNumber);
    if (!student) return 0;
    
    let completed = 0;
    const total = 4;
    
    if (student.mbti) completed++;
    if (student.learningStyle) completed++;
    if (student.ams !== null) completed++;
    if (student.cooperative !== null) completed++;
    
    return Math.round((completed / total) * 100);
}

// Get grouping statistics
async function getGroupingStats() {
    return await apiCall('/grouping/status');
}

// Check if grouping is complete
async function isGroupingComplete() {
    const stats = await getGroupingStats();
    return stats.groupingComplete;
}

// Get course name
async function getCourseName() {
    const stats = await getGroupingStats();
    return stats.courseName;
}

// Check teacher password
async function checkTeacherPassword(password) {
    try {
        const result = await apiCall('/auth/teacher', {
            method: 'POST',
            body: JSON.stringify({ password })
        });
        return result.valid;
    } catch (error) {
        return false;
    }
}

// Get student's group (only if results are visible)
async function getStudentGroup(studentNumber) {
    try {
        return await apiCall(`/student/${studentNumber}/group`);
    } catch (error) {
        if (error.message.includes('not yet visible')) {
            return { error: 'results_not_visible', message: 'نتایج هنوز توسط معلم نمایش داده نشده است.' };
        }
        if (error.message.includes('not assigned')) {
            return { error: 'not_assigned', message: 'شما هنوز به گروهی اختصاص داده نشده‌اید.' };
        }
        throw error;
    }
}

// Reset grouping only (keep student data)
async function resetGrouping(password) {
    return await apiCall('/grouping/reset', {
        method: 'POST',
        body: JSON.stringify({ password })
    });
}

// Reset ALL data (student profiles + grouping)
async function resetAllData(password) {
    return await apiCall('/data/reset-all', {
        method: 'POST',
        body: JSON.stringify({ password })
    });
}

// Toggle results visibility
async function toggleResultsVisibility(password) {
    return await apiCall('/grouping/toggle-visibility', {
        method: 'POST',
        body: JSON.stringify({ password })
    });
}

// Legacy functions for backward compatibility (these are handled by backend now)
function saveData(data) {
    console.warn('saveData is deprecated - data is automatically saved to backend');
}

function initializeData() {
    console.log('Data is managed by backend');
    return true;
}

function addNewStudent(studentNumber, name, grade = 15) {
    console.warn('addNewStudent should be done through admin panel');
    return { success: false, message: 'Use backend API for adding students' };
}

function saveStudents(students) {
    console.warn('saveStudents is deprecated - use backend API');
}

function deleteStudent(studentNumber) {
    console.warn('deleteStudent should be done through admin panel');
    return false;
}

function setGroupingComplete(status) {
    console.warn('setGroupingComplete is handled by backend');
}

function setCourseName(name) {
    console.warn('setCourseName is handled by backend');
}

function resetData() {
    console.warn('resetData should be done through teacher dashboard');
}

// Export functions for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getData,
        getStudent,
        updateStudent,
        getAllStudents,
        studentExists,
        getStudentsWithCompleteInfo,
        hasCompleteProfile,
        getProfileCompletion,
        isGroupingComplete,
        getCourseName,
        checkTeacherPassword,
        getGroupingStats,
        getStudentGroup
    };
}

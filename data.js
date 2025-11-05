// Student Grouping System - Data Management
// This file handles all data operations using localStorage

const STORAGE_KEY = 'studentGroupingData';

// Initial 30 students data
const initialStudents = [
    { studentNumber: 'S001', name: 'Emma Johnson', mbti: null, learningStyle: null, grade: 85, preferredStudents: [], group: null },
    { studentNumber: 'S002', name: 'Liam Smith', mbti: null, learningStyle: null, grade: 78, preferredStudents: [], group: null },
    { studentNumber: 'S003', name: 'Olivia Williams', mbti: null, learningStyle: null, grade: 92, preferredStudents: [], group: null },
    { studentNumber: 'S004', name: 'Noah Brown', mbti: null, learningStyle: null, grade: 88, preferredStudents: [], group: null },
    { studentNumber: 'S005', name: 'Ava Jones', mbti: null, learningStyle: null, grade: 95, preferredStudents: [], group: null },
    { studentNumber: 'S006', name: 'Ethan Garcia', mbti: null, learningStyle: null, grade: 82, preferredStudents: [], group: null },
    { studentNumber: 'S007', name: 'Sophia Martinez', mbti: null, learningStyle: null, grade: 90, preferredStudents: [], group: null },
    { studentNumber: 'S008', name: 'Mason Rodriguez', mbti: null, learningStyle: null, grade: 76, preferredStudents: [], group: null },
    { studentNumber: 'S009', name: 'Isabella Hernandez', mbti: null, learningStyle: null, grade: 89, preferredStudents: [], group: null },
    { studentNumber: 'S010', name: 'James Lopez', mbti: null, learningStyle: null, grade: 84, preferredStudents: [], group: null },
    { studentNumber: 'S011', name: 'Mia Gonzalez', mbti: null, learningStyle: null, grade: 91, preferredStudents: [], group: null },
    { studentNumber: 'S012', name: 'Benjamin Wilson', mbti: null, learningStyle: null, grade: 79, preferredStudents: [], group: null },
    { studentNumber: 'S013', name: 'Charlotte Anderson', mbti: null, learningStyle: null, grade: 87, preferredStudents: [], group: null },
    { studentNumber: 'S014', name: 'Lucas Thomas', mbti: null, learningStyle: null, grade: 93, preferredStudents: [], group: null },
    { studentNumber: 'S015', name: 'Amelia Taylor', mbti: null, learningStyle: null, grade: 86, preferredStudents: [], group: null },
    { studentNumber: 'S016', name: 'Henry Moore', mbti: null, learningStyle: null, grade: 80, preferredStudents: [], group: null },
    { studentNumber: 'S017', name: 'Evelyn Jackson', mbti: null, learningStyle: null, grade: 94, preferredStudents: [], group: null },
    { studentNumber: 'S018', name: 'Alexander Martin', mbti: null, learningStyle: null, grade: 77, preferredStudents: [], group: null },
    { studentNumber: 'S019', name: 'Harper Lee', mbti: null, learningStyle: null, grade: 88, preferredStudents: [], group: null },
    { studentNumber: 'S020', name: 'Michael White', mbti: null, learningStyle: null, grade: 83, preferredStudents: [], group: null },
    { studentNumber: 'S021', name: 'Abigail Harris', mbti: null, learningStyle: null, grade: 90, preferredStudents: [], group: null },
    { studentNumber: 'S022', name: 'Daniel Clark', mbti: null, learningStyle: null, grade: 81, preferredStudents: [], group: null },
    { studentNumber: 'S023', name: 'Emily Lewis', mbti: null, learningStyle: null, grade: 89, preferredStudents: [], group: null },
    { studentNumber: 'S024', name: 'Matthew Robinson', mbti: null, learningStyle: null, grade: 75, preferredStudents: [], group: null },
    { studentNumber: 'S025', name: 'Elizabeth Walker', mbti: null, learningStyle: null, grade: 92, preferredStudents: [], group: null },
    { studentNumber: 'S026', name: 'David Young', mbti: null, learningStyle: null, grade: 87, preferredStudents: [], group: null },
    { studentNumber: 'S027', name: 'Sofia Allen', mbti: null, learningStyle: null, grade: 84, preferredStudents: [], group: null },
    { studentNumber: 'S028', name: 'Joseph King', mbti: null, learningStyle: null, grade: 91, preferredStudents: [], group: null },
    { studentNumber: 'S029', name: 'Avery Wright', mbti: null, learningStyle: null, grade: 86, preferredStudents: [], group: null },
    { studentNumber: 'S030', name: 'Samuel Scott', mbti: null, learningStyle: null, grade: 78, preferredStudents: [], group: null }
];

// Initialize data if not exists
function initializeData() {
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) {
        const initialData = {
            students: initialStudents,
            courseName: '',
            groupingComplete: false,
            teacherPassword: 'teacher123' // Simple password for demo
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(initialData));
        return initialData;
    }
    return JSON.parse(data);
}

// Get all data
function getData() {
    return initializeData();
}

// Save data
function saveData(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

// Get student by student number
function getStudent(studentNumber) {
    const data = getData();
    return data.students.find(s => s.studentNumber === studentNumber);
}

// Update student information
function updateStudent(studentNumber, updates) {
    const data = getData();
    const studentIndex = data.students.findIndex(s => s.studentNumber === studentNumber);
    if (studentIndex !== -1) {
        data.students[studentIndex] = { ...data.students[studentIndex], ...updates };
        saveData(data);
        return true;
    }
    return false;
}

// Get all students
function getAllStudents() {
    const data = getData();
    return data.students;
}

// Get students with complete information
function getStudentsWithCompleteInfo() {
    const data = getData();
    return data.students.filter(s => s.mbti && s.learningStyle);
}

// Check if grouping is complete
function isGroupingComplete() {
    const data = getData();
    return data.groupingComplete;
}

// Set grouping status
function setGroupingComplete(status) {
    const data = getData();
    data.groupingComplete = status;
    saveData(data);
}

// Get course name
function getCourseName() {
    const data = getData();
    return data.courseName;
}

// Set course name
function setCourseName(name) {
    const data = getData();
    data.courseName = name;
    saveData(data);
}

// Reset all data (for testing)
function resetData() {
    localStorage.removeItem(STORAGE_KEY);
    initializeData();
}

// Check teacher password
function checkTeacherPassword(password) {
    const data = getData();
    return password === data.teacherPassword;
}

// Export functions for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeData,
        getData,
        saveData,
        getStudent,
        updateStudent,
        getAllStudents,
        getStudentsWithCompleteInfo,
        isGroupingComplete,
        setGroupingComplete,
        getCourseName,
        setCourseName,
        resetData,
        checkTeacherPassword
    };
}

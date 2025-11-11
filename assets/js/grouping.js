// Grouping Logic with ChatGPT API Integration
// This file handles the student grouping process

/**
 * Main grouping function
 * @param {string} courseName - The name of the course
 * @returns {Promise<Object>} - Grouping results
 */
async function performGrouping(courseName) {
    const studentsWithInfo = getStudentsWithCompleteInfo();
    
    if (studentsWithInfo.length === 0) {
        throw new Error('No students have completed their profiles yet.');
    }

    // Uncomment this section when you have a ChatGPT API key
    /*
    try {
        const groups = await groupWithChatGPT(studentsWithInfo, courseName);
        return groups;
    } catch (error) {
        console.error('ChatGPT API failed, falling back to random grouping:', error);
        // Fall back to random grouping if API fails
        return randomGrouping(studentsWithInfo);
    }
    */

    // For now, use random grouping (comment this out when using API)
    return randomGrouping(studentsWithInfo);
}

/**
 * Group students using ChatGPT API
 * @param {Array} students - Students with complete information
 * @param {string} courseName - The name of the course
 * @returns {Promise<Object>} - Grouping results
 */
async function groupWithChatGPT(students, courseName) {
    const apiKey = 'YOUR_CHATGPT_API_KEY_HERE'; // Replace with your actual API key
    const apiUrl = 'https://api.openai.com/v1/chat/completions';

    // Prepare student data for the prompt
    const studentData = students.map(s => ({
        studentNumber: s.studentNumber,
        name: s.name,
        mbti: s.mbti,
        learningStyle: s.learningStyle,
        grade: s.grade,
        preferredStudents: s.preferredStudents || []
    }));

    // Create the prompt
    const prompt = `You are an educational AI assistant helping to group students for a ${courseName} course.

Student Information:
${JSON.stringify(studentData, null, 2)}

Please create balanced study groups considering:
1. MBTI compatibility (complementary personality types work well together)
2. Learning style diversity (mix of different learning styles in each group)
3. Grade balance (each group should have a mix of different performance levels)
4. Student preferences (try to honor preferred groupmates when possible, but not at the expense of balance)

Guidelines:
- Create groups of 5-6 students each
- Ensure each group has diverse MBTI types and learning styles
- Balance grades across groups
- Try to include at least one preferred groupmate per student when possible
- Prioritize group balance over all individual preferences

Return ONLY a JSON object in this exact format:
{
  "groups": [
    {
      "groupNumber": 1,
      "students": ["S001", "S002", "S003", "S004", "S005"],
      "reasoning": "Brief explanation of the group composition"
    }
  ]
}`;

    // Make API call
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: 'gpt-4',
            messages: [
                {
                    role: 'system',
                    content: 'You are an expert educational consultant specializing in student grouping and team formation.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.7,
            max_tokens: 2000
        })
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();
    const content = data.choices[0].message.content;

    // Parse the JSON response
    const groupingResult = JSON.parse(content);

    return groupingResult;
}

/**
 * Random grouping fallback (used when API is not available)
 * @param {Array} students - Students with complete information
 * @returns {Object} - Grouping results
 */
function randomGrouping(students) {
    // Shuffle students
    const shuffled = [...students].sort(() => Math.random() - 0.5);
    
    // Determine group size (aim for groups of 5-6)
    const groupSize = 5;
    const numGroups = Math.ceil(shuffled.length / groupSize);
    
    const groups = [];
    
    for (let i = 0; i < numGroups; i++) {
        const groupStudents = shuffled.slice(i * groupSize, (i + 1) * groupSize);
        
        groups.push({
            groupNumber: i + 1,
            students: groupStudents.map(s => s.studentNumber),
            reasoning: 'Random grouping (API not configured)'
        });
    }
    
    return { groups };
}

/**
 * Apply grouping results to student data
 * @param {Object} groupingResult - Results from grouping function
 * @param {string} courseName - The name of the course
 */
function applyGrouping(groupingResult, courseName) {
    const data = getData();
    
    // Reset all groups first
    data.students.forEach(student => {
        student.group = null;
    });
    
    // Apply new grouping
    groupingResult.groups.forEach(group => {
        group.students.forEach(studentNumber => {
            const studentIndex = data.students.findIndex(s => s.studentNumber === studentNumber);
            if (studentIndex !== -1) {
                data.students[studentIndex].group = group.groupNumber;
            }
        });
    });
    
    // Set course name and grouping status
    data.courseName = courseName;
    data.groupingComplete = true;
    data.groupingResults = groupingResult; // Store full results for teacher reference
    
    saveData(data);
}

/**
 * Get grouping statistics
 * @returns {Object} - Statistics about current grouping
 */
function getGroupingStats() {
    const data = getData();
    const allStudents = data.students;
    const studentsWithInfo = allStudents.filter(s => s.mbti && s.learningStyle);
    
    const stats = {
        totalStudents: allStudents.length,
        studentsWithCompleteInfo: studentsWithInfo.length,
        studentsGrouped: allStudents.filter(s => s.group !== null).length,
        groupingComplete: data.groupingComplete,
        courseName: data.courseName,
        groups: []
    };
    
    if (data.groupingComplete && data.groupingResults) {
        stats.groups = data.groupingResults.groups;
    }
    
    return stats;
}

/**
 * Reset grouping (clear all group assignments)
 */
function resetGrouping() {
    const data = getData();
    
    data.students.forEach(student => {
        student.group = null;
    });
    
    data.groupingComplete = false;
    data.courseName = '';
    data.groupingResults = null;
    
    saveData(data);
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        performGrouping,
        applyGrouping,
        getGroupingStats,
        resetGrouping
    };
}

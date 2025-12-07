// Grouping Logic with Backend API Integration
// This file handles the student grouping process through the backend

// API_BASE_URL is defined in data.js (loaded first)
// No need to redeclare it here to avoid "already been declared" error

/**
 * Main grouping function - calls backend API
 * @param {string} courseName - The name of the course
 * @returns {Promise<Object>} - Grouping results
 */
async function performGrouping(courseName) {
    try {
        console.log(`Requesting grouping from backend for course: ${courseName}`);
        
        const response = await fetch(`${API_BASE_URL}/grouping/perform`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                courseName
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Grouping failed');
        }

        const result = await response.json();
        console.log('Grouping successful!', result);
        return result.results;
    } catch (error) {
        console.error('Grouping error:', error);
        throw error;
    }
}

/**
 * Get grouping statistics
 * @returns {Promise<Object>} - Statistics about current grouping
 */
async function getGroupingStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/grouping/status`);
        if (!response.ok) {
            throw new Error('Failed to get grouping status');
        }
        return await response.json();
    } catch (error) {
        console.error('Error getting grouping stats:', error);
        throw error;
    }
}

/**
 * Toggle visibility of results to students
 * @param {string} password - Teacher password
 * @returns {Promise<Object>} - New visibility status
 */
async function toggleResultsVisibility(password) {
    try {
        const response = await fetch(`${API_BASE_URL}/grouping/toggle-visibility`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to toggle visibility');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error toggling visibility:', error);
        throw error;
    }
}

/**
 * Reset grouping (clear all group assignments)
 * @param {string} password - Teacher password
 */
async function resetGrouping(password) {
    try {
        const response = await fetch(`${API_BASE_URL}/grouping/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to reset grouping');
        }

        return await response.json();
    } catch (error) {
        console.error('Error resetting grouping:', error);
        throw error;
    }
}

/**
 * Get student's group information
 * @param {string} studentNumber - Student number
 * @returns {Promise<Object>} - Group information
 */
async function getStudentGroup(studentNumber) {
    try {
        const response = await fetch(`${API_BASE_URL}/student/${studentNumber}/group`);
        
        if (!response.ok) {
            const error = await response.json();
            if (error.detail.includes('not yet visible')) {
                return { 
                    error: 'not_visible', 
                    message: 'نتایج هنوز توسط استاد نمایش داده نشده است.' 
                };
            }
            if (error.detail.includes('not assigned')) {
                return { 
                    error: 'not_assigned', 
                    message: 'شما هنوز به گروهی اختصاص داده نشده‌اید.' 
                };
            }
            throw new Error(error.detail);
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting student group:', error);
        throw error;
    }
}

// Legacy function - now handled by backend
function applyGrouping(groupingResult, courseName) {
    console.warn('applyGrouping is now handled automatically by the backend');
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        performGrouping,
        getGroupingStats,
        toggleResultsVisibility,
        resetGrouping,
        getStudentGroup,
        applyGrouping
    };
}

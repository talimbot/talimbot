// Configuration for TalimBot
// Switch between development (localhost) and production (Render.com)

const CONFIG = {
    // Set to 'production' when deploying to GitHub Pages
    // Set to 'development' when testing locally
    MODE: 'development', // Change to 'production' after deploying backend
    
    // Development API (your local laptop)
    DEVELOPMENT_API: 'http://localhost:8000/api',
    
    // Production API (Render.com - UPDATE THIS after deployment!)
    // Example: 'https://talimbot-api.onrender.com/api'
    PRODUCTION_API: 'https://YOUR-RENDER-URL-HERE.onrender.com/api',
    
    // Get the current API URL based on mode
    getApiUrl() {
        return this.MODE === 'production' ? this.PRODUCTION_API : this.DEVELOPMENT_API;
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

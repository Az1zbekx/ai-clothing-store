// api.js - Centralized API utility for the AI Clothing Store

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Handles API fetch requests with token authorization and error handling.
 * @param {string} endpoint - The API endpoint path (e.g., '/auth/login').
 * @param {object} options - Fetch options (method, headers, body).
 * @returns {Promise<any>} - The JSON response or throws an error.
 */
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Setup default headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Attach Bearer token if it exists
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(url, config);
        
        // Handle unauthorized or forbidden errors globally
        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = 'login.html';
            throw new Error('Authentication failed. Please login again.');
        }

        // Parse JSON response
        let data;
        try {
            data = await response.json();
        } catch (e) {
            data = null; // Some endpoints might not return JSON
        }

        if (!response.ok) {
            const errorMsg = data?.detail || data?.message || `Error ${response.status}: ${response.statusText}`;
            throw new Error(errorMsg);
        }

        return data;
    } catch (error) {
        console.error('API Fetch Error:', error);
        throw error;
    }
}

/**
 * Shows a loading indicator inside a specific container
 */
function showLoader(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '<div class="loader-container"><div class="loader"></div></div>';
    }
}

/**
 * Shows an error message inside a specific container
 */
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="error-message">${message}</div>`;
    }
}

// Export functions globally for browser usage
window.api = {
    fetch: apiFetch,
    showLoader,
    showError
};

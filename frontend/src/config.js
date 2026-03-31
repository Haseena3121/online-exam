// Central API base URL
// In Docker: nginx proxies /api/ to backend, so base is empty string (relative URLs)
// In local dev: points to localhost:5000
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default API_BASE;

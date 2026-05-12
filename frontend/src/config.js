/* eslint-disable no-unused-vars */
// In production (Docker/Nginx), the frontend and backend share the same origin.
// Nginx proxies /api/* to the backend, so API_BASE is empty string.
// In development, the backend runs on port 5000.
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default API_BASE;

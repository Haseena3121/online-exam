import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT) || 30000;

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Handle responses
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  login: (email, password) => 
    api.post('/auth/login', { email, password }),
  register: (name, email, password, phone, role) =>
    api.post('/auth/register', { name, email, password, phone, role }),
  getCurrentUser: () =>
    api.get('/auth/me'),
  logout: () =>
    api.post('/auth/logout'),
  refreshToken: () =>
    api.post('/auth/refresh-token')
};

// Exam API
export const examAPI = {
  getAll: () =>
    api.get('/exams'),
  getById: (examId) =>
    api.get(`/exams/${examId}`),
  getMyExams: () =>
    api.get('/exams/my-exams'),
  create: (examData) =>
    api.post('/exams', examData),
  addQuestion: (examId, questionData) =>
    api.post(`/exams/${examId}/questions`, questionData),
  enroll: (examId) =>
    api.post(`/exams/${examId}/enroll`),
  submitAcceptanceForm: (examId, formData) =>
    api.post(`/exams/${examId}/acceptance-form`, formData),
  startExam: (examId) =>
    api.post(`/exams/${examId}/start`)
};

// Proctoring API
export const proctoringAPI = {
  reportViolation: (violationData) =>
    api.post('/proctoring/violation', violationData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  getSessionStatus: (sessionId) =>
    api.get(`/proctoring/session/${sessionId}`),
  sendWarning: (sessionId) =>
    api.post(`/proctoring/session/${sessionId}/warning`),
  submitExam: (answers) =>
    api.post('/proctoring/submit', { answers }),
  getAnalytics: (sessionId) =>
    api.get(`/proctoring/analytics/${sessionId}`),
  updateAnalytics: (sessionId, analyticsData) =>
    api.post(`/proctoring/update-analytics/${sessionId}`, analyticsData)
};

// Violations API
export const violationsAPI = {
  getHistory: (examId) =>
    api.get(`/violations/history/${examId}`),
  getByExam: (examId) =>
    api.get(`/violations/by-exam/${examId}`),
  getDetails: (violationId) =>
    api.get(`/violations/${violationId}`)
};

// Results API
export const resultsAPI = {
  getResult: (examId) =>
    api.get(`/results/${examId}`),
  getAllResults: () =>
    api.get('/results/all'),
  getDetailedResult: (examId) =>
    api.get(`/results/detailed/${examId}`),
  getExamResults: (examId) =>
    api.get(`/results/exam/${examId}/all-students`)
};
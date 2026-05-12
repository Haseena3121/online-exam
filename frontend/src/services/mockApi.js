/* eslint-disable no-unused-vars */
// Mock API for development/testing when backend is not available

const MOCK_DELAY = 500; // Simulate network delay

// Mock data
const mockUsers = {
  student: {
    _id: 'student-001',
    name: 'John Student',
    email: 'student@test.com',
    role: 'student',
    phone: '1234567890'
  },
  teacher: {
    _id: 'teacher-001',
    name: 'Dr. Jane Teacher',
    email: 'teacher@test.com',
    role: 'teacher',
    phone: '0987654321'
  }
};

const mockExams = [
  {
    _id: 'exam-001',
    title: 'Mathematics Final Exam',
    description: 'Comprehensive mathematics examination covering algebra, calculus, and statistics.',
    duration: 120,
    totalQuestions: 10,
    passingScore: 60,
    startTime: new Date(Date.now() + 3600000).toISOString(),
    endTime: new Date(Date.now() + 7200000).toISOString(),
    status: 'upcoming',
    createdBy: mockUsers.teacher,
    questions: [
      { _id: 'q1', questionText: 'What is 2 + 2?', options: ['3', '4', '5', '6'], correctAnswer: 1, marks: 10 },
      { _id: 'q2', questionText: 'Solve: x² - 4 = 0', options: ['x = 2', 'x = ±2', 'x = 4', 'x = -2'], correctAnswer: 1, marks: 10 },
      { _id: 'q3', questionText: 'What is the derivative of x³?', options: ['x²', '3x²', '3x', 'x³'], correctAnswer: 1, marks: 10 },
      { _id: 'q4', questionText: 'Calculate: 15% of 200', options: ['20', '25', '30', '35'], correctAnswer: 2, marks: 10 },
      { _id: 'q5', questionText: 'What is √144?', options: ['10', '11', '12', '14'], correctAnswer: 2, marks: 10 },
    ]
  },
  {
    _id: 'exam-002',
    title: 'Physics Midterm',
    description: 'Physics examination covering mechanics and thermodynamics.',
    duration: 90,
    totalQuestions: 8,
    passingScore: 50,
    startTime: new Date(Date.now() - 3600000).toISOString(),
    endTime: new Date(Date.now() + 3600000).toISOString(),
    status: 'active',
    createdBy: mockUsers.teacher,
    questions: [
      { _id: 'q1', questionText: 'What is Newton\'s first law?', options: ['Law of inertia', 'F=ma', 'Action-reaction', 'Gravity'], correctAnswer: 0, marks: 10 },
      { _id: 'q2', questionText: 'Unit of force is?', options: ['Joule', 'Newton', 'Watt', 'Pascal'], correctAnswer: 1, marks: 10 },
    ]
  }
];

const mockResults = [
  {
    _id: 'result-001',
    examId: 'exam-001',
    studentId: 'student-001',
    score: 85,
    totalMarks: 100,
    percentage: 85,
    status: 'passed',
    submittedAt: new Date().toISOString()
  }
];

// Helper to simulate async response
const mockResponse = (data, delay = MOCK_DELAY) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ data });
    }, delay);
  });
};

const mockError = (message, status = 400) => {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject({ response: { data: { error: message }, status } });
    }, MOCK_DELAY);
  });
};

// Mock Auth API
export const mockAuthAPI = {
  login: (email, password) => {
    if (email === 'student@test.com' && password === 'password') {
      localStorage.setItem('access_token', 'mock-token-student');
      localStorage.setItem('user_role', 'student');
      return mockResponse({ 
        access_token: 'mock-token-student', 
        user: mockUsers.student 
      });
    }
    if (email === 'teacher@test.com' && password === 'password') {
      localStorage.setItem('access_token', 'mock-token-teacher');
      localStorage.setItem('user_role', 'teacher');
      return mockResponse({ 
        access_token: 'mock-token-teacher', 
        user: mockUsers.teacher 
      });
    }
    return mockError('Invalid email or password', 401);
  },
  
  register: (name, email, password, phone, role) => {
    return mockResponse({ 
      message: 'Registration successful',
      user: { _id: 'new-user', name, email, role, phone }
    });
  },
  
  getCurrentUser: () => {
    const token = localStorage.getItem('access_token');
    if (token === 'mock-token-student') {
      return mockResponse(mockUsers.student);
    }
    if (token === 'mock-token-teacher') {
      return mockResponse(mockUsers.teacher);
    }
    return mockError('Unauthorized', 401);
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    return mockResponse({ message: 'Logged out successfully' });
  },
  
  refreshToken: () => {
    return mockResponse({ access_token: localStorage.getItem('access_token') });
  }
};

// Mock Exam API
export const mockExamAPI = {
  getAll: () => mockResponse(mockExams),
  
  getById: (examId) => {
    const exam = mockExams.find(e => e._id === examId);
    if (exam) return mockResponse(exam);
    return mockError('Exam not found', 404);
  },
  
  getMyExams: () => mockResponse(mockExams),
  
  create: (examData) => {
    const newExam = { _id: `exam-${Date.now()}`, ...examData, status: 'upcoming' };
    mockExams.push(newExam);
    return mockResponse(newExam);
  },
  
  addQuestion: (examId, questionData) => {
    return mockResponse({ message: 'Question added', question: questionData });
  },
  
  enroll: (examId) => {
    return mockResponse({ message: 'Enrolled successfully' });
  },
  
  submitAcceptanceForm: (examId, formData) => {
    return mockResponse({ message: 'Acceptance form submitted', sessionId: `session-${Date.now()}` });
  },
  
  startExam: (examId) => {
    const exam = mockExams.find(e => e._id === examId);
    return mockResponse({ 
      message: 'Exam started', 
      sessionId: `session-${Date.now()}`,
      exam 
    });
  }
};

// Mock Proctoring API
export const mockProctoringAPI = {
  reportViolation: (violationData) => {
    return mockResponse({ message: 'Violation reported', violationId: `vio-${Date.now()}` });
  },
  
  getSessionStatus: (sessionId) => {
    return mockResponse({ 
      sessionId, 
      status: 'active', 
      warnings: 0, 
      violations: [] 
    });
  },
  
  sendWarning: (sessionId) => {
    return mockResponse({ message: 'Warning sent' });
  },
  
  submitExam: (answers) => {
    const score = Math.floor(Math.random() * 40) + 60; // Random score 60-100
    return mockResponse({ 
      message: 'Exam submitted successfully',
      score,
      totalMarks: 100,
      percentage: score,
      status: score >= 60 ? 'passed' : 'failed'
    });
  },
  
  getAnalytics: (sessionId) => {
    return mockResponse({
      sessionId,
      tabSwitches: 2,
      faceNotDetected: 1,
      multipleFaces: 0,
      totalViolations: 3
    });
  },
  
  updateAnalytics: (sessionId, analyticsData) => {
    return mockResponse({ message: 'Analytics updated' });
  }
};

// Mock Violations API
export const mockViolationsAPI = {
  getHistory: (examId) => {
    return mockResponse([
      { _id: 'v1', type: 'tab_switch', timestamp: new Date().toISOString(), severity: 'medium' },
      { _id: 'v2', type: 'face_not_detected', timestamp: new Date().toISOString(), severity: 'high' }
    ]);
  },
  
  getByExam: (examId) => {
    return mockResponse([]);
  },
  
  getDetails: (violationId) => {
    return mockResponse({ _id: violationId, type: 'tab_switch', details: 'User switched tabs' });
  }
};

// Mock Results API
export const mockResultsAPI = {
  getResult: (examId) => {
    const result = mockResults.find(r => r.examId === examId);
    if (result) return mockResponse(result);
    return mockError('Result not found', 404);
  },
  
  getAllResults: () => mockResponse(mockResults),
  
  getDetailedResult: (examId) => {
    return mockResponse({
      examId,
      score: 85,
      totalMarks: 100,
      answers: [],
      timeSpent: 45
    });
  },
  
  getExamResults: (examId) => {
    return mockResponse([
      { studentName: 'John Student', score: 85, status: 'passed' },
      { studentName: 'Jane Doe', score: 72, status: 'passed' }
    ]);
  }
};

// Check if we should use mock API
export const USE_MOCK_API = true; // Set to false when backend is available

console.log('[Mock API] Mock API is enabled. Use these credentials to login:');
console.log('[Mock API] Student: student@test.com / password');
console.log('[Mock API] Teacher: teacher@test.com / password');

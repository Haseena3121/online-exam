import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';

function ExaminerDashboard() {
  const { token, user } = useAuth();
  const navigate = useNavigate();

  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user is examiner on component mount
  useEffect(() => {
    const currentUser = JSON.parse(localStorage.getItem("user") || "{}");
    const currentToken = localStorage.getItem("access_token");
    
    console.log('ExaminerDashboard - Current user:', currentUser);
    console.log('ExaminerDashboard - Has token:', !!currentToken);
    
    if (!currentToken || !currentUser.id) {
      console.log('No authentication, redirecting to login');
      navigate('/login');
      return;
    }
    
    if (currentUser.role !== 'examiner') {
      console.log('User is not examiner, role:', currentUser.role);
      alert('Access denied. You must be logged in as an examiner.');
      navigate('/login');
      return;
    }
    
    fetchExams();
  }, [navigate]);

  const fetchExams = async () => {
    try {
      console.log('Fetching exams...');
      const token = localStorage.getItem("access_token");
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      
      console.log('Current user:', user);
      console.log('Token exists:', !!token);
      
      if (!token) {
        console.error('No token found, redirecting to login');
        navigate('/login');
        return;
      }
      
      if (user.role !== 'examiner') {
        console.error('User is not an examiner:', user.role);
        alert('You must be logged in as an examiner to access this page');
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:5000/api/exams/my-exams', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Exams data:', data);
        console.log('Exams array:', data.exams);
        setExams(data.exams);
      } else if (response.status === 403) {
        console.error('403 Forbidden - Token invalid or user not examiner');
        alert('Authentication failed. Please login again as an examiner.');
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        navigate('/login');
      } else {
        console.error('Failed to fetch exams:', response.status);
        const errorData = await response.json().catch(() => ({}));
        console.error('Error details:', errorData);
      }
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePublish = async (examId, currentStatus) => {
    try {
      const response = await fetch(`http://localhost:5000/api/exams/${examId}/publish`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify({ is_published: !currentStatus })
      });

      if (response.ok) {
        alert(`Exam ${!currentStatus ? 'published' : 'unpublished'} successfully!`);
        fetchExams(); // Refresh the list
      } else {
        alert('Failed to update exam status');
      }
    } catch (error) {
      console.error('Error updating exam:', error);
      alert('Error updating exam status');
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="examiner-dashboard">
      <h1>👨‍🏫 Examiner Dashboard</h1>

      {/* Action Buttons */}
      <div style={{ marginBottom: "20px", display: "flex", gap: "10px" }}>
        <button
          onClick={() => navigate("/create-exam")}
          className="btn btn-primary"
        >
          ➕ Create New Exam
        </button>
        <button
          onClick={() => navigate("/live-monitoring")}
          className="btn btn-success"
          style={{ background: "#4caf50" }}
        >
          🎥 Live Monitoring
        </button>
      </div>

      <div className="examiner-grid">
        <div className="exams-sidebar">
          <h2>📚 My Exams ({exams.length})</h2>
          <div className="exams-list">
            {exams.length > 0 ? (
              exams.map(exam => (
                <div
                  key={exam.id}
                  className="exam-item"
                  onClick={() => setSelectedExam(exam)}
                  style={{
                    padding: '15px',
                    margin: '10px 0',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    backgroundColor: selectedExam?.id === exam.id ? '#e3f2fd' : 'white'
                  }}
                >
                  <h4>{exam.title}</h4>
                  <p>⏱️ {exam.duration} min | ⭐ {exam.total_marks} marks</p>
                  <p style={{ 
                    fontSize: '12px', 
                    color: exam.is_published ? '#4caf50' : '#ff9800',
                    fontWeight: 'bold'
                  }}>
                    {exam.is_published ? '✅ Published' : '⚠️ Not Published'}
                  </p>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      togglePublish(exam.id, exam.is_published);
                    }}
                    style={{
                      marginTop: '10px',
                      marginRight: '10px',
                      padding: '8px 16px',
                      backgroundColor: exam.is_published ? '#ff9800' : '#4caf50',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    {exam.is_published ? 'Unpublish' : 'Publish'}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/exam/${exam.id}/results`);
                    }}
                    style={{
                      marginTop: '10px',
                      padding: '8px 16px',
                      backgroundColor: '#667eea',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    📊 View Results
                  </button>
                </div>
              ))
            ) : (
              <p style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                No exams created yet. Click "Create New Exam" to get started!
              </p>
            )}
          </div>
        </div>

        <div className="main-content">
          {selectedExam ? (
            <div>
              <h2>{selectedExam.title}</h2>
              <p>Duration: {selectedExam.duration} minutes</p>
              <p>Total Marks: {selectedExam.total_marks}</p>
            </div>
          ) : (
            <div className="empty-state">
              <p>Select an exam to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ExaminerDashboard;
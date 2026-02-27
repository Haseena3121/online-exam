import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';

function ExaminerDashboard() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      console.log('Fetching exams...');
      const response = await fetch('http://localhost:5000/api/exams/my-exams', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Exams data:', data);
        console.log('Exams array:', data.exams);
        setExams(data.exams);
      } else {
        console.error('Failed to fetch exams:', response.status);
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

      {/* 🔥 CREATE EXAM BUTTON */}
      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={() => navigate("/create-exam")}
          className="btn btn-primary"
        >
          ➕ Create New Exam
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
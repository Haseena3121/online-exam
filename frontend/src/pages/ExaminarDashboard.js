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
      const response = await fetch('http://localhost:5000/api/exams/my-exams', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
         //#  Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setExams(data.exams);
      }
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
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
          <h2>📚 My Exams</h2>
          <div className="exams-list">
            {exams.length > 0 ? (
              exams.map(exam => (
                <div
                  key={exam.id}
                  className="exam-item"
                  onClick={() => setSelectedExam(exam)}
                >
                  <h4>{exam.title}</h4>
                  <p>⏱️ {exam.duration} min | ⭐ {exam.total_marks} marks</p>
                </div>
              ))
            ) : (
              <p>No exams created yet</p>
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
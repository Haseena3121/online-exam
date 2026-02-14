import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

function ExamList() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredExams, setFilteredExams] = useState([]);

  useEffect(() => {
    fetchExams();
  }, []);

  useEffect(() => {
    const filtered = exams.filter(exam =>
      exam.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      exam.description?.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredExams(filtered);
  }, [searchTerm, exams]);

  const fetchExams = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/exams', {
        headers: {
          'Authorization': `Bearer ${token}`
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

  if (loading) {
    return <div className="loading">Loading exams...</div>;
  }

  return (
    <div className="exam-list-container">
      <div className="exam-list-header">
        <h1>📚 Available Exams</h1>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search exams..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {filteredExams.length > 0 ? (
        <div className="exams-list">
          {filteredExams.map(exam => (
            <div key={exam.id} className="exam-list-item">
              <div className="exam-info">
                <h3>{exam.title}</h3>
                <p className="description">{exam.description}</p>
                <div className="exam-details">
                  <span>⏱️ Duration: {exam.duration} minutes</span>
                  <span>⭐ Total Marks: {exam.total_marks}</span>
                  <span>✅ Passing Marks: {exam.passing_marks}</span>
                  <span>❓ Questions: {exam.question_count}</span>
                </div>
              </div>
              <button
                className="btn btn-primary"
                onClick={() => navigate(`/exam/${exam.id}/acceptance`)}
              >
                Take Exam →
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No exams found</p>
        </div>
      )}
    </div>
  );
}

export default ExamList;
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import '../styles/CreateExam.css';

function CreateExam() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Exam Details, 2: Add Questions
  const [examId, setExamId] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    instructions: "",
    duration: "",
    total_marks: "",
    passing_marks: ""
  });
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState({
    question_text: "",
    option_a: "",
    option_b: "",
    option_c: "",
    option_d: "",
    correct_answer: "",
    marks: ""
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleQuestionChange = (e) => {
    setCurrentQuestion({
      ...currentQuestion,
      [e.target.name]: e.target.value
    });
  };

  const addQuestion = () => {
    if (!currentQuestion.question_text || !currentQuestion.marks) {
      alert("Please fill in question text and marks");
      return;
    }

    if (!currentQuestion.option_a || !currentQuestion.option_b || 
        !currentQuestion.option_c || !currentQuestion.option_d) {
      alert("Please fill in all options");
      return;
    }

    if (!currentQuestion.correct_answer) {
      alert("Please select the correct answer");
      return;
    }

    setQuestions([...questions, { ...currentQuestion, id: Date.now() }]);
    setCurrentQuestion({
      question_text: "",
      option_a: "",
      option_b: "",
      option_c: "",
      option_d: "",
      correct_answer: "",
      marks: ""
    });
  };

  const removeQuestion = (id) => {
    setQuestions(questions.filter(q => q.id !== id));
  };

  const handleSubmitExam = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/exams/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description,
          instructions: formData.instructions,
          duration: parseInt(formData.duration),
          total_marks: parseInt(formData.total_marks),
          passing_marks: parseInt(formData.passing_marks),
          negative_marking: 0,
          is_published: false
        })
      });

      const data = await response.json();

      if (response.ok) {
        setExamId(data.exam_id);
        setStep(2);
      } else {
        alert(`Failed to create exam: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`Error creating exam: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitQuestions = async () => {
    if (questions.length === 0) {
      alert("Please add at least one question");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`http://localhost:5000/api/exams/${examId}/questions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ questions })
      });

      const data = await response.json();

      if (response.ok) {
        alert(`Exam created successfully with ${questions.length} questions!`);
        navigate("/examiner-dashboard");
      } else {
        alert(`Failed to add questions: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`Error adding questions: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const skipQuestions = () => {
    if (window.confirm("Skip adding questions? You can add them later using the helper script.")) {
      navigate("/examiner-dashboard");
    }
  };

  const totalMarks = questions.reduce((sum, q) => sum + parseInt(q.marks || 0), 0);

  return (
    <div className="create-exam-container">
      <div className="create-exam-card">
        {/* Progress Indicator */}
        <div className="progress-steps">
          <div className={`step ${step === 1 ? 'active' : 'completed'}`}>
            <div className="step-number">1</div>
            <div className="step-label">Exam Details</div>
          </div>
          <div className="step-line"></div>
          <div className={`step ${step === 2 ? 'active' : ''}`}>
            <div className="step-number">2</div>
            <div className="step-label">Add Questions</div>
          </div>
        </div>

        {/* Step 1: Exam Details */}
        {step === 1 && (
          <div className="step-content">
            <h2>📝 Create New Exam</h2>
            <p>Fill in the exam details to get started</p>
            
            <form onSubmit={handleSubmitExam}>
              <div className="form-group">
                <label>Exam Title *</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  placeholder="e.g., Mathematics Final Exam"
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  placeholder="Brief description of the exam"
                  onChange={handleChange}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label>Instructions</label>
                <textarea
                  name="instructions"
                  value={formData.instructions}
                  placeholder="Exam instructions for students"
                  onChange={handleChange}
                  rows="4"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Duration (minutes) *</label>
                  <input
                    type="number"
                    name="duration"
                    value={formData.duration}
                    placeholder="60"
                    onChange={handleChange}
                    min="1"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Total Marks *</label>
                  <input
                    type="number"
                    name="total_marks"
                    value={formData.total_marks}
                    placeholder="100"
                    onChange={handleChange}
                    min="1"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Passing Marks *</label>
                  <input
                    type="number"
                    name="passing_marks"
                    value={formData.passing_marks}
                    placeholder="40"
                    onChange={handleChange}
                    min="1"
                    max={formData.total_marks || 100}
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button 
                  type="button" 
                  onClick={() => navigate("/examiner-dashboard")}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? "Creating..." : "Next: Add Questions →"}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Step 2: Add Questions */}
        {step === 2 && (
          <div className="step-content">
            <h2>❓ Add Questions</h2>
            <p>Add questions to your exam: {formData.title}</p>

            <div className="questions-summary">
              <div className="summary-item">
                <span className="label">Questions Added:</span>
                <span className="value">{questions.length}</span>
              </div>
              <div className="summary-item">
                <span className="label">Total Marks:</span>
                <span className="value">{totalMarks} / {formData.total_marks}</span>
              </div>
            </div>

            {/* Add Question Form */}
            <div className="question-form">
              <h3>New Question</h3>
              
              <div className="form-group">
                <label>Question Text *</label>
                <textarea
                  name="question_text"
                  value={currentQuestion.question_text}
                  placeholder="Enter your question here"
                  onChange={handleQuestionChange}
                  rows="3"
                />
              </div>

              <div className="form-row">
                <div className="form-group" style={{ flex: 3 }}>
                  <label>Option A *</label>
                  <input
                    type="text"
                    name="option_a"
                    value={currentQuestion.option_a}
                    placeholder="First option"
                    onChange={handleQuestionChange}
                  />
                </div>
                <div className="form-group" style={{ flex: 3 }}>
                  <label>Option B *</label>
                  <input
                    type="text"
                    name="option_b"
                    value={currentQuestion.option_b}
                    placeholder="Second option"
                    onChange={handleQuestionChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group" style={{ flex: 3 }}>
                  <label>Option C *</label>
                  <input
                    type="text"
                    name="option_c"
                    value={currentQuestion.option_c}
                    placeholder="Third option"
                    onChange={handleQuestionChange}
                  />
                </div>
                <div className="form-group" style={{ flex: 3 }}>
                  <label>Option D *</label>
                  <input
                    type="text"
                    name="option_d"
                    value={currentQuestion.option_d}
                    placeholder="Fourth option"
                    onChange={handleQuestionChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Correct Answer *</label>
                  <select
                    name="correct_answer"
                    value={currentQuestion.correct_answer}
                    onChange={handleQuestionChange}
                  >
                    <option value="">Select correct answer</option>
                    <option value="a">Option A</option>
                    <option value="b">Option B</option>
                    <option value="c">Option C</option>
                    <option value="d">Option D</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Marks *</label>
                  <input
                    type="number"
                    name="marks"
                    value={currentQuestion.marks}
                    placeholder="5"
                    onChange={handleQuestionChange}
                    min="1"
                  />
                </div>
              </div>

              <button 
                type="button" 
                onClick={addQuestion}
                className="btn btn-success"
              >
                ➕ Add Question
              </button>
            </div>

            {/* Questions List */}
            {questions.length > 0 && (
              <div className="questions-list">
                <h3>Added Questions ({questions.length})</h3>
                {questions.map((q, index) => (
                  <div key={q.id} className="question-item">
                    <div className="question-header">
                      <span className="question-number">Q{index + 1}</span>
                      <span className="question-marks">{q.marks} marks</span>
                      <button 
                        onClick={() => removeQuestion(q.id)}
                        className="btn-remove"
                      >
                        🗑️ Remove
                      </button>
                    </div>
                    <div className="question-text">{q.question_text}</div>
                    <div className="question-options">
                      <div className={q.correct_answer === 'a' ? 'correct' : ''}>A: {q.option_a}</div>
                      <div className={q.correct_answer === 'b' ? 'correct' : ''}>B: {q.option_b}</div>
                      <div className={q.correct_answer === 'c' ? 'correct' : ''}>C: {q.option_c}</div>
                      <div className={q.correct_answer === 'd' ? 'correct' : ''}>D: {q.option_d}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="form-actions">
              <button 
                type="button" 
                onClick={skipQuestions}
                className="btn btn-secondary"
              >
                Skip for Now
              </button>
              <button 
                type="button" 
                onClick={handleSubmitQuestions}
                disabled={loading || questions.length === 0}
                className="btn btn-primary"
              >
                {loading ? "Saving..." : `✓ Create Exam with ${questions.length} Questions`}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CreateExam;

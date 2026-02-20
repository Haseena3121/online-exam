import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function CreateExam() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    title: "",
    duration: "",
    total_marks: "",
    passing_marks: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:5000/api/exams/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
      title: formData.title,
      description: "",
      instructions: "",
      duration: parseInt(formData.duration),
      total_marks: parseInt(formData.total_marks),
      passing_marks: parseInt(formData.passing_marks),
      negative_marking: 0,
      is_published: false
})
    });

    if (response.ok) {
      alert("Exam created successfully!");
      navigate("/examiner-dashboard");
    } else {
      alert("Failed to create exam");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Create New Exam</h2>

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px" }}>
        <input
          type="text"
          name="title"
          placeholder="Exam Title"
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="duration"
          placeholder="Duration (minutes)"
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="total_marks"
          placeholder="Total Marks"
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="passing_marks"
          placeholder="Passing Marks"
          onChange={handleChange}
          required
        />

        <button type="submit">Create Exam</button>
      </form>
    </div>
  );
}

export default CreateExam;
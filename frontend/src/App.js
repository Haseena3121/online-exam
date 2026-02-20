import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ExaminarDashboard from "./pages/ExaminarDashboard";
import ExamInterface from "./pages/ExamInterface";
import ExamList from "./pages/ExamList";
import Results from "./pages/Results";
import AcceptanceForm from "./pages/AcceptanceForm";
import ViolationDetails from "./pages/ViolationDetails";
import CreateExam from "./pages/CreateExam";

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Student Routes */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/exam-list" element={<ExamList />} />
        <Route path="/exam" element={<ExamInterface />} />
        <Route path="/results" element={<Results />} />
        <Route path="/acceptance" element={<AcceptanceForm />} />

        {/* Examiner Routes */}
        <Route path="/examiner-dashboard" element={<ExaminarDashboard />} />
        <Route path="/violation-details" element={<ViolationDetails />} />
        <Route path="/create-exam" element={<CreateExam />} />
      </Routes>
    </Router>
  );
}

export default App;

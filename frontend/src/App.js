import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

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
import CameraTest from "./pages/CameraTest";
import Navbar from "./components/Navbar";

function App() {
  return (
    <AuthProvider>
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Navbar />
        <Routes>
          {/* Auth Routes */}
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Student Routes */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/camera-test" element={<CameraTest />} />
          <Route path="/exam-list" element={<ExamList />} />
          <Route path="/exam/:examId/acceptance" element={<AcceptanceForm />} />
          <Route path="/exam/:examId/:sessionId" element={<ExamInterface />} />
          <Route path="/results" element={<Results />} />
          <Route path="/result/:examId" element={<Results />} />

          {/* Examiner Routes */}
          <Route path="/examiner-dashboard" element={<ExaminarDashboard />} />
          <Route path="/violation-details" element={<ViolationDetails />} />
          <Route path="/create-exam" element={<CreateExam />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

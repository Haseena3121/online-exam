/* eslint-disable no-unused-vars, no-console, react-hooks/exhaustive-deps, no-useless-escape */
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function PrivateRoute({ children }) {
  const { user, token } = useAuth();

  if (!token || !user) {
    return <Navigate to="/login" />;
  }

  return children;
}

export default PrivateRoute;
/* eslint-disable no-unused-vars, no-console, react-hooks/exhaustive-deps, no-useless-escape */
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Silence tfjs duplicate kernel warnings in dev mode
const originalWarn = console.warn;
console.warn = (...args) => {
  if (args[0] && typeof args[0] === 'string' && args[0].includes('is already registered')) {
    return;
  }
  originalWarn(...args);
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

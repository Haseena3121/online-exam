import React from 'react';

export default function ShieldLogo({ size = 80, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Shield body with gradient */}
      <defs>
        <linearGradient id="shieldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#1e40af" />
          <stop offset="50%" stopColor="#3b82f6" />
          <stop offset="100%" stopColor="#60a5fa" />
        </linearGradient>
        <linearGradient id="innerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#1e3a8a" />
          <stop offset="100%" stopColor="#2563eb" />
        </linearGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#1e40af" floodOpacity="0.3"/>
        </filter>
      </defs>
      
      {/* Main shield shape */}
      <path
        d="M50 5L10 20V45C10 70 25 88 50 95C75 88 90 70 90 45V20L50 5Z"
        fill="url(#shieldGradient)"
        filter="url(#shadow)"
      />
      
      {/* Inner shield border */}
      <path
        d="M50 10L15 23V45C15 67 28 83 50 89C72 83 85 67 85 45V23L50 10Z"
        fill="url(#innerGradient)"
      />
      
      {/* Graduation cap */}
      <g filter="url(#glow)">
        {/* Cap base */}
        <path
          d="M50 32L25 42L50 52L75 42L50 32Z"
          fill="#fff"
        />
        {/* Cap top */}
        <path
          d="M35 45V58C35 62 42 67 50 67C58 67 65 62 65 58V45L50 52L35 45Z"
          fill="#fff"
          fillOpacity="0.9"
        />
        {/* Tassel line */}
        <line x1="70" y1="42" x2="70" y2="60" stroke="#fbbf24" strokeWidth="2" strokeLinecap="round"/>
        {/* Tassel end */}
        <circle cx="70" cy="62" r="3" fill="#fbbf24"/>
      </g>
      
      {/* Security checkmark */}
      <circle cx="72" cy="75" r="10" fill="#10b981" stroke="#fff" strokeWidth="2"/>
      <path
        d="M67 75L70 78L77 71"
        stroke="#fff"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

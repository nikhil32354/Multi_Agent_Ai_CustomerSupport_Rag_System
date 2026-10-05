import React from 'react'

export default function Avatar({ size = 'medium' }){
  const cls = `avatar ${size}`
  return (
    <div className={cls}>
      <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <defs>
          <radialGradient id="g" cx="30%" cy="25%">
            <stop offset="0%" stopColor="#ff8080" />
            <stop offset="60%" stopColor="#d33" />
            <stop offset="100%" stopColor="#8b1416" />
          </radialGradient>
        </defs>
        <g fill="none" fillRule="evenodd">
          {/* outer gradient circle */}
          <circle cx="32" cy="32" r="30" fill="url(#g)" />
          {/* subtle inner shadow */}
          <circle cx="32" cy="32" r="25" fill="rgba(0,0,0,0.28)" />
          {/* thin ring removed per request */}

          {/* robot head */}
          <g transform="translate(14,14)">
            <rect x="10" y="10" width="28" height="22" rx="8" fill="#fff" opacity="0.95" />
            {/* antenna */}
            <rect x="22" y="2" width="4" height="12" rx="2" fill="#fff" opacity="0.95" />
            <circle cx="24" cy="2" r="3" fill="#fff" opacity="0.95" />
            {/* eyes */}
            <rect x="16" y="18" width="6" height="6" rx="3" fill="#b32b2f" />
            <rect x="30" y="18" width="6" height="6" rx="3" fill="#b32b2f" />
            {/* mouth */}
            <rect x="22" y="26" width="10" height="4" rx="2" fill="#2b0a0a" opacity="0.9" />
          </g>
        </g>
      </svg>
    </div>
  )
}

import React from 'react';

interface LogoProps {
  className?: string;
  width?: number;
  height?: number;
}

const Logo: React.FC<LogoProps> = ({ className = '', width = 40, height = 40 }) => {
  return (
    <div className={`flex items-center ${className}`}>
      <svg
        width={width}
        height={height}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Magic Wand */}
        <path
          d="M30 10L35 5M25 8L26 3M32 15L37 16"
          stroke="#6366F1"
          strokeWidth="2"
          strokeLinecap="round"
        />
        {/* AI Symbol */}
        <path
          d="M8 28L14 16H18L24 28"
          stroke="#6366F1"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M10 24H22"
          stroke="#6366F1"
          strokeWidth="2"
          strokeLinecap="round"
        />
        {/* Magic Aura */}
        <circle
          cx="20"
          cy="20"
          r="15"
          stroke="#6366F1"
          strokeWidth="2"
          strokeDasharray="4 4"
        />
        {/* Center Star */}
        <path
          d="M20 12L22 18L28 20L22 22L20 28L18 22L12 20L18 18L20 12Z"
          fill="#6366F1"
        />
      </svg>
      <span className="ml-2 text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
        App Magic
      </span>
    </div>
  );
};

export default Logo; 
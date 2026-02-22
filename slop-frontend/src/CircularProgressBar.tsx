import React from 'react'

interface CircularProgressBarProps {
  progress: number // 0-100
  size?: number // diameter in pixels
  strokeWidth?: number
  color?: string
  backgroundColor?: string
  text?: string
  textColor?: string
  fontSize?: number
}

export const CircularProgressBar: React.FC<CircularProgressBarProps> = ({
  progress,
  size = 200,
  strokeWidth = 8,
  color = '#3b82f6',
  backgroundColor = '#e5e7eb',
  text = `${Math.round(progress)}%`,
  textColor = '#1f2937',
  fontSize = 24,
}) => {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (progress / 100) * circumference

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <svg width={size} height={size} style={{ position: 'relative' }}>
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={backgroundColor}
          strokeWidth={strokeWidth}
        />
        
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            transition: 'stroke-dashoffset 0.35s ease',
            transform: 'rotate(-90deg)',
            transformOrigin: `${size / 2}px ${size / 2}px`,
          }}
        />
        
        {/* Center text */}
        <text
          x={size / 2}
          y={size / 2}
          textAnchor="middle"
          dominantBaseline="central"
          fontSize={fontSize}
          fontWeight="bold"
          fill={textColor}
        >
          {text}
        </text>
      </svg>
    </div>
  )
}

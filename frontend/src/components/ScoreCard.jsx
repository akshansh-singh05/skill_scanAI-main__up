import { useState } from 'react'

const ScoreCard = ({ 
  title, 
  score, 
  description,
  gradient = 'from-indigo-500 to-purple-600',
  icon = null,
  maxScore = 100
}) => {
  const [isHovered, setIsHovered] = useState(false)
  
  const percentage = Math.min((score / maxScore) * 100, 100)
  
  const getScoreColor = () => {
    if (percentage >= 80) return 'text-emerald-400'
    if (percentage >= 60) return 'text-yellow-400'
    if (percentage >= 40) return 'text-orange-400'
    return 'text-red-400'
  }

  return (
    <div
      className={`
        relative overflow-hidden rounded-2xl p-6
        bg-gradient-to-br ${gradient}
        transform transition-all duration-300 ease-out
        ${isHovered ? 'scale-105 shadow-2xl shadow-indigo-500/30' : 'scale-100 shadow-lg'}
        cursor-pointer group
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-32 h-32 transform translate-x-8 -translate-y-8">
        <div className={`
          w-full h-full rounded-full bg-white/10
          transition-transform duration-500
          ${isHovered ? 'scale-150' : 'scale-100'}
        `} />
      </div>
      
      {/* Shine effect on hover */}
      <div className={`
        absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent
        transform -skew-x-12 transition-transform duration-700
        ${isHovered ? 'translate-x-full' : '-translate-x-full'}
      `} />

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white/90 tracking-wide">
            {title}
          </h3>
          {icon && (
            <div className={`
              p-2 rounded-lg bg-white/20 backdrop-blur-sm
              transition-transform duration-300
              ${isHovered ? 'rotate-12 scale-110' : ''}
            `}>
              {icon}
            </div>
          )}
        </div>

        {/* Score */}
        <div className="flex items-baseline gap-1 mb-3">
          <span className={`
            text-5xl font-bold text-white
            transition-all duration-300
            ${isHovered ? 'tracking-wider' : ''}
          `}>
            {score}
          </span>
          <span className="text-xl text-white/60 font-medium">
            /{maxScore}
          </span>
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-white/20 rounded-full overflow-hidden mb-4">
          <div 
            className={`
              h-full bg-white rounded-full
              transition-all duration-500 ease-out
              ${isHovered ? 'opacity-100' : 'opacity-80'}
            `}
            style={{ 
              width: `${percentage}%`,
              transition: 'width 0.8s ease-out'
            }}
          />
        </div>

        {/* Description */}
        <p className={`
          text-sm text-white/70 leading-relaxed
          transition-all duration-300
          ${isHovered ? 'text-white/90' : ''}
        `}>
          {description}
        </p>

        {/* Score indicator badge */}
        <div className={`
          absolute bottom-4 right-4
          px-3 py-1 rounded-full
          bg-white/20 backdrop-blur-sm
          text-xs font-semibold text-white
          transition-all duration-300
          ${isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}
        `}>
          {percentage >= 80 ? 'Excellent' : 
           percentage >= 60 ? 'Good' : 
           percentage >= 40 ? 'Average' : 'Needs Work'}
        </div>
      </div>
    </div>
  )
}

// Preset gradient variants
ScoreCard.gradients = {
  indigo: 'from-indigo-500 to-purple-600',
  emerald: 'from-emerald-500 to-teal-600',
  rose: 'from-rose-500 to-pink-600',
  amber: 'from-amber-500 to-orange-600',
  cyan: 'from-cyan-500 to-blue-600',
  violet: 'from-violet-500 to-fuchsia-600',
  slate: 'from-slate-600 to-slate-800',
}

export default ScoreCard

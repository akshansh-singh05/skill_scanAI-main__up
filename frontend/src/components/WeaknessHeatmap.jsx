import React from 'react';
import { motion } from 'framer-motion';

/**
 * WeaknessHeatmap Component
 * 
 * Visualizes skill levels with color-coded heatmap.
 * Low scores are highlighted in red, high scores in green.
 */
const WeaknessHeatmap = ({ skills = [], title = "Skill Heatmap", showLegend = true }) => {
  // Default skills if none provided
  const defaultSkills = [
    { name: 'DSA', score: 60 },
    { name: 'Backend', score: 75 },
    { name: 'System Design', score: 30 },
    { name: 'Communication', score: 80 },
  ];

  const skillsData = skills.length > 0 ? skills : defaultSkills;

  // Sort by score to show weaknesses first
  const sortedSkills = [...skillsData].sort((a, b) => a.score - b.score);

  // Get color based on score
  const getColor = (score) => {
    if (score >= 80) return { bg: 'bg-green-500', text: 'text-green-400', glow: 'shadow-green-500/30' };
    if (score >= 60) return { bg: 'bg-blue-500', text: 'text-blue-400', glow: 'shadow-blue-500/30' };
    if (score >= 40) return { bg: 'bg-yellow-500', text: 'text-yellow-400', glow: 'shadow-yellow-500/30' };
    return { bg: 'bg-red-500', text: 'text-red-400', glow: 'shadow-red-500/30' };
  };

  // Get background gradient for the bar
  const getBarGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-400';
    if (score >= 60) return 'from-blue-500 to-cyan-400';
    if (score >= 40) return 'from-yellow-500 to-orange-400';
    return 'from-red-500 to-rose-400';
  };

  // Get status label
  const getStatus = (score) => {
    if (score >= 80) return 'Strong';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Work';
    return 'Weak';
  };

  // Calculate average
  const avgScore = Math.round(skillsData.reduce((sum, s) => sum + s.score, 0) / skillsData.length);

  // Find weakest areas
  const weakAreas = sortedSkills.filter(s => s.score < 50);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-800/50 rounded-xl border border-gray-700/50 p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
              />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">{title}</h3>
            <p className="text-sm text-gray-400">Areas requiring attention highlighted</p>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${getColor(avgScore).text}`}>{avgScore}%</div>
          <div className="text-xs text-gray-400">Average</div>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="grid gap-3 mb-4">
        {sortedSkills.map((skill, index) => {
          const colors = getColor(skill.score);
          const isWeak = skill.score < 50;
          
          return (
            <motion.div
              key={skill.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`
                relative rounded-lg p-4 transition-all duration-300
                ${isWeak 
                  ? 'bg-red-500/10 border-2 border-red-500/50 shadow-lg shadow-red-500/20' 
                  : 'bg-gray-700/30 border border-gray-600/30'
                }
              `}
            >
              {/* Weak indicator */}
              {isWeak && (
                <div className="absolute top-2 right-2">
                  <span className="flex items-center gap-1 px-2 py-0.5 bg-red-500/20 text-red-400 text-xs font-medium rounded-full">
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Focus Area
                  </span>
                </div>
              )}

              {/* Skill Info */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`text-lg font-semibold ${isWeak ? 'text-red-300' : 'text-white'}`}>
                    {skill.name}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded ${colors.bg}/20 ${colors.text}`}>
                    {getStatus(skill.score)}
                  </span>
                </div>
                <span className={`text-xl font-bold ${colors.text}`}>
                  {skill.score}%
                </span>
              </div>

              {/* Progress Bar */}
              <div className="h-3 bg-gray-700/50 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${skill.score}%` }}
                  transition={{ duration: 0.8, ease: 'easeOut', delay: index * 0.1 }}
                  className={`h-full bg-gradient-to-r ${getBarGradient(skill.score)} rounded-full relative`}
                >
                  {/* Animated shine effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
                </motion.div>
              </div>

              {/* Score markers */}
              <div className="flex justify-between mt-1 text-xs text-gray-500">
                <span>0</span>
                <span>50</span>
                <span>100</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Legend */}
      {showLegend && (
        <div className="flex items-center justify-center gap-4 pt-4 border-t border-gray-700/50">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-xs text-gray-400">Weak (&lt;50%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span className="text-xs text-gray-400">Needs Work (50-60%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span className="text-xs text-gray-400">Good (60-80%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-xs text-gray-400">Strong (80%+)</span>
          </div>
        </div>
      )}

      {/* Weak Areas Summary */}
      {weakAreas.length > 0 && (
        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
          <div className="flex items-start gap-2">
            <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" 
              />
            </svg>
            <div>
              <p className="text-sm font-medium text-red-400">
                Priority Areas: {weakAreas.map(s => s.name).join(', ')}
              </p>
              <p className="text-xs text-red-300/70 mt-1">
                Focus on these areas to improve your overall interview readiness.
              </p>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
};

/**
 * Compact Heatmap Row
 * For displaying in tables or lists
 */
export const HeatmapRow = ({ name, score }) => {
  const getColor = (s) => {
    if (s >= 80) return 'bg-green-500';
    if (s >= 60) return 'bg-blue-500';
    if (s >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-gray-300 w-32 truncate">{name}</span>
      <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
        <div 
          className={`h-full ${getColor(score)} rounded-full transition-all`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className={`text-sm font-medium min-w-[3rem] text-right ${
        score < 50 ? 'text-red-400' : score < 70 ? 'text-yellow-400' : 'text-green-400'
      }`}>
        {score}%
      </span>
    </div>
  );
};

/**
 * Mini Heatmap Cell
 * For grid displays
 */
export const HeatmapCell = ({ name, score, size = 'md' }) => {
  const getBgColor = (s) => {
    if (s >= 80) return 'bg-green-500/80';
    if (s >= 60) return 'bg-blue-500/80';
    if (s >= 40) return 'bg-yellow-500/80';
    return 'bg-red-500/80';
  };

  const sizeClasses = {
    sm: 'w-16 h-16 text-xs',
    md: 'w-20 h-20 text-sm',
    lg: 'w-24 h-24 text-base',
  };

  return (
    <div 
      className={`${sizeClasses[size]} ${getBgColor(score)} rounded-lg flex flex-col items-center justify-center text-white font-medium shadow-lg transition-transform hover:scale-105`}
    >
      <span className="font-bold">{score}%</span>
      <span className="text-white/80 truncate px-1">{name}</span>
    </div>
  );
};

export default WeaknessHeatmap;

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * CommunicationScore Component
 * 
 * Displays detailed communication analysis including:
 * - Clarity and Structure scores
 * - Filler word detection
 * - Issues and suggestions
 * - Visual score indicators
 */
const CommunicationScore = ({ analysis, compact = false }) => {
  if (!analysis) return null;

  const {
    clarity_score = 0,
    structure_score = 0,
    confidence_score = 0,
    overall_score = 0,
    filler_words = [],
    filler_count = 0,
    issues = [],
    suggestions = [],
    strengths = [],
    word_count = 0,
    grades = {}
  } = analysis;

  // Score color based on value
  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-400';
    if (score >= 6) return 'text-blue-400';
    if (score >= 4) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBg = (score) => {
    if (score >= 8) return 'bg-green-500/20 border-green-500/30';
    if (score >= 6) return 'bg-blue-500/20 border-blue-500/30';
    if (score >= 4) return 'bg-yellow-500/20 border-yellow-500/30';
    return 'bg-red-500/20 border-red-500/30';
  };

  const getBarColor = (score) => {
    if (score >= 8) return 'bg-green-500';
    if (score >= 6) return 'bg-blue-500';
    if (score >= 4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Compact view for inline display
  if (compact) {
    return (
      <div className="flex items-center gap-3 text-sm">
        <div className="flex items-center gap-1">
          <span className="text-gray-400">Clarity:</span>
          <span className={`font-semibold ${getScoreColor(clarity_score)}`}>
            {clarity_score}/10
          </span>
        </div>
        <div className="w-px h-4 bg-gray-600" />
        <div className="flex items-center gap-1">
          <span className="text-gray-400">Structure:</span>
          <span className={`font-semibold ${getScoreColor(structure_score)}`}>
            {structure_score}/10
          </span>
        </div>
        {filler_count > 0 && (
          <>
            <div className="w-px h-4 bg-gray-600" />
            <span className="text-yellow-400 text-xs">
              {filler_count} filler{filler_count !== 1 ? 's' : ''}
            </span>
          </>
        )}
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-800/50 rounded-xl border border-gray-700/50 p-4 space-y-4"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <h4 className="text-lg font-semibold text-white flex items-center gap-2">
          <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" 
            />
          </svg>
          Communication Analysis
        </h4>
        <span className="text-xs text-gray-400">{word_count} words</span>
      </div>

      {/* Score Bars */}
      <div className="grid gap-3">
        {/* Clarity Score */}
        <div className="space-y-1">
          <div className="flex justify-between text-sm">
            <span className="text-gray-300">Clarity</span>
            <span className={`font-bold ${getScoreColor(clarity_score)}`}>
              {clarity_score}/10
              {grades.clarity && (
                <span className="ml-1 text-xs opacity-70">({grades.clarity.label})</span>
              )}
            </span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${clarity_score * 10}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              className={`h-full ${getBarColor(clarity_score)} rounded-full`}
            />
          </div>
        </div>

        {/* Structure Score */}
        <div className="space-y-1">
          <div className="flex justify-between text-sm">
            <span className="text-gray-300">Structure</span>
            <span className={`font-bold ${getScoreColor(structure_score)}`}>
              {structure_score}/10
              {grades.structure && (
                <span className="ml-1 text-xs opacity-70">({grades.structure.label})</span>
              )}
            </span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${structure_score * 10}%` }}
              transition={{ duration: 0.5, ease: 'easeOut', delay: 0.1 }}
              className={`h-full ${getBarColor(structure_score)} rounded-full`}
            />
          </div>
        </div>

        {/* Confidence Score */}
        <div className="space-y-1">
          <div className="flex justify-between text-sm">
            <span className="text-gray-300">Confidence</span>
            <span className={`font-bold ${getScoreColor(confidence_score)}`}>
              {confidence_score}/10
            </span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${confidence_score * 10}%` }}
              transition={{ duration: 0.5, ease: 'easeOut', delay: 0.2 }}
              className={`h-full ${getBarColor(confidence_score)} rounded-full`}
            />
          </div>
        </div>
      </div>

      {/* Filler Words */}
      {filler_words.length > 0 && (
        <div className="pt-2 border-t border-gray-700/50">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" 
              />
            </svg>
            <span className="text-sm text-yellow-400 font-medium">
              Filler Words Detected ({filler_count})
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {filler_words.map((filler, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-yellow-500/10 border border-yellow-500/20 rounded text-xs text-yellow-300"
              >
                "{filler.word}" × {filler.count}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Issues */}
      {issues.length > 0 && (
        <div className="pt-2 border-t border-gray-700/50">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M6 18L18 6M6 6l12 12" 
              />
            </svg>
            <span className="text-sm text-red-400 font-medium">Issues Found</span>
          </div>
          <ul className="space-y-1">
            {issues.slice(0, 3).map((issue, idx) => (
              <li key={idx} className="text-sm text-gray-400 flex items-start gap-2">
                <span className="text-red-400 mt-0.5">•</span>
                {issue}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="pt-2 border-t border-gray-700/50">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" 
              />
            </svg>
            <span className="text-sm text-blue-400 font-medium">Suggestions</span>
          </div>
          <ul className="space-y-1">
            {suggestions.slice(0, 3).map((suggestion, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-blue-400 mt-0.5">→</span>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Strengths */}
      {strengths.length > 0 && (
        <div className="pt-2 border-t border-gray-700/50">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M5 13l4 4L19 7" 
              />
            </svg>
            <span className="text-sm text-green-400 font-medium">Strengths</span>
          </div>
          <ul className="space-y-1">
            {strengths.map((strength, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-green-400 mt-0.5">✓</span>
                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

/**
 * Compact Score Badge
 * For showing quick score indicator
 */
export const CommunicationBadge = ({ clarity, structure }) => {
  const avgScore = Math.round((clarity + structure) / 2);
  
  const getBadgeStyle = (score) => {
    if (score >= 8) return 'bg-green-500/20 text-green-400 border-green-500/30';
    if (score >= 6) return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    if (score >= 4) return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
    return 'bg-red-500/20 text-red-400 border-red-500/30';
  };

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getBadgeStyle(avgScore)}`}>
      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
          d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" 
        />
      </svg>
      {clarity}/{structure}
    </span>
  );
};

export default CommunicationScore;

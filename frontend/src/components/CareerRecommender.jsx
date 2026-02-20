import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * CareerRecommender Component
 * 
 * Displays AI-powered career path recommendations based on resume analysis.
 * Shows primary recommendation prominently with alternatives and insights.
 */
const CareerRecommender = ({ resumeText, skills = [], onCareerSelect }) => {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState(null);
  const [expandedCareer, setExpandedCareer] = useState(null);

  useEffect(() => {
    if (resumeText && resumeText.length > 50) {
      fetchRecommendations();
    }
  }, [resumeText]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/resume/career-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          resume_text: resumeText,
          skills: skills 
        }),
      });
      
      if (!response.ok) throw new Error('Failed to get recommendations');
      
      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getFitColor = (score) => {
    if (score >= 70) return { bg: 'bg-green-500', text: 'text-green-400', border: 'border-green-500/30' };
    if (score >= 50) return { bg: 'bg-blue-500', text: 'text-blue-400', border: 'border-blue-500/30' };
    if (score >= 30) return { bg: 'bg-yellow-500', text: 'text-yellow-400', border: 'border-yellow-500/30' };
    return { bg: 'bg-gray-500', text: 'text-gray-400', border: 'border-gray-500/30' };
  };

  if (loading) {
    return (
      <div className="bg-gray-800/50 rounded-xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-center gap-3">
          <div className="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-gray-400">Analyzing your career fit...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4">
        <p className="text-red-400 text-center">{error}</p>
        <button 
          onClick={fetchRecommendations}
          className="mt-2 mx-auto block px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!recommendations || !recommendations.primary_recommendation) {
    return null;
  }

  const { primary_recommendation, all_recommendations, insights, summary, career_diversity_score, skill_gaps_for_primary } = recommendations;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
            />
          </svg>
        </div>
        <div>
          <h3 className="text-xl font-bold text-white">AI Career Path Recommender</h3>
          <p className="text-sm text-gray-400">Based on your resume analysis</p>
        </div>
        {career_diversity_score && (
          <span className="ml-auto px-3 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-full">
            {career_diversity_score}
          </span>
        )}
      </div>

      {/* Summary Quote */}
      <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-xl p-4">
        <p className="text-lg text-white italic">"{summary}"</p>
      </div>

      {/* Primary Recommendation - Featured */}
      <motion.div
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
        className={`bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border-2 ${getFitColor(primary_recommendation.fit_score).border} p-6 relative overflow-hidden`}
      >
        {/* Background glow */}
        <div className="absolute top-0 right-0 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl" />
        
        <div className="relative">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-4">
              <span className="text-4xl">{primary_recommendation.icon}</span>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="text-2xl font-bold text-white">{primary_recommendation.title}</h4>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getFitColor(primary_recommendation.fit_score).bg} text-white`}>
                    Best Match
                  </span>
                </div>
                <p className="text-gray-400 mt-1">{primary_recommendation.description}</p>
              </div>
            </div>
            <div className="text-right">
              <div className={`text-4xl font-bold ${getFitColor(primary_recommendation.fit_score).text}`}>
                {primary_recommendation.fit_score}%
              </div>
              <div className="text-sm text-gray-400">{primary_recommendation.fit_level}</div>
            </div>
          </div>

          {/* Fit Score Bar */}
          <div className="h-3 bg-gray-700 rounded-full overflow-hidden mb-4">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${primary_recommendation.fit_score}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
              className={`h-full ${getFitColor(primary_recommendation.fit_score).bg} rounded-full`}
            />
          </div>

          {/* Matching Skills */}
          <div className="mb-4">
            <h5 className="text-sm font-medium text-gray-400 mb-2">Your Matching Skills</h5>
            <div className="flex flex-wrap gap-2">
              {primary_recommendation.matching_skills.map((skill, idx) => (
                <span 
                  key={idx}
                  className="px-3 py-1 bg-green-500/20 text-green-400 text-sm rounded-full border border-green-500/30"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Skill Gaps */}
          {skill_gaps_for_primary && skill_gaps_for_primary.length > 0 && (
            <div className="mb-4">
              <h5 className="text-sm font-medium text-gray-400 mb-2">Skills to Develop</h5>
              <div className="flex flex-wrap gap-2">
                {skill_gaps_for_primary.map((skill, idx) => (
                  <span 
                    key={idx}
                    className="px-3 py-1 bg-yellow-500/10 text-yellow-400 text-sm rounded-full border border-yellow-500/30"
                  >
                    + {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Potential Roles */}
          <div>
            <h5 className="text-sm font-medium text-gray-400 mb-2">Potential Roles</h5>
            <div className="flex flex-wrap gap-2">
              {primary_recommendation.potential_roles.map((role, idx) => (
                <span 
                  key={idx}
                  className="px-3 py-1 bg-blue-500/20 text-blue-400 text-sm rounded-full"
                >
                  {role}
                </span>
              ))}
            </div>
          </div>

          {/* Select Button */}
          {onCareerSelect && (
            <button
              onClick={() => onCareerSelect(primary_recommendation)}
              className="mt-4 w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-300 shadow-lg"
            >
              Prepare for {primary_recommendation.title} →
            </button>
          )}
        </div>
      </motion.div>

      {/* Other Recommendations */}
      {all_recommendations.length > 1 && (
        <div>
          <h4 className="text-lg font-semibold text-white mb-3">Other Career Paths for You</h4>
          <div className="grid gap-3">
            {all_recommendations.slice(1, 4).map((rec, idx) => {
              const colors = getFitColor(rec.fit_score);
              const isExpanded = expandedCareer === rec.career_id;
              
              return (
                <motion.div
                  key={rec.career_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`bg-gray-800/60 rounded-xl border ${colors.border} overflow-hidden`}
                >
                  <button
                    onClick={() => setExpandedCareer(isExpanded ? null : rec.career_id)}
                    className="w-full p-4 text-left flex items-center gap-4 hover:bg-gray-700/30 transition"
                  >
                    <span className="text-2xl">{rec.icon}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h5 className="font-semibold text-white">{rec.title}</h5>
                        <span className={`text-xs ${colors.text}`}>{rec.fit_level}</span>
                      </div>
                      <p className="text-sm text-gray-400 truncate">{rec.description}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className={`text-xl font-bold ${colors.text}`}>{rec.fit_score}%</div>
                      <svg 
                        className={`w-5 h-5 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                        fill="none" stroke="currentColor" viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </button>
                  
                  <AnimatePresence>
                    {isExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="border-t border-gray-700/50 overflow-hidden"
                      >
                        <div className="p-4 space-y-3">
                          {/* Matching Skills */}
                          <div>
                            <h6 className="text-xs font-medium text-gray-400 mb-1">Matching Skills</h6>
                            <div className="flex flex-wrap gap-1">
                              {rec.matching_skills.slice(0, 6).map((skill, sidx) => (
                                <span key={sidx} className="px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                          
                          {/* Roles */}
                          <div>
                            <h6 className="text-xs font-medium text-gray-400 mb-1">Roles</h6>
                            <p className="text-sm text-gray-300">{rec.potential_roles.join(' • ')}</p>
                          </div>
                          
                          {onCareerSelect && (
                            <button
                              onClick={() => onCareerSelect(rec)}
                              className={`w-full py-2 ${colors.bg}/20 ${colors.text} text-sm font-medium rounded-lg hover:${colors.bg}/30 transition`}
                            >
                              Explore {rec.title} →
                            </button>
                          )}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              );
            })}
          </div>
        </div>
      )}

      {/* Insights */}
      {insights && insights.length > 0 && (
        <div className="bg-gray-800/40 rounded-xl border border-gray-700/50 p-4">
          <h4 className="text-sm font-semibold text-purple-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" 
              />
            </svg>
            AI Insights
          </h4>
          <ul className="space-y-2">
            {insights.map((insight, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                <span className="text-purple-400 mt-0.5">→</span>
                {insight}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

export default CareerRecommender;

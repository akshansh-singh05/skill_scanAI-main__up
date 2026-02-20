import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  Legend
} from 'recharts'
import { getReport } from '../services'
import { PageTransition, GlassCard, WeaknessHeatmap } from '../components'
import { staggerContainer, fadeInUp } from '../utils/animations'

const Report = () => {
  const [reportData, setReportData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadReport()
  }, [])

  const loadReport = async () => {
    try {
      // Get data from localStorage
      const resumeDataStr = localStorage.getItem('resumeData')
      const interviewResultStr = localStorage.getItem('interviewResult')
      
      const resumeData = resumeDataStr ? JSON.parse(resumeDataStr) : {}
      const interviewResult = interviewResultStr ? JSON.parse(interviewResultStr) : {}
      
      // Get scores from stored data (handle both snake_case and camelCase)
      const resumeScore = resumeData.ats_score || resumeData.atsScore || 70
      const technicalScore = interviewResult.technical_score || interviewResult.technicalScore || 75
      const hrScore = interviewResult.hr_score || interviewResult.hrScore || 72
      
      // Try to get full report from API
      const response = await getReport({
        resume_score: resumeScore,
        technical_score: technicalScore,
        hr_score: hrScore,
        role: resumeData.role || 'SDE'
      })
      
      // Map API response to expected format
      setReportData({
        resumeScore: response.scores?.resume_score || resumeScore,
        technicalScore: response.scores?.technical_score || technicalScore,
        hrScore: response.scores?.hr_score || hrScore,
        overallReadiness: response.overall_readiness,
        readinessLevel: response.readiness_level,
        skills: {
          problemSolving: 85,
          communication: 78,
          technicalKnowledge: technicalScore,
          leadership: 70,
          adaptability: 88,
          teamwork: 75,
        },
        improvements: response.action_items?.map((item, index) => ({
          id: index + 1,
          text: item.action,
          timeframe: item.timeframe,
          completed: false
        })) || [
          { id: 1, text: 'Add more quantifiable achievements to your resume', completed: false },
          { id: 2, text: 'Practice explaining complex technical concepts simply', completed: false },
          { id: 3, text: 'Prepare more STAR-method stories for behavioral questions', completed: false },
        ],
        summary: response.summary,
        strengths: response.strengths,
        weaknesses: response.weaknesses
      })
    } catch {
      // Fallback to localStorage data only
      const resumeData = localStorage.getItem('resumeData')
      const interviewResult = localStorage.getItem('interviewResult')
      
      const parsedResume = resumeData ? JSON.parse(resumeData) : {}
      const parsedInterview = interviewResult ? JSON.parse(interviewResult) : {}
      
      if (resumeData || interviewResult) {
        setReportData({
          resumeScore: parsedResume.ats_score || parsedResume.atsScore || 75,
          technicalScore: parsedInterview.technical_score || parsedInterview.technicalScore || 78,
          hrScore: parsedInterview.hr_score || parsedInterview.hrScore || 82,
          skills: {
            problemSolving: 85,
            communication: 78,
            technicalKnowledge: 82,
            leadership: 70,
            adaptability: 88,
            teamwork: 75,
          },
          improvements: [
            { id: 1, text: 'Add more quantifiable achievements to your resume', completed: false },
            { id: 2, text: 'Practice explaining complex technical concepts simply', completed: false },
            { id: 3, text: 'Prepare more STAR-method stories for behavioral questions', completed: false },
            { id: 4, text: 'Research company-specific interview patterns', completed: false },
            { id: 5, text: 'Work on system design fundamentals', completed: false },
          ],
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return { text: 'text-green-400', bg: 'bg-green-500', gradient: 'from-green-500 to-emerald-600' }
    if (score >= 60) return { text: 'text-yellow-400', bg: 'bg-yellow-500', gradient: 'from-yellow-500 to-orange-500' }
    return { text: 'text-red-400', bg: 'bg-red-500', gradient: 'from-red-500 to-rose-600' }
  }

  const calculateOverallReadiness = () => {
    if (!reportData) return 0
    const { resumeScore, technicalScore, hrScore } = reportData
    return Math.round((resumeScore + technicalScore + hrScore) / 3)
  }

  const getRadarData = () => {
    if (!reportData?.skills) return []
    return [
      { skill: 'Problem Solving', value: reportData.skills.problemSolving, fullMark: 100 },
      { skill: 'Communication', value: reportData.skills.communication, fullMark: 100 },
      { skill: 'Technical', value: reportData.skills.technicalKnowledge, fullMark: 100 },
      { skill: 'Leadership', value: reportData.skills.leadership, fullMark: 100 },
      { skill: 'Adaptability', value: reportData.skills.adaptability, fullMark: 100 },
      { skill: 'Teamwork', value: reportData.skills.teamwork, fullMark: 100 },
    ]
  }

  const [improvements, setImprovements] = useState([])

  useEffect(() => {
    if (reportData?.improvements) {
      setImprovements(reportData.improvements)
    }
  }, [reportData])

  const toggleImprovement = (id) => {
    setImprovements(prev => 
      prev.map(item => 
        item.id === id ? { ...item, completed: !item.completed } : item
      )
    )
  }

  const ScoreCard = ({ title, score, icon, description }) => {
    const colors = getScoreColor(score)
    return (
      <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-slate-600 transition-colors">
        <div className="flex items-start justify-between mb-4">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colors.gradient} flex items-center justify-center shadow-lg`}>
            {icon}
          </div>
          <span className={`text-3xl font-bold ${colors.text}`}>{score}%</span>
        </div>
        <h3 className="text-white font-semibold mb-1">{title}</h3>
        <p className="text-slate-400 text-sm">{description}</p>
        <div className="mt-4 h-2 bg-slate-700 rounded-full overflow-hidden">
          <div 
            className={`h-full bg-gradient-to-r ${colors.gradient} transition-all duration-1000`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-12 flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <svg className="w-12 h-12 animate-spin text-blue-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <p className="text-slate-400">Loading your report...</p>
        </div>
      </div>
    )
  }

  if (!reportData) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4">Interview Report</h1>
            <p className="text-slate-400">View your performance analysis and feedback</p>
          </div>

          <div className="bg-slate-800 rounded-xl p-8 border border-slate-700">
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold text-white mb-2">No Report Available</h2>
              <p className="text-slate-400 mb-6">Complete an interview first to generate your performance report.</p>
              <Link to="/interview" className="inline-block bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
                Start Interview
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const overallReadiness = calculateOverallReadiness()
  const readinessColors = getScoreColor(overallReadiness)

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Print Header - Only visible when printing */}
          <div className="hidden print:block print-header" style={{ marginBottom: '20px', paddingBottom: '15px', borderBottom: '3px solid #2563eb', textAlign: 'center' }}>
            <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b', marginBottom: '8px' }}>SkillScan AI - Interview Performance Report</h1>
            <p style={{ fontSize: '12px', color: '#64748b' }}>
              Generated on: {new Date().toLocaleDateString('en-IN', { 
                day: 'numeric', 
                month: 'long', 
                year: 'numeric'
              })} at {new Date().toLocaleTimeString('en-IN', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </p>
            <div style={{ marginTop: '10px', display: 'flex', justifyContent: 'center', gap: '30px', fontSize: '11px', color: '#475569' }}>
              <span>Resume Score: {reportData.resumeScore}%</span>
              <span>Technical Score: {reportData.technicalScore}%</span>
              <span>HR Score: {reportData.hrScore}%</span>
              <span style={{ fontWeight: 'bold', color: '#2563eb' }}>Overall: {calculateOverallReadiness()}%</span>
            </div>
          </div>

          {/* Header */}
          <motion.div 
            className="text-center mb-10"
            variants={staggerContainer}
            initial="hidden"
            animate="visible"
          >
            <motion.h1 
              variants={fadeInUp}
              className="text-4xl font-bold text-white mb-3"
            >
              Your Interview Report
            </motion.h1>
            <motion.p 
              variants={fadeInUp}
              className="text-slate-400"
            >
              Comprehensive analysis of your interview performance
            </motion.p>
          </motion.div>

          {/* Overall Readiness */}
          <GlassCard className="p-8 mb-8 print-section" delay={0.1}>
            <div className="flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="text-center md:text-left">
                <h2 className="text-xl text-slate-400 mb-2">Overall Interview Readiness</h2>
                <div className="flex items-baseline gap-2">
                  <motion.span 
                    className={`text-6xl font-bold ${readinessColors.text}`}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', stiffness: 200, delay: 0.3 }}
                  >
                    {overallReadiness}%
                  </motion.span>
                  <span className="text-slate-400 text-lg">ready</span>
                </div>
                <p className="text-slate-400 mt-3 max-w-md">
                  {overallReadiness >= 80 
                    ? "Excellent! You're well-prepared for your interviews."
                    : overallReadiness >= 60 
                    ? "Good progress! A few more improvements will boost your confidence."
                    : "Keep practicing! Focus on the improvement areas below."}
                </p>
              </div>
              
              {/* Circular Progress */}
              <motion.div 
                className="relative w-48 h-48"
                initial={{ opacity: 0, rotate: -90 }}
                animate={{ opacity: 1, rotate: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <svg className="w-48 h-48 transform -rotate-90">
                  <circle
                    cx="96"
                    cy="96"
                    r="88"
                    stroke="currentColor"
                    strokeWidth="12"
                    fill="none"
                    className="text-slate-700"
                  />
                  <motion.circle
                    cx="96"
                    cy="96"
                    r="88"
                    stroke="url(#gradient)"
                    strokeWidth="12"
                    fill="none"
                    strokeLinecap="round"
                    initial={{ strokeDasharray: '0 553' }}
                    animate={{ strokeDasharray: `${overallReadiness * 5.53} 553` }}
                    transition={{ duration: 1.5, delay: 0.5, ease: 'easeOut' }}
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#3b82f6" />
                      <stop offset="100%" stopColor="#8b5cf6" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-4xl font-bold text-white">{overallReadiness}%</span>
                  <span className="text-slate-400 text-sm">Readiness</span>
                </div>
              </motion.div>
            </div>
          </GlassCard>

          {/* Score Cards */}
          <motion.div 
            className="grid md:grid-cols-3 gap-6 mb-8 print-section"
            variants={staggerContainer}
            initial="hidden"
            animate="visible"
          >
            <motion.div variants={fadeInUp}>
              <ScoreCard 
                title="ATS Score"
                score={reportData.resumeScore}
                description="ATS compatibility and content quality"
                icon={<svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>}
              />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <ScoreCard 
                title="Technical Score"
                score={reportData.technicalScore}
                description="Coding and problem-solving abilities"
                icon={<svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>}
              />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <ScoreCard 
                title="HR Score"
                score={reportData.hrScore}
                description="Communication and behavioral skills"
                icon={<svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>}
              />
            </motion.div>
          </motion.div>

          {/* Charts and Improvements */}
          <div className="grid lg:grid-cols-2 gap-8 print-section">
            {/* Skill Radar Chart */}
            <GlassCard className="p-6" delay={0.4}>
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
                Skill Radar
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={getRadarData()}>
                    <PolarGrid stroke="#475569" />
                    <PolarAngleAxis 
                      dataKey="skill" 
                      tick={{ fill: '#94a3b8', fontSize: 12 }}
                    />
                    <PolarRadiusAxis 
                      angle={30} 
                      domain={[0, 100]} 
                      tick={{ fill: '#64748b', fontSize: 10 }}
                    />
                    <Radar
                      name="Your Skills"
                      dataKey="value"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                    <Legend 
                      wrapperStyle={{ color: '#94a3b8' }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </GlassCard>

            {/* Improvement Checklist */}
            <GlassCard className="p-6" delay={0.5}>
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <svg className="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                Improvement Checklist
              </h3>
              <div className="space-y-3">
                {improvements.map((item, index) => (
                  <motion.div 
                    key={item.id}
                    onClick={() => toggleImprovement(item.id)}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    whileHover={{ x: 5 }}
                    className={`
                      flex items-start gap-3 p-4 rounded-xl cursor-pointer transition-all duration-200
                      ${item.completed 
                        ? 'bg-green-500/10 border border-green-500/30 backdrop-blur-sm' 
                        : 'bg-white/5 border border-white/10 hover:border-white/20 backdrop-blur-sm'
                      }
                    `}
                  >
                    <motion.div 
                      className={`
                        w-6 h-6 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors
                        ${item.completed 
                          ? 'bg-green-500 text-white' 
                          : 'bg-slate-700 border border-slate-600'
                        }
                      `}
                      whileTap={{ scale: 0.9 }}
                    >
                      {item.completed && (
                        <motion.svg 
                          className="w-4 h-4" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ type: 'spring', stiffness: 300 }}
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </motion.svg>
                      )}
                    </motion.div>
                    <span className={`text-sm ${item.completed ? 'text-green-400 line-through' : 'text-slate-300'}`}>
                      {item.text}
                    </span>
                  </motion.div>
              ))}
              </div>
              <div className="mt-6 pt-4 border-t border-white/10">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 text-sm">Progress</span>
                  <span className="text-white font-medium">
                    {improvements.filter(i => i.completed).length}/{improvements.length} completed
                  </span>
                </div>
                <div className="mt-2 h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${(improvements.filter(i => i.completed).length / improvements.length) * 100}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
            </GlassCard>
          </div>

          {/* Weakness Heatmap */}
          <motion.div 
            className="mt-8 print-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <WeaknessHeatmap 
              skills={[
                { name: 'DSA & Algorithms', score: Math.round(reportData.skills.problemSolving * 0.8) },
                { name: 'Backend Development', score: reportData.technicalScore || 75 },
                { name: 'System Design', score: Math.round(reportData.skills.technicalKnowledge * 0.5) },
                { name: 'Communication', score: reportData.skills.communication },
                { name: 'Leadership', score: reportData.skills.leadership },
                { name: 'Problem Solving', score: reportData.skills.problemSolving },
              ]}
              title="Interview Readiness Heatmap"
            />
          </motion.div>

          {/* Actions */}
          <motion.div 
            className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4 no-print print:hidden"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Link 
                to="/interview"
                className="block w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold transition-all text-center shadow-lg shadow-blue-500/25"
              >
                Retake Interview
              </Link>
            </motion.div>
            <button 
              type="button"
              onClick={() => { window.print(); }}
              className="w-full sm:w-auto px-8 py-3 rounded-xl border border-white/20 hover:border-white/40 hover:bg-white/5 backdrop-blur-sm text-white font-semibold transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print Report
            </button>
          </motion.div>
        </div>
      </div>
    </PageTransition>
  )
}

export default Report

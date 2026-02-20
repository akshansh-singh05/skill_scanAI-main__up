import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { InterviewChat, HRInterview, PageTransition, CompanySelector, CareerRecommender, GlassCard } from '../components'

const Interview = () => {
  const [resumeData, setResumeData] = useState(null)
  const [selectedCompany, setSelectedCompany] = useState(null)
  const [currentRound, setCurrentRound] = useState('company-select') // 'company-select', 'technical', or 'hr'
  const [technicalScore, setTechnicalScore] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Get resume data from localStorage
    const storedData = localStorage.getItem('resumeData')
    if (storedData) {
      setResumeData(JSON.parse(storedData))
    }
  }, [])

  const handleCompanySelect = (company) => {
    setSelectedCompany(company)
  }

  const startInterview = () => {
    if (selectedCompany) {
      setCurrentRound('technical')
    }
  }

  const handleTechnicalComplete = (result) => {
    // Store technical score and move to HR round
    setTechnicalScore(result.technical_score)
    setCurrentRound('hr')
  }

  const handleHRComplete = (result) => {
    // Calculate HR score from answers
    const hrAnswers = result.answers || []
    let hrScore = 75 // default
    
    if (hrAnswers.length > 0) {
      const totalScore = hrAnswers.reduce((acc, ans) => {
        const avgScore = (ans.scores.clarity + ans.scores.confidence + ans.scores.structure) / 3
        return acc + avgScore
      }, 0)
      hrScore = Math.round(totalScore / hrAnswers.length)
    }

    // Store both scores and navigate to report
    const interviewResult = {
      technical_score: technicalScore,
      hr_score: hrScore,
      hr_answers: hrAnswers
    }
    localStorage.setItem('interviewResult', JSON.stringify(interviewResult))
    navigate('/report')
  }

  const getRoundInfo = () => {
    if (currentRound === 'company-select') {
      return {
        title: 'Select Interview Mode',
        subtitle: 'Choose a company to practice their specific interview style',
        icon: (
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        ),
        gradient: 'from-indigo-500 to-purple-600',
        shadowColor: 'shadow-indigo-500/25'
      }
    } else if (currentRound === 'technical') {
      return {
        title: `Technical Interview ${selectedCompany ? `- ${selectedCompany.name}` : ''}`,
        subtitle: selectedCompany?.description || 'Answer technical questions based on your skills',
        icon: (
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        ),
        gradient: 'from-blue-500 to-purple-600',
        shadowColor: 'shadow-purple-500/25'
      }
    } else {
      return {
        title: 'HR Interview Round',
        subtitle: 'Answer behavioral and situational questions',
        icon: (
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        ),
        gradient: 'from-green-500 to-emerald-600',
        shadowColor: 'shadow-green-500/25'
      }
    }
  }

  const roundInfo = getRoundInfo()

  // Company Selection Screen
  if (currentRound === 'company-select') {
    return (
      <PageTransition>
        <div className="min-h-[calc(100vh-140px)] flex flex-col">
          <div className="container mx-auto px-4 py-8 flex-1">
            <div className="max-w-5xl mx-auto space-y-6">
              {/* Career Recommender - Show based on resume */}
              {resumeData?.resume_text && (
                <GlassCard className="p-6">
                  <CareerRecommender 
                    resumeText={resumeData.resume_text}
                    skills={resumeData.matched_skills || []}
                  />
                </GlassCard>
              )}
              
              <GlassCard className="p-8">
                <CompanySelector 
                  onSelect={handleCompanySelect}
                  selectedCompany={selectedCompany?.id}
                />
                
                {/* Start Interview Button */}
                <div className="mt-8 pt-6 border-t border-slate-700">
                  <button
                    onClick={startInterview}
                    disabled={!selectedCompany}
                    className={`
                      w-full py-4 px-6 rounded-xl font-semibold text-white
                      transition-all duration-200 flex items-center justify-center gap-3
                      ${selectedCompany
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 hover:shadow-lg hover:shadow-purple-500/25'
                        : 'bg-slate-700 cursor-not-allowed text-slate-400'
                      }
                    `}
                  >
                    {selectedCompany ? (
                      <>
                        <span className="text-xl">{selectedCompany.logo}</span>
                        <span>Start {selectedCompany.name} Interview</span>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                      </>
                    ) : (
                      <span>Select a Company to Continue</span>
                    )}
                  </button>
                </div>
              </GlassCard>
            </div>
          </div>
        </div>
      </PageTransition>
    )
  }

  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-140px)] flex flex-col overflow-hidden">
        {/* Header */}
        <motion.div 
          className="bg-white/5 backdrop-blur-xl border-b border-white/10 px-6 py-4 flex-shrink-0"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <div className="container mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <motion.div 
                  className={`w-10 h-10 bg-gradient-to-br ${roundInfo.gradient} rounded-xl flex items-center justify-center shadow-lg ${roundInfo.shadowColor}`}
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 300 }}
                  key={currentRound}
                >
                  {roundInfo.icon}
                </motion.div>
                {roundInfo.title}
              </h1>
              <p className="text-slate-400 text-sm mt-1 ml-13">{roundInfo.subtitle}</p>
            </div>
            <motion.div 
              className="flex items-center gap-3"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              {/* Round indicators */}
              <div className="flex items-center gap-2 mr-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                  currentRound === 'technical' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-green-600 text-white'
                }`}>
                  1
                </div>
                <div className={`w-12 h-1 rounded ${
                  currentRound === 'hr' ? 'bg-green-500' : 'bg-slate-600'
                }`} />
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                  currentRound === 'hr' 
                    ? 'bg-green-600 text-white' 
                    : 'bg-slate-600 text-slate-400'
                }`}>
                  2
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium backdrop-blur-sm border ${
                currentRound === 'technical'
                  ? 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                  : 'bg-green-500/20 text-green-400 border-green-500/30'
              }`}>
                {currentRound === 'technical' ? 'Round 1: Technical' : 'Round 2: HR'}
              </span>
            </motion.div>
          </div>
        </motion.div>

        {/* Chat Area */}
        <motion.div 
          className="flex-1 bg-slate-900/30 backdrop-blur-sm overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          key={currentRound}
        >
          <div className="container mx-auto h-full max-w-4xl">
            <div className="bg-white/5 backdrop-blur-xl h-full border-x border-white/10 overflow-hidden">
              {currentRound === 'technical' ? (
                <InterviewChat 
                  resumeData={resumeData} 
                  company={selectedCompany}
                  onComplete={handleTechnicalComplete} 
                />
              ) : (
                <HRInterview 
                  resumeData={resumeData}
                  company={selectedCompany}
                  onComplete={handleHRComplete} 
                />
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  )
}

export default Interview

import { useState, useRef, useEffect } from 'react'
import { submitHRAnswer } from '../services'
import ProctorCamera from './ProctorCamera'

const HR_QUESTIONS = [
  "Tell me about yourself and your career journey.",
  "Describe a challenging situation at work and how you handled it.",
  "Where do you see yourself in 5 years?",
  "Why are you interested in this role?",
  "Tell me about a time you had to work with a difficult team member.",
]

const HRInterview = ({ resumeData, onComplete }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [userInput, setUserInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [answers, setAnswers] = useState([])
  const [showResults, setShowResults] = useState(false)
  const [proctorViolations, setProctorViolations] = useState([])
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [currentQuestionIndex])

  // Handle proctor violations
  const handleProctorViolation = (violation) => {
    setProctorViolations(prev => [...prev, violation])
    console.log('HR Round proctor violation:', violation)
  }

  const currentQuestion = HR_QUESTIONS[currentQuestionIndex]
  const progress = ((currentQuestionIndex) / HR_QUESTIONS.length) * 100

  const getScoreColor = (score) => {
    if (score >= 80) return { text: 'text-green-400', bg: 'bg-green-500', light: 'bg-green-500/20' }
    if (score >= 60) return { text: 'text-yellow-400', bg: 'bg-yellow-500', light: 'bg-yellow-500/20' }
    return { text: 'text-red-400', bg: 'bg-red-500', light: 'bg-red-500/20' }
  }

  const handleSubmitAnswer = async (e) => {
    e.preventDefault()
    if (!userInput.trim() || isLoading) return

    const answer = userInput.trim()
    setIsLoading(true)

    try {
      const response = await submitHRAnswer({
        question: currentQuestion,
        answer,
        questionNumber: currentQuestionIndex + 1,
      })

      const newAnswer = {
        question: currentQuestion,
        answer,
        scores: {
          clarity: response.clarity || Math.floor(Math.random() * 30) + 70,
          confidence: response.confidence || Math.floor(Math.random() * 30) + 70,
          structure: response.structure || Math.floor(Math.random() * 30) + 70,
        },
        feedback: response.feedback || 'Good response with clear communication.',
      }

      setAnswers((prev) => [...prev, newAnswer])
      setUserInput('')

      if (currentQuestionIndex < HR_QUESTIONS.length - 1) {
        setCurrentQuestionIndex((prev) => prev + 1)
      } else {
        setShowResults(true)
        // Don't call onComplete immediately - let user see results first
      }
    } catch (error) {
      console.error('Error submitting HR answer:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const calculateOverallScores = () => {
    if (answers.length === 0) return { clarity: 0, confidence: 0, structure: 0, overall: 0 }
    
    const totals = answers.reduce(
      (acc, ans) => ({
        clarity: acc.clarity + ans.scores.clarity,
        confidence: acc.confidence + ans.scores.confidence,
        structure: acc.structure + ans.scores.structure,
      }),
      { clarity: 0, confidence: 0, structure: 0 }
    )

    const count = answers.length
    const clarity = Math.round(totals.clarity / count)
    const confidence = Math.round(totals.confidence / count)
    const structure = Math.round(totals.structure / count)
    const overall = Math.round((clarity + confidence + structure) / 3)

    return { clarity, confidence, structure, overall }
  }

  const ScoreCard = ({ label, score, icon }) => {
    const colors = getScoreColor(score)
    return (
      <div className={`p-4 rounded-xl ${colors.light} border border-slate-700`}>
        <div className="flex items-center gap-3 mb-3">
          <div className={`w-10 h-10 rounded-lg ${colors.bg} flex items-center justify-center`}>
            {icon}
          </div>
          <span className="text-white font-medium">{label}</span>
        </div>
        <div className="flex items-end gap-2">
          <span className={`text-3xl font-bold ${colors.text}`}>{score}</span>
          <span className="text-slate-400 text-sm mb-1">/100</span>
        </div>
        <div className="mt-2 h-2 bg-slate-700 rounded-full overflow-hidden">
          <div 
            className={`h-full ${colors.bg} transition-all duration-700`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
    )
  }

  if (showResults) {
    const scores = calculateOverallScores()
    
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-green-500/25">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">HR Round Complete!</h2>
          <p className="text-slate-400">Here's your performance summary</p>
        </div>

        {/* Overall Score */}
        <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">Overall Performance</h3>
          <div className="flex items-center justify-center gap-6">
            <div className={`text-6xl font-bold ${getScoreColor(scores.overall).text}`}>
              {scores.overall}%
            </div>
            <div className="text-left">
              <p className="text-white font-medium">
                {scores.overall >= 80 ? 'Excellent!' : scores.overall >= 60 ? 'Good Job!' : 'Keep Practicing'}
              </p>
              <p className="text-slate-400 text-sm">
                Based on {answers.length} questions answered
              </p>
            </div>
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <ScoreCard 
            label="Clarity" 
            score={scores.clarity}
            icon={<svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>}
          />
          <ScoreCard 
            label="Confidence" 
            score={scores.confidence}
            icon={<svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>}
          />
          <ScoreCard 
            label="Structure" 
            score={scores.structure}
            icon={<svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>}
          />
        </div>

        {/* Answer Feedback */}
        <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Question-wise Feedback</h3>
          <div className="space-y-4">
            {answers.map((ans, index) => (
              <div key={index} className="p-4 bg-slate-900/50 rounded-xl border border-slate-700">
                <div className="flex items-start justify-between mb-2">
                  <p className="text-blue-400 font-medium text-sm">Q{index + 1}: {ans.question}</p>
                  <div className="flex gap-2">
                    <span className={`px-2 py-0.5 rounded text-xs ${getScoreColor(ans.scores.clarity).light} ${getScoreColor(ans.scores.clarity).text}`}>
                      C: {ans.scores.clarity}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs ${getScoreColor(ans.scores.confidence).light} ${getScoreColor(ans.scores.confidence).text}`}>
                      Cf: {ans.scores.confidence}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs ${getScoreColor(ans.scores.structure).light} ${getScoreColor(ans.scores.structure).text}`}>
                      S: {ans.scores.structure}
                    </span>
                  </div>
                </div>
                <p className="text-slate-400 text-sm">{ans.feedback}</p>
              </div>
            ))}
          </div>
        </div>

        {/* View Report Button */}
        <div className="mt-6 text-center">
          <button
            onClick={() => onComplete?.({ answers })}
            className="px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-300 shadow-lg"
          >
            View Report →
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-full">
      {/* Proctor Camera Sidebar */}
      <div className="w-80 flex-shrink-0 p-4 border-r border-slate-700 bg-slate-900/50">
        <div className="sticky top-4">
          <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
            Proctoring Active
          </h3>
          <ProctorCamera 
            isActive={!showResults}
            onViolation={handleProctorViolation}
            showWarnings={true}
          />
          {proctorViolations.length > 0 && (
            <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
              <p className="text-red-400 text-sm font-medium">⚠️ {proctorViolations.length} violation(s) recorded</p>
              <p className="text-slate-400 text-xs mt-1">Stay focused on the screen to maintain a good proctoring score.</p>
            </div>
          )}
        </div>
      </div>

      {/* Main HR Interview Area */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-3xl mx-auto">
          {/* Progress */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Question {currentQuestionIndex + 1} of {HR_QUESTIONS.length}</span>
              <span className="text-sm text-slate-400">{Math.round(progress)}% Complete</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Question Card */}
      <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700 mb-6">
        <div className="flex items-start gap-4 mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <p className="text-purple-400 text-sm font-medium mb-1">HR Question</p>
            <h2 className="text-xl text-white font-semibold">{currentQuestion}</h2>
          </div>
        </div>

        <form onSubmit={handleSubmitAnswer}>
          <textarea
            ref={inputRef}
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your answer here... Be specific and use examples from your experience."
            className="w-full px-4 py-4 rounded-xl bg-slate-900 border border-slate-600 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
            rows={6}
            disabled={isLoading}
          />
          
          <div className="flex items-center justify-between mt-4">
            <p className="text-slate-500 text-sm">
              {userInput.length} characters
            </p>
            <button
              type="submit"
              disabled={!userInput.trim() || isLoading}
              className={`
                px-8 py-3 rounded-xl font-semibold text-white transition-all duration-200
                flex items-center gap-2
                ${!userInput.trim() || isLoading
                  ? 'bg-slate-700 cursor-not-allowed text-slate-400'
                  : 'bg-gradient-to-r from-purple-500 to-pink-600 hover:shadow-lg hover:shadow-purple-500/25'
                }
              `}
            >
              {isLoading ? (
                <>
                  <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Evaluating...
                </>
              ) : (
                <>
                  Submit Answer
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Tips */}
      <div className="bg-purple-500/10 rounded-xl p-4 border border-purple-500/20">
        <div className="flex items-start gap-3">
          <svg className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <p className="text-purple-300 font-medium text-sm mb-1">Pro Tip</p>
            <p className="text-slate-400 text-sm">
              Use the STAR method (Situation, Task, Action, Result) to structure your behavioral answers effectively.
            </p>
          </div>
        </div>
      </div>

      {/* Previous Answers Summary */}
      {answers.length > 0 && (
        <div className="mt-6">
          <h3 className="text-white font-medium mb-3">Previous Answers</h3>
          <div className="space-y-2">
            {answers.map((ans, index) => {
              const avgScore = Math.round((ans.scores.clarity + ans.scores.confidence + ans.scores.structure) / 3)
              const colors = getScoreColor(avgScore)
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700">
                  <span className="text-slate-400 text-sm truncate flex-1 mr-4">Q{index + 1}: {ans.question}</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${colors.light} ${colors.text}`}>
                    {avgScore}%
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      )}
        </div>
      </div>
    </div>
  )
}

export default HRInterview

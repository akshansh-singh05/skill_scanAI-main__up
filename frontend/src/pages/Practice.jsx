import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PageTransition } from '../components'
import api from '../services/api'

const Practice = () => {
  // Active Tab State
  const [activeTab, setActiveTab] = useState('coding') // coding, aptitude, situational, cases
  
  // Coding Problems State
  const [questions, setQuestions] = useState([])
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [code, setCode] = useState('')
  const [hints, setHints] = useState([])
  const [hintsRevealed, setHintsRevealed] = useState(0)
  const [solution, setSolution] = useState(null)
  const [submitResult, setSubmitResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [filter, setFilter] = useState('all')
  const [showSolution, setShowSolution] = useState(false)

  // Aptitude State
  const [aptitudeQuestions, setAptitudeQuestions] = useState([])
  const [selectedAptitude, setSelectedAptitude] = useState(null)
  const [aptitudeAnswer, setAptitudeAnswer] = useState(null)
  const [aptitudeResult, setAptitudeResult] = useState(null)
  const [aptitudeFilter, setAptitudeFilter] = useState('all')

  // Situational State
  const [situationalQuestions, setSituationalQuestions] = useState([])
  const [selectedSituational, setSelectedSituational] = useState(null)
  const [situationalAnswer, setSituationalAnswer] = useState(null)
  const [situationalResult, setSituationalResult] = useState(null)

  // Case Studies State
  const [caseStudies, setCaseStudies] = useState([])
  const [selectedCase, setSelectedCase] = useState(null)

  useEffect(() => {
    fetchQuestions()
    fetchAptitudeQuestions()
    fetchSituationalQuestions()
    fetchCaseStudies()
  }, [])

  const fetchQuestions = async () => {
    try {
      const response = await api.get('/practice/questions')
      setQuestions(response.questions || response.data?.questions || [])
    } catch (error) {
      console.error('Error fetching questions:', error)
    }
  }

  const fetchAptitudeQuestions = async () => {
    try {
      const response = await api.get('/aptitude/questions')
      setAptitudeQuestions(response.questions || [])
    } catch (error) {
      console.error('Error fetching aptitude questions:', error)
    }
  }

  const fetchSituationalQuestions = async () => {
    try {
      const response = await api.get('/aptitude/situational')
      setSituationalQuestions(response.questions || [])
    } catch (error) {
      console.error('Error fetching situational questions:', error)
    }
  }

  const fetchCaseStudies = async () => {
    try {
      const response = await api.get('/aptitude/case-studies')
      setCaseStudies(response.case_studies || [])
    } catch (error) {
      console.error('Error fetching case studies:', error)
    }
  }

  const selectQuestion = async (questionId) => {
    try {
      setIsLoading(true)
      const response = await api.get(`/practice/questions/${questionId}`)
      setSelectedQuestion(response)
      setCode(response.starter_code)
      setHints([])
      setHintsRevealed(0)
      setSolution(null)
      setSubmitResult(null)
      setShowSolution(false)
    } catch (error) {
      console.error('Error fetching question:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const revealHint = async () => {
    if (hintsRevealed >= selectedQuestion.hints_count) return
    
    try {
      const response = await api.get(`/practice/questions/${selectedQuestion.id}/hint/${hintsRevealed}`)
      setHints(prev => [...prev, response.hint])
      setHintsRevealed(prev => prev + 1)
    } catch (error) {
      console.error('Error fetching hint:', error)
    }
  }

  const viewSolution = async () => {
    try {
      const response = await api.get(`/practice/questions/${selectedQuestion.id}/solution`)
      setSolution(response)
      setShowSolution(true)
    } catch (error) {
      console.error('Error fetching solution:', error)
    }
  }

  const submitCode = async () => {
    setIsLoading(true)
    setSubmitResult(null)
    
    try {
      const response = await api.post('/practice/submit', {
        question_id: selectedQuestion.id,
        code: code
      })
      setSubmitResult(response)
    } catch (error) {
      console.error('Error submitting code:', error)
      setSubmitResult({
        status: 'error',
        message: 'Failed to submit code. Please try again.'
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return 'text-green-400 bg-green-500/20 border-green-500/30'
      case 'medium': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30'
      case 'hard': return 'text-red-400 bg-red-500/20 border-red-500/30'
      default: return 'text-slate-400 bg-slate-500/20 border-slate-500/30'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'accepted': return 'text-green-400 bg-green-500/20 border-green-500'
      case 'partial': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500'
      case 'wrong': return 'text-red-400 bg-red-500/20 border-red-500'
      default: return 'text-slate-400 bg-slate-500/20 border-slate-500'
    }
  }

  const filteredQuestions = questions.filter(q => 
    filter === 'all' || q.difficulty.toLowerCase() === filter
  )

  const filteredAptitude = aptitudeQuestions.filter(q =>
    aptitudeFilter === 'all' || q.category.toLowerCase().includes(aptitudeFilter)
  )

  const selectAptitudeQuestion = (question) => {
    setSelectedAptitude(question)
    setAptitudeAnswer(null)
    setAptitudeResult(null)
  }

  const submitAptitudeAnswer = async () => {
    if (!aptitudeAnswer || !selectedAptitude) return
    try {
      setIsLoading(true)
      const response = await api.post('/aptitude/check-answer', {
        question_id: selectedAptitude.id,
        answer: aptitudeAnswer
      })
      setAptitudeResult(response)
    } catch (error) {
      console.error('Error checking answer:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const selectSituationalQuestion = (question) => {
    setSelectedSituational(question)
    setSituationalAnswer(null)
    setSituationalResult(null)
  }

  const submitSituationalAnswer = async () => {
    if (!situationalAnswer || !selectedSituational) return
    try {
      setIsLoading(true)
      const response = await api.post('/aptitude/situational/check-answer', {
        question_id: selectedSituational.id,
        answer: situationalAnswer
      })
      setSituationalResult(response)
    } catch (error) {
      console.error('Error checking answer:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getCategoryColor = (category) => {
    switch (category?.toLowerCase()) {
      case 'quantitative': return 'text-blue-400 bg-blue-500/20 border-blue-500/30'
      case 'logical reasoning': return 'text-purple-400 bg-purple-500/20 border-purple-500/30'
      case 'data interpretation': return 'text-cyan-400 bg-cyan-500/20 border-cyan-500/30'
      default: return 'text-slate-400 bg-slate-500/20 border-slate-500/30'
    }
  }

  // Tab Configuration
  const tabs = [
    { id: 'coding', label: 'Coding Problems', icon: '💻' },
    { id: 'aptitude', label: 'Aptitude', icon: '🧠' },
    { id: 'situational', label: 'Situational', icon: '🎯' },
    { id: 'cases', label: 'Case Studies', icon: '📊' }
  ]

  return (
    <PageTransition>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <h1 className="text-4xl font-bold text-white mb-2">Practice Problems</h1>
            <p className="text-slate-400">Master coding, aptitude, and situational interview questions</p>
          </motion.div>

          {/* Tabs */}
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-2 mb-6 p-1 bg-slate-800/50 rounded-xl w-fit"
          >
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2.5 rounded-lg font-medium transition-all flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </motion.div>

          {/* CODING TAB */}
          {activeTab === 'coding' && (
          <div className="flex gap-6">
            {/* Left Panel - Question List */}
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="w-80 flex-shrink-0"
            >
              {/* Filter Tabs */}
              <div className="flex gap-2 mb-4">
                {['all', 'easy', 'medium', 'hard'].map(f => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium capitalize transition-all ${
                      filter === f 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>

              {/* Questions List */}
              <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                <div className="max-h-[calc(100vh-250px)] overflow-y-auto">
                  {filteredQuestions.map((q, index) => (
                    <motion.button
                      key={q.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      onClick={() => selectQuestion(q.id)}
                      className={`w-full p-4 text-left border-b border-slate-700 hover:bg-slate-700/50 transition-colors ${
                        selectedQuestion?.id === q.id ? 'bg-slate-700' : ''
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-white font-medium text-sm">{q.id}. {q.title}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getDifficultyColor(q.difficulty)}`}>
                          {q.difficulty}
                        </span>
                        <div className="flex gap-1">
                          {q.topics?.slice(0, 2).map(topic => (
                            <span key={topic} className="text-xs text-slate-500">{topic}</span>
                          ))}
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Right Panel - Question Details & Editor */}
            <motion.div 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex-1"
            >
              {selectedQuestion ? (
                <div className="space-y-4">
                  {/* Question Header */}
                  <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-2xl font-bold text-white">
                        {selectedQuestion.id}. {selectedQuestion.title}
                      </h2>
                      <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getDifficultyColor(selectedQuestion.difficulty)}`}>
                        {selectedQuestion.difficulty}
                      </span>
                    </div>
                    <div className="flex gap-2 mb-4">
                      {selectedQuestion.topics?.map(topic => (
                        <span key={topic} className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-300">
                          {topic}
                        </span>
                      ))}
                    </div>
                    <div className="prose prose-invert max-w-none">
                      <pre className="text-slate-300 whitespace-pre-wrap text-sm font-sans leading-relaxed">
                        {selectedQuestion.description}
                      </pre>
                    </div>
                  </div>

                  {/* Code Editor */}
                  <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700 bg-slate-800">
                      <span className="text-sm text-slate-400">Python</span>
                      <div className="flex gap-2">
                        <button
                          onClick={revealHint}
                          disabled={hintsRevealed >= selectedQuestion.hints_count}
                          className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded text-sm hover:bg-yellow-500/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Hint ({hintsRevealed}/{selectedQuestion.hints_count})
                        </button>
                        <button
                          onClick={viewSolution}
                          className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded text-sm hover:bg-purple-500/30 transition-colors"
                        >
                          Solution
                        </button>
                      </div>
                    </div>
                    <textarea
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      className="w-full h-64 p-4 bg-slate-900 text-green-400 font-mono text-sm resize-none focus:outline-none"
                      spellCheck="false"
                      placeholder="Write your solution here..."
                    />
                  </div>

                  {/* Hints Section */}
                  <AnimatePresence>
                    {hints.length > 0 && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="bg-yellow-500/10 rounded-xl p-4 border border-yellow-500/30"
                      >
                        <h3 className="text-yellow-400 font-semibold mb-3 flex items-center gap-2">
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                          </svg>
                          Hints
                        </h3>
                        <div className="space-y-2">
                          {hints.map((hint, i) => (
                            <motion.div
                              key={i}
                              initial={{ opacity: 0, x: -10 }}
                              animate={{ opacity: 1, x: 0 }}
                              className="flex items-start gap-2"
                            >
                              <span className="text-yellow-500 font-bold">{i + 1}.</span>
                              <span className="text-yellow-200 text-sm">{hint}</span>
                            </motion.div>
                          ))}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* Submit Button & Result */}
                  <div className="flex items-center gap-4">
                    <button
                      onClick={submitCode}
                      disabled={isLoading}
                      className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-semibold rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all disabled:opacity-50 flex items-center gap-2"
                    >
                      {isLoading ? (
                        <>
                          <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Running...
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Submit
                        </>
                      )}
                    </button>

                    {/* Result Badge */}
                    <AnimatePresence>
                      {submitResult && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.9 }}
                          className={`px-4 py-2 rounded-xl border flex items-center gap-3 ${getStatusColor(submitResult.status)}`}
                        >
                          {submitResult.status === 'accepted' ? (
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          ) : (
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          )}
                          <div>
                            <p className="font-semibold capitalize">{submitResult.status}</p>
                            <p className="text-sm opacity-80">{submitResult.passed}/{submitResult.total} tests passed</p>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* Result Message */}
                  <AnimatePresence>
                    {submitResult && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className={`p-4 rounded-xl border ${getStatusColor(submitResult.status)}`}
                      >
                        <p>{submitResult.message}</p>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* Solution Modal */}
                  <AnimatePresence>
                    {showSolution && solution && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-6"
                        onClick={() => setShowSolution(false)}
                      >
                        <motion.div
                          initial={{ scale: 0.9, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          exit={{ scale: 0.9, opacity: 0 }}
                          className="bg-slate-800 rounded-2xl border border-slate-700 max-w-3xl w-full max-h-[80vh] overflow-hidden"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
                            <h3 className="text-xl font-bold text-white">Solution</h3>
                            <button
                              onClick={() => setShowSolution(false)}
                              className="text-slate-400 hover:text-white transition-colors"
                            >
                              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          </div>
                          <div className="p-6 overflow-y-auto max-h-[calc(80vh-80px)]">
                            <pre className="bg-slate-900 p-4 rounded-xl text-green-400 font-mono text-sm overflow-x-auto whitespace-pre-wrap">
                              {solution.solution}
                            </pre>
                            
                            {/* Test Cases */}
                            <h4 className="text-white font-semibold mt-6 mb-3">Test Cases</h4>
                            <div className="space-y-2">
                              {solution.test_cases?.map((tc, i) => (
                                <div key={i} className="bg-slate-700/50 p-3 rounded-lg">
                                  <div className="text-sm">
                                    <span className="text-slate-400">Input: </span>
                                    <span className="text-blue-400 font-mono">{JSON.stringify(tc.input)}</span>
                                  </div>
                                  <div className="text-sm">
                                    <span className="text-slate-400">Expected: </span>
                                    <span className="text-green-400 font-mono">{JSON.stringify(tc.expected)}</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </motion.div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ) : (
                <div className="bg-slate-800/50 rounded-xl p-12 border border-slate-700 text-center">
                  <svg className="w-16 h-16 mx-auto text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  <h3 className="text-xl text-slate-400 mb-2">Select a Problem</h3>
                  <p className="text-slate-500">Choose a problem from the list to start practicing</p>
                </div>
              )}
            </motion.div>
          </div>
          )}

          {/* APTITUDE TAB */}
          {activeTab === 'aptitude' && (
            <div className="flex gap-6">
              {/* Left Panel - Question List */}
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="w-80 flex-shrink-0"
              >
                {/* Category Filters */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {['all', 'quantitative', 'logical', 'data'].map(f => (
                    <button
                      key={f}
                      onClick={() => setAptitudeFilter(f)}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium capitalize transition-all ${
                        aptitudeFilter === f 
                          ? 'bg-purple-500 text-white' 
                          : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                      }`}
                    >
                      {f === 'data' ? 'Data Int.' : f}
                    </button>
                  ))}
                </div>

                {/* Questions List */}
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                  <div className="max-h-[calc(100vh-300px)] overflow-y-auto">
                    {filteredAptitude.map((q, index) => (
                      <motion.button
                        key={q.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.03 }}
                        onClick={() => selectAptitudeQuestion(q)}
                        className={`w-full p-4 text-left border-b border-slate-700 hover:bg-slate-700/50 transition-colors ${
                          selectedAptitude?.id === q.id ? 'bg-slate-700' : ''
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-white font-medium text-sm">{q.title}</span>
                        </div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getCategoryColor(q.category)}`}>
                            {q.category}
                          </span>
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getDifficultyColor(q.difficulty)}`}>
                            {q.difficulty}
                          </span>
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>
              </motion.div>

              {/* Right Panel - Question Details */}
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex-1"
              >
                {selectedAptitude ? (
                  <div className="space-y-4">
                    {/* Question Card */}
                    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                      <div className="flex items-center gap-3 mb-4">
                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getCategoryColor(selectedAptitude.category)}`}>
                          {selectedAptitude.category}
                        </span>
                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getDifficultyColor(selectedAptitude.difficulty)}`}>
                          {selectedAptitude.difficulty}
                        </span>
                        <span className="text-slate-500 text-sm">{selectedAptitude.topic}</span>
                      </div>
                      
                      <h2 className="text-2xl font-bold text-white mb-4">{selectedAptitude.title}</h2>
                      
                      <div className="bg-slate-900/50 rounded-xl p-4 mb-6">
                        <p className="text-slate-300 whitespace-pre-wrap">{selectedAptitude.question}</p>
                      </div>

                      {/* Options */}
                      <div className="space-y-3">
                        {selectedAptitude.options?.map((option, i) => (
                          <button
                            key={i}
                            onClick={() => setAptitudeAnswer(option.charAt(0))}
                            disabled={aptitudeResult}
                            className={`w-full p-4 rounded-xl border text-left transition-all ${
                              aptitudeAnswer === option.charAt(0)
                                ? aptitudeResult
                                  ? aptitudeResult.correct
                                    ? 'bg-green-500/20 border-green-500 text-green-400'
                                    : 'bg-red-500/20 border-red-500 text-red-400'
                                  : 'bg-blue-500/20 border-blue-500 text-blue-400'
                                : aptitudeResult && option.charAt(0) === aptitudeResult.correct_answer
                                  ? 'bg-green-500/20 border-green-500 text-green-400'
                                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500'
                            }`}
                          >
                            {option}
                          </button>
                        ))}
                      </div>

                      {/* Submit Button */}
                      {!aptitudeResult && (
                        <button
                          onClick={submitAptitudeAnswer}
                          disabled={!aptitudeAnswer || isLoading}
                          className="mt-6 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50"
                        >
                          {isLoading ? 'Checking...' : 'Check Answer'}
                        </button>
                      )}

                      {/* Result & Explanation */}
                      <AnimatePresence>
                        {aptitudeResult && (
                          <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`mt-6 p-4 rounded-xl border ${
                              aptitudeResult.correct 
                                ? 'bg-green-500/10 border-green-500/30' 
                                : 'bg-red-500/10 border-red-500/30'
                            }`}
                          >
                            <div className="flex items-center gap-2 mb-3">
                              {aptitudeResult.correct ? (
                                <>
                                  <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                  </svg>
                                  <span className="text-green-400 font-bold">Correct!</span>
                                </>
                              ) : (
                                <>
                                  <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                  </svg>
                                  <span className="text-red-400 font-bold">Incorrect</span>
                                </>
                              )}
                            </div>
                            <p className="text-slate-300 text-sm whitespace-pre-wrap">{aptitudeResult.explanation}</p>
                            
                            <button
                              onClick={() => {
                                setSelectedAptitude(null)
                                setAptitudeAnswer(null)
                                setAptitudeResult(null)
                              }}
                              className="mt-4 px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors"
                            >
                              Next Question
                            </button>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-800/50 rounded-xl p-12 border border-slate-700 text-center">
                    <span className="text-6xl mb-4 block">🧠</span>
                    <h3 className="text-xl text-slate-400 mb-2">Select an Aptitude Question</h3>
                    <p className="text-slate-500">Practice quantitative, logical, and data interpretation problems</p>
                  </div>
                )}
              </motion.div>
            </div>
          )}

          {/* SITUATIONAL TAB */}
          {activeTab === 'situational' && (
            <div className="flex gap-6">
              {/* Left Panel */}
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="w-80 flex-shrink-0"
              >
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                  <div className="max-h-[calc(100vh-250px)] overflow-y-auto">
                    {situationalQuestions.map((q, index) => (
                      <motion.button
                        key={q.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.03 }}
                        onClick={() => selectSituationalQuestion(q)}
                        className={`w-full p-4 text-left border-b border-slate-700 hover:bg-slate-700/50 transition-colors ${
                          selectedSituational?.id === q.id ? 'bg-slate-700' : ''
                        }`}
                      >
                        <span className="text-white font-medium text-sm block mb-2">{q.title}</span>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getDifficultyColor(q.difficulty)}`}>
                            {q.difficulty}
                          </span>
                          {q.competencies?.slice(0, 2).map(c => (
                            <span key={c} className="text-xs text-slate-500">{c}</span>
                          ))}
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>
              </motion.div>

              {/* Right Panel */}
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex-1"
              >
                {selectedSituational ? (
                  <div className="space-y-4">
                    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                      <div className="flex items-center gap-3 mb-4">
                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getDifficultyColor(selectedSituational.difficulty)}`}>
                          {selectedSituational.difficulty}
                        </span>
                        <div className="flex gap-2">
                          {selectedSituational.competencies?.map(c => (
                            <span key={c} className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">
                              {c}
                            </span>
                          ))}
                        </div>
                      </div>

                      <h2 className="text-2xl font-bold text-white mb-4">{selectedSituational.title}</h2>

                      {/* Scenario */}
                      <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-xl p-5 mb-6 border-l-4 border-yellow-500">
                        <h3 className="text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                          <span>📋</span> Scenario
                        </h3>
                        <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">{selectedSituational.scenario}</p>
                      </div>

                      <p className="text-white font-medium mb-4">{selectedSituational.question}</p>

                      {/* Options */}
                      <div className="space-y-3">
                        {selectedSituational.options?.map((option, i) => (
                          <button
                            key={i}
                            onClick={() => setSituationalAnswer(option.charAt(0))}
                            disabled={situationalResult}
                            className={`w-full p-4 rounded-xl border text-left transition-all ${
                              situationalAnswer === option.charAt(0)
                                ? situationalResult
                                  ? situationalResult.score === 100
                                    ? 'bg-green-500/20 border-green-500 text-green-400'
                                    : situationalResult.score === 0
                                      ? 'bg-red-500/20 border-red-500 text-red-400'
                                      : 'bg-yellow-500/20 border-yellow-500 text-yellow-400'
                                  : 'bg-blue-500/20 border-blue-500 text-blue-400'
                                : situationalResult && option.charAt(0) === situationalResult.best_answer
                                  ? 'bg-green-500/20 border-green-500 text-green-400'
                                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500'
                            }`}
                          >
                            {option}
                          </button>
                        ))}
                      </div>

                      {/* Submit */}
                      {!situationalResult && (
                        <button
                          onClick={submitSituationalAnswer}
                          disabled={!situationalAnswer || isLoading}
                          className="mt-6 px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-xl hover:from-cyan-600 hover:to-blue-600 transition-all disabled:opacity-50"
                        >
                          {isLoading ? 'Evaluating...' : 'Submit Answer'}
                        </button>
                      )}

                      {/* Result */}
                      <AnimatePresence>
                        {situationalResult && (
                          <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mt-6 space-y-4"
                          >
                            {/* Score Badge */}
                            <div className={`p-4 rounded-xl border ${
                              situationalResult.score === 100
                                ? 'bg-green-500/10 border-green-500/30'
                                : situationalResult.score === 0
                                  ? 'bg-red-500/10 border-red-500/30'
                                  : 'bg-yellow-500/10 border-yellow-500/30'
                            }`}>
                              <div className="flex items-center gap-3 mb-2">
                                <div className={`text-4xl font-bold ${
                                  situationalResult.score === 100 ? 'text-green-400' :
                                  situationalResult.score === 0 ? 'text-red-400' : 'text-yellow-400'
                                }`}>
                                  {situationalResult.score}%
                                </div>
                                <p className={`font-medium ${
                                  situationalResult.score === 100 ? 'text-green-400' :
                                  situationalResult.score === 0 ? 'text-red-400' : 'text-yellow-400'
                                }`}>
                                  {situationalResult.feedback}
                                </p>
                              </div>
                            </div>

                            {/* Explanation */}
                            <div className="bg-slate-900/50 rounded-xl p-4">
                              <h4 className="text-white font-semibold mb-2">Explanation</h4>
                              <p className="text-slate-300 text-sm whitespace-pre-wrap">{situationalResult.explanation}</p>
                            </div>

                            <button
                              onClick={() => {
                                setSelectedSituational(null)
                                setSituationalAnswer(null)
                                setSituationalResult(null)
                              }}
                              className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors"
                            >
                              Next Question
                            </button>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-800/50 rounded-xl p-12 border border-slate-700 text-center">
                    <span className="text-6xl mb-4 block">🎯</span>
                    <h3 className="text-xl text-slate-400 mb-2">Select a Situational Question</h3>
                    <p className="text-slate-500">Practice workplace scenarios and behavioral interview questions</p>
                  </div>
                )}
              </motion.div>
            </div>
          )}

          {/* CASE STUDIES TAB */}
          {activeTab === 'cases' && (
            <div className="flex gap-6">
              {/* Left Panel */}
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="w-80 flex-shrink-0"
              >
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                  <div className="max-h-[calc(100vh-250px)] overflow-y-auto">
                    {caseStudies.map((c, index) => (
                      <motion.button
                        key={c.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        onClick={() => setSelectedCase(c)}
                        className={`w-full p-4 text-left border-b border-slate-700 hover:bg-slate-700/50 transition-colors ${
                          selectedCase?.id === c.id ? 'bg-slate-700' : ''
                        }`}
                      >
                        <span className="text-white font-medium text-sm block mb-2">{c.title}</span>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getDifficultyColor(c.difficulty)}`}>
                            {c.difficulty}
                          </span>
                          {c.topics?.slice(0, 2).map(t => (
                            <span key={t} className="text-xs text-slate-500">{t}</span>
                          ))}
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>
              </motion.div>

              {/* Right Panel */}
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex-1"
              >
                {selectedCase ? (
                  <div className="space-y-4">
                    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                      <div className="flex items-center gap-3 mb-4">
                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getDifficultyColor(selectedCase.difficulty)}`}>
                          {selectedCase.difficulty}
                        </span>
                        <div className="flex gap-2">
                          {selectedCase.topics?.map(t => (
                            <span key={t} className="px-2 py-1 bg-purple-500/20 text-purple-400 rounded text-xs">
                              {t}
                            </span>
                          ))}
                        </div>
                      </div>

                      <h2 className="text-2xl font-bold text-white mb-4">{selectedCase.title}</h2>

                      {/* Scenario */}
                      <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-xl p-5 mb-6 border-l-4 border-purple-500">
                        <h3 className="text-purple-400 font-semibold mb-3 flex items-center gap-2">
                          <span>📊</span> Case Scenario
                        </h3>
                        <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">{selectedCase.scenario}</p>
                      </div>

                      {/* Questions & Key Points */}
                      <div className="space-y-6">
                        {selectedCase.questions?.map((q, i) => (
                          <div key={i} className="bg-slate-900/50 rounded-xl p-5">
                            <h4 className="text-white font-semibold mb-4 flex items-center gap-2">
                              <span className="w-7 h-7 rounded-full bg-purple-500 flex items-center justify-center text-sm">
                                {i + 1}
                              </span>
                              {q.q}
                            </h4>
                            
                            <details className="group">
                              <summary className="cursor-pointer text-purple-400 hover:text-purple-300 transition-colors">
                                Click to reveal key points
                              </summary>
                              <ul className="mt-4 space-y-2">
                                {q.key_points?.map((point, j) => (
                                  <li key={j} className="flex items-start gap-2 text-slate-300 text-sm">
                                    <span className="text-green-400 mt-0.5">✓</span>
                                    {point}
                                  </li>
                                ))}
                              </ul>
                            </details>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-800/50 rounded-xl p-12 border border-slate-700 text-center">
                    <span className="text-6xl mb-4 block">📊</span>
                    <h3 className="text-xl text-slate-400 mb-2">Select a Case Study</h3>
                    <p className="text-slate-500">Practice in-depth analysis and decision-making scenarios</p>
                  </div>
                )}
              </motion.div>
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  )
}

export default Practice

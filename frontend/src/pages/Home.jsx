import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ResumeUpload, PageTransition, GlassCard } from '../components'
import { staggerContainer, fadeInUp } from '../utils/animations'

const Home = () => {
  const navigate = useNavigate()

  const handleUploadSuccess = (data) => {
    // Store resume data and navigate to interview
    localStorage.setItem('resumeData', JSON.stringify(data))
    navigate('/interview')
  }

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <motion.div 
          className="text-center max-w-4xl mx-auto mb-16"
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
        >
          <motion.div 
            variants={fadeInUp}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-6 backdrop-blur-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Powered by AI
          </motion.div>
          
          <motion.h1 
            variants={fadeInUp}
            className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight"
          >
            AI Interview
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              Simulation Platform
            </span>
          </motion.h1>
          
          <motion.p 
            variants={fadeInUp}
            className="text-lg md:text-xl text-slate-400 mb-8 max-w-2xl mx-auto leading-relaxed"
          >
            Upload your resume for instant <span className="text-white font-medium">ATS analysis</span>, 
            then practice with our AI-powered <span className="text-white font-medium">mock interviews</span> 
            tailored to your skills and target role.
          </motion.p>
        </motion.div>

        {/* Resume Upload Section */}
        <div className="max-w-2xl mx-auto mb-16">
          <GlassCard className="p-8" delay={0.3}>
          <h2 className="text-2xl font-bold text-white text-center mb-2">
            Start Your Journey
          </h2>
          <p className="text-slate-400 text-center mb-8">
            Upload your resume to begin the AI-powered interview simulation
          </p>
            <ResumeUpload onUploadSuccess={handleUploadSuccess} />
          </GlassCard>
        </div>

        {/* Features Section */}
        <motion.div 
          className="max-w-5xl mx-auto"
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
        >
          <motion.h2 
            variants={fadeInUp}
            className="text-2xl font-bold text-white text-center mb-8"
          >
            How It Works
          </motion.h2>
          <div className="grid md:grid-cols-3 gap-6">
            <GlassCard className="p-6" delay={0.4}>
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-blue-500/25">
                <span className="text-white font-bold">1</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Upload Resume</h3>
              <p className="text-slate-400">Our AI analyzes your resume for ATS compatibility and extracts key skills.</p>
            </GlassCard>

            <GlassCard className="p-6" delay={0.5}>
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-green-500/25">
                <span className="text-white font-bold">2</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Mock Interview</h3>
              <p className="text-slate-400">Answer AI-generated technical and HR questions based on your profile.</p>
            </GlassCard>

            <GlassCard className="p-6" delay={0.6}>
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-purple-500/25">
                <span className="text-white font-bold">3</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Get Feedback</h3>
              <p className="text-slate-400">Receive detailed performance reports with improvement suggestions.</p>
            </GlassCard>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  )
}

export default Home

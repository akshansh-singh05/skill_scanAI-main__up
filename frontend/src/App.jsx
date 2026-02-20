import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { Navbar } from './components'
import { Home, Interview, Report, Practice, VideoInterviewPage } from './pages'

function AnimatedRoutes() {
  const location = useLocation()
  
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/report" element={<Report />} />
        <Route path="/video-interview" element={<VideoInterviewPage />} />
      </Routes>
    </AnimatePresence>
  )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex flex-col">
        <Navbar />
        <main className="flex-1 relative z-0 overflow-hidden">
          <AnimatedRoutes />
        </main>
        <footer className="border-t border-white/10 backdrop-blur-sm bg-slate-900 relative z-10 flex-shrink-0">
          <div className="container mx-auto px-4 py-6 text-center text-slate-400">
            <p>&copy; 2026 AI Mock Interviewer. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App

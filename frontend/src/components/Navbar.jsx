import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const linkClasses = ({ isActive }) =>
    `px-4 py-2 rounded-lg transition-all duration-200 ${
      isActive
        ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
        : 'text-slate-300 hover:text-white hover:bg-white/10'
    }`

  const mobileLinkClasses = ({ isActive }) =>
    `block px-4 py-3 rounded-lg transition-all duration-200 ${
      isActive
        ? 'bg-blue-600 text-white'
        : 'text-slate-300 hover:text-white hover:bg-white/10'
    }`

  return (
    <motion.nav 
      className="bg-white/5 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50 no-print print:hidden"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <NavLink to="/" className="text-xl font-bold text-white flex items-center gap-3 group">
            <motion.div 
              className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-shadow"
              whileHover={{ scale: 1.1, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </motion.div>
            <span className="hidden sm:block">AI Mock Interviewer</span>
            <span className="sm:hidden">AI Mock</span>
          </NavLink>

          {/* Desktop Navigation */}
          <ul className="hidden md:flex items-center space-x-2">
            {[
              { to: '/', label: 'Home', end: true },
              { to: '/interview', label: 'Interview' },
              { to: '/video-interview', label: 'Video' },
              { to: '/practice', label: 'Practice' },
              { to: '/report', label: 'Report' },
            ].map((link, index) => (
              <motion.li 
                key={link.to}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + index * 0.1 }}
              >
                <NavLink to={link.to} className={linkClasses} end={link.end}>
                  {link.label}
                </NavLink>
              </motion.li>
            ))}
          </ul>

          {/* Mobile Menu Button */}
          <motion.button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
            aria-label="Toggle menu"
            whileTap={{ scale: 0.9 }}
          >
            {isMenuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </motion.button>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div 
              className="md:hidden py-4 border-t border-white/10"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              <ul className="space-y-2">
                <li>
                  <NavLink to="/" className={mobileLinkClasses} end onClick={() => setIsMenuOpen(false)}>
                    Home
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/interview" className={mobileLinkClasses} onClick={() => setIsMenuOpen(false)}>
                    Interview
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/video-interview" className={mobileLinkClasses} onClick={() => setIsMenuOpen(false)}>
                    Video Interview
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/practice" className={mobileLinkClasses} onClick={() => setIsMenuOpen(false)}>
                    Practice
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/report" className={mobileLinkClasses} onClick={() => setIsMenuOpen(false)}>
                    Report
                  </NavLink>
                </li>
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.nav>
  )
}

export default Navbar

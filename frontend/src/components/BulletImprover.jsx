import { useState } from 'react'
import { improveBullet } from '../services'

/**
 * BulletImprover - Transform weak resume bullet points into impactful statements
 * 
 * Features:
 * - Input field for original bullet point
 * - One-click improvement with AI-powered suggestions
 * - Multiple alternatives to choose from
 * - Tips for writing better bullet points
 */
const BulletImprover = ({ role = 'SDE' }) => {
  const [inputBullet, setInputBullet] = useState('')
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [copiedIndex, setCopiedIndex] = useState(null)

  const exampleBullets = [
    "Built a website using React",
    "Worked on database stuff",
    "Helped with API development",
    "Made some Python scripts",
    "Did testing for the app",
  ]

  const handleImprove = async () => {
    if (!inputBullet.trim()) {
      setError('Please enter a bullet point to improve')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await improveBullet(inputBullet, role)
      setResult(response)
    } catch (err) {
      setError(err.message || 'Failed to improve bullet point')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = async (text, index) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleExampleClick = (example) => {
    setInputBullet(example)
    setResult(null)
    setError(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">Resume Bullet Improver</h3>
          <p className="text-sm text-slate-400">Transform weak bullet points into impactful statements</p>
        </div>
      </div>

      {/* Input Section */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-slate-300">
          Enter your bullet point
        </label>
        <div className="relative">
          <textarea
            value={inputBullet}
            onChange={(e) => setInputBullet(e.target.value)}
            placeholder="e.g., Built a website using React"
            className="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white 
                       placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 
                       focus:border-transparent transition-all duration-200 resize-none"
            rows={2}
          />
        </div>

        {/* Example Bullets */}
        <div className="flex flex-wrap gap-2">
          <span className="text-xs text-slate-500">Try:</span>
          {exampleBullets.slice(0, 3).map((example, idx) => (
            <button
              key={idx}
              onClick={() => handleExampleClick(example)}
              className="text-xs px-2 py-1 rounded-md bg-slate-700/50 text-slate-400 
                         hover:bg-slate-700 hover:text-slate-300 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Improve Button */}
      <button
        onClick={handleImprove}
        disabled={isLoading || !inputBullet.trim()}
        className={`
          w-full py-3 px-6 rounded-xl font-semibold text-white
          transition-all duration-200 flex items-center justify-center gap-2
          ${isLoading || !inputBullet.trim()
            ? 'bg-slate-700 cursor-not-allowed text-slate-400'
            : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 hover:shadow-lg hover:shadow-purple-500/25'
          }
        `}
      >
        {isLoading ? (
          <>
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span>Improving...</span>
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>Improve This Bullet Point</span>
          </>
        )}
      </button>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/50 flex items-start gap-3">
          <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-4 animate-fadeIn">
          {/* Original vs Improved */}
          <div className="grid gap-4">
            {/* Original */}
            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <span className="w-2 h-2 rounded-full bg-red-500"></span>
                <span className="text-xs font-medium text-red-400 uppercase tracking-wide">Original</span>
              </div>
              <p className="text-slate-400 line-through">{result.original}</p>
            </div>

            {/* Arrow */}
            <div className="flex justify-center">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center">
                <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                </svg>
              </div>
            </div>

            {/* Improved - Main */}
            <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/30 relative group">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-green-500"></span>
                  <span className="text-xs font-medium text-green-400 uppercase tracking-wide">Improved</span>
                </div>
                <button
                  onClick={() => handleCopy(result.improved, 'main')}
                  className="p-1.5 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors"
                  title="Copy to clipboard"
                >
                  {copiedIndex === 'main' ? (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  )}
                </button>
              </div>
              <p className="text-green-300 font-medium">{result.improved}</p>
            </div>
          </div>

          {/* Alternatives */}
          {result.alternatives && result.alternatives.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-slate-300">Alternative Versions</h4>
              {result.alternatives.map((alt, idx) => (
                <div 
                  key={idx}
                  className="p-3 rounded-xl bg-slate-800/50 border border-slate-700 flex items-center justify-between group hover:border-slate-600 transition-colors"
                >
                  <p className="text-slate-300 text-sm flex-1">{alt}</p>
                  <button
                    onClick={() => handleCopy(alt, idx)}
                    className="ml-3 p-1.5 rounded-lg bg-slate-700 text-slate-400 hover:bg-slate-600 hover:text-white transition-colors opacity-0 group-hover:opacity-100"
                    title="Copy to clipboard"
                  >
                    {copiedIndex === idx ? (
                      <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Changes Made */}
          {result.changes && result.changes.length > 0 && (
            <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
              <h4 className="text-sm font-medium text-blue-400 mb-3 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Improvements Made
              </h4>
              <ul className="space-y-2">
                {result.changes.map((change, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                    <svg className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {change}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Pro Tips */}
          {result.tips && result.tips.length > 0 && (
            <div className="p-4 rounded-xl bg-yellow-500/10 border border-yellow-500/20">
              <h4 className="text-sm font-medium text-yellow-400 mb-3 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Pro Tips for Better Bullet Points
              </h4>
              <ul className="space-y-2">
                {result.tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-yellow-400">•</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* CSS for fadeIn animation */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  )
}

export default BulletImprover

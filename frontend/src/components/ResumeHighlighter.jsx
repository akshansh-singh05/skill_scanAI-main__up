import { useMemo } from 'react'

/**
 * ResumeHighlighter - Visual keyword highlighter for resume analysis
 * 
 * Highlights:
 * - Matched skills in GREEN (strong areas found in resume)
 * - Missing skills shown in RED tags (skills to add)
 */
const ResumeHighlighter = ({ resumeText, matchedSkills = [], missingSkills = [] }) => {
  // Create highlighted resume text
  const highlightedContent = useMemo(() => {
    if (!resumeText || matchedSkills.length === 0) {
      return resumeText || ''
    }

    // Sort skills by length (longest first) to avoid partial replacements
    const sortedSkills = [...matchedSkills].sort((a, b) => b.length - a.length)
    
    // Create a regex pattern for all matched skills
    const escapeRegex = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    
    let result = resumeText
    const highlights = []
    
    // Find all skill matches with their positions
    sortedSkills.forEach(skill => {
      const regex = new RegExp(`\\b${escapeRegex(skill)}\\b`, 'gi')
      let match
      while ((match = regex.exec(resumeText)) !== null) {
        highlights.push({
          start: match.index,
          end: match.index + match[0].length,
          text: match[0],
          skill: skill
        })
      }
    })
    
    // Sort by position and remove overlapping highlights
    highlights.sort((a, b) => a.start - b.start)
    const nonOverlapping = []
    let lastEnd = -1
    highlights.forEach(h => {
      if (h.start >= lastEnd) {
        nonOverlapping.push(h)
        lastEnd = h.end
      }
    })
    
    // Build the result with highlights
    if (nonOverlapping.length === 0) {
      return resumeText
    }
    
    const parts = []
    let currentIndex = 0
    
    nonOverlapping.forEach((highlight, idx) => {
      // Add text before this highlight
      if (highlight.start > currentIndex) {
        parts.push({
          type: 'text',
          content: resumeText.slice(currentIndex, highlight.start)
        })
      }
      // Add the highlighted skill
      parts.push({
        type: 'highlight',
        content: highlight.text,
        skill: highlight.skill
      })
      currentIndex = highlight.end
    })
    
    // Add remaining text
    if (currentIndex < resumeText.length) {
      parts.push({
        type: 'text',
        content: resumeText.slice(currentIndex)
      })
    }
    
    return parts
  }, [resumeText, matchedSkills])

  if (!resumeText) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Missing Skills - Red Highlights */}
      {missingSkills.length > 0 && (
        <div className="bg-red-500/5 rounded-2xl p-5 border border-red-500/20">
          <h4 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Missing Keywords - Add These to Your Resume
          </h4>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-lg bg-red-500/20 border border-red-500/40 text-red-400 text-sm font-medium
                           animate-pulse hover:animate-none hover:bg-red-500/30 transition-colors cursor-default"
                title="This skill is missing from your resume"
              >
                <span className="mr-1.5">✗</span>
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Matched Skills - Green Highlights */}
      {matchedSkills.length > 0 && (
        <div className="bg-green-500/5 rounded-2xl p-5 border border-green-500/20">
          <h4 className="text-sm font-semibold text-green-400 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Strong Keywords Found
          </h4>
          <div className="flex flex-wrap gap-2">
            {matchedSkills.map((skill, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-lg bg-green-500/20 border border-green-500/40 text-green-400 text-sm font-medium
                           hover:bg-green-500/30 transition-colors cursor-default"
                title="This skill was found in your resume"
              >
                <span className="mr-1.5">✓</span>
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Resume Text with Highlights */}
      <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
        <h4 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
          <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Resume Preview with Keyword Highlights
        </h4>
        
        <div className="max-h-96 overflow-y-auto pr-2 custom-scrollbar">
          <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap font-mono">
            {Array.isArray(highlightedContent) ? (
              highlightedContent.map((part, idx) => (
                part.type === 'highlight' ? (
                  <mark
                    key={idx}
                    className="bg-green-500/30 text-green-300 px-1 py-0.5 rounded border-b-2 border-green-500 
                               hover:bg-green-500/50 transition-colors cursor-default"
                    title={`Matched skill: ${part.skill}`}
                  >
                    {part.content}
                  </mark>
                ) : (
                  <span key={idx}>{part.content}</span>
                )
              ))
            ) : (
              highlightedContent
            )}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-4 pt-4 border-t border-slate-700 flex items-center gap-6 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 rounded bg-green-500/30 border border-green-500"></span>
            <span>Matched Skills (Strong)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 rounded bg-red-500/30 border border-red-500"></span>
            <span>Missing Skills (Add These)</span>
          </div>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-green-500/10 rounded-xl p-4 border border-green-500/20 text-center">
          <div className="text-3xl font-bold text-green-400">{matchedSkills.length}</div>
          <div className="text-sm text-green-400/70 mt-1">Skills Matched</div>
        </div>
        <div className="bg-red-500/10 rounded-xl p-4 border border-red-500/20 text-center">
          <div className="text-3xl font-bold text-red-400">{missingSkills.length}</div>
          <div className="text-sm text-red-400/70 mt-1">Skills to Add</div>
        </div>
      </div>
    </div>
  )
}

export default ResumeHighlighter

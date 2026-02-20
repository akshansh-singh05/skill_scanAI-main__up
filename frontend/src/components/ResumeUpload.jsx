import { useState, useRef } from 'react'
import { uploadResume } from '../services'
import ResumeHighlighter from './ResumeHighlighter'
import BulletImprover from './BulletImprover'

const TARGET_ROLES = [
  { value: 'SDE', label: 'Software Development Engineer (SDE)' },
  { value: 'Data Analyst', label: 'Data Analyst' },
  { value: 'ML Engineer', label: 'ML Engineer' },
]

const ResumeUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [targetRole, setTargetRole] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState(null)
  const [atsResult, setAtsResult] = useState(null)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    validateAndSetFile(droppedFile)
  }

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    validateAndSetFile(selectedFile)
  }

  const validateAndSetFile = (file) => {
    setError(null)
    setAtsResult(null)
    
    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file only')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      return
    }

    setFile(file)
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a resume file')
      return
    }

    if (!targetRole) {
      setError('Please select a target role')
      return
    }

    setIsUploading(true)
    setError(null)
    setAtsResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('role', targetRole)
      
      const response = await uploadResume(formData)
      setAtsResult(response)
      // Don't navigate immediately - show results first
    } catch (err) {
      const errorMsg = typeof err === 'string' ? err : (err.message || err.detail || 'Failed to upload resume')
      setError(errorMsg)
    } finally {
      setIsUploading(false)
    }
  }

  const removeFile = () => {
    setFile(null)
    setError(null)
    setAtsResult(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'from-green-500 to-green-600'
    if (score >= 60) return 'from-yellow-500 to-yellow-600'
    return 'from-red-500 to-red-600'
  }

  return (
    <div className="w-full max-w-xl mx-auto">
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !file && fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 text-center
          transition-all duration-300 ease-out
          ${!file ? 'cursor-pointer' : ''}
          ${isDragging 
            ? 'border-blue-500 bg-blue-500/10 scale-[1.02]' 
            : 'border-slate-600 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-800'
          }
          ${file ? 'border-green-500 bg-green-500/10' : ''}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="hidden"
        />

        {!file ? (
          <>
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-700 flex items-center justify-center">
              <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">
              Drop your resume here
            </h3>
            <p className="text-slate-400 mb-4">
              or click to browse files
            </p>
            <p className="text-sm text-slate-500">
              PDF files only (Max 5MB)
            </p>
          </>
        ) : (
          <div className="flex items-center justify-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="text-left">
              <p className="text-white font-medium truncate max-w-[200px]">{file.name}</p>
              <p className="text-sm text-slate-400">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                removeFile()
              }}
              className="p-2 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Target Role Dropdown */}
      <div className="mt-6">
        <label className="block text-sm font-medium text-slate-300 mb-2">
          Target Role
        </label>
        <select
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          className="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     transition-all duration-200 appearance-none cursor-pointer"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239ca3af' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")`,
            backgroundPosition: 'right 0.75rem center',
            backgroundRepeat: 'no-repeat',
            backgroundSize: '1.5em 1.5em',
          }}
        >
          <option value="" className="bg-slate-800">Select a target role...</option>
          {TARGET_ROLES.map((role) => (
            <option key={role.value} value={role.value} className="bg-slate-800">
              {role.label}
            </option>
          ))}
        </select>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/50 flex items-start gap-3">
          <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={isUploading || !file || !targetRole}
        className={`
          w-full mt-6 py-3 px-6 rounded-xl font-semibold text-white
          transition-all duration-200
          ${isUploading || !file || !targetRole
            ? 'bg-slate-700 cursor-not-allowed text-slate-400'
            : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg hover:shadow-blue-500/25'
          }
        `}
      >
        {isUploading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Analyzing Resume...
          </span>
        ) : (
          'Upload & Analyze Resume'
        )}
      </button>

      {/* ATS Score Result */}
      {atsResult && (
        <div className="mt-8 space-y-6">
          {/* Score Card */}
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              ATS Compatibility Score
            </h3>
            
            <div className="flex items-center gap-6">
              <div className={`text-5xl font-bold ${getScoreColor(atsResult.ats_score || 0)}`}>
                {atsResult.ats_score || 0}%
              </div>
              <div className="flex-1">
                <div className="h-4 bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    className={`h-full bg-gradient-to-r ${getScoreBgColor(atsResult.ats_score || 0)} transition-all duration-1000 ease-out`}
                    style={{ width: `${atsResult.ats_score || 0}%` }}
                  />
                </div>
                <p className="text-sm text-slate-400 mt-2">
                  {atsResult.ats_score >= 80 
                    ? 'Excellent! Your resume is well-optimized.'
                    : atsResult.ats_score >= 60
                    ? 'Good, but there\'s room for improvement.'
                    : 'Needs improvement to pass ATS filters.'}
                </p>
              </div>
            </div>
          </div>

          {/* Live Keyword Highlighter */}
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Live Keyword Analysis
            </h3>
            
            <ResumeHighlighter
              resumeText={atsResult.resume_text}
              matchedSkills={atsResult.matched_skills || []}
              missingSkills={atsResult.missing_skills || []}
            />
          </div>

          {/* Bullet Point Improver */}
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
            <BulletImprover role={targetRole} />
          </div>

          {/* Continue to Interview Button */}
          <button
            onClick={() => onUploadSuccess?.(atsResult)}
            className="w-full py-4 px-6 rounded-xl font-semibold text-white
                       bg-gradient-to-r from-green-500 to-emerald-600 
                       hover:from-green-600 hover:to-emerald-700
                       hover:shadow-lg hover:shadow-green-500/25
                       transition-all duration-200 flex items-center justify-center gap-3"
          >
            <span>Continue to Mock Interview</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      )}
    </div>
  )
}

export default ResumeUpload

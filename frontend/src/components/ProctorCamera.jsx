import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * ProctorCamera - Anti-cheating camera monitoring component
 * 
 * Features:
 * - Continuous camera monitoring during interview
 * - Tab switch / window blur detection
 * - Face presence detection (basic)
 * - Warning system with violation tracking
 * - Visual indicators for monitoring status
 */
const ProctorCamera = ({ 
  isActive = true, 
  onViolation = () => {}, 
  onStatusChange = () => {},
  showWarnings = true 
}) => {
  // Camera states
  const [stream, setStream] = useState(null)
  const [isCameraReady, setIsCameraReady] = useState(false)
  const [cameraError, setCameraError] = useState(null)
  
  // Monitoring states
  const [isMonitoring, setIsMonitoring] = useState(false)
  const [violations, setViolations] = useState([])
  const [warningCount, setWarningCount] = useState(0)
  const [currentWarning, setCurrentWarning] = useState(null)
  const [tabSwitchCount, setTabSwitchCount] = useState(0)
  const [faceDetected, setFaceDetected] = useState(true)
  const [lookAwayCount, setLookAwayCount] = useState(0)
  const [isOutOfFrame, setIsOutOfFrame] = useState(false)
  const [outOfFrameDuration, setOutOfFrameDuration] = useState(0)
  const [consecutiveNoFaceFrames, setConsecutiveNoFaceFrames] = useState(0)
  
  // Refs
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const warningTimeoutRef = useRef(null)
  const faceCheckIntervalRef = useRef(null)
  const outOfFrameTimerRef = useRef(null)
  
  // Violation types
  const VIOLATION_TYPES = {
    TAB_SWITCH: 'TAB_SWITCH',
    WINDOW_BLUR: 'WINDOW_BLUR',
    NO_FACE: 'NO_FACE',
    OUT_OF_FRAME: 'OUT_OF_FRAME',
    MULTIPLE_FACES: 'MULTIPLE_FACES',
    LOOKING_AWAY: 'LOOKING_AWAY',
    CAMERA_BLOCKED: 'CAMERA_BLOCKED'
  }
  
  // Warning messages
  const WARNING_MESSAGES = {
    TAB_SWITCH: '⚠️ Tab switch detected! Stay focused on the interview.',
    WINDOW_BLUR: '⚠️ Window focus lost! Return to the interview window.',
    NO_FACE: '⚠️ Face not detected! Please stay visible to the camera.',
    OUT_OF_FRAME: '🚨 YOU ARE OUT OF FRAME! Return to camera view immediately.',
    MULTIPLE_FACES: '⚠️ Multiple faces detected! Only the candidate should be visible.',
    LOOKING_AWAY: '⚠️ Please look at the screen. Frequent looking away is being recorded.',
    CAMERA_BLOCKED: '⚠️ Camera appears blocked! Please uncover your camera.'
  }

  // Initialize camera
  const initCamera = useCallback(async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 320 }, 
          height: { ideal: 240 }, 
          facingMode: 'user' 
        },
        audio: false
      })
      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      setIsCameraReady(true)
      setCameraError(null)
      setIsMonitoring(true)
      onStatusChange({ status: 'active', message: 'Camera monitoring active' })
    } catch (error) {
      console.error('Camera access error:', error)
      setCameraError('Camera access required for proctoring. Please grant camera permissions.')
      setIsCameraReady(false)
      onStatusChange({ status: 'error', message: 'Camera access denied' })
    }
  }, [onStatusChange])

  // Stop camera
  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
    }
    setIsCameraReady(false)
    setIsMonitoring(false)
  }, [stream])

  // Record violation
  const recordViolation = useCallback((type) => {
    const timestamp = new Date().toISOString()
    const violation = { type, timestamp, message: WARNING_MESSAGES[type] }
    
    setViolations(prev => [...prev, violation])
    setWarningCount(prev => prev + 1)
    setCurrentWarning(WARNING_MESSAGES[type])
    
    // Notify parent
    onViolation(violation)
    
    // Clear warning after 3 seconds
    if (warningTimeoutRef.current) {
      clearTimeout(warningTimeoutRef.current)
    }
    warningTimeoutRef.current = setTimeout(() => {
      setCurrentWarning(null)
    }, 3000)
  }, [onViolation])

  // Tab visibility change handler
  const handleVisibilityChange = useCallback(() => {
    if (document.hidden && isMonitoring) {
      setTabSwitchCount(prev => prev + 1)
      recordViolation(VIOLATION_TYPES.TAB_SWITCH)
    }
  }, [isMonitoring, recordViolation])

  // Window blur handler
  const handleWindowBlur = useCallback(() => {
    if (isMonitoring) {
      recordViolation(VIOLATION_TYPES.WINDOW_BLUR)
    }
  }, [isMonitoring, recordViolation])

  // Basic face detection using canvas brightness analysis
  const checkFacePresence = useCallback(() => {
    if (!videoRef.current || !canvasRef.current || !isMonitoring) return
    
    const video = videoRef.current
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    
    // Draw current frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Get image data from center region (where face should be)
    const centerX = canvas.width * 0.25
    const centerY = canvas.height * 0.1
    const regionWidth = canvas.width * 0.5
    const regionHeight = canvas.height * 0.6
    
    try {
      const imageData = ctx.getImageData(centerX, centerY, regionWidth, regionHeight)
      const data = imageData.data
      
      // Calculate average brightness and color variance
      let totalBrightness = 0
      let skinTonePixels = 0
      
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i]
        const g = data[i + 1]
        const b = data[i + 2]
        
        // Calculate brightness
        const brightness = (r + g + b) / 3
        totalBrightness += brightness
        
        // Basic skin tone detection (simplified)
        // Skin tones typically have R > G > B with certain ratios
        if (r > 60 && g > 40 && b > 20 && r > b && (r - g) < 100 && Math.abs(r - g) <= 80) {
          skinTonePixels++
        }
      }
      
      const avgBrightness = totalBrightness / (data.length / 4)
      const skinToneRatio = skinTonePixels / (data.length / 4)
      
      // Check for blocked camera (very dark)
      if (avgBrightness < 15) {
        if (faceDetected) {
          setFaceDetected(false)
          recordViolation(VIOLATION_TYPES.CAMERA_BLOCKED)
        }
        return
      }
      
      // Check for face presence based on skin tone detection
      const hasFace = skinToneRatio > 0.05 // At least 5% skin tone pixels
      
      if (!hasFace) {
        // No face detected - increment consecutive no-face frames
        setConsecutiveNoFaceFrames(prev => {
          const newCount = prev + 1
          
          // After 2 consecutive checks (4 seconds), show immediate warning
          if (newCount === 2 && !isOutOfFrame) {
            setIsOutOfFrame(true)
            setCurrentWarning(WARNING_MESSAGES.OUT_OF_FRAME)
            recordViolation(VIOLATION_TYPES.OUT_OF_FRAME)
            
            // Start counting out-of-frame duration
            outOfFrameTimerRef.current = setInterval(() => {
              setOutOfFrameDuration(prev => prev + 1)
            }, 1000)
          }
          
          // After 1 check, show initial warning
          if (newCount === 1 && faceDetected) {
            setFaceDetected(false)
            setCurrentWarning(WARNING_MESSAGES.NO_FACE)
          }
          
          return newCount
        })
        
        setLookAwayCount(prev => prev + 1)
      } else {
        // Face detected - reset counters
        if (!faceDetected || isOutOfFrame) {
          setFaceDetected(true)
          setIsOutOfFrame(false)
          setConsecutiveNoFaceFrames(0)
          
          // Stop out-of-frame timer
          if (outOfFrameTimerRef.current) {
            clearInterval(outOfFrameTimerRef.current)
            outOfFrameTimerRef.current = null
          }
          
          // Reset duration after logging if it was significant
          if (outOfFrameDuration > 3) {
            recordViolation(VIOLATION_TYPES.OUT_OF_FRAME)
          }
          setOutOfFrameDuration(0)
          
          // Clear current warning after face returns
          setTimeout(() => {
            setCurrentWarning(null)
          }, 1500)
        }
        setConsecutiveNoFaceFrames(0)
      }
    } catch (e) {
      // Canvas security error or other issue
      console.log('Face check error:', e)
    }
  }, [isMonitoring, faceDetected, isOutOfFrame, outOfFrameDuration, recordViolation])

  // Initialize on mount
  useEffect(() => {
    if (isActive) {
      initCamera()
    }
    
    return () => {
      stopCamera()
      if (warningTimeoutRef.current) {
        clearTimeout(warningTimeoutRef.current)
      }
      if (faceCheckIntervalRef.current) {
        clearInterval(faceCheckIntervalRef.current)
      }
      if (outOfFrameTimerRef.current) {
        clearInterval(outOfFrameTimerRef.current)
      }
    }
  }, [isActive])

  // Set up event listeners
  useEffect(() => {
    if (isMonitoring) {
      document.addEventListener('visibilitychange', handleVisibilityChange)
      window.addEventListener('blur', handleWindowBlur)
      
      // Start face checking interval
      faceCheckIntervalRef.current = setInterval(checkFacePresence, 2000)
      
      return () => {
        document.removeEventListener('visibilitychange', handleVisibilityChange)
        window.removeEventListener('blur', handleWindowBlur)
        if (faceCheckIntervalRef.current) {
          clearInterval(faceCheckIntervalRef.current)
        }
      }
    }
  }, [isMonitoring, handleVisibilityChange, handleWindowBlur, checkFacePresence])

  // Get status indicator color
  const getStatusColor = () => {
    if (cameraError) return 'bg-red-500'
    if (!isCameraReady) return 'bg-yellow-500'
    if (warningCount > 5) return 'bg-red-500'
    if (warningCount > 2) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const getWarningLevel = () => {
    if (warningCount >= 5) return { level: 'critical', text: 'Critical', color: 'text-red-400' }
    if (warningCount >= 3) return { level: 'warning', text: 'Warning', color: 'text-yellow-400' }
    if (warningCount >= 1) return { level: 'caution', text: 'Caution', color: 'text-orange-400' }
    return { level: 'good', text: 'Good', color: 'text-green-400' }
  }

  return (
    <div className="proctor-camera-container">
      {/* Camera View */}
      <div className="relative rounded-xl overflow-hidden bg-slate-900 border border-slate-700">
        {/* Status indicator */}
        <div className="absolute top-2 left-2 z-10 flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${getStatusColor()} animate-pulse`} />
          <span className="text-xs text-white bg-black/50 px-2 py-1 rounded">
            {isMonitoring ? 'MONITORING' : 'INITIALIZING...'}
          </span>
        </div>
        
        {/* Recording indicator */}
        {isMonitoring && (
          <div className="absolute top-2 right-2 z-10 flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-xs text-red-400 font-medium">REC</span>
          </div>
        )}
        
        {/* Video element */}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-auto min-h-[180px] max-h-[200px] object-cover mirror"
          style={{ transform: 'scaleX(-1)' }} // Mirror effect
        />
        
        {/* Hidden canvas for face detection */}
        <canvas 
          ref={canvasRef} 
          width={160} 
          height={120} 
          className="hidden"
        />
        
        {/* Camera error state */}
        {cameraError && (
          <div className="absolute inset-0 flex items-center justify-center bg-slate-900/90">
            <div className="text-center p-4">
              <div className="text-red-400 text-4xl mb-2">📷</div>
              <p className="text-red-400 text-sm">{cameraError}</p>
              <button 
                onClick={initCamera}
                className="mt-3 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
              >
                Retry Camera Access
              </button>
            </div>
          </div>
        )}
        
        {/* Warning banner */}
        {showWarnings && currentWarning && !isOutOfFrame && (
          <div className="absolute bottom-0 left-0 right-0 bg-red-600/90 text-white text-sm py-2 px-3 animate-pulse">
            {currentWarning}
          </div>
        )}
        
        {/* OUT OF FRAME - Full overlay warning */}
        {isOutOfFrame && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-red-900/95 z-20 animate-pulse">
            <div className="text-6xl mb-3">🚨</div>
            <div className="text-white text-lg font-bold text-center px-4">
              OUT OF FRAME!
            </div>
            <div className="text-red-200 text-sm text-center mt-2 px-4">
              Return to camera view immediately
            </div>
            <div className="mt-3 px-3 py-1 bg-red-600 rounded-full text-white text-xs font-medium">
              {outOfFrameDuration}s out of frame
            </div>
            {outOfFrameDuration >= 5 && (
              <div className="mt-2 text-red-200 text-xs text-center px-4">
                ⚠️ This violation is being recorded
              </div>
            )}
          </div>
        )}
        
        {/* Face detection status indicator */}
        {isMonitoring && !cameraError && !isOutOfFrame && (
          <div className={`absolute bottom-12 right-2 z-10 px-2 py-1 rounded text-xs ${
            faceDetected 
              ? 'bg-green-500/80 text-white' 
              : 'bg-yellow-500/80 text-white animate-pulse'
          }`}>
            {faceDetected ? '✓ Face detected' : '? Checking...'}
          </div>
        )}
      </div>
      
      {/* Stats panel */}
      <div className="mt-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">Status:</span>
            <span className={getWarningLevel().color}>{getWarningLevel().text}</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className={faceDetected ? 'text-green-400' : 'text-red-400'}>
              {faceDetected ? '👤' : '❌'}
            </span>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-xs text-slate-400 mt-2">
          <span>Warnings: <span className={warningCount > 0 ? 'text-yellow-400' : 'text-green-400'}>{warningCount}</span></span>
          <span>Tab switches: <span className={tabSwitchCount > 0 ? 'text-red-400' : 'text-green-400'}>{tabSwitchCount}</span></span>
          <span>Look away: <span className={lookAwayCount > 2 ? 'text-red-400' : lookAwayCount > 0 ? 'text-yellow-400' : 'text-green-400'}>{lookAwayCount}</span></span>
        </div>
        
        {/* Warning threshold indicator */}
        {warningCount >= 3 && (
          <div className="mt-2 p-2 bg-red-500/20 rounded-lg border border-red-500/30">
            <p className="text-xs text-red-400">
              ⚠️ Multiple violations detected. This may affect your interview evaluation. 
              {warningCount >= 5 && ' Interview may be flagged for review.'}
            </p>
          </div>
        )}
      </div>
      
      {/* Violation log (collapsible) */}
      {violations.length > 0 && (
        <details className="mt-3">
          <summary className="text-xs text-slate-500 cursor-pointer hover:text-slate-400">
            View violation log ({violations.length} events)
          </summary>
          <div className="mt-2 max-h-32 overflow-y-auto space-y-1">
            {violations.map((v, i) => (
              <div key={i} className="text-xs text-slate-500 bg-slate-800/30 px-2 py-1 rounded">
                <span className="text-slate-600">
                  {new Date(v.timestamp).toLocaleTimeString()}
                </span>
                {' - '}{v.type.replace('_', ' ')}
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  )
}

export default ProctorCamera

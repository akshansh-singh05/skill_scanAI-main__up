import { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const VideoInterview = () => {
  // Video states
  const [stream, setStream] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isCameraReady, setIsCameraReady] = useState(false);
  const [cameraError, setCameraError] = useState(null);

  // Timer states
  const [timeLeft, setTimeLeft] = useState(60);
  const [timerActive, setTimerActive] = useState(false);

  // Transcript states
  const [transcript, setTranscript] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');

  // Analysis states
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  // Current question
  const [currentQuestion, setCurrentQuestion] = useState(
    "Tell me about yourself and why you're interested in this position."
  );

  // Refs
  const videoRef = useRef(null);
  const recognitionRef = useRef(null);
  const timerRef = useRef(null);
  const transcriptBoxRef = useRef(null);

  // Sample questions for rotation
  const questions = [
    "Tell me about yourself and why you're interested in this position.",
    "What are your greatest strengths and how do they apply to this role?",
    "Describe a challenging project you've worked on and how you handled it.",
    "Where do you see yourself in five years?",
    "Why should we hire you over other candidates?",
    "Tell me about a time you demonstrated leadership.",
    "How do you handle stress and pressure?",
    "What motivates you to do your best work?",
  ];

  // Initialize camera
  const initCamera = useCallback(async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' },
        audio: true,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsCameraReady(true);
      setCameraError(null);
    } catch (error) {
      console.error('Camera access error:', error);
      setCameraError('Unable to access camera. Please ensure camera permissions are granted.');
      setIsCameraReady(false);
    }
  }, []);

  // Initialize speech recognition
  const initSpeechRecognition = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      setCameraError('Speech recognition is not supported in this browser. Please use Chrome.');
      return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let interim = '';
      let final = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          final += result[0].transcript + ' ';
        } else {
          interim += result[0].transcript;
        }
      }

      if (final) {
        setTranscript((prev) => prev + final);
      }
      setInterimTranscript(interim);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      if (event.error === 'no-speech') {
        // Restart recognition if no speech detected
        if (isRecording) {
          recognition.start();
        }
      }
    };

    recognition.onend = () => {
      // Restart if still recording
      if (isRecording && recognitionRef.current) {
        try {
          recognitionRef.current.start();
        } catch (e) {
          console.log('Recognition restart error:', e);
        }
      }
    };

    return recognition;
  }, [isRecording]);

  // Start recording
  const startRecording = () => {
    if (!isCameraReady) {
      initCamera();
      return;
    }

    // Reset states
    setTranscript('');
    setInterimTranscript('');
    setAnalysisResult(null);
    setTimeLeft(60);
    setIsRecording(true);
    setTimerActive(true);

    // Initialize and start speech recognition
    const recognition = initSpeechRecognition();
    if (recognition) {
      recognitionRef.current = recognition;
      recognition.start();
    }

    // Pick a random question
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
    setCurrentQuestion(randomQuestion);
  };

  // Stop recording
  const stopRecording = async () => {
    setIsRecording(false);
    setTimerActive(false);

    // Stop speech recognition
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    // Clear timer
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    // Analyze the transcript
    if (transcript.trim() || interimTranscript.trim()) {
      await analyzeTranscript(transcript + interimTranscript);
    }
  };

  // Analyze transcript
  const analyzeTranscript = async (text) => {
    if (!text.trim()) {
      setAnalysisResult({
        confidence_score: 0,
        clarity_score: 0,
        filler_words_count: 0,
        sentiment: 'neutral',
        feedback: 'No speech was detected. Please try again and speak clearly.',
      });
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/video-analysis`, {
        transcript: text,
        question: currentQuestion,
        duration: 60 - timeLeft,
      });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error('Analysis error:', error);
      setAnalysisResult({
        confidence_score: 5,
        clarity_score: 5,
        filler_words_count: 0,
        sentiment: 'neutral',
        feedback: 'Unable to analyze response. Please try again.',
        error: true,
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Timer effect
  useEffect(() => {
    if (timerActive && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            stopRecording();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [timerActive]);

  // Auto-scroll transcript
  useEffect(() => {
    if (transcriptBoxRef.current) {
      transcriptBoxRef.current.scrollTop = transcriptBoxRef.current.scrollHeight;
    }
  }, [transcript, interimTranscript]);

  // Initialize camera on mount
  useEffect(() => {
    initCamera();

    return () => {
      // Cleanup
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  // Format time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Get timer color
  const getTimerColor = () => {
    if (timeLeft > 30) return 'text-green-400';
    if (timeLeft > 10) return 'text-yellow-400';
    return 'text-red-400';
  };

  // Get score color
  const getScoreColor = (score) => {
    if (score >= 7) return 'text-green-400';
    if (score >= 4) return 'text-yellow-400';
    return 'text-red-400';
  };

  // Get sentiment emoji
  const getSentimentEmoji = (sentiment) => {
    const sentiments = {
      positive: '😊',
      negative: '😔',
      neutral: '😐',
      confident: '💪',
      nervous: '😰',
    };
    return sentiments[sentiment?.toLowerCase()] || '😐';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            🎥 Video Interview Practice
          </h1>
          <p className="text-gray-400">
            Practice your interview skills with AI-powered feedback
          </p>
        </div>

        {/* Main Content - Split Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Side - Camera */}
          <div className="space-y-4">
            {/* Video Container */}
            <div className="relative bg-gray-800 rounded-2xl overflow-hidden shadow-2xl border border-gray-700">
              {/* Timer Badge */}
              {isRecording && (
                <div className="absolute top-4 right-4 z-10 bg-gray-900/80 backdrop-blur-sm px-4 py-2 rounded-full flex items-center gap-2">
                  <span className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                  </span>
                  <span className={`font-mono text-xl font-bold ${getTimerColor()}`}>
                    {formatTime(timeLeft)}
                  </span>
                </div>
              )}

              {/* Video Preview */}
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="w-full aspect-video object-cover bg-gray-900"
              />

              {/* Camera Error Overlay */}
              {cameraError && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-900/90">
                  <div className="text-center p-6">
                    <div className="text-5xl mb-4">📷</div>
                    <p className="text-red-400 text-sm">{cameraError}</p>
                    <button
                      onClick={initCamera}
                      className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm transition-colors"
                    >
                      Retry Camera Access
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="flex justify-center gap-4">
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  disabled={!isCameraReady && !cameraError}
                  className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-xl text-white font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" />
                  </svg>
                  Start Recording
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 rounded-xl text-white font-semibold text-lg transition-all transform hover:scale-105 shadow-lg animate-pulse"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <rect x="6" y="6" width="12" height="12" rx="2" />
                  </svg>
                  Stop Recording
                </button>
              )}
            </div>

            {/* Instructions */}
            {!isRecording && !analysisResult && (
              <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                <h3 className="text-white font-semibold mb-2">📋 Instructions</h3>
                <ul className="text-gray-400 text-sm space-y-1">
                  <li>• Click "Start Recording" to begin your practice session</li>
                  <li>• Answer the question displayed on the right</li>
                  <li>• You have 60 seconds to respond</li>
                  <li>• Click "Stop" when finished or wait for timer</li>
                  <li>• Receive AI-powered feedback on your response</li>
                </ul>
              </div>
            )}
          </div>

          {/* Right Side - Question + Transcript + Results */}
          <div className="space-y-4">
            {/* Question Card */}
            <div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 rounded-xl p-6 border border-blue-700/50 shadow-xl">
              <div className="flex items-start gap-3">
                <span className="text-3xl">💬</span>
                <div>
                  <h3 className="text-blue-300 text-sm font-medium mb-1">Interview Question</h3>
                  <p className="text-white text-lg font-medium">{currentQuestion}</p>
                </div>
              </div>
            </div>

            {/* Transcript Box */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-xl">
              <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
                <h3 className="text-white font-semibold flex items-center gap-2">
                  <span>📝</span> Live Transcript
                </h3>
                {isRecording && (
                  <span className="text-xs text-green-400 flex items-center gap-1">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    Listening...
                  </span>
                )}
              </div>
              <div
                ref={transcriptBoxRef}
                className="h-48 overflow-y-auto p-4 text-gray-300 text-sm leading-relaxed"
              >
                {transcript || interimTranscript ? (
                  <>
                    <span>{transcript}</span>
                    <span className="text-gray-500 italic">{interimTranscript}</span>
                  </>
                ) : (
                  <span className="text-gray-500 italic">
                    {isRecording
                      ? 'Start speaking... Your words will appear here.'
                      : 'Your transcript will appear here when you start recording.'}
                  </span>
                )}
              </div>
            </div>

            {/* Loading Spinner */}
            {isAnalyzing && (
              <div className="bg-gray-800 rounded-xl p-8 border border-gray-700 flex flex-col items-center justify-center">
                <div className="relative w-16 h-16 mb-4">
                  <div className="absolute inset-0 border-4 border-blue-500/30 rounded-full"></div>
                  <div className="absolute inset-0 border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
                </div>
                <p className="text-white font-medium">Analyzing your response...</p>
                <p className="text-gray-400 text-sm mt-1">This may take a few seconds</p>
              </div>
            )}

            {/* Analysis Results */}
            {analysisResult && !isAnalyzing && (
              <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-xl overflow-hidden">
                <div className="px-4 py-3 border-b border-gray-700 bg-gradient-to-r from-green-900/30 to-blue-900/30">
                  <h3 className="text-white font-semibold flex items-center gap-2">
                    <span>📊</span> Analysis Results
                  </h3>
                </div>
                <div className="p-4 space-y-4">
                  {/* Scores Grid */}
                  <div className="grid grid-cols-2 gap-4">
                    {/* Confidence Score */}
                    <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                      <div className="text-gray-400 text-sm mb-1">Confidence</div>
                      <div className={`text-3xl font-bold ${getScoreColor(analysisResult.confidence_score)}`}>
                        {analysisResult.confidence_score}/10
                      </div>
                    </div>

                    {/* Clarity Score */}
                    <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                      <div className="text-gray-400 text-sm mb-1">Clarity</div>
                      <div className={`text-3xl font-bold ${getScoreColor(analysisResult.clarity_score)}`}>
                        {analysisResult.clarity_score}/10
                      </div>
                    </div>

                    {/* Filler Words */}
                    <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                      <div className="text-gray-400 text-sm mb-1">Filler Words</div>
                      <div className="text-3xl font-bold text-orange-400">
                        {analysisResult.filler_words_count}
                      </div>
                    </div>

                    {/* Sentiment */}
                    <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                      <div className="text-gray-400 text-sm mb-1">Sentiment</div>
                      <div className="text-3xl">
                        {getSentimentEmoji(analysisResult.sentiment)}
                      </div>
                      <div className="text-xs text-gray-400 capitalize mt-1">
                        {analysisResult.sentiment}
                      </div>
                    </div>
                  </div>

                  {/* Filler Words List */}
                  {analysisResult.filler_words_found && analysisResult.filler_words_found.length > 0 && (
                    <div className="bg-gray-900/50 rounded-lg p-4">
                      <div className="text-gray-400 text-sm mb-2">Filler Words Detected</div>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.filler_words_found.map((word, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-orange-900/50 text-orange-300 rounded text-xs"
                          >
                            {word}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Feedback */}
                  <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-4">
                    <div className="text-blue-300 text-sm font-medium mb-2 flex items-center gap-2">
                      <span>💡</span> AI Feedback
                    </div>
                    <p className="text-gray-300 text-sm leading-relaxed">
                      {analysisResult.feedback}
                    </p>
                  </div>

                  {/* Suggestions */}
                  {analysisResult.suggestions && analysisResult.suggestions.length > 0 && (
                    <div className="bg-gray-900/50 rounded-lg p-4">
                      <div className="text-gray-400 text-sm font-medium mb-2 flex items-center gap-2">
                        <span>✨</span> Suggestions for Improvement
                      </div>
                      <ul className="space-y-1">
                        {analysisResult.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-gray-300 text-sm flex items-start gap-2">
                            <span className="text-green-400 mt-1">•</span>
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Try Again Button */}
                  <button
                    onClick={() => {
                      setAnalysisResult(null);
                      setTranscript('');
                      setInterimTranscript('');
                      setTimeLeft(60);
                    }}
                    className="w-full py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors"
                  >
                    Practice Another Question
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoInterview;

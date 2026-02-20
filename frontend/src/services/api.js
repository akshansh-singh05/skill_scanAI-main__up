import axios from 'axios'

// Base URL for all API requests - use relative path for proxy
const API_BASE_URL = '/api'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred'
    
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

/**
 * Upload resume file for analysis
 * @param {FormData} formData - Form data containing the resume file
 * @returns {Promise} - Parsed resume data
 */
export const uploadResume = async (formData) => {
  return apiClient.post('/resume/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * Start the interview process
 * @param {Object} data - Interview configuration data
 * @returns {Promise} - Interview session data with first question
 */
export const startInterview = async (data) => {
  return apiClient.post('/interview/start-interview', data)
}

/**
 * Submit answer to a technical interview question
 * @param {Object} data - Answer data including question and response
 * @returns {Promise} - Next question or completion status
 */
export const submitAnswer = async (data) => {
  return apiClient.post('/interview/submit-answer', data)
}

/**
 * Submit answer to an HR interview question
 * @param {Object} data - HR answer data
 * @returns {Promise} - Next HR question or completion status
 */
export const submitHRAnswer = async (data) => {
  return apiClient.post('/hr/hr-round', data)
}

/**
 * Get the final interview report
 * @param {Object} data - Scores data
 * @returns {Promise} - Complete interview report with scores and feedback
 */
export const getReport = async (data) => {
  return apiClient.post('/report/generate-report', data)
}

/**
 * Improve a single resume bullet point
 * @param {string} bullet - Original bullet point text
 * @param {string} role - Target role (SDE, Data Analyst, ML Engineer)
 * @returns {Promise} - Improved bullet point with suggestions
 */
export const improveBullet = async (bullet, role = 'SDE') => {
  return apiClient.post('/resume/improve-bullet', { bullet, role })
}

/**
 * Improve multiple bullet points at once
 * @param {string[]} bullets - Array of bullet point texts
 * @param {string} role - Target role
 * @returns {Promise} - Array of improved bullet points
 */
export const improveBulletsBatch = async (bullets, role = 'SDE') => {
  return apiClient.post('/resume/improve-bullets-batch', { bullets, role })
}

// Export the axios instance for custom requests
export default apiClient

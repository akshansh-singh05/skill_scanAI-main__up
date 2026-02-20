# SkillScan AI

An AI-powered resume analysis and interview preparation platform that helps job seekers ace their interviews through mock sessions, skill assessments, and personalized feedback.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-06B6D4?logo=tailwindcss)

## Features

### Resume Analysis
- **ATS Scoring** - Get instant compatibility scores for Applicant Tracking Systems
- **Resume Parsing** - Automatic extraction of skills, experience, and education
- **Skill Highlighting** - Visual representation of your key competencies
- **Bullet Point Improver** - AI-powered suggestions to enhance resume bullet points

### AI Mock Interviews
- **Technical Interviews** - Role-specific questions based on your resume and target position
- **HR Round Simulation** - Practice behavioral and situational questions
- **Video Interviews** - Real-time interview simulation with camera support
- **Proctoring** - Monitor interview environment for realistic practice

### Skill Assessment
- **Aptitude Tests** - Quantitative, logical, and verbal reasoning assessments
- **Practice Questions** - Topic-wise practice with multiple difficulty levels
- **Skill Gap Analysis** - Identify areas for improvement based on your target role
- **Communication Analysis** - Evaluate your interview responses for clarity and confidence

### Reports & Insights
- **Comprehensive Reports** - Detailed performance breakdown after each session
- **Career Recommendations** - AI-suggested career paths based on your profile
- **Weakness Heatmap** - Visual representation of areas needing improvement
- **Progress Tracking** - Monitor your growth over multiple practice sessions

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Pydantic** - Data validation and settings management
- **pdfplumber** - PDF parsing for resume extraction
- **scikit-learn** - Machine learning for analysis features
- **pytesseract** - OCR for image-based resume processing

### Frontend
- **React 19** - Modern UI library with latest features
- **Vite** - Next-generation frontend build tool
- **TailwindCSS 4** - Utility-first CSS framework
- **Framer Motion** - Production-ready animations
- **Recharts** - Composable charting library
- **Axios** - HTTP client for API requests

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Tesseract OCR (for image-based resume parsing)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file for environment variables (if needed):
   ```env
   # Add your API keys and configuration here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:5173`

## Project Structure

```
skill_scanAI-main/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models for data validation
│   ├── requirements.txt     # Python dependencies
│   ├── config/
│   │   ├── company_modes.py # Company-specific interview configurations
│   │   └── skill_sets.py    # Skill categorization definitions
│   ├── routers/
│   │   ├── aptitude.py      # Aptitude test endpoints
│   │   ├── hr.py            # HR interview endpoints
│   │   ├── interview.py     # Technical interview endpoints
│   │   ├── practice.py      # Practice questions endpoints
│   │   ├── report.py        # Report generation endpoints
│   │   ├── resume.py        # Resume analysis endpoints
│   │   └── video.py         # Video interview endpoints
│   └── services/
│       ├── aptitude_questions.py    # Aptitude question generation
│       ├── ats_scorer.py            # ATS compatibility scoring
│       ├── bullet_improver.py       # Resume bullet enhancement
│       ├── career_recommender.py    # Career path suggestions
│       ├── communication_analyzer.py # Response analysis
│       ├── hr_analyzer.py           # HR response evaluation
│       ├── interview_engine.py      # Interview orchestration
│       ├── practice_questions.py    # Practice question bank
│       ├── report_generator.py      # Report compilation
│       ├── resume_parser.py         # Resume text extraction
│       └── skill_gap_analyzer.py    # Skill gap identification
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page-level components
│   │   ├── services/        # API client services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── layouts/         # Layout components
│   │   └── utils/           # Helper functions and animations
│   ├── public/              # Static assets
│   └── package.json         # Node.js dependencies
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/resume/upload-resume` | POST | Upload and parse resume |
| `/api/resume/improve-bullet` | POST | Improve a resume bullet point |
| `/api/interview/start-interview` | POST | Start a mock interview session |
| `/api/interview/submit-answer` | POST | Submit answer and get next question |
| `/api/hr/hr-round` | POST | HR interview round |
| `/api/report/generate-report` | POST | Generate performance report |
| `/api/aptitude/*` | Various | Aptitude assessment endpoints |
| `/api/practice/*` | Various | Practice question endpoints |

## Usage

1. **Upload Your Resume** - Start by uploading your resume in PDF format on the home page
2. **Review ATS Score** - Check your resume's compatibility with Applicant Tracking Systems
3. **Start Mock Interview** - Begin an AI-powered interview tailored to your skills and target role
4. **Answer Questions** - Respond to technical and HR questions in real-time
5. **Get Feedback** - Receive detailed reports with scores and improvement suggestions
6. **Practice More** - Use practice questions and aptitude tests to strengthen weak areas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [React](https://react.dev/) and [TailwindCSS](https://tailwindcss.com/)
- Animations by [Framer Motion](https://www.framer.com/motion/)

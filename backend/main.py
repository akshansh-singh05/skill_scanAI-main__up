from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import resume, interview, hr, report, practice, aptitude, video

app = FastAPI(
    title="SkillScan AI",
    description="AI-powered resume analysis and interview preparation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(hr.router, prefix="/api/hr", tags=["HR"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])
app.include_router(practice.router, prefix="/api", tags=["Practice"])
app.include_router(aptitude.router, prefix="/api", tags=["Aptitude"])
app.include_router(video.router, prefix="/api", tags=["Video Interview"])


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy", "message": "SkillScan AI API is running"}

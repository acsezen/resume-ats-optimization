"""
AI Resume Builder MVP - FastHTML Application
One-click AI-powered resume optimization for ATS compliance
"""
import os
import json
import tempfile
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# FastHTML imports
from fasthtml.common import *

# Internal imports
from models.resume_models import Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory
from models.ats_models import ATSAnalysisResult
from services.ai_service import AIResumeOptimizer
from services.ats_analyzer import ATSAnalyzer
from processors.file_processor import FileProcessor, ResumeExporter

# Initialize FastHTML app
# Get absolute path to static directory
static_dir = Path(__file__).parent / "static"

app, rt = fast_app(
    hdrs=[
        Link(rel="stylesheet", href="/static/css/modern-style.css"),
        Script(src="/static/js/app.js"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Title("AI Resume Builder - ATS Optimization")
    ]
)

# Mount static files manually
from starlette.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize services
file_processor = FileProcessor()
resume_exporter = ResumeExporter()

def create_head():
    """Create standard HTML head with CSS and JS"""
    return Head(
        Link(rel="stylesheet", href="/static/css/ultra-modern.css"),
        Script(src="/static/js/app.js"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Meta(name="theme-color", content="#0ea5e9"),
        Meta(name="description", content="AI-powered resume optimization for ATS compatibility. Get instant analysis and professional resume enhancement."),
        Title("AI Resume Builder - ATS Optimization")
    )

# Global variables for services (will be initialized when API key is provided)
ai_optimizer = None
ats_analyzer = ATSAnalyzer()

def init_ai_services(api_key: str):
    """Initialize AI services with API key"""
    global ai_optimizer
    try:
        ai_optimizer = AIResumeOptimizer(api_key)
        return True
    except Exception as e:
        print(f"Failed to initialize AI services: {e}")
        return False

# Check for API key on startup
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    init_ai_services(openai_api_key)
    print("✅ AI services initialized with API key")
else:
    print("⚠️ OPENAI_API_KEY not found. AI features will be limited.")

def create_header():
    """Create application header"""
    return Header(
        Div(
            A("🤖 AI Resume Builder", href="/", cls="logo"),
            Nav(
                Ul(
                    Li(A("Home", href="/")),
                    Li(A("Builder", href="/builder")),
                    Li(A("Analyzer", href="/analyzer")),
                    cls="nav-links"
                )
            ),
            cls="header-content"
        ),
        cls="header"
    )

def create_footer():
    """Create application footer"""
    return Footer(
        Div(
            P("© 2024 AI Resume Builder MVP - Optimize your resume for ATS compliance"),
            cls="footer"
        ),
        cls="footer"
    )

@rt("/")
def get():
    """Home page with overview and file upload"""
    return Html(
        create_head(),
        Body(
            Div(
                create_header(),
                
                # Main Content Container
                Div(
                    # Hero Section
                    Div(
                        H1("AI-Powered Resume Optimization", cls="hero-title"),
                        P("Upload your resume and get instant ATS compatibility analysis with one-click AI optimization", 
                          cls="hero-subtitle"),
                        
                        # Stats Cards
                        Div(
                            Div(
                                Div("98%", cls="stat-number"),
                                Div("ATS Pass Rate", cls="stat-label"),
                                cls="stat-card"
                            ),
                            Div(
                                Div("30s", cls="stat-number"),
                                Div("Optimization Time", cls="stat-label"),
                                cls="stat-card"
                            ),
                            Div(
                                Div("AI", cls="stat-number"),
                                Div("Powered Analysis", cls="stat-label"),
                                cls="stat-card"
                            ),
                            cls="stats-grid"
                        ),
                        cls="hero-section"
                    ),
                    
                    # Upload Section
                    Div(
                        H2("Upload Your Resume", cls="upload-title"),
                        Div(
                            Div("📄", cls="upload-icon"),
                            Div("Drag and drop your resume here, or click to browse", cls="upload-text"),
                            Div("Supports PDF, DOCX, Markdown, and Text files", cls="upload-subtext"),
                            cls="upload-zone",
                            id="file-upload",
                            onclick="document.getElementById('file-input').click()"
                        ),
                        Input(type="file", id="file-input", accept=".pdf,.docx,.md,.txt", style="display: none;"),
                        cls="upload-section"
                    ),
                    
                    # Features Section
                    Div(
                        H2("Key Features", cls="features-title"),
                        Div(
                            Div(
                                Div(
                                    Div("🎯", cls="feature-icon"),
                                    H3("ATS Optimization", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Advanced AI analysis ensures your resume passes through Applicant Tracking Systems", cls="feature-description"),
                                cls="feature-card"
                            ),
                            Div(
                                Div(
                                    Div("🚀", cls="feature-icon"),
                                    H3("One-Click Enhancement", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Instantly optimize your resume with AI-powered content suggestions and keyword matching", cls="feature-description"),
                                cls="feature-card"
                            ),
                            Div(
                                Div(
                                    Div("📊", cls="feature-icon"),
                                    H3("Real-time Scoring", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Get immediate feedback on ATS compatibility with detailed scoring and recommendations", cls="feature-description"),
                                cls="feature-card"
                            ),
                            Div(
                                Div(
                                    Div("📁", cls="feature-icon"),
                                    H3("Multiple Formats", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Export your optimized resume in PDF, DOCX, Markdown, HTML, and text formats", cls="feature-description"),
                                cls="feature-card"
                            ),
                            Div(
                                Div(
                                    Div("🔍", cls="feature-icon"),
                                    H3("Keyword Analysis", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Identify missing keywords and optimize content to match job descriptions perfectly", cls="feature-description"),
                                cls="feature-card"
                            ),
                            Div(
                                Div(
                                    Div("⚡", cls="feature-icon"),
                                    H3("Instant Results", cls="feature-title"),
                                    cls="feature-header"
                                ),
                                P("Get professional-quality resume optimization in seconds, not hours", cls="feature-description"),
                                cls="feature-card"
                            ),
                            cls="features-grid"
                        ),
                        cls="features-section"
                    ),
                    cls="main-content"
                ),
                
                # Loading indicator
                Div(id="loading-container", cls="hidden", style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 2rem; border-radius: 1rem; box-shadow: 0 25px 50px rgba(0,0,0,0.2); z-index: 1000; border: 1px solid rgba(255,255,255,0.3);"),
                
                # Alert container
                Div(id="alert-container", style="position: fixed; top: 1rem; right: 1rem; z-index: 1000;"),
                
                create_footer(),
                cls="app-container"
            )
        )
    )

@rt("/builder")
def get():
    """Resume builder page with form and live preview"""
    return Html(
        create_head(),
        Body(
            Div(
                create_header(),
                
                Div(
                    H1("Resume Builder", cls="hero-title"),
                    
                    Div(
                        # Left Column - Form
                        Div(
                            # Contact Information
                            Div(
                                H2("Contact Information", cls="card-title"),
                                Div(
                                    Div(
                                        Label("Full Name", cls="form-label"),
                                        Input(type="text", id="full-name", cls="form-input resume-input", placeholder="John Doe"),
                                        cls="form-group"
                                    ),
                                    Div(
                                        Label("Email", cls="form-label"),
                                        Input(type="email", id="email", cls="form-input resume-input", placeholder="john@example.com"),
                                        cls="form-group"
                                    ),
                                    cls="grid grid-2"
                                ),
                                cls="card"
                            ),
                            Div(
                                H2("Additional Information", cls="card-title"),
                                Div(
                                    Div(
                                        Label("Phone", cls="form-label"),
                                        Input(type="tel", id="phone", cls="form-input resume-input", placeholder="(555) 123-4567"),
                                        cls="form-group"
                                    ),
                                    Div(
                                        Label("Location", cls="form-label"),
                                        Input(type="text", id="location", cls="form-input resume-input", placeholder="City, State"),
                                        cls="form-group"
                                    ),
                                    cls="grid grid-2"
                                ),
                            Div(
                                Div(
                                    Label("LinkedIn URL", cls="form-label"),
                                    Input(type="url", id="linkedin-url", cls="form-input resume-input", placeholder="https://linkedin.com/in/username"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("GitHub URL", cls="form-label"),
                                    Input(type="url", id="github-url", cls="form-input resume-input", placeholder="https://github.com/username"),
                                    cls="form-group"
                                ),
                                cls="grid grid-2"
                            ),
                            Div(
                                Label("Portfolio URL", cls="form-label"),
                                Input(type="url", id="portfolio-url", cls="form-input resume-input", placeholder="https://yourportfolio.com"),
                                cls="form-group"
                            ),
                            cls="card"
                        ),
                        
                        # Professional Summary
                        Div(
                            H2("Professional Summary", cls="card-title"),
                            Div(
                                Label("Professional Summary", cls="form-label"),
                                Textarea(id="professional-summary", cls="form-textarea resume-input", 
                                        placeholder="Write a compelling 2-3 sentence summary highlighting your experience and value proposition..."),
                                cls="form-group"
                            ),
                            cls="card"
                        ),
                        
                        # Work Experience (Simplified for MVP)
                        Div(
                            H2("Work Experience", cls="card-title"),
                            Div(
                                Div(
                                    Label("Job Title", cls="form-label"),
                                    Input(type="text", id="job-title", cls="form-input resume-input", placeholder="Software Engineer"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Company", cls="form-label"),
                                    Input(type="text", id="company", cls="form-input resume-input", placeholder="Tech Company Inc."),
                                    cls="form-group"
                                ),
                                cls="grid grid-2"
                            ),
                            Div(
                                Div(
                                    Label("Location", cls="form-label"),
                                    Input(type="text", id="work-location", cls="form-input resume-input", placeholder="San Francisco, CA"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Start Date", cls="form-label"),
                                    Input(type="text", id="start-date", cls="form-input resume-input", placeholder="01/2022"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("End Date", cls="form-label"),
                                    Input(type="text", id="end-date", cls="form-input resume-input", placeholder="Present"),
                                    cls="form-group"
                                ),
                                cls="grid grid-3"
                            ),
                            Div(
                                Label("Job Description (one bullet per line)", cls="form-label"),
                                Textarea(id="job-description-text", cls="form-textarea resume-input", 
                                        placeholder="• Developed web applications using React and Node.js\n• Improved system performance by 40%\n• Led team of 5 developers"),
                                cls="form-group"
                            ),
                            cls="card"
                        ),
                        
                        # Skills
                        Div(
                            H2("Skills", cls="card-title"),
                            Div(
                                Label("Technical Skills (comma-separated)", cls="form-label"),
                                Textarea(id="skills", cls="form-textarea resume-input", 
                                        placeholder="Python, JavaScript, React, Node.js, AWS, Docker, SQL, Git"),
                                cls="form-group"
                            ),
                            cls="card"
                        ),
                        
                        # Education
                        Div(
                            H2("Education", cls="card-title"),
                            Div(
                                Div(
                                    Label("Degree", cls="form-label"),
                                    Input(type="text", id="degree", cls="form-input resume-input", placeholder="Bachelor of Science in Computer Science"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Institution", cls="form-label"),
                                    Input(type="text", id="institution", cls="form-input resume-input", placeholder="University of Technology"),
                                    cls="form-group"
                                ),
                                cls="grid grid-2"
                            ),
                            Div(
                                Div(
                                    Label("Location", cls="form-label"),
                                    Input(type="text", id="edu-location", cls="form-input resume-input", placeholder="Boston, MA"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Graduation Date", cls="form-label"),
                                    Input(type="text", id="graduation-date", cls="form-input resume-input", placeholder="05/2020"),
                                    cls="form-group"
                                ),
                                cls="grid grid-2"
                            ),
                            cls="card"
                        ),
                        
                        # Job Description for Optimization
                        Div(
                            H2("Target Job Description", cls="card-title"),
                            P("Paste the job description you're applying for to get AI-powered optimization", 
                              cls="mb-2", style="color: #64748b;"),
                            Div(
                                Label("Job Description", cls="form-label"),
                                Textarea(id="job-description", cls="form-textarea", 
                                        placeholder="Paste the full job description here for AI optimization...",
                                        style="min-height: 150px;"),
                                cls="form-group"
                            ),
                            Div(
                                Button("🚀 One-Click Optimize", id="optimize-btn", cls="btn btn-primary btn-lg"),
                                Button("📊 Analyze ATS", id="analyze-btn", cls="btn btn-secondary btn-lg"),
                                cls="flex gap-2"
                            ),
                            cls="card"
                        ),
                        
                        # Export Options
                        Div(
                            H2("Export Resume", cls="card-title"),
                            Div(
                                Button("📄 PDF", cls="btn btn-outline export-btn", **{"data-format": "pdf"}),
                                Button("📝 DOCX", cls="btn btn-outline export-btn", **{"data-format": "docx"}),
                                Button("📋 Markdown", cls="btn btn-outline export-btn", **{"data-format": "md"}),
                                Button("🌐 HTML", cls="btn btn-outline export-btn", **{"data-format": "html"}),
                                Button("📄 Text", cls="btn btn-outline export-btn", **{"data-format": "txt"}),
                                cls="grid grid-3"
                            ),
                            cls="card"
                        )
                        , cls="form-column"), # End form-column
                    
                    # Right Column - Preview and Analysis
                    Div(
                        # Resume Preview
                        Div(
                            H2("Resume Preview", cls="card-title"),
                            Div(id="resume-preview", cls="resume-preview"),
                            cls="card"
                        ),
                        
                        # ATS Score
                        Div(
                            H2("ATS Compatibility Score", cls="card-title"),
                            Div(
                                P("Upload a resume and run ATS analysis to see your compatibility score", 
                                  cls="text-center", style="color: #64748b; padding: 2rem;"),
                                id="ats-score-container"),
                            cls="card"
                        ),
                        
                        # Recommendations
                        Div(id="recommendations-container", cls="card", style="display: none;"),
                        
                        # Keywords
                        Div(id="keywords-container", cls="card", style="display: none;")
                    , cls="preview-column")
                ),
                
                cls="container"
            ),
            
            # Loading and Alert containers
            Div(id="loading-container", cls="hidden"),
            Div(id="alert-container"),
            
            create_footer()
        )
    ),
    cls="main-content"
    )
@rt("/analyzer")
def get():
    """Standalone ATS analyzer page"""
    return Html(
        create_head(),
        Body(
            create_header(),
            
            Div(
                H1("ATS Compatibility Analyzer", cls="text-center mb-3"),
                P("Upload your resume to get detailed ATS compatibility analysis and recommendations", 
                  cls="text-center mb-3", style="color: #64748b;"),
                
                # File Upload
                Div(
                    H2("Upload Resume for Analysis", cls="card-title"),
                    Div(
                        Div("📊", cls="file-upload-icon"),
                        P("Upload your resume for comprehensive ATS analysis", cls="file-upload-text"),
                        P("Get detailed scoring, recommendations, and keyword analysis", cls="file-upload-hint"),
                        id="file-upload",
                        cls="file-upload"
                    ),
                    Input(type="file", id="file-input", accept=".pdf,.docx,.md,.txt", style="display: none;"),
                    cls="card"
                ),
                
                # Analysis Results (Hidden initially)
                Div(
                    Div(
                        # ATS Score
                        Div(
                            H2("ATS Compatibility Score", cls="card-title"),
                            Div(id="ats-score-container"),
                            cls="card"
                        ),
                        
                        # Detailed Breakdown
                        Div(
                            H2("Detailed Analysis", cls="card-title"),
                            Div(id="detailed-analysis-container"),
                            cls="card"
                        ),
                        
                        cls="grid grid-2"
                    ),
                    
                    # Recommendations
                    Div(id="recommendations-container", cls="card"),
                    
                    # Keywords Analysis
                    Div(id="keywords-container", cls="card"),
                    
                    id="analysis-results",
                    style="display: none;"
                ),
                
                cls="container"
            ),
            
            # Loading and Alert containers
            Div(id="loading-container", cls="hidden"),
            Div(id="alert-container"),
            
            create_footer()
        )
    )

@rt("/upload-resume", methods=["POST"])
async def upload_resume(request):
    """Handle resume file upload and parsing"""
    try:
        form = await request.form()
        file = form.get("file")
        
        if not file or not file.filename:
            return {"success": False, "error": "No file uploaded"}
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text from file
            text_content = file_processor.extract_text_from_file(tmp_file_path)
            
            # Parse resume using AI if available
            if ai_optimizer:
                resume = await ai_optimizer.parse_resume_from_text(text_content)
            else:
                # Fallback to basic parsing
                parsed_data = file_processor.parse_resume_text(text_content)
                resume = create_resume_from_parsed_data(parsed_data)
            
            return {
                "success": True,
                "resume": resume.model_dump(),
                "message": "Resume uploaded and parsed successfully"
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        return {"success": False, "error": f"Failed to process resume: {str(e)}"}

@rt("/optimize-resume", methods=["POST"])
async def optimize_resume(request):
    """Handle AI-powered resume optimization"""
    try:
        if not ai_optimizer:
            return {"success": False, "error": "AI optimization not available. Please set OPENAI_API_KEY."}
        
        data = await request.json()
        resume_data = data.get("resume")
        job_description = data.get("job_description", "")
        
        if not resume_data:
            return {"success": False, "error": "No resume data provided"}
        
        if not job_description.strip():
            return {"success": False, "error": "Job description is required for optimization"}
        
        # Convert dict to Resume object
        resume = Resume(**resume_data)
        
        # Perform one-click optimization
        optimized_resume, suggestions = await ai_optimizer.one_click_optimize(resume, job_description)
        
        return {
            "success": True,
            "optimized_resume": optimized_resume.model_dump(),
            "suggestions": [s.model_dump() for s in suggestions],
            "message": f"Resume optimized with {len(suggestions)} improvements"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Optimization failed: {str(e)}"}

@rt("/analyze-ats", methods=["POST"])
async def analyze_ats(request):
    """Handle ATS compatibility analysis"""
    try:
        data = await request.json()
        resume_data = data.get("resume")
        job_description = data.get("job_description", "")
        
        if not resume_data:
            return {"success": False, "error": "No resume data provided"}
        
        # Convert dict to Resume object
        resume = Resume(**resume_data)
        
        # Perform ATS analysis
        analysis = await ats_analyzer.analyze_resume(resume, job_description if job_description.strip() else None)
        
        return {
            "success": True,
            "analysis": analysis.model_dump(),
            "message": "ATS analysis completed"
        }
        
    except Exception as e:
        return {"success": False, "error": f"ATS analysis failed: {str(e)}"}

@rt("/export-resume", methods=["POST"])
async def export_resume(request):
    """Handle resume export in various formats"""
    try:
        data = await request.json()
        resume_data = data.get("resume")
        format = data.get("format", "pdf").lower()
        
        if not resume_data:
            return {"success": False, "error": "No resume data provided"}
        
        # Convert dict to Resume object
        resume = Resume(**resume_data)
        
        # Create temporary file for export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.{format}"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Export resume
            exported_path = resume_exporter.export_resume(resume, format, output_path)
            
            # Read file content
            with open(exported_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            content_types = {
                'pdf': 'application/pdf',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'md': 'text/markdown',
                'html': 'text/html',
                'txt': 'text/plain',
                'json': 'application/json'
            }
            
            content_type = content_types.get(format, 'application/octet-stream')
            
            return Response(
                content=content,
                media_type=content_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_path):
                os.unlink(output_path)
            
    except Exception as e:
        return {"success": False, "error": f"Export failed: {str(e)}"}

def create_resume_from_parsed_data(parsed_data: Dict[str, Any]) -> Resume:
    """Create Resume object from parsed data (fallback when AI is not available)"""
    contact_info = ContactInfo(
        full_name=parsed_data.get('contact_info', {}).get('full_name', ''),
        email=parsed_data.get('contact_info', {}).get('email', ''),
        phone=parsed_data.get('contact_info', {}).get('phone'),
        location=parsed_data.get('contact_info', {}).get('location'),
        linkedin_url=parsed_data.get('contact_info', {}).get('linkedin_url'),
        github_url=parsed_data.get('contact_info', {}).get('github_url'),
        portfolio_url=parsed_data.get('contact_info', {}).get('portfolio_url')
    )
    
    # Convert skills to Skill objects
    skills = []
    for skill_name in parsed_data.get('skills', []):
        skills.append(Skill(name=skill_name, category=SkillCategory.TECHNICAL))
    
    # Convert experience to WorkExperience objects
    work_experience = []
    for exp_data in parsed_data.get('experience', []):
        work_experience.append(WorkExperience(
            job_title=exp_data.get('job_title', ''),
            company=exp_data.get('company', ''),
            start_date=exp_data.get('date_range', '').split(' - ')[0] if ' - ' in exp_data.get('date_range', '') else '',
            end_date=exp_data.get('date_range', '').split(' - ')[1] if ' - ' in exp_data.get('date_range', '') else None,
            description=[]
        ))
    
    # Convert education to Education objects
    education = []
    for edu_data in parsed_data.get('education', []):
        education.append(Education(
            degree=edu_data.get('degree', ''),
            institution=edu_data.get('institution', ''),
            graduation_date=edu_data.get('date', '')
        ))
    
    return Resume(
        contact_info=contact_info,
        professional_summary=None,
        work_experience=work_experience,
        skills=skills,
        education=education
    )

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting AI Resume Builder MVP on port {port}")
    print(f"📝 Features: File upload, AI optimization, ATS analysis, Multi-format export")
    print(f"🤖 AI Status: {'Enabled' if ai_optimizer else 'Disabled (set OPENAI_API_KEY to enable)'}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
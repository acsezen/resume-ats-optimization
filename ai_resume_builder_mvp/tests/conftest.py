"""
Pytest configuration and fixtures for AI Resume Builder MVP tests
"""
import pytest
import asyncio
import tempfile
import os
from typing import Generator
from models.resume_models import (
    Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory
)
from services.ats_analyzer import ATSAnalyzer
from processors.file_processor import FileProcessor, ResumeExporter


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_contact_info() -> ContactInfo:
    """Create sample contact information for testing"""
    return ContactInfo(
        full_name="John Doe",
        email="john.doe@example.com",
        phone="(555) 123-4567",
        location="San Francisco, CA",
        linkedin_url="https://linkedin.com/in/johndoe",
        github_url="https://github.com/johndoe",
        portfolio_url="https://johndoe.dev"
    )


@pytest.fixture
def sample_skills() -> list[Skill]:
    """Create sample skills for testing"""
    return [
        Skill(name="Python", category=SkillCategory.PROGRAMMING),
        Skill(name="JavaScript", category=SkillCategory.PROGRAMMING),
        Skill(name="React", category=SkillCategory.FRAMEWORK),
        Skill(name="Node.js", category=SkillCategory.FRAMEWORK),
        Skill(name="AWS", category=SkillCategory.CLOUD),
        Skill(name="Docker", category=SkillCategory.TOOLS),
        Skill(name="PostgreSQL", category=SkillCategory.DATABASE),
        Skill(name="Git", category=SkillCategory.TOOLS),
        Skill(name="Machine Learning", category=SkillCategory.TECHNICAL),
        Skill(name="Leadership", category=SkillCategory.SOFT_SKILLS),
        Skill(name="Spanish", category=SkillCategory.LANGUAGE),
        Skill(name="AWS Certified", category=SkillCategory.CERTIFICATION)
    ]


@pytest.fixture
def sample_work_experience() -> list[WorkExperience]:
    """Create sample work experience for testing"""
    return [
        WorkExperience(
            job_title="Senior Software Engineer",
            company="Tech Innovations Inc.",
            location="San Francisco, CA",
            start_date="01/2022",
            end_date="Present",
            description=[
                "Led development of microservices architecture serving 1M+ users daily",
                "Improved system performance by 40% through optimization and caching strategies",
                "Mentored team of 5 junior developers and conducted code reviews",
                "Implemented CI/CD pipelines reducing deployment time from 2 hours to 15 minutes",
                "Collaborated with product team to deliver 15+ features on schedule"
            ],
            key_achievements=[
                "Reduced system latency by 40%",
                "Led team of 5 developers",
                "Delivered 15+ features on time"
            ]
        ),
        WorkExperience(
            job_title="Software Engineer",
            company="StartupXYZ",
            location="Palo Alto, CA",
            start_date="06/2020",
            end_date="12/2021",
            description=[
                "Developed full-stack web applications using React and Node.js",
                "Built RESTful APIs handling 100K+ requests per day",
                "Integrated third-party services and payment processing systems",
                "Participated in agile development process and sprint planning"
            ]
        )
    ]


@pytest.fixture
def sample_education() -> list[Education]:
    """Create sample education for testing"""
    return [
        Education(
            institution="University of California, Berkeley",
            degree="Bachelor of Science in Computer Science",
            location="Berkeley, CA",
            graduation_date="05/2020",
            gpa=3.8,
            honors=["Magna Cum Laude", "Dean's List"],
            relevant_coursework=["Data Structures", "Algorithms", "Machine Learning", "Database Systems"]
        )
    ]


@pytest.fixture
def sample_resume(
    sample_contact_info: ContactInfo,
    sample_skills: list[Skill],
    sample_work_experience: list[WorkExperience],
    sample_education: list[Education]
) -> Resume:
    """Create a complete sample resume for testing"""
    return Resume(
        contact_info=sample_contact_info,
        professional_summary="Experienced software engineer with 4+ years developing scalable web applications and microservices. Proven track record of improving system performance and leading development teams. Passionate about clean code, system architecture, and mentoring junior developers.",
        work_experience=sample_work_experience,
        skills=sample_skills,
        education=sample_education,
        target_role="Senior Software Engineer",
        industry="Technology"
    )


@pytest.fixture
def sample_job_description() -> str:
    """Create sample job description for testing"""
    return """
    Senior Software Engineer - Full Stack Development
    
    Company: TechCorp Solutions
    Location: San Francisco, CA (Remote friendly)
    
    About the Role:
    We are seeking a Senior Software Engineer to join our growing engineering team. You will be responsible for designing, developing, and maintaining scalable web applications that serve millions of users worldwide.
    
    Key Responsibilities:
    • Design and develop full-stack web applications using modern technologies
    • Build and maintain microservices architecture
    • Collaborate with cross-functional teams including product, design, and DevOps
    • Mentor junior developers and conduct code reviews
    • Participate in system architecture decisions and technical planning
    • Ensure high code quality through testing and best practices
    
    Required Qualifications:
    • 5+ years of experience in software development
    • Strong proficiency in Python, JavaScript, and modern web frameworks
    • Experience with React, Node.js, and RESTful API development
    • Knowledge of cloud platforms (AWS, Azure, or GCP)
    • Experience with containerization (Docker, Kubernetes)
    • Familiarity with database systems (PostgreSQL, MongoDB)
    • Understanding of CI/CD pipelines and DevOps practices
    • Bachelor's degree in Computer Science or related field
    
    Preferred Qualifications:
    • Experience with microservices architecture
    • Knowledge of machine learning and data science
    • Leadership experience and team mentoring
    • Agile/Scrum development experience
    • Open source contributions
    """


@pytest.fixture
def ats_analyzer() -> ATSAnalyzer:
    """Create ATS analyzer instance for testing"""
    return ATSAnalyzer()


@pytest.fixture
def file_processor() -> FileProcessor:
    """Create file processor instance for testing"""
    return FileProcessor()


@pytest.fixture
def resume_exporter() -> ResumeExporter:
    """Create resume exporter instance for testing"""
    return ResumeExporter()


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create temporary directory for file operations"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_openai_api_key(monkeypatch):
    """Mock OpenAI API key for testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key-12345")


@pytest.fixture
def sample_resume_text() -> str:
    """Sample resume text for parsing tests"""
    return """
    John Doe
    Software Engineer
    john.doe@example.com | (555) 123-4567 | San Francisco, CA
    LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 4+ years developing scalable web applications.
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, TypeScript
    Frameworks: React, Node.js, Django, Flask
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Docker, Kubernetes
    Tools: Git, Jenkins, JIRA
    
    WORK EXPERIENCE
    
    Senior Software Engineer | Tech Corp | San Francisco, CA | 01/2022 - Present
    • Led development of microservices architecture serving 1M+ users
    • Improved system performance by 40% through optimization
    • Mentored team of 5 junior developers
    
    Software Engineer | StartupXYZ | Palo Alto, CA | 06/2020 - 12/2021
    • Developed full-stack web applications using React and Node.js
    • Built RESTful APIs handling 100K+ requests per day
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of California, Berkeley | Berkeley, CA | 2020
    GPA: 3.8, Magna Cum Laude
    """


@pytest.fixture
def invalid_resume_data() -> dict:
    """Invalid resume data for error testing"""
    return {
        "contact_info": {
            "full_name": "",  # Invalid: empty name
            "email": "invalid-email",  # Invalid: bad email format
            "phone": "123",  # Invalid: too short
            "location": ""
        },
        "professional_summary": "",
        "work_experience": [],
        "skills": [],
        "education": []
    }


@pytest.fixture
def large_resume_data(sample_contact_info, sample_skills) -> Resume:
    """Create a resume with large amounts of data for stress testing"""
    # Create many work experiences
    work_experiences = []
    for i in range(20):
        work_experiences.append(
            WorkExperience(
                job_title=f"Software Engineer {i}",
                company=f"Company {i}",
                location="San Francisco, CA",
                start_date=f"01/202{i % 10}",
                end_date=f"12/202{i % 10}",
                description=[f"Task {j} for company {i}" for j in range(10)]
            )
        )
    
    # Create many education entries
    education_entries = []
    for i in range(10):
        education_entries.append(
            Education(
                institution=f"University {i}",
                degree=f"Degree {i}",
                location="Berkeley, CA",
                graduation_date=f"05/202{i % 10}"
            )
        )
    
    return Resume(
        contact_info=sample_contact_info,
        professional_summary="Very long professional summary " * 50,
        work_experience=work_experiences,
        skills=sample_skills * 10,  # Duplicate skills
        education=education_entries,
        target_role="Senior Software Engineer",
        industry="Technology"
    )


def create_sample_resume():
    """Create a sample resume for testing - standalone function"""
    from models.resume_models import Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory
    
    contact_info = ContactInfo(
        full_name="John Doe",
        email="john.doe@example.com",
        phone="(555) 123-4567",
        location="San Francisco, CA",
        linkedin_url="https://linkedin.com/in/johndoe",
        github_url="https://github.com/johndoe",
        portfolio_url="https://johndoe.dev"
    )
    
    skills = [
        Skill(name="Python", category=SkillCategory.PROGRAMMING),
        Skill(name="JavaScript", category=SkillCategory.PROGRAMMING),
        Skill(name="React", category=SkillCategory.FRAMEWORK),
        Skill(name="Node.js", category=SkillCategory.FRAMEWORK),
        Skill(name="AWS", category=SkillCategory.CLOUD),
        Skill(name="Docker", category=SkillCategory.TOOLS),
        Skill(name="PostgreSQL", category=SkillCategory.DATABASE),
        Skill(name="Git", category=SkillCategory.TOOLS),
        Skill(name="Machine Learning", category=SkillCategory.TECHNICAL),
        Skill(name="Leadership", category=SkillCategory.SOFT_SKILLS)
    ]
    
    work_experience = [
        WorkExperience(
            job_title="Senior Software Engineer",
            company="Tech Innovations Inc.",
            location="San Francisco, CA",
            start_date="01/2022",
            end_date="Present",
            description=[
                "Led development of microservices architecture serving 1M+ users daily",
                "Improved system performance by 40% through optimization and caching strategies",
                "Mentored team of 5 junior developers and conducted code reviews"
            ]
        )
    ]
    
    education = [
        Education(
            institution="University of California, Berkeley",
            degree="Bachelor of Science in Computer Science",
            location="Berkeley, CA",
            graduation_date="05/2020"
        )
    ]
    
    return Resume(
        contact_info=contact_info,
        professional_summary="Experienced software engineer with 4+ years developing scalable web applications.",
        work_experience=work_experience,
        skills=skills,
        education=education,
        target_role="Senior Software Engineer",
        industry="Technology"
    )

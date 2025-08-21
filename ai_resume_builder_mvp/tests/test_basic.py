"""
Basic tests for AI Resume Builder MVP
"""
import pytest
from models.resume_models import Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory
from services.ats_analyzer import ATSAnalyzer
from processors.file_processor import ResumeExporter


def test_contact_info_creation():
    """Test ContactInfo model creation"""
    contact = ContactInfo(
        full_name="John Doe",
        email="john@example.com",
        phone="555-1234",
        location="San Francisco, CA"
    )
    assert contact.full_name == "John Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "555-1234"
    assert contact.location == "San Francisco, CA"


def test_skill_creation():
    """Test Skill model creation"""
    skill = Skill(name="Python", category=SkillCategory.PROGRAMMING)
    assert skill.name == "Python"
    assert skill.category == SkillCategory.PROGRAMMING


def test_work_experience_creation():
    """Test WorkExperience model creation"""
    work_exp = WorkExperience(
        job_title="Software Engineer",
        company="Tech Corp",
        location="San Francisco, CA",
        start_date="01/2022",
        end_date="Present",
        description=["Developed web applications", "Led team projects"]
    )
    assert work_exp.job_title == "Software Engineer"
    assert work_exp.company == "Tech Corp"
    assert len(work_exp.description) == 2


def test_education_creation():
    """Test Education model creation"""
    education = Education(
        institution="UC Berkeley",
        degree="BS Computer Science",
        location="Berkeley, CA",
        graduation_date="05/2020"
    )
    assert education.institution == "UC Berkeley"
    assert education.degree == "BS Computer Science"


def test_resume_creation():
    """Test Resume model creation"""
    contact = ContactInfo(
        full_name="John Doe",
        email="john@example.com",
        phone="555-1234",
        location="San Francisco, CA"
    )
    
    skills = [
        Skill(name="Python", category=SkillCategory.PROGRAMMING),
        Skill(name="JavaScript", category=SkillCategory.PROGRAMMING)
    ]
    
    resume = Resume(
        contact_info=contact,
        professional_summary="Experienced software engineer",
        work_experience=[],
        skills=skills,
        education=[],
        target_role="Software Engineer",
        industry="Technology"
    )
    
    assert resume.contact_info.full_name == "John Doe"
    assert len(resume.skills) == 2
    assert resume.target_role == "Software Engineer"


def test_ats_analyzer_initialization():
    """Test ATS analyzer can be initialized"""
    analyzer = ATSAnalyzer()
    assert analyzer is not None


def test_resume_exporter_initialization():
    """Test resume exporter can be initialized"""
    exporter = ResumeExporter()
    assert exporter is not None


def test_skill_categories():
    """Test all skill categories are available"""
    categories = [
        SkillCategory.PROGRAMMING,
        SkillCategory.FRAMEWORK,
        SkillCategory.DATABASE,
        SkillCategory.CLOUD,
        SkillCategory.TOOLS,
        SkillCategory.TECHNICAL,
        SkillCategory.SOFT_SKILLS,
        SkillCategory.LANGUAGE,
        SkillCategory.CERTIFICATION
    ]
    
    for category in categories:
        skill = Skill(name="Test Skill", category=category)
        assert skill.category == category
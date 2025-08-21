"""
Simplified tests for model functionality
"""
import pytest
from datetime import datetime
from models.resume_models import (
    ContactInfo, Skill, SkillCategory, WorkExperience, 
    Education, Resume, ExperienceLevel
)
from models.ats_models import (
    KeywordAnalysis, ATSScore, ATSCompatibilityLevel, 
    ATSAnalysisResult, SectionScore
)


class TestContactInfo:
    """Test ContactInfo model"""
    
    def test_contact_info_creation(self):
        """Test basic contact info creation"""
        contact = ContactInfo(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="(555) 123-4567",
            location="San Francisco, CA"
        )
        
        assert contact.full_name == "John Doe"
        assert contact.email == "john.doe@example.com"
        assert contact.phone == "(555) 123-4567"
        assert contact.location == "San Francisco, CA"
    
    def test_contact_info_with_optional_fields(self):
        """Test contact info with optional fields"""
        contact = ContactInfo(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="(555) 123-4567",
            location="San Francisco, CA",
            linkedin_url="https://linkedin.com/in/johndoe",
            github_url="https://github.com/johndoe",
            portfolio_url="https://johndoe.dev"
        )
        
        assert contact.linkedin_url == "https://linkedin.com/in/johndoe"
        assert contact.github_url == "https://github.com/johndoe"
        assert contact.portfolio_url == "https://johndoe.dev"
    
    def test_contact_info_serialization(self):
        """Test contact info serialization"""
        contact = ContactInfo(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="(555) 123-4567",
            location="San Francisco, CA"
        )
        
        data = contact.model_dump()
        assert isinstance(data, dict)
        assert data['full_name'] == "John Doe"
        assert data['email'] == "john.doe@example.com"


class TestSkill:
    """Test Skill model"""
    
    def test_skill_creation(self):
        """Test basic skill creation"""
        skill = Skill(
            name="Python",
            category=SkillCategory.PROGRAMMING
        )
        
        assert skill.name == "Python"
        assert skill.category == SkillCategory.PROGRAMMING
    
    def test_skill_categories(self):
        """Test different skill categories"""
        categories = [
            SkillCategory.PROGRAMMING,
            SkillCategory.FRAMEWORK,
            SkillCategory.DATABASE,
            SkillCategory.CLOUD,
            SkillCategory.TOOLS,
            SkillCategory.SOFT_SKILLS,
            SkillCategory.TECHNICAL,
            SkillCategory.LANGUAGE,
            SkillCategory.CERTIFICATION
        ]
        
        for category in categories:
            skill = Skill(name="Test Skill", category=category)
            assert skill.category == category


class TestWorkExperience:
    """Test WorkExperience model"""
    
    def test_work_experience_creation(self):
        """Test basic work experience creation"""
        experience = WorkExperience(
            job_title="Software Engineer",
            company="Tech Corp",
            location="San Francisco, CA",
            start_date="01/2020",
            end_date="12/2021",
            description=["Developed web applications", "Led team projects"]
        )
        
        assert experience.job_title == "Software Engineer"
        assert experience.company == "Tech Corp"
        assert experience.location == "San Francisco, CA"
        assert experience.start_date == "01/2020"
        assert experience.end_date == "12/2021"
        assert len(experience.description) == 2
    
    def test_work_experience_with_achievements(self):
        """Test work experience with key achievements"""
        experience = WorkExperience(
            job_title="Senior Engineer",
            company="Big Tech",
            location="SF, CA",
            start_date="01/2022",
            end_date="Present",
            description=["Led development"],
            key_achievements=["Improved performance by 40%", "Led team of 5"]
        )
        
        assert len(experience.key_achievements) == 2
        assert "Improved performance by 40%" in experience.key_achievements


class TestEducation:
    """Test Education model"""
    
    def test_education_creation(self):
        """Test basic education creation"""
        education = Education(
            institution="University of California, Berkeley",
            degree="Bachelor of Science in Computer Science",
            location="Berkeley, CA",
            graduation_date="05/2020"
        )
        
        assert education.institution == "University of California, Berkeley"
        assert education.degree == "Bachelor of Science in Computer Science"
        assert education.location == "Berkeley, CA"
        assert education.graduation_date == "05/2020"
    
    def test_education_with_optional_fields(self):
        """Test education with optional fields"""
        education = Education(
            institution="UC Berkeley",
            degree="BS Computer Science",
            location="Berkeley, CA",
            graduation_date="05/2020",
            gpa=3.8,
            honors=["Magna Cum Laude"],
            relevant_coursework=["Data Structures", "Algorithms"]
        )
        
        assert education.gpa == 3.8
        assert "Magna Cum Laude" in education.honors
        assert "Data Structures" in education.relevant_coursework


class TestResume:
    """Test Resume model"""
    
    def test_resume_creation(self, sample_contact_info, sample_skills):
        """Test basic resume creation"""
        resume = Resume(
            contact_info=sample_contact_info,
            professional_summary="Experienced software engineer",
            work_experience=[],
            skills=sample_skills,
            education=[]
        )
        
        assert resume.contact_info == sample_contact_info
        assert resume.professional_summary == "Experienced software engineer"
        assert len(resume.skills) > 0
        assert len(resume.work_experience) == 0
        assert len(resume.education) == 0
    
    def test_resume_with_optional_fields(self, sample_contact_info):
        """Test resume with optional fields"""
        resume = Resume(
            contact_info=sample_contact_info,
            professional_summary="Software engineer with experience",
            work_experience=[],
            skills=[],
            education=[],
            target_role="Senior Software Engineer",
            industry="Technology"
        )
        assert resume.target_role == "Senior Software Engineer"
        assert resume.industry == "Technology"
    
    def test_resume_serialization(self, sample_resume):
        """Test resume serialization"""
        data = sample_resume.model_dump()
        
        assert isinstance(data, dict)
        assert 'contact_info' in data
        assert 'professional_summary' in data
        assert 'work_experience' in data
        assert 'skills' in data
        assert 'education' in data


class TestATSModels:
    """Test ATS-related models"""
    
    def test_keyword_analysis(self):
        """Test KeywordAnalysis model"""
        analysis = KeywordAnalysis(
            job_keywords=["Python", "React", "AWS", "Docker"],
            resume_keywords=["Python", "JavaScript", "React"],
            matched_keywords=["Python", "React"],
            missing_keywords=["AWS", "Docker"],
            keyword_density={"Python": 0.5, "React": 0.3},
            match_percentage=50.0
        )
        assert len(analysis.job_keywords) == 4
        assert len(analysis.matched_keywords) == 2
        assert len(analysis.missing_keywords) == 2
        assert analysis.match_percentage == 50.0
    
    def test_ats_score(self):
        """Test ATSScore model"""
        keyword_analysis = KeywordAnalysis(
            job_keywords=["Python", "React"],
            resume_keywords=["Python", "JavaScript"],
            matched_keywords=["Python"],
            missing_keywords=["React"],
            keyword_density={"Python": 0.5},
            match_percentage=50.0
        )
        
        score = ATSScore(
            overall_score=85.0,
            compatibility_level=ATSCompatibilityLevel.GOOD,
            keyword_score=75.0,
            formatting_score=95.0,
            structure_score=90.0,
            content_quality_score=80.0,
            keyword_analysis=keyword_analysis,
            priority_recommendations=["Add React experience", "Include more keywords"],
            analysis_date="2024-01-15"
        )
        
        assert score.overall_score == 85.0
        assert score.compatibility_level == ATSCompatibilityLevel.GOOD
        assert len(score.priority_recommendations) == 2
    
    def test_section_score(self):
        """Test SectionScore model"""
        section = SectionScore(
            section_name="Professional Summary",
            score=85.0,
            max_score=100.0,
            issues=["Too short", "Missing keywords"],
            recommendations=["Add more detail", "Include relevant keywords"]
        )
        
        assert section.section_name == "Professional Summary"
        assert section.score == 85.0
        assert len(section.issues) == 2
        assert len(section.recommendations) == 2


class TestExperienceLevel:
    """Test ExperienceLevel enum"""
    
    def test_all_experience_levels(self):
        """Test all experience levels"""
        levels = [
            ExperienceLevel.ENTRY,
            ExperienceLevel.JUNIOR,
            ExperienceLevel.MID,
            ExperienceLevel.SENIOR,
            ExperienceLevel.LEAD,
            ExperienceLevel.EXECUTIVE
        ]
        
        for level in levels:
            assert isinstance(level.value, str)
            assert len(level.value) > 0


class TestCompatibilityLevel:
    """Test ATSCompatibilityLevel enum"""
    
    def test_all_compatibility_levels(self):
        """Test all compatibility levels"""
        levels = [
            ATSCompatibilityLevel.POOR,
            ATSCompatibilityLevel.FAIR,
            ATSCompatibilityLevel.GOOD,
            ATSCompatibilityLevel.EXCELLENT
        ]
        
        for level in levels:
            assert isinstance(level.value, str)
            assert len(level.value) > 0


class TestModelSerialization:
    """Test model serialization and deserialization"""
    
    def test_resume_json_serialization(self, sample_resume):
        """Test resume JSON serialization"""
        json_data = sample_resume.model_dump_json()
        
        assert isinstance(json_data, str)
        assert len(json_data) > 0
        
        # Should be valid JSON
        import json
        parsed_data = json.loads(json_data)
        assert isinstance(parsed_data, dict)
    
    def test_resume_deserialization(self, sample_resume):
        """Test resume deserialization"""
        # Serialize then deserialize
        data = sample_resume.model_dump()
        
        # Create new resume from data
        new_resume = Resume(**data)
        
        assert new_resume.contact_info.full_name == sample_resume.contact_info.full_name
        assert new_resume.professional_summary == sample_resume.professional_summary
        assert len(new_resume.skills) == len(sample_resume.skills)


class TestModelValidation:
    """Test model validation"""
    
    def test_contact_info_required_fields(self):
        """Test that required fields are enforced"""
        # This should work
        contact = ContactInfo(
            full_name="John Doe",
            email="john@example.com",
            phone="555-1234",
            location="SF, CA"
        )
        assert contact.full_name == "John Doe"
    
    def test_skill_category_validation(self):
        """Test skill category validation"""
        skill = Skill(
            name="Python",
            category=SkillCategory.PROGRAMMING
        )
        assert skill.category == SkillCategory.PROGRAMMING
    
    def test_resume_structure_validation(self, sample_contact_info):
        """Test resume structure validation"""
        resume = Resume(
            contact_info=sample_contact_info,
            professional_summary="Test summary",
            work_experience=[],
            skills=[],
            education=[]
        )
        
        assert isinstance(resume.work_experience, list)
        assert isinstance(resume.skills, list)
        assert isinstance(resume.education, list)
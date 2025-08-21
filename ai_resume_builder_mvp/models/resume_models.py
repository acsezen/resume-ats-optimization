"""
Core data models for resume structure and content.
Designed for ATS compatibility and AI optimization.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, date

class ExperienceLevel(str, Enum):
    """Professional experience levels"""
    ENTRY = "entry"
    JUNIOR = "junior" 
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class SkillCategory(str, Enum):
    """Skill categorization for better ATS parsing"""
    TECHNICAL = "technical"
    PROGRAMMING = "programming"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    TOOLS = "tools"
    SOFT_SKILLS = "soft_skills"
    LANGUAGE = "language"
    CERTIFICATION = "certification"

class ContactInfo(BaseModel):
    """Personal contact information"""
    full_name: str = Field(description="Full name as it should appear on resume")
    email: str = Field(description="Professional email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="City, State or City, Country")
    linkedin_url: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    portfolio_url: Optional[str] = Field(default=None, description="Portfolio or personal website")
    github_url: Optional[str] = Field(default=None, description="GitHub profile URL")

class Skill(BaseModel):
    """Individual skill with categorization"""
    name: str = Field(description="Skill name")
    category: SkillCategory = Field(description="Skill category for ATS parsing")
    proficiency: Optional[str] = Field(default=None, description="Proficiency level (Beginner, Intermediate, Advanced, Expert)")
    years_experience: Optional[int] = Field(default=None, description="Years of experience with this skill")

class WorkExperience(BaseModel):
    """Work experience entry"""
    job_title: str = Field(description="Job title/position")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    start_date: str = Field(description="Start date (MM/YYYY format)")
    end_date: Optional[str] = Field(default=None, description="End date (MM/YYYY format) or 'Present'")
    description: List[str] = Field(default=[], description="List of bullet points describing responsibilities and achievements")
    key_achievements: List[str] = Field(default=[], description="Quantified achievements and results")

class Education(BaseModel):
    """Education entry"""
    institution: str = Field(description="School/University name")
    degree: str = Field(description="Degree type and field of study")
    location: Optional[str] = Field(default=None, description="Institution location")
    graduation_date: Optional[str] = Field(default=None, description="Graduation date (MM/YYYY)")
    gpa: Optional[float] = Field(default=None, description="GPA if notable (3.5+)")
    honors: List[str] = Field(default=[], description="Academic honors, awards, or distinctions")
    relevant_coursework: List[str] = Field(default=[], description="Relevant courses for the target role")

class Project(BaseModel):
    """Project entry for showcasing work"""
    name: str = Field(description="Project name")
    description: str = Field(description="Brief project description")
    technologies: List[str] = Field(default=[], description="Technologies and tools used")
    url: Optional[str] = Field(default=None, description="Project URL or repository link")
    date: Optional[str] = Field(default=None, description="Project completion date")
    highlights: List[str] = Field(default=[], description="Key achievements or results")

class Certification(BaseModel):
    """Professional certification"""
    name: str = Field(description="Certification name")
    issuer: str = Field(description="Issuing organization")
    date_obtained: Optional[str] = Field(default=None, description="Date obtained (MM/YYYY)")
    expiry_date: Optional[str] = Field(default=None, description="Expiry date if applicable")
    credential_id: Optional[str] = Field(default=None, description="Credential ID or verification number")
    url: Optional[str] = Field(default=None, description="Verification URL")

class Resume(BaseModel):
    """Complete resume structure optimized for ATS"""
    # Core Information
    contact_info: ContactInfo = Field(description="Personal contact information")
    professional_summary: Optional[str] = Field(default=None, description="Professional summary or objective statement")
    
    # Experience and Skills
    work_experience: List[WorkExperience] = Field(default=[], description="Work history in reverse chronological order")
    skills: List[Skill] = Field(default=[], description="Technical and soft skills")
    education: List[Education] = Field(default=[], description="Educational background")
    
    # Optional Sections
    projects: List[Project] = Field(default=[], description="Notable projects")
    certifications: List[Certification] = Field(default=[], description="Professional certifications")
    languages: List[str] = Field(default=[], description="Languages spoken")
    volunteer_experience: List[WorkExperience] = Field(default=[], description="Volunteer work")
    
    # Metadata
    target_role: Optional[str] = Field(default=None, description="Target job title/role")
    industry: Optional[str] = Field(default=None, description="Target industry")
    experience_level: Optional[ExperienceLevel] = Field(default=None, description="Overall experience level")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

class ResumeSection(str, Enum):
    """Resume sections for targeted optimization"""
    PROFESSIONAL_SUMMARY = "professional_summary"
    WORK_EXPERIENCE = "work_experience"
    SKILLS = "skills"
    EDUCATION = "education"
    PROJECTS = "projects"
    CERTIFICATIONS = "certifications"

class OptimizationRequest(BaseModel):
    """Request for AI-powered resume optimization"""
    resume: Resume = Field(description="Current resume data")
    job_description: Optional[str] = Field(default=None, description="Target job description")
    target_sections: List[ResumeSection] = Field(default=[], description="Sections to optimize")
    optimization_focus: List[str] = Field(default=[], description="Specific areas to focus on (keywords, achievements, etc.)")
    preserve_content: bool = Field(default=True, description="Whether to preserve existing content structure")
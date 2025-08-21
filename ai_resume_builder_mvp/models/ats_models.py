"""
ATS analysis and scoring models.
Used for compatibility checking and optimization recommendations.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class ATSCompatibilityLevel(str, Enum):
    """ATS compatibility levels"""
    EXCELLENT = "excellent"  # 90-100%
    GOOD = "good"           # 75-89%
    FAIR = "fair"           # 60-74%
    POOR = "poor"           # Below 60%

class FormattingIssue(BaseModel):
    """Formatting issue detected by ATS analyzer"""
    issue_type: str = Field(description="Type of formatting issue")
    description: str = Field(description="Detailed description of the issue")
    location: Optional[str] = Field(default=None, description="Where the issue occurs")
    severity: str = Field(description="Severity level: critical, warning, info")
    recommendation: str = Field(description="How to fix the issue")

class KeywordAnalysis(BaseModel):
    """Keyword matching analysis results"""
    job_keywords: List[str] = Field(default=[], description="Keywords extracted from job description")
    resume_keywords: List[str] = Field(default=[], description="Keywords found in resume")
    matched_keywords: List[str] = Field(default=[], description="Keywords that match between job and resume")
    missing_keywords: List[str] = Field(default=[], description="Important keywords missing from resume")
    keyword_density: Dict[str, float] = Field(default={}, description="Frequency of keywords in resume")
    match_percentage: float = Field(description="Percentage of job keywords found in resume")

class SectionScore(BaseModel):
    """Score for individual resume section"""
    section_name: str = Field(description="Name of the resume section")
    score: float = Field(description="Section score (0-100)")
    max_score: float = Field(description="Maximum possible score for this section")
    issues: List[str] = Field(default=[], description="Issues found in this section")
    recommendations: List[str] = Field(default=[], description="Recommendations for improvement")

class ATSScore(BaseModel):
    """Comprehensive ATS compatibility score"""
    overall_score: float = Field(description="Overall ATS compatibility score (0-100)")
    compatibility_level: ATSCompatibilityLevel = Field(description="Compatibility level category")
    
    # Detailed scoring breakdown
    keyword_score: float = Field(description="Keyword matching score (0-100)")
    formatting_score: float = Field(description="Formatting compatibility score (0-100)")
    structure_score: float = Field(description="Resume structure score (0-100)")
    content_quality_score: float = Field(description="Content quality score (0-100)")
    
    # Section-specific scores
    section_scores: List[SectionScore] = Field(default=[], description="Scores for individual sections")
    
    # Analysis details
    keyword_analysis: KeywordAnalysis = Field(description="Detailed keyword analysis")
    formatting_issues: List[FormattingIssue] = Field(default=[], description="Formatting issues found")
    
    # Recommendations
    priority_recommendations: List[str] = Field(default=[], description="High-priority recommendations")
    general_recommendations: List[str] = Field(default=[], description="General improvement suggestions")
    
    # Metadata
    analysis_date: str = Field(description="Date of analysis")
    job_title_analyzed: Optional[str] = Field(default=None, description="Job title used for analysis")

class CompetitorAnalysis(BaseModel):
    """Analysis comparing resume to typical requirements"""
    industry_standards: Dict[str, Any] = Field(default={}, description="Industry standard requirements")
    skill_gaps: List[str] = Field(default=[], description="Skills commonly required but missing")
    experience_comparison: Dict[str, Any] = Field(default={}, description="Experience level comparison")
    improvement_areas: List[str] = Field(default=[], description="Areas for improvement")

class OptimizationSuggestion(BaseModel):
    """AI-generated optimization suggestion"""
    section: str = Field(description="Resume section to optimize")
    current_content: str = Field(description="Current content")
    suggested_content: str = Field(description="AI-suggested improved content")
    reasoning: str = Field(description="Why this change is recommended")
    impact_score: float = Field(description="Expected impact on ATS score (0-10)")
    keywords_added: List[str] = Field(default=[], description="Keywords that would be added")

class ATSAnalysisResult(BaseModel):
    """Complete ATS analysis result"""
    ats_score: ATSScore = Field(description="ATS compatibility scoring")
    optimization_suggestions: List[OptimizationSuggestion] = Field(default=[], description="AI-generated suggestions")
    competitor_analysis: Optional[CompetitorAnalysis] = Field(default=None, description="Industry comparison")
    
    # Quick stats
    estimated_pass_rate: float = Field(description="Estimated percentage of ATS systems this resume would pass")
    time_to_optimize: int = Field(description="Estimated minutes to implement all suggestions")
    
    # Export data
    exportable_data: Dict[str, Any] = Field(default={}, description="Data formatted for export/reporting")

class JobDescriptionAnalysis(BaseModel):
    """Analysis of job description for optimization"""
    job_title: str = Field(description="Job title from description")
    company: Optional[str] = Field(default=None, description="Company name if mentioned")
    required_skills: List[str] = Field(default=[], description="Required skills extracted")
    preferred_skills: List[str] = Field(default=[], description="Preferred skills extracted")
    experience_requirements: Dict[str, Any] = Field(default={}, description="Experience requirements")
    education_requirements: List[str] = Field(default=[], description="Education requirements")
    key_responsibilities: List[str] = Field(default=[], description="Key job responsibilities")
    industry_keywords: List[str] = Field(default=[], description="Industry-specific keywords")
    company_culture_keywords: List[str] = Field(default=[], description="Company culture keywords")
    
    # Analysis metadata
    confidence_score: float = Field(description="Confidence in extraction accuracy (0-1)")
    analysis_notes: List[str] = Field(default=[], description="Notes about the analysis")
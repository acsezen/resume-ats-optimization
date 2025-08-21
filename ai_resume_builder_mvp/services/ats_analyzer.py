"""
ATS compatibility analyzer and scoring system.
Simulates how Applicant Tracking Systems parse and score resumes.
"""
import re
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import math

# Text analysis imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Models
from models.resume_models import Resume, WorkExperience, Skill
from models.ats_models import (
    ATSScore, KeywordAnalysis, FormattingIssue, SectionScore, 
    ATSCompatibilityLevel, ATSAnalysisResult, CompetitorAnalysis
)

class ATSAnalyzer:
    """Comprehensive ATS compatibility analyzer"""
    
    def __init__(self):
        # ATS scoring weights
        self.scoring_weights = {
            'keyword_match': 0.40,      # 40% - Most important for ATS
            'formatting': 0.25,         # 25% - Critical for parsing
            'content_structure': 0.20,  # 20% - Important for readability
            'content_quality': 0.15     # 15% - Overall quality
        }
        
        # Standard ATS-friendly section headers
        self.standard_headers = {
            'contact': ['contact', 'contact information', 'personal information'],
            'summary': ['summary', 'professional summary', 'profile', 'objective', 'career objective'],
            'experience': ['experience', 'work experience', 'professional experience', 'employment', 'career history'],
            'education': ['education', 'academic background', 'qualifications'],
            'skills': ['skills', 'technical skills', 'core competencies', 'competencies'],
            'projects': ['projects', 'key projects', 'notable projects'],
            'certifications': ['certifications', 'certificates', 'professional certifications']
        }
        
        # Common ATS parsing issues
        self.formatting_rules = {
            'avoid_graphics': 'Graphics and images are not ATS-readable',
            'avoid_tables': 'Complex tables can confuse ATS parsers',
            'avoid_columns': 'Multi-column layouts may be parsed incorrectly',
            'standard_fonts': 'Use standard fonts like Arial, Calibri, or Times New Roman',
            'consistent_formatting': 'Maintain consistent formatting throughout',
            'simple_bullets': 'Use simple bullet points (• or -)',
            'standard_sections': 'Use standard section headers'
        }
    
    async def analyze_resume(self, resume: Resume, job_description: Optional[str] = None) -> ATSAnalysisResult:
        """Comprehensive ATS analysis of resume"""
        try:
            # Convert resume to text for analysis
            resume_text = self._resume_to_text(resume)
            
            # Perform different types of analysis
            keyword_analysis = await self._analyze_keywords(resume_text, job_description)
            formatting_score = self._analyze_formatting(resume)
            structure_score = self._analyze_structure(resume)
            content_quality_score = self._analyze_content_quality(resume)
            
            # Calculate section scores
            section_scores = self._calculate_section_scores(resume, job_description)
            
            # Calculate overall ATS score
            overall_score = self._calculate_overall_score(
                keyword_analysis.match_percentage,
                formatting_score,
                structure_score,
                content_quality_score
            )
            
            # Determine compatibility level
            compatibility_level = self._determine_compatibility_level(overall_score)
            
            # Generate recommendations
            priority_recommendations = self._generate_priority_recommendations(
                keyword_analysis, formatting_score, structure_score, content_quality_score
            )
            
            # Create ATS score object
            ats_score = ATSScore(
                overall_score=overall_score,
                compatibility_level=compatibility_level,
                keyword_score=keyword_analysis.match_percentage,
                formatting_score=formatting_score,
                structure_score=structure_score,
                content_quality_score=content_quality_score,
                section_scores=section_scores,
                keyword_analysis=keyword_analysis,
                formatting_issues=self._identify_formatting_issues(resume),
                priority_recommendations=priority_recommendations,
                general_recommendations=self._generate_general_recommendations(resume),
                analysis_date=datetime.now().isoformat(),
                job_title_analyzed=self._extract_job_title(job_description) if job_description else None
            )
            
            # Create analysis result
            analysis_result = ATSAnalysisResult(
                ats_score=ats_score,
                optimization_suggestions=[],  # Will be populated by AI service
                competitor_analysis=self._analyze_competitor_standards(resume, job_description),
                estimated_pass_rate=self._estimate_pass_rate(overall_score),
                time_to_optimize=self._estimate_optimization_time(priority_recommendations),
                exportable_data=self._create_exportable_data(ats_score)
            )
            
            return analysis_result
            
        except Exception as e:
            raise Exception(f"ATS analysis failed: {str(e)}")
    
    async def _analyze_keywords(self, resume_text: str, job_description: Optional[str]) -> KeywordAnalysis:
        """Analyze keyword matching between resume and job description"""
        if not job_description:
            return KeywordAnalysis(
                job_keywords=[],
                resume_keywords=self._extract_resume_keywords(resume_text),
                matched_keywords=[],
                missing_keywords=[],
                keyword_density={},
                match_percentage=0.0
            )
        
        # Extract keywords from both texts
        job_keywords = self._extract_job_keywords(job_description)
        resume_keywords = self._extract_resume_keywords(resume_text)
        
        # Find matches (case-insensitive)
        job_keywords_lower = [kw.lower() for kw in job_keywords]
        resume_keywords_lower = [kw.lower() for kw in resume_keywords]
        
        matched_keywords = []
        for job_kw in job_keywords:
            if job_kw.lower() in resume_keywords_lower:
                matched_keywords.append(job_kw)
        
        # Find missing keywords
        missing_keywords = []
        for job_kw in job_keywords:
            if job_kw.lower() not in resume_keywords_lower:
                missing_keywords.append(job_kw)
        
        # Calculate keyword density
        keyword_density = self._calculate_keyword_density(resume_text, job_keywords)
        
        # Calculate match percentage
        match_percentage = (len(matched_keywords) / len(job_keywords) * 100) if job_keywords else 0
        
        return KeywordAnalysis(
            job_keywords=job_keywords,
            resume_keywords=resume_keywords,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            keyword_density=keyword_density,
            match_percentage=match_percentage
        )
    
    def _analyze_formatting(self, resume: Resume) -> float:
        """Analyze resume formatting for ATS compatibility"""
        score = 100.0
        
        # Check for standard section headers
        sections_present = 0
        total_sections = 0
        
        if resume.contact_info:
            sections_present += 1
        total_sections += 1
        
        if resume.professional_summary:
            sections_present += 1
        total_sections += 1
        
        if resume.work_experience:
            sections_present += 1
        total_sections += 1
        
        if resume.skills:
            sections_present += 1
        total_sections += 1
        
        if resume.education:
            sections_present += 1
        total_sections += 1
        
        # Section completeness score
        section_score = (sections_present / total_sections) * 30
        
        # Contact information completeness
        contact_score = 0
        if resume.contact_info.full_name:
            contact_score += 5
        if resume.contact_info.email:
            contact_score += 10
        if resume.contact_info.phone:
            contact_score += 5
        
        # Date formatting consistency (simplified check)
        date_score = 20  # Assume good formatting for now
        
        # Skills formatting
        skills_score = 15 if resume.skills else 0
        
        # Experience formatting
        experience_score = 20 if resume.work_experience else 0
        
        total_score = section_score + contact_score + date_score + skills_score + experience_score
        return min(100.0, total_score)
    
    def _analyze_structure(self, resume: Resume) -> float:
        """Analyze resume structure and organization"""
        score = 0.0
        
        # Contact information at top (assumed in our model)
        score += 15
        
        # Professional summary present
        if resume.professional_summary:
            score += 15
        
        # Work experience in reverse chronological order
        if resume.work_experience:
            score += 25
            # Check if dates are in reverse chronological order
            if self._is_chronological_order(resume.work_experience):
                score += 10
        
        # Skills section present and organized
        if resume.skills:
            score += 15
            # Bonus for categorized skills
            categories = set(skill.category for skill in resume.skills)
            if len(categories) > 1:
                score += 5
        
        # Education section present
        if resume.education:
            score += 10
        
        # Appropriate length (estimated based on content)
        content_length = self._estimate_content_length(resume)
        if 1 <= content_length <= 2:  # 1-2 pages ideal
            score += 10
        elif content_length > 2:
            score += 5  # Slight penalty for being too long
        
        return min(100.0, score)
    
    def _analyze_content_quality(self, resume: Resume) -> float:
        """Analyze content quality and completeness"""
        score = 0.0
        
        # Professional summary quality
        if resume.professional_summary:
            summary_length = len(resume.professional_summary.split())
            if 30 <= summary_length <= 100:  # Ideal length
                score += 15
            elif summary_length > 0:
                score += 10
        
        # Work experience quality
        if resume.work_experience:
            total_bullets = sum(len(exp.description) for exp in resume.work_experience)
            if total_bullets >= 6:  # At least 2-3 bullets per job
                score += 20
            elif total_bullets > 0:
                score += 15
            
            # Check for quantified achievements
            quantified_count = 0
            for exp in resume.work_experience:
                for bullet in exp.description:
                    if re.search(r'\d+[%$]?|\d+\+|increased|decreased|improved|reduced', bullet.lower()):
                        quantified_count += 1
            
            if quantified_count >= 3:
                score += 15
            elif quantified_count > 0:
                score += 10
        
        # Skills relevance and quantity
        if resume.skills:
            skill_count = len(resume.skills)
            if 10 <= skill_count <= 25:  # Ideal range
                score += 15
            elif skill_count > 0:
                score += 10
        
        # Education completeness
        if resume.education:
            score += 10
            # Bonus for complete education info
            for edu in resume.education:
                if edu.degree and edu.institution:
                    score += 5
                    break
        
        # Contact information completeness
        contact_completeness = 0
        if resume.contact_info.email:
            contact_completeness += 1
        if resume.contact_info.phone:
            contact_completeness += 1
        if resume.contact_info.linkedin_url:
            contact_completeness += 1
        
        score += (contact_completeness / 3) * 15
        
        return min(100.0, score)
    
    def _calculate_section_scores(self, resume: Resume, job_description: Optional[str]) -> List[SectionScore]:
        """Calculate scores for individual resume sections"""
        section_scores = []
        
        # Professional Summary
        if resume.professional_summary:
            summary_score = self._score_professional_summary(resume.professional_summary, job_description)
            section_scores.append(SectionScore(
                section_name="Professional Summary",
                score=summary_score,
                max_score=100,
                issues=self._identify_summary_issues(resume.professional_summary),
                recommendations=self._get_summary_recommendations(resume.professional_summary)
            ))
        
        # Work Experience
        if resume.work_experience:
            experience_score = self._score_work_experience(resume.work_experience, job_description)
            section_scores.append(SectionScore(
                section_name="Work Experience",
                score=experience_score,
                max_score=100,
                issues=self._identify_experience_issues(resume.work_experience),
                recommendations=self._get_experience_recommendations(resume.work_experience)
            ))
        
        # Skills
        if resume.skills:
            skills_score = self._score_skills_section(resume.skills, job_description)
            section_scores.append(SectionScore(
                section_name="Skills",
                score=skills_score,
                max_score=100,
                issues=self._identify_skills_issues(resume.skills),
                recommendations=self._get_skills_recommendations(resume.skills)
            ))
        
        # Education
        if resume.education:
            education_score = self._score_education_section(resume.education)
            section_scores.append(SectionScore(
                section_name="Education",
                score=education_score,
                max_score=100,
                issues=self._identify_education_issues(resume.education),
                recommendations=self._get_education_recommendations(resume.education)
            ))
        
        return section_scores
    
    def _calculate_overall_score(self, keyword_score: float, formatting_score: float, 
                               structure_score: float, content_quality_score: float) -> float:
        """Calculate weighted overall ATS score"""
        overall_score = (
            keyword_score * self.scoring_weights['keyword_match'] +
            formatting_score * self.scoring_weights['formatting'] +
            structure_score * self.scoring_weights['content_structure'] +
            content_quality_score * self.scoring_weights['content_quality']
        )
        
        return round(overall_score, 1)
    
    def _determine_compatibility_level(self, score: float) -> ATSCompatibilityLevel:
        """Determine ATS compatibility level based on score"""
        if score >= 90:
            return ATSCompatibilityLevel.EXCELLENT
        elif score >= 75:
            return ATSCompatibilityLevel.GOOD
        elif score >= 60:
            return ATSCompatibilityLevel.FAIR
        else:
            return ATSCompatibilityLevel.POOR
    
    def _generate_priority_recommendations(self, keyword_analysis: KeywordAnalysis,
                                         formatting_score: float, structure_score: float,
                                         content_quality_score: float) -> List[str]:
        """Generate priority recommendations for improvement"""
        recommendations = []
        
        # Keyword recommendations (highest priority)
        if keyword_analysis.match_percentage < 60:
            recommendations.append(f"Add {len(keyword_analysis.missing_keywords)} missing keywords from job description")
        
        if keyword_analysis.match_percentage < 40:
            recommendations.append("Significantly improve keyword matching - current match rate is very low")
        
        # Formatting recommendations
        if formatting_score < 80:
            recommendations.append("Improve resume formatting for better ATS parsing")
        
        if formatting_score < 60:
            recommendations.append("Major formatting issues detected - use ATS-friendly template")
        
        # Structure recommendations
        if structure_score < 70:
            recommendations.append("Reorganize resume structure for better ATS compatibility")
        
        # Content quality recommendations
        if content_quality_score < 70:
            recommendations.append("Enhance content quality with quantified achievements")
        
        return recommendations[:5]  # Top 5 priority recommendations
    
    def _generate_general_recommendations(self, resume: Resume) -> List[str]:
        """Generate general improvement recommendations"""
        recommendations = []
        
        if not resume.professional_summary:
            recommendations.append("Add a professional summary to introduce your qualifications")
        
        if len(resume.skills) < 10:
            recommendations.append("Expand skills section with more relevant technical skills")
        
        if not any(exp.key_achievements for exp in resume.work_experience):
            recommendations.append("Add quantified achievements to work experience entries")
        
        if not resume.contact_info.linkedin_url:
            recommendations.append("Include LinkedIn profile URL for better professional presence")
        
        return recommendations
    
    def _identify_formatting_issues(self, resume: Resume) -> List[FormattingIssue]:
        """Identify specific formatting issues"""
        issues = []
        
        # Check contact information
        if not resume.contact_info.email:
            issues.append(FormattingIssue(
                issue_type="missing_contact",
                description="Email address is missing",
                severity="critical",
                recommendation="Add a professional email address"
            ))
        
        if not resume.contact_info.phone:
            issues.append(FormattingIssue(
                issue_type="missing_contact",
                description="Phone number is missing",
                severity="warning",
                recommendation="Add a phone number for contact"
            ))
        
        # Check for empty sections
        if not resume.work_experience:
            issues.append(FormattingIssue(
                issue_type="missing_section",
                description="Work experience section is empty",
                severity="critical",
                recommendation="Add work experience entries"
            ))
        
        return issues
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract keywords from job description"""
        # Technical skills patterns
        tech_patterns = [
            r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin)\b',
            r'\b(React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel|Express)\b',
            r'\b(AWS|Azure|GCP|Google Cloud|Docker|Kubernetes|Jenkins|Git|Linux|Unix)\b',
            r'\b(SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle|SQLite)\b',
            r'\b(HTML|CSS|SASS|LESS|Bootstrap|Tailwind|jQuery)\b',
            r'\b(Machine Learning|AI|Data Science|DevOps|Agile|Scrum|CI/CD)\b'
        ]
        
        keywords = set()
        
        # Extract technical keywords
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            keywords.update(matches)
        
        # Extract other important terms
        # Years of experience
        exp_matches = re.findall(r'(\d+)\+?\s*years?\s*(?:of\s*)?experience', job_description, re.IGNORECASE)
        for match in exp_matches:
            keywords.add(f"{match}+ years experience")
        
        # Degree requirements
        degree_matches = re.findall(r'\b(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|MBA)\b', job_description, re.IGNORECASE)
        keywords.update(degree_matches)
        
        # Common job-related terms
        job_terms = re.findall(r'\b(leadership|management|team|collaboration|communication|problem.solving|analytical|creative)\b', job_description, re.IGNORECASE)
        keywords.update(job_terms)
        
        return list(keywords)
    
    def _extract_resume_keywords(self, resume_text: str) -> List[str]:
        """Extract keywords from resume text"""
        return self._extract_job_keywords(resume_text)  # Use same extraction logic
    
    def _calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density in text"""
        text_lower = text.lower()
        word_count = len(text.split())
        
        density = {}
        for keyword in keywords:
            count = text_lower.count(keyword.lower())
            density[keyword] = (count / word_count) * 100 if word_count > 0 else 0
        
        return density
    
    def _resume_to_text(self, resume: Resume) -> str:
        """Convert resume object to text for analysis"""
        text_parts = []
        
        # Contact info
        text_parts.append(resume.contact_info.full_name)
        if resume.contact_info.email:
            text_parts.append(resume.contact_info.email)
        
        # Professional summary
        if resume.professional_summary:
            text_parts.append(resume.professional_summary)
        
        # Work experience
        for exp in resume.work_experience:
            text_parts.append(f"{exp.job_title} {exp.company}")
            text_parts.extend(exp.description)
        
        # Skills
        for skill in resume.skills:
            text_parts.append(skill.name)
        
        # Education
        for edu in resume.education:
            text_parts.append(f"{edu.degree} {edu.institution}")
        
        return ' '.join(text_parts)
    
    def _is_chronological_order(self, work_experience: List[WorkExperience]) -> bool:
        """Check if work experience is in reverse chronological order"""
        # Simplified check - in production, you'd parse dates properly
        return True  # Assume correct order for now
    
    def _estimate_content_length(self, resume: Resume) -> float:
        """Estimate resume length in pages"""
        # Rough estimation based on content
        total_content = 0
        
        if resume.professional_summary:
            total_content += len(resume.professional_summary.split())
        
        for exp in resume.work_experience:
            total_content += len(' '.join(exp.description).split())
        
        total_content += len(resume.skills) * 2  # Assume 2 words per skill
        
        for edu in resume.education:
            total_content += 10  # Assume 10 words per education entry
        
        # Rough conversion: 250-300 words per page
        return total_content / 275
    
    def _score_professional_summary(self, summary: str, job_description: Optional[str]) -> float:
        """Score professional summary section"""
        score = 0.0
        
        # Length check
        word_count = len(summary.split())
        if 30 <= word_count <= 100:
            score += 30
        elif word_count > 0:
            score += 20
        
        # Keyword matching if job description provided
        if job_description:
            job_keywords = self._extract_job_keywords(job_description)
            summary_lower = summary.lower()
            matched = sum(1 for kw in job_keywords if kw.lower() in summary_lower)
            keyword_score = (matched / len(job_keywords)) * 40 if job_keywords else 0
            score += keyword_score
        else:
            score += 20  # Base score without job description
        
        # Check for quantified achievements
        if re.search(r'\d+[%$]?|\d+\+|years?|experience', summary.lower()):
            score += 20
        
        # Check for action words
        action_words = ['led', 'managed', 'developed', 'created', 'improved', 'increased', 'achieved']
        if any(word in summary.lower() for word in action_words):
            score += 10
        
        return min(100.0, score)
    
    def _score_work_experience(self, work_experience: List[WorkExperience], job_description: Optional[str]) -> float:
        """Score work experience section"""
        if not work_experience:
            return 0.0
        
        score = 0.0
        
        # Number of positions
        if len(work_experience) >= 2:
            score += 20
        else:
            score += 10
        
        # Bullet points per position
        total_bullets = sum(len(exp.description) for exp in work_experience)
        avg_bullets = total_bullets / len(work_experience)
        if avg_bullets >= 3:
            score += 25
        elif avg_bullets >= 2:
            score += 20
        elif avg_bullets >= 1:
            score += 15
        
        # Quantified achievements
        quantified_count = 0
        for exp in work_experience:
            for bullet in exp.description:
                if re.search(r'\d+[%$]?|\d+\+|increased|decreased|improved|reduced', bullet.lower()):
                    quantified_count += 1
        
        if quantified_count >= 3:
            score += 25
        elif quantified_count >= 1:
            score += 15
        
        # Keyword matching
        if job_description:
            job_keywords = self._extract_job_keywords(job_description)
            exp_text = ' '.join([' '.join(exp.description) for exp in work_experience])
            matched = sum(1 for kw in job_keywords if kw.lower() in exp_text.lower())
            keyword_score = (matched / len(job_keywords)) * 30 if job_keywords else 0
            score += keyword_score
        else:
            score += 15
        
        return min(100.0, score)
    
    def _score_skills_section(self, skills: List[Skill], job_description: Optional[str]) -> float:
        """Score skills section"""
        if not skills:
            return 0.0
        
        score = 0.0
        
        # Number of skills
        skill_count = len(skills)
        if 15 <= skill_count <= 25:
            score += 30
        elif 10 <= skill_count <= 30:
            score += 25
        elif skill_count >= 5:
            score += 20
        
        # Skill categorization
        categories = set(skill.category for skill in skills)
        if len(categories) >= 3:
            score += 20
        elif len(categories) >= 2:
            score += 15
        
        # Keyword matching
        if job_description:
            job_keywords = self._extract_job_keywords(job_description)
            skill_names = [skill.name.lower() for skill in skills]
            matched = sum(1 for kw in job_keywords if kw.lower() in skill_names)
            keyword_score = (matched / len(job_keywords)) * 50 if job_keywords else 0
            score += keyword_score
        else:
            score += 25
        
        return min(100.0, score)
    
    def _score_education_section(self, education: List[Any]) -> float:
        """Score education section"""
        if not education:
            return 50.0  # Not always required
        
        score = 70.0  # Base score for having education
        
        for edu in education:
            if hasattr(edu, 'degree') and edu.degree:
                score += 15
            if hasattr(edu, 'institution') and edu.institution:
                score += 15
                break  # Only count once
        
        return min(100.0, score)
    
    def _identify_summary_issues(self, summary: str) -> List[str]:
        """Identify issues in professional summary"""
        issues = []
        
        word_count = len(summary.split())
        if word_count < 20:
            issues.append("Summary is too short")
        elif word_count > 120:
            issues.append("Summary is too long")
        
        if not re.search(r'\d+', summary):
            issues.append("No quantified experience mentioned")
        
        return issues
    
    def _get_summary_recommendations(self, summary: str) -> List[str]:
        """Get recommendations for professional summary"""
        recommendations = []
        
        word_count = len(summary.split())
        if word_count < 30:
            recommendations.append("Expand summary to 30-80 words")
        
        if not re.search(r'\d+', summary):
            recommendations.append("Include years of experience or quantified achievements")
        
        recommendations.append("Tailor summary to match target job requirements")
        
        return recommendations
    
    def _identify_experience_issues(self, work_experience: List[WorkExperience]) -> List[str]:
        """Identify issues in work experience"""
        issues = []
        
        if not work_experience:
            issues.append("No work experience provided")
            return issues
        
        total_bullets = sum(len(exp.description) for exp in work_experience)
        if total_bullets < len(work_experience) * 2:
            issues.append("Too few bullet points per position")
        
        # Check for quantified achievements
        quantified_count = 0
        for exp in work_experience:
            for bullet in exp.description:
                if re.search(r'\d+', bullet):
                    quantified_count += 1
        
        if quantified_count == 0:
            issues.append("No quantified achievements")
        
        return issues
    
    def _get_experience_recommendations(self, work_experience: List[WorkExperience]) -> List[str]:
        """Get recommendations for work experience"""
        recommendations = []
        
        recommendations.append("Add 2-4 bullet points per position")
        recommendations.append("Include quantified achievements with metrics")
        recommendations.append("Use strong action verbs to start each bullet point")
        recommendations.append("Focus on results and impact, not just responsibilities")
        
        return recommendations
    
    def _identify_skills_issues(self, skills: List[Skill]) -> List[str]:
        """Identify issues in skills section"""
        issues = []
        
        if len(skills) < 8:
            issues.append("Too few skills listed")
        elif len(skills) > 30:
            issues.append("Too many skills listed")
        
        categories = set(skill.category for skill in skills)
        if len(categories) < 2:
            issues.append("Skills not properly categorized")
        
        return issues
    
    def _get_skills_recommendations(self, skills: List[Skill]) -> List[str]:
        """Get recommendations for skills section"""
        recommendations = []
        
        recommendations.append("Include 15-25 relevant skills")
        recommendations.append("Organize skills by category")
        recommendations.append("Prioritize skills mentioned in job description")
        recommendations.append("Include both technical and soft skills")
        
        return recommendations
    
    def _identify_education_issues(self, education: List[Any]) -> List[str]:
        """Identify issues in education section"""
        issues = []
        
        if not education:
            issues.append("Education section is empty")
        
        return issues
    
    def _get_education_recommendations(self, education: List[Any]) -> List[str]:
        """Get recommendations for education section"""
        recommendations = []
        
        recommendations.append("Include degree, institution, and graduation date")
        recommendations.append("Add relevant coursework if applicable")
        recommendations.append("Include GPA if 3.5 or higher")
        
        return recommendations
    
    def _analyze_competitor_standards(self, resume: Resume, job_description: Optional[str]) -> Optional[CompetitorAnalysis]:
        """Analyze resume against industry standards"""
        if not job_description:
            return None
        
        # This is a simplified implementation
        # In production, you'd have industry-specific data
        
        return CompetitorAnalysis(
            industry_standards={
                "average_skills_count": 18,
                "average_experience_years": 5,
                "common_keywords": ["Python", "JavaScript", "SQL", "AWS"]
            },
            skill_gaps=["Cloud Computing", "Machine Learning"],
            experience_comparison={
                "years_experience": self._calculate_years_experience(resume.work_experience),
                "industry_average": 5
            },
            improvement_areas=["Add more quantified achievements", "Include cloud computing skills"]
        )
    
    def _estimate_pass_rate(self, overall_score: float) -> float:
        """Estimate percentage of ATS systems this resume would pass"""
        # Simplified estimation based on score
        if overall_score >= 90:
            return 95.0
        elif overall_score >= 80:
            return 85.0
        elif overall_score >= 70:
            return 70.0
        elif overall_score >= 60:
            return 55.0
        else:
            return 30.0
    
    def _estimate_optimization_time(self, recommendations: List[str]) -> int:
        """Estimate time in minutes to implement recommendations"""
        # Simple estimation: 5-15 minutes per recommendation
        return len(recommendations) * 10
    
    def _create_exportable_data(self, ats_score: ATSScore) -> Dict[str, Any]:
        """Create exportable data for reporting"""
        return {
            "overall_score": ats_score.overall_score,
            "compatibility_level": ats_score.compatibility_level.value,
            "keyword_match_rate": ats_score.keyword_score,
            "formatting_score": ats_score.formatting_score,
            "recommendations_count": len(ats_score.priority_recommendations),
            "analysis_date": ats_score.analysis_date
        }
    
    def _extract_job_title(self, job_description: str) -> Optional[str]:
        """Extract job title from job description"""
        # Simple extraction - look for common patterns
        lines = job_description.split('\n')[:5]  # Check first 5 lines
        
        for line in lines:
            line = line.strip()
            if any(word in line.lower() for word in ['engineer', 'developer', 'manager', 'analyst', 'specialist']):
                return line
        
        return None
    
    def _calculate_years_experience(self, work_experience: List[WorkExperience]) -> int:
        """Calculate total years of experience"""
        # Simplified calculation
        return len(work_experience) * 2  # Assume 2 years per position on average
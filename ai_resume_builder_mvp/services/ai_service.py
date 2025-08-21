"""
AI-powered resume optimization service with advanced prompting techniques.
Implements one-click optimization for ATS compliance and content enhancement.
"""
import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import asyncio

# AI imports
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Models
from models.resume_models import Resume, WorkExperience, Skill, SkillCategory, ResumeSection, OptimizationRequest
from models.ats_models import ATSScore, KeywordAnalysis, OptimizationSuggestion, JobDescriptionAnalysis

class AIResumeOptimizer:
    """AI-powered resume optimization with advanced prompting techniques"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = OpenAIModel("gpt-4o")
        
        # Initialize specialized agents for different optimization tasks
        self._init_agents()
        
        # ATS optimization prompts
        self.prompts = {
            'professional_summary': self._get_summary_prompt(),
            'work_experience': self._get_experience_prompt(),
            'skills_optimization': self._get_skills_prompt(),
            'keyword_extraction': self._get_keyword_extraction_prompt(),
            'ats_analysis': self._get_ats_analysis_prompt(),
            'job_analysis': self._get_job_analysis_prompt()
        }
    
    def _init_agents(self):
        """Initialize specialized PydanticAI agents for different tasks"""
        
        # Resume parsing agent
        self.resume_parser = Agent(
            model=self.model,
            output_type=Resume,
            system_prompt="""You are an expert resume parser. Extract structured data from resume text.
            Focus on:
            - Accurate contact information extraction
            - Proper categorization of skills
            - Clear work experience with quantified achievements
            - Educational background
            - ATS-friendly formatting requirements
            
            Always preserve the original meaning while structuring the data properly."""
        )
        
        # ATS optimization agent
        self.ats_optimizer = Agent(
            model=self.model,
            output_type=OptimizationSuggestion,
            system_prompt="""You are an ATS optimization expert. Your goal is to make resumes pass through 
            Applicant Tracking Systems while maintaining authenticity.
            
            Key ATS requirements:
            - Use standard section headers (Experience, Education, Skills)
            - Include relevant keywords from job descriptions
            - Use simple, clean formatting
            - Quantify achievements with metrics
            - Match job requirements closely
            - Avoid graphics, tables, or complex formatting
            
            Provide specific, actionable suggestions with high impact scores."""
        )
        
        # Job description analyzer
        self.job_analyzer = Agent(
            model=self.model,
            output_type=JobDescriptionAnalysis,
            system_prompt="""You are a job description analysis expert. Extract key requirements, 
            skills, and keywords that candidates should include in their resumes.
            
            Focus on:
            - Required vs preferred skills
            - Industry-specific keywords
            - Experience level requirements
            - Key responsibilities and qualifications
            - Company culture indicators
            
            Provide confidence scores for your extractions."""
        )
    
    def _get_summary_prompt(self) -> str:
        """Advanced prompt for professional summary optimization"""
        return """
        Create an ATS-optimized professional summary that:
        
        1. KEYWORD INTEGRATION: Naturally incorporate 5-7 relevant keywords from the job description
        2. QUANTIFIED IMPACT: Include 2-3 specific metrics or achievements
        3. VALUE PROPOSITION: Clearly state what value you bring to the role
        4. ROLE ALIGNMENT: Directly address the target position requirements
        5. ATS COMPLIANCE: Use simple, scannable language without complex formatting
        
        STRUCTURE (2-3 sentences, 50-80 words):
        - Sentence 1: Professional identity + years of experience + key expertise areas
        - Sentence 2: Major achievements with quantified results
        - Sentence 3: Value proposition for target role
        
        EXAMPLE FRAMEWORK:
        "[Experience Level] [Job Title] with [X] years of experience in [Key Skills/Industries]. 
        Proven track record of [Specific Achievement with Metrics]. 
        Seeking to leverage [Relevant Skills] to drive [Value/Results] at [Company/Role Type]."
        
        KEYWORDS TO PRIORITIZE:
        - Exact job title matches
        - Required technical skills
        - Industry-specific terms
        - Action verbs from job description
        - Soft skills mentioned in requirements
        
        Make it compelling yet ATS-friendly. Avoid buzzwords without substance.
        """
    
    def _get_experience_prompt(self) -> str:
        """Advanced prompt for work experience optimization"""
        return """
        Optimize work experience entries for maximum ATS compatibility and impact:
        
        1. JOB TITLE OPTIMIZATION:
        - Use standard industry job titles when possible
        - Include keywords from target job description
        - Format: "Job Title | Company Name | Location | Date Range"
        
        2. BULLET POINT FORMULA (Use STAR method):
        - Situation/Task: Brief context
        - Action: What you did (use strong action verbs)
        - Result: Quantified outcome/impact
        
        3. ATS-FRIENDLY ACTION VERBS:
        - Achieved, Implemented, Developed, Managed, Led, Created
        - Improved, Increased, Reduced, Streamlined, Optimized
        - Collaborated, Coordinated, Facilitated, Mentored
        
        4. QUANTIFICATION REQUIREMENTS:
        - Include numbers, percentages, dollar amounts
        - Show scope (team size, budget, timeline)
        - Demonstrate impact (efficiency gains, cost savings)
        
        5. KEYWORD INTEGRATION:
        - Mirror language from job description
        - Include technical skills naturally
        - Use industry-standard terminology
        
        BULLET POINT TEMPLATE:
        "[Action Verb] [What you did] [How you did it] resulting in [Quantified Result]"
        
        EXAMPLES:
        ❌ "Responsible for managing team projects"
        ✅ "Led cross-functional team of 8 developers to deliver 15 software projects, reducing delivery time by 30%"
        
        ❌ "Worked on improving processes"
        ✅ "Streamlined deployment processes using CI/CD pipelines, reducing deployment time from 4 hours to 30 minutes"
        
        Focus on achievements, not just responsibilities. Make every bullet point count.
        """
    
    def _get_skills_prompt(self) -> str:
        """Advanced prompt for skills section optimization"""
        return """
        Optimize the skills section for maximum ATS impact:
        
        1. SKILL CATEGORIZATION:
        - Technical Skills: Programming languages, frameworks, tools
        - Software/Platforms: Specific applications and systems
        - Methodologies: Agile, DevOps, project management approaches
        - Certifications: Professional credentials and licenses
        
        2. ATS KEYWORD MATCHING:
        - Use exact terms from job description
        - Include both acronyms and full forms (e.g., "AI/Artificial Intelligence")
        - Match skill variations (e.g., "JavaScript" and "JS")
        
        3. SKILL PRIORITIZATION:
        - List most relevant skills first
        - Group related skills together
        - Include proficiency levels when beneficial
        
        4. FORMATTING FOR ATS:
        - Use simple bullet points or comma-separated lists
        - Avoid graphics, charts, or progress bars
        - Keep consistent formatting throughout
        
        5. SKILL VALIDATION:
        - Only include skills you can demonstrate
        - Align with experience section examples
        - Include emerging/trending skills in your field
        
        CATEGORIES TO CONSIDER:
        - Programming Languages: Python, Java, JavaScript, etc.
        - Frameworks/Libraries: React, Django, Spring Boot, etc.
        - Databases: MySQL, PostgreSQL, MongoDB, etc.
        - Cloud Platforms: AWS, Azure, Google Cloud, etc.
        - Tools: Git, Docker, Jenkins, Jira, etc.
        - Soft Skills: Leadership, Communication, Problem-solving, etc.
        
        KEYWORD DENSITY STRATEGY:
        - Include 15-25 relevant technical skills
        - Repeat key skills in experience descriptions
        - Use industry-standard terminology
        
        Make skills scannable and keyword-rich while remaining authentic.
        """
    
    def _get_keyword_extraction_prompt(self) -> str:
        """Prompt for extracting keywords from job descriptions"""
        return """
        Extract and categorize keywords from the job description for ATS optimization:
        
        1. REQUIRED SKILLS (Must-have):
        - Technical skills explicitly stated as required
        - Years of experience requirements
        - Educational requirements
        - Certifications mentioned as required
        
        2. PREFERRED SKILLS (Nice-to-have):
        - Skills listed as "preferred" or "plus"
        - Additional qualifications
        - Bonus skills or experience
        
        3. ACTION KEYWORDS:
        - Verbs describing job responsibilities
        - Performance expectations
        - Key activities and tasks
        
        4. INDUSTRY KEYWORDS:
        - Industry-specific terminology
        - Company-specific language
        - Domain expertise terms
        
        5. SOFT SKILLS:
        - Communication requirements
        - Leadership expectations
        - Collaboration needs
        - Problem-solving abilities
        
        6. COMPANY CULTURE KEYWORDS:
        - Values and culture indicators
        - Work environment descriptors
        - Team dynamics expectations
        
        EXTRACTION STRATEGY:
        - Identify exact phrases and terms
        - Note frequency of keyword mentions
        - Distinguish between required vs preferred
        - Consider synonyms and variations
        
        PRIORITIZATION:
        - High Priority: Required skills, job title keywords
        - Medium Priority: Preferred skills, industry terms
        - Low Priority: Soft skills, culture keywords
        
        Return keywords with frequency counts and priority levels.
        """
    
    def _get_ats_analysis_prompt(self) -> str:
        """Prompt for comprehensive ATS analysis"""
        return """
        Perform comprehensive ATS compatibility analysis:
        
        1. KEYWORD ANALYSIS (40% of score):
        - Match rate between resume and job description keywords
        - Keyword density and distribution
        - Missing critical keywords
        - Keyword context and relevance
        
        2. FORMATTING ANALYSIS (25% of score):
        - Standard section headers usage
        - Simple, clean formatting
        - Consistent font and styling
        - Absence of graphics/tables/columns
        - Proper file format compatibility
        
        3. CONTENT STRUCTURE (20% of score):
        - Logical section ordering
        - Clear job titles and company names
        - Proper date formatting
        - Contact information completeness
        - Professional summary presence
        
        4. READABILITY (15% of score):
        - Clear, concise language
        - Proper grammar and spelling
        - Scannable bullet points
        - Appropriate length (1-2 pages)
        - White space utilization
        
        SCORING CRITERIA:
        - 90-100: Excellent ATS compatibility
        - 75-89: Good compatibility, minor improvements needed
        - 60-74: Fair compatibility, several improvements needed
        - Below 60: Poor compatibility, major overhaul required
        
        ANALYSIS OUTPUT:
        - Overall ATS score with breakdown
        - Specific issues identified
        - Priority recommendations
        - Expected improvement impact
        - Implementation difficulty level
        
        Focus on actionable insights that will improve ATS pass-through rates.
        """
    
    def _get_job_analysis_prompt(self) -> str:
        """Prompt for job description analysis"""
        return """
        Analyze job description to extract optimization targets:
        
        1. ROLE REQUIREMENTS:
        - Job title and level
        - Years of experience required
        - Education requirements
        - Location/remote options
        
        2. TECHNICAL REQUIREMENTS:
        - Programming languages
        - Frameworks and tools
        - Platforms and systems
        - Methodologies
        
        3. RESPONSIBILITY ANALYSIS:
        - Primary job functions
        - Key performance indicators
        - Team interaction requirements
        - Project scope and complexity
        
        4. COMPANY CONTEXT:
        - Industry and domain
        - Company size and stage
        - Culture and values
        - Growth opportunities
        
        5. OPTIMIZATION OPPORTUNITIES:
        - High-impact keywords to include
        - Skills to emphasize
        - Experience to highlight
        - Achievements to quantify
        
        EXTRACTION METHODOLOGY:
        - Identify explicit requirements vs implicit preferences
        - Note keyword frequency and emphasis
        - Understand role context and expectations
        - Map requirements to resume optimization strategies
        
        CONFIDENCE SCORING:
        - High confidence: Explicitly stated requirements
        - Medium confidence: Implied or inferred requirements
        - Low confidence: Assumptions based on industry standards
        
        Provide actionable insights for resume customization.
        """
    
    async def parse_resume_from_text(self, resume_text: str) -> Resume:
        """Parse resume text into structured Resume object using AI"""
        try:
            result = await self.resume_parser.run(
                f"Parse this resume text into structured data:\n\n{resume_text}"
            )
            return result.output
        except Exception as e:
            raise Exception(f"Resume parsing failed: {str(e)}")
    
    async def analyze_job_description(self, job_description: str) -> JobDescriptionAnalysis:
        """Analyze job description to extract requirements and keywords"""
        try:
            result = await self.job_analyzer.run(
                f"Analyze this job description:\n\n{job_description}"
            )
            return result.output
        except Exception as e:
            raise Exception(f"Job description analysis failed: {str(e)}")
    
    async def extract_keywords(self, job_description: str) -> KeywordAnalysis:
        """Extract and analyze keywords from job description"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompts['keyword_extraction']},
                    {"role": "user", "content": f"Extract keywords from this job description:\n\n{job_description}"}
                ],
                temperature=0.3
            )
            
            # Parse the response to extract keywords
            content = response.choices[0].message.content
            
            # Simple keyword extraction (in production, you'd use more sophisticated parsing)
            job_keywords = self._extract_keywords_from_text(content)
            
            return KeywordAnalysis(
                job_keywords=job_keywords,
                resume_keywords=[],  # Will be filled when comparing with resume
                matched_keywords=[],
                missing_keywords=[],
                keyword_density={},
                match_percentage=0.0
            )
        except Exception as e:
            raise Exception(f"Keyword extraction failed: {str(e)}")
    
    async def optimize_professional_summary(self, 
                                          current_summary: Optional[str], 
                                          job_description: str,
                                          resume_context: Dict[str, Any]) -> str:
        """Generate optimized professional summary"""
        try:
            context = f"""
            Current Summary: {current_summary or 'None'}
            
            Job Description: {job_description}
            
            Resume Context:
            - Experience Level: {resume_context.get('experience_level', 'Not specified')}
            - Key Skills: {', '.join(resume_context.get('key_skills', []))}
            - Industry: {resume_context.get('industry', 'Not specified')}
            - Years of Experience: {resume_context.get('years_experience', 'Not specified')}
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompts['professional_summary']},
                    {"role": "user", "content": f"Create an optimized professional summary:\n\n{context}"}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Summary optimization failed: {str(e)}")
    
    async def optimize_work_experience(self, 
                                     experience_entries: List[WorkExperience],
                                     job_description: str) -> List[WorkExperience]:
        """Optimize work experience entries for ATS compatibility"""
        optimized_entries = []
        
        for entry in experience_entries:
            try:
                context = f"""
                Current Experience Entry:
                Job Title: {entry.job_title}
                Company: {entry.company}
                Duration: {entry.start_date} - {entry.end_date or 'Present'}
                Current Description: {entry.description}
                
                Target Job Description: {job_description}
                """
                
                response = await self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.prompts['work_experience']},
                        {"role": "user", "content": f"Optimize this work experience entry:\n\n{context}"}
                    ],
                    temperature=0.6
                )
                
                # Parse the optimized content
                optimized_content = response.choices[0].message.content
                optimized_bullets = self._parse_bullet_points(optimized_content)
                
                # Create optimized entry
                optimized_entry = WorkExperience(
                    job_title=entry.job_title,
                    company=entry.company,
                    location=entry.location,
                    start_date=entry.start_date,
                    end_date=entry.end_date,
                    description=optimized_bullets,
                    key_achievements=entry.key_achievements
                )
                
                optimized_entries.append(optimized_entry)
                
            except Exception as e:
                # If optimization fails, keep original entry
                optimized_entries.append(entry)
        
        return optimized_entries
    
    async def optimize_skills(self, 
                            current_skills: List[Skill],
                            job_description: str) -> List[Skill]:
        """Optimize skills section for better ATS matching"""
        try:
            current_skills_text = ', '.join([skill.name for skill in current_skills])
            
            context = f"""
            Current Skills: {current_skills_text}
            
            Target Job Description: {job_description}
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompts['skills_optimization']},
                    {"role": "user", "content": f"Optimize skills for this job:\n\n{context}"}
                ],
                temperature=0.4
            )
            
            # Parse optimized skills
            optimized_skills_text = response.choices[0].message.content
            optimized_skills = self._parse_skills_from_text(optimized_skills_text)
            
            return optimized_skills
            
        except Exception as e:
            # If optimization fails, return original skills
            return current_skills
    
    async def one_click_optimize(self, resume: Resume, job_description: str) -> Tuple[Resume, List[OptimizationSuggestion]]:
        """One-click comprehensive resume optimization"""
        try:
            # Analyze job description first
            job_analysis = await self.analyze_job_description(job_description)
            
            # Create resume context for optimization
            resume_context = {
                'experience_level': resume.experience_level,
                'key_skills': [skill.name for skill in resume.skills[:10]],
                'industry': resume.industry,
                'years_experience': self._calculate_years_experience(resume.work_experience)
            }
            
            # Optimize different sections concurrently
            optimization_tasks = []
            
            # Professional Summary
            if resume.professional_summary or True:  # Always optimize summary
                optimization_tasks.append(
                    self.optimize_professional_summary(
                        resume.professional_summary, 
                        job_description, 
                        resume_context
                    )
                )
            
            # Work Experience
            if resume.work_experience:
                optimization_tasks.append(
                    self.optimize_work_experience(resume.work_experience, job_description)
                )
            
            # Skills
            if resume.skills:
                optimization_tasks.append(
                    self.optimize_skills(resume.skills, job_description)
                )
            
            # Execute optimizations
            results = await asyncio.gather(*optimization_tasks, return_exceptions=True)
            
            # Create optimized resume
            optimized_resume = resume.model_copy(deep=True)
            suggestions = []
            
            # Apply optimizations
            if len(results) > 0 and not isinstance(results[0], Exception):
                optimized_resume.professional_summary = results[0]
                suggestions.append(OptimizationSuggestion(
                    section="professional_summary",
                    current_content=resume.professional_summary or "",
                    suggested_content=results[0],
                    reasoning="AI-optimized for ATS compatibility and keyword matching",
                    impact_score=8.5,
                    keywords_added=self._extract_keywords_from_text(results[0])
                ))
            
            if len(results) > 1 and not isinstance(results[1], Exception):
                optimized_resume.work_experience = results[1]
                suggestions.append(OptimizationSuggestion(
                    section="work_experience",
                    current_content="Work experience entries",
                    suggested_content="Optimized work experience with quantified achievements",
                    reasoning="Enhanced with metrics, keywords, and ATS-friendly formatting",
                    impact_score=9.0,
                    keywords_added=[]
                ))
            
            if len(results) > 2 and not isinstance(results[2], Exception):
                optimized_resume.skills = results[2]
                suggestions.append(OptimizationSuggestion(
                    section="skills",
                    current_content="Skills section",
                    suggested_content="Optimized skills matching job requirements",
                    reasoning="Aligned with job description keywords and requirements",
                    impact_score=7.5,
                    keywords_added=[skill.name for skill in results[2]]
                ))
            
            # Update metadata
            optimized_resume.updated_at = datetime.now()
            optimized_resume.target_role = job_analysis.job_title
            
            return optimized_resume, suggestions
            
        except Exception as e:
            raise Exception(f"One-click optimization failed: {str(e)}")
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from text using simple patterns"""
        # This is a simplified implementation
        # In production, you'd use more sophisticated NLP
        
        # Common technical keywords pattern
        tech_patterns = [
            r'\b(Python|Java|JavaScript|React|Angular|Vue|Node\.js|Django|Flask)\b',
            r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|Linux|SQL)\b',
            r'\b(Machine Learning|AI|Data Science|DevOps|Agile|Scrum)\b'
        ]
        
        keywords = set()
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.update([match.lower() for match in matches])
        
        return list(keywords)
    
    def _parse_bullet_points(self, text: str) -> List[str]:
        """Parse bullet points from AI-generated text"""
        lines = text.split('\n')
        bullets = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullets.append(line[1:].strip())
            elif line and not line.startswith('#') and len(line) > 20:
                bullets.append(line)
        
        return bullets[:6]  # Limit to 6 bullets per job
    
    def _parse_skills_from_text(self, text: str) -> List[Skill]:
        """Parse skills from AI-generated text"""
        skills = []
        
        # Extract skills from different categories
        categories = {
            'programming': SkillCategory.PROGRAMMING,
            'technical': SkillCategory.TECHNICAL,
            'framework': SkillCategory.FRAMEWORK,
            'database': SkillCategory.DATABASE,
            'cloud': SkillCategory.CLOUD,
            'tools': SkillCategory.TOOLS
        }
        
        for line in text.split('\n'):
            line = line.strip()
            if ':' in line:
                category_name, skills_text = line.split(':', 1)
                category_name = category_name.lower().strip()
                
                # Find matching category
                skill_category = SkillCategory.TECHNICAL  # default
                for cat_key, cat_value in categories.items():
                    if cat_key in category_name:
                        skill_category = cat_value
                        break
                
                # Extract individual skills
                skill_names = [s.strip() for s in skills_text.split(',')]
                for skill_name in skill_names:
                    if skill_name and len(skill_name) > 1:
                        skills.append(Skill(
                            name=skill_name,
                            category=skill_category
                        ))
        
        return skills[:25]  # Limit to 25 skills
    
    def _calculate_years_experience(self, work_experience: List[WorkExperience]) -> int:
        """Calculate total years of experience"""
        total_months = 0
        
        for exp in work_experience:
            try:
                # Simple calculation - in production, you'd use proper date parsing
                start_parts = exp.start_date.split('/')
                if len(start_parts) == 2:
                    start_year = int(start_parts[1])
                    
                    if exp.end_date and exp.end_date.lower() != 'present':
                        end_parts = exp.end_date.split('/')
                        if len(end_parts) == 2:
                            end_year = int(end_parts[1])
                        else:
                            end_year = datetime.now().year
                    else:
                        end_year = datetime.now().year
                    
                    total_months += (end_year - start_year) * 12
            except:
                continue
        
        return max(1, total_months // 12)  # At least 1 year
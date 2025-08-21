"""
Test script for AI Resume Builder MVP
Creates sample data and tests core functionality
"""
import asyncio
import os
from models.resume_models import Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory
from services.ats_analyzer import ATSAnalyzer
from processors.file_processor import FileProcessor, ResumeExporter

# Sample resume data
def create_sample_resume() -> Resume:
    """Create a sample resume for testing"""
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
    
    education = [
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
    
    return Resume(
        contact_info=contact_info,
        professional_summary="Experienced software engineer with 4+ years developing scalable web applications and microservices. Proven track record of improving system performance and leading development teams. Passionate about clean code, system architecture, and mentoring junior developers.",
        work_experience=work_experience,
        skills=skills,
        education=education,
        target_role="Senior Software Engineer",
        industry="Technology"
    )

# Sample job description
SAMPLE_JOB_DESCRIPTION = """
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

What We Offer:
• Competitive salary and equity package
• Comprehensive health, dental, and vision insurance
• Flexible work arrangements and remote options
• Professional development opportunities
• Collaborative and innovative work environment
"""

async def test_ats_analysis():
    """Test ATS analysis functionality"""
    print("🧪 Testing ATS Analysis")
    print("=" * 50)
    
    # Create sample resume
    resume = create_sample_resume()
    print(f"✅ Created sample resume for {resume.contact_info.full_name}")
    
    # Initialize ATS analyzer
    ats_analyzer = ATSAnalyzer()
    
    # Perform ATS analysis
    try:
        analysis = await ats_analyzer.analyze_resume(resume, SAMPLE_JOB_DESCRIPTION)
        
        print(f"\n📊 ATS Analysis Results:")
        print(f"   Overall Score: {analysis.ats_score.overall_score}/100")
        print(f"   Compatibility Level: {analysis.ats_score.compatibility_level.value}")
        print(f"   Keyword Match: {analysis.ats_score.keyword_score:.1f}%")
        print(f"   Formatting Score: {analysis.ats_score.formatting_score:.1f}%")
        print(f"   Structure Score: {analysis.ats_score.structure_score:.1f}%")
        print(f"   Content Quality: {analysis.ats_score.content_quality_score:.1f}%")
        
        print(f"\n🎯 Keyword Analysis:")
        keyword_analysis = analysis.ats_score.keyword_analysis
        print(f"   Job Keywords Found: {len(keyword_analysis.job_keywords)}")
        print(f"   Resume Keywords: {len(keyword_analysis.resume_keywords)}")
        print(f"   Matched Keywords: {len(keyword_analysis.matched_keywords)}")
        print(f"   Missing Keywords: {len(keyword_analysis.missing_keywords)}")
        
        if keyword_analysis.matched_keywords:
            print(f"   ✅ Matched: {', '.join(keyword_analysis.matched_keywords[:5])}...")
        
        if keyword_analysis.missing_keywords:
            print(f"   ❌ Missing: {', '.join(keyword_analysis.missing_keywords[:5])}...")
        
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(analysis.ats_score.priority_recommendations[:3], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n📈 Estimated Pass Rate: {analysis.estimated_pass_rate}%")
        print(f"⏱️  Time to Optimize: {analysis.time_to_optimize} minutes")
        
    except Exception as e:
        print(f"❌ ATS analysis failed: {e}")

def test_file_processing():
    """Test file processing functionality"""
    print("\n🧪 Testing File Processing")
    print("=" * 50)
    
    # Create sample resume
    resume = create_sample_resume()
    
    # Initialize file processor and exporter
    file_processor = FileProcessor()
    resume_exporter = ResumeExporter()
    
    # Test exports
    formats = ['md', 'html', 'txt', 'json']
    
    for format in formats:
        try:
            output_path = f"/tmp/test_resume.{format}"
            exported_path = resume_exporter.export_resume(resume, format, output_path)
            
            # Check if file was created
            if os.path.exists(exported_path):
                file_size = os.path.getsize(exported_path)
                print(f"   ✅ {format.upper()} export: {file_size} bytes")
                
                # Clean up
                os.remove(exported_path)
            else:
                print(f"   ❌ {format.upper()} export failed")
                
        except Exception as e:
            print(f"   ❌ {format.upper()} export error: {e}")

def test_ai_services():
    """Test AI services if available"""
    print("\n🧪 Testing AI Services")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("   ⚠️  OPENAI_API_KEY not found - AI features disabled")
        return
    
    try:
        from services.ai_service import AIResumeOptimizer
        
        print("   ✅ AI services available")
        print("   📝 Note: AI testing requires API calls - run manually if needed")
        
    except Exception as e:
        print(f"   ❌ AI services error: {e}")

async def main():
    """Run all tests"""
    print("🚀 AI Resume Builder MVP - Test Suite")
    print("=" * 60)
    
    # Test ATS analysis
    await test_ats_analysis()
    
    # Test file processing
    test_file_processing()
    
    # Test AI services
    test_ai_services()
    
    print("\n🎉 Testing completed!")
    print("\nTo start the web application:")
    print("   export OPENAI_API_KEY='your-api-key'  # Optional, for AI features")
    print("   python main.py")

if __name__ == "__main__":
    asyncio.run(main())
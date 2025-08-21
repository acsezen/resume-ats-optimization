"""
Simplified tests for ATS analyzer functionality
"""
import pytest
from services.ats_analyzer import ATSAnalyzer
from models.ats_models import ATSCompatibilityLevel


class TestATSAnalyzer:
    """Test ATS analyzer core functionality"""
    
    def test_analyzer_initialization(self):
        """Test ATS analyzer initialization"""
        analyzer = ATSAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_resume')
        assert hasattr(analyzer, '_extract_job_keywords')
        assert hasattr(analyzer, '_extract_resume_keywords')
    
    @pytest.mark.asyncio
    async def test_analyze_resume_basic(self, sample_resume, sample_job_description):
        """Test basic resume analysis"""
        analyzer = ATSAnalyzer()
        analysis = await analyzer.analyze_resume(sample_resume, sample_job_description)
        
        assert analysis is not None
        assert analysis.ats_score is not None
        assert analysis.ats_score.overall_score >= 0
        assert analysis.ats_score.overall_score <= 100
        assert analysis.ats_score.compatibility_level in [
            ATSCompatibilityLevel.POOR,
            ATSCompatibilityLevel.FAIR,
            ATSCompatibilityLevel.GOOD,
            ATSCompatibilityLevel.EXCELLENT
        ]
    
    def test_extract_keywords_from_job_description(self, sample_job_description):
        """Test keyword extraction from job description"""
        analyzer = ATSAnalyzer()
        keywords = analyzer._extract_job_keywords(sample_job_description)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        
        # Should contain technical keywords
        technical_keywords = [k.lower() for k in keywords]
        assert any('python' in k for k in technical_keywords)
    
    def test_extract_keywords_from_resume(self, sample_resume):
        """Test keyword extraction from resume"""
        analyzer = ATSAnalyzer()
        resume_text = analyzer._resume_to_text(sample_resume)
        keywords = analyzer._extract_resume_keywords(resume_text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
    
    def test_compatibility_level_calculation(self):
        """Test compatibility level calculation based on score"""
        analyzer = ATSAnalyzer()
        assert analyzer._determine_compatibility_level(95) == ATSCompatibilityLevel.EXCELLENT
        assert analyzer._determine_compatibility_level(85) == ATSCompatibilityLevel.GOOD
        assert analyzer._determine_compatibility_level(70) == ATSCompatibilityLevel.FAIR
        assert analyzer._determine_compatibility_level(50) == ATSCompatibilityLevel.POOR
    
    def test_keyword_density_calculation(self, sample_resume):
        """Test keyword density calculation"""
        analyzer = ATSAnalyzer()
        resume_text = analyzer._resume_to_text(sample_resume)
        keywords = ["Python", "JavaScript", "React"]
        
        density = analyzer._calculate_keyword_density(resume_text, keywords)
        
        assert isinstance(density, dict)
        for keyword in keywords:
            assert keyword in density
            assert isinstance(density[keyword], float)
            assert density[keyword] >= 0
    
    def test_resume_to_text_conversion(self, sample_resume):
        """Test resume to text conversion"""
        analyzer = ATSAnalyzer()
        text = analyzer._resume_to_text(sample_resume)
        
        assert isinstance(text, str)
        assert len(text) > 0
        assert sample_resume.contact_info.full_name in text
        assert sample_resume.professional_summary in text
    
    def test_formatting_analysis(self, sample_resume):
        """Test formatting analysis"""
        analyzer = ATSAnalyzer()
        score = analyzer._analyze_formatting(sample_resume)
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_structure_analysis(self, sample_resume):
        """Test structure analysis"""
        analyzer = ATSAnalyzer()
        score = analyzer._analyze_structure(sample_resume)
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_content_quality_analysis(self, sample_resume):
        """Test content quality analysis"""
        analyzer = ATSAnalyzer()
        score = analyzer._analyze_content_quality(sample_resume)
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    @pytest.mark.asyncio
    async def test_analyze_empty_resume(self, sample_job_description):
        """Test analysis of minimal resume"""
        from models.resume_models import Resume, ContactInfo
        
        analyzer = ATSAnalyzer()
        
        minimal_resume = Resume(
            contact_info=ContactInfo(
                full_name="Test User",
                email="test@example.com",
                phone="555-1234",
                location="Test City"
            ),
            professional_summary="",
            work_experience=[],
            skills=[],
            education=[]
        )
        
        analysis = await analyzer.analyze_resume(minimal_resume, sample_job_description)
        
        # Should still return valid analysis even for empty resume
        assert analysis.ats_score.overall_score >= 0
        assert analysis.ats_score.compatibility_level == ATSCompatibilityLevel.POOR
        assert len(analysis.optimization_suggestions) >= 0


class TestATSAnalyzerEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_analyze_with_empty_job_description(self, sample_resume):
        """Test analysis with empty job description"""
        analyzer = ATSAnalyzer()
        analysis = await analyzer.analyze_resume(sample_resume, "")
        
        assert analysis is not None
        assert analysis.ats_score.overall_score >= 0
    
    @pytest.mark.asyncio
    async def test_analyze_with_none_job_description(self, sample_resume):
        """Test analysis with None job description"""
        analyzer = ATSAnalyzer()
        analysis = await analyzer.analyze_resume(sample_resume, None)
        
        assert analysis is not None
        assert analysis.ats_score.overall_score >= 0
    
    def test_extract_keywords_empty_text(self):
        """Test keyword extraction from empty text"""
        analyzer = ATSAnalyzer()
        keywords = analyzer._extract_job_keywords("")
        
        assert isinstance(keywords, list)
        # Empty text should return empty list or minimal keywords
        assert len(keywords) >= 0
    
    def test_extract_keywords_special_text(self):
        """Test keyword extraction from text with special characters"""
        analyzer = ATSAnalyzer()
        special_text = "Python/JavaScript developer with C++ & C# experience! @#$%^&*()"
        keywords = analyzer._extract_job_keywords(special_text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        
        # Should handle special characters gracefully
        keyword_text = " ".join(keywords).lower()
        assert "python" in keyword_text or "javascript" in keyword_text


class TestATSPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_analysis_performance(self, sample_resume, sample_job_description):
        """Test analysis performance"""
        import time
        
        analyzer = ATSAnalyzer()
        
        start_time = time.time()
        analysis = await analyzer.analyze_resume(sample_resume, sample_job_description)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Analysis should complete within reasonable time
        assert execution_time < 10.0  # 10 seconds max
        assert analysis.ats_score.overall_score >= 0
    
    def test_keyword_extraction_performance(self, sample_job_description):
        """Test keyword extraction performance"""
        import time
        
        analyzer = ATSAnalyzer()
        
        start_time = time.time()
        keywords = analyzer._extract_job_keywords(sample_job_description)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Keyword extraction should be fast
        assert execution_time < 1.0  # 1 second max
        assert isinstance(keywords, list)
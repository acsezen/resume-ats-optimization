"""
Simplified integration tests for AI Resume Builder MVP
"""
import pytest
import asyncio
import os
import tempfile
from processors.file_processor import FileProcessor, ResumeExporter
from services.ats_analyzer import ATSAnalyzer


class TestBasicWorkflow:
    """Test basic resume processing workflow"""
    
    @pytest.mark.asyncio
    async def test_file_to_analysis_workflow(
        self, 
        sample_resume, 
        sample_job_description, 
        temp_dir
    ):
        """Test workflow from resume to ATS analysis"""
        
        # Initialize services
        ats_analyzer = ATSAnalyzer()
        resume_exporter = ResumeExporter()
        
        # Step 1: Export resume to file
        resume_file = os.path.join(temp_dir, 'test_resume.txt')
        resume_exporter.export_to_text(sample_resume, resume_file)
        
        assert os.path.exists(resume_file)
        assert os.path.getsize(resume_file) > 0
        
        # Step 2: Perform ATS analysis
        analysis = await ats_analyzer.analyze_resume(sample_resume, sample_job_description)
        
        assert analysis.ats_score.overall_score >= 0
        assert analysis.ats_score.overall_score <= 100
        assert len(analysis.optimization_suggestions) >= 0
    
    def test_export_import_cycle(
        self, 
        sample_resume, 
        temp_dir
    ):
        """Test exporting and re-importing resume data"""
        
        file_processor = FileProcessor()
        resume_exporter = ResumeExporter()
        
        # Export to text
        text_file = os.path.join(temp_dir, 'cycle_test.txt')
        resume_exporter.export_to_text(sample_resume, text_file)
        
        # Re-import the text
        extracted_text = file_processor.extract_text_from_file(text_file)
        
        # Verify key information is preserved
        assert sample_resume.contact_info.full_name.upper() in extracted_text.upper()
        assert sample_resume.contact_info.email in extracted_text
    
    def test_multiple_format_export(
        self, 
        sample_resume, 
        temp_dir
    ):
        """Test exporting resume in multiple formats"""
        
        resume_exporter = ResumeExporter()
        formats = ['txt', 'md', 'html', 'json']
        
        for format_type in formats:
            output_file = os.path.join(temp_dir, f'multi_format.{format_type}')
            result_path = resume_exporter.export_resume(sample_resume, format_type, output_file)
            
            assert os.path.exists(result_path)
            assert os.path.getsize(result_path) > 0
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis(
        self, 
        sample_resume, 
        sample_job_description
    ):
        """Test concurrent ATS analysis"""
        
        ats_analyzer = ATSAnalyzer()
        
        # Run multiple analyses concurrently
        tasks = [
            ats_analyzer.analyze_resume(sample_resume, sample_job_description)
            for _ in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        for result in results:
            assert result.ats_score.overall_score >= 0
            assert result.ats_score.overall_score <= 100
    
    def test_error_handling_workflow(
        self, 
        temp_dir
    ):
        """Test error handling in workflow"""
        
        file_processor = FileProcessor()
        
        # Test with non-existent file
        with pytest.raises(Exception):
            file_processor.extract_text_from_file('/nonexistent/file.txt')
        
        # Test with unsupported file type
        unsupported_file = os.path.join(temp_dir, 'test.exe')
        with open(unsupported_file, 'wb') as f:
            f.write(b'fake executable')
        
        # Should raise an exception for unsupported file type
        with pytest.raises(Exception):
            file_processor.extract_text_from_file(unsupported_file)


class TestDataIntegrity:
    """Test data integrity throughout workflow"""
    
    def test_resume_data_preservation(
        self, 
        sample_resume, 
        temp_dir
    ):
        """Test that resume data is preserved through export/import"""
        
        resume_exporter = ResumeExporter()
        
        # Export to JSON (most complete format)
        json_file = os.path.join(temp_dir, 'integrity_test.json')
        resume_exporter.export_to_json(sample_resume, json_file)
        
        # Read back and verify
        import json
        with open(json_file, 'r') as f:
            exported_data = json.load(f)
        
        # Verify key data is preserved
        assert exported_data['contact_info']['full_name'] == sample_resume.contact_info.full_name
        assert exported_data['contact_info']['email'] == sample_resume.contact_info.email
        assert exported_data['professional_summary'] == sample_resume.professional_summary
        assert len(exported_data['skills']) == len(sample_resume.skills)
    
    @pytest.mark.asyncio
    async def test_analysis_consistency(
        self, 
        sample_resume, 
        sample_job_description
    ):
        """Test that analysis results are consistent"""
        
        ats_analyzer = ATSAnalyzer()
        
        # Run analysis multiple times
        results = []
        for _ in range(3):
            analysis = await ats_analyzer.analyze_resume(sample_resume, sample_job_description)
            results.append(analysis.ats_score.overall_score)
        
        # Verify consistency (scores should be identical for same input)
        first_score = results[0]
        for score in results[1:]:
            # Allow small floating point differences
            assert abs(score - first_score) < 0.1


class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_analysis_performance(
        self, 
        sample_resume, 
        sample_job_description
    ):
        """Test analysis performance"""
        import time
        
        ats_analyzer = ATSAnalyzer()
        
        start_time = time.time()
        analysis = await ats_analyzer.analyze_resume(sample_resume, sample_job_description)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Analysis should complete within reasonable time
        assert execution_time < 10.0  # 10 seconds max
        assert analysis.ats_score.overall_score >= 0
    
    def test_export_performance(
        self, 
        sample_resume, 
        temp_dir
    ):
        """Test export performance"""
        import time
        
        resume_exporter = ResumeExporter()
        
        start_time = time.time()
        
        # Export in multiple formats
        formats = ['txt', 'md', 'html', 'json']
        for format_type in formats:
            output_file = os.path.join(temp_dir, f'perf_test.{format_type}')
            resume_exporter.export_resume(sample_resume, format_type, output_file)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Export should complete quickly
        assert execution_time < 5.0  # 5 seconds max for all formats
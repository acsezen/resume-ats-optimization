"""
File processing utilities for importing and exporting resumes.
Supports PDF, DOCX, and Markdown formats with ATS-friendly output.
"""
import os
import re
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile
from datetime import datetime

# Document processing imports
import PyPDF2
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import markdown
import markdown2

# Models
from models.resume_models import Resume, ContactInfo, WorkExperience, Education, Skill, SkillCategory

class FileProcessor:
    """Handles file import/export operations for resumes"""
    
    def __init__(self):
        self.supported_import_formats = ['.pdf', '.docx', '.md', '.txt']
        self.supported_export_formats = ['.pdf', '.docx', '.md', '.html', '.txt', '.json']
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text content from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")
    
    def extract_text_from_markdown(self, file_path: str) -> str:
        """Extract text content from Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Convert markdown to plain text (remove markdown syntax)
                html = markdown.markdown(content)
                # Simple HTML tag removal
                text = re.sub(r'<[^>]+>', '', html)
                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading Markdown file: {str(e)}")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from supported file formats"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_ext in ['.md', '.markdown']:
            return self.extract_text_from_markdown(file_path)
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Basic parsing of resume text into structured data"""
        # This is a simple parser - in production, you'd use more sophisticated NLP
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        parsed_data = {
            'raw_text': text,
            'contact_info': self._extract_contact_info(text),
            'sections': self._identify_sections(lines),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience_entries(lines),
            'education': self._extract_education_entries(lines)
        }
        
        return parsed_data
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using regex patterns"""
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone pattern (various formats)
        phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        
        # LinkedIn URL pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin_url'] = f"https://{linkedin_match.group()}"
        
        # GitHub URL pattern
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info['github_url'] = f"https://{github_match.group()}"
        
        # Extract name (first non-empty line, typically)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Look for a line that looks like a name (not email, phone, etc.)
            for line in lines[:5]:  # Check first 5 lines
                if not re.search(r'[@\d]', line) and len(line.split()) <= 4:
                    contact_info['full_name'] = line
                    break
        
        return contact_info
    
    def _identify_sections(self, lines: List[str]) -> Dict[str, List[str]]:
        """Identify resume sections based on common headers"""
        sections = {}
        current_section = None
        section_patterns = {
            'experience': r'(work\s+)?experience|employment|professional\s+experience',
            'education': r'education|academic|qualifications',
            'skills': r'skills|technical\s+skills|competencies',
            'projects': r'projects|portfolio',
            'certifications': r'certifications?|certificates?',
            'summary': r'summary|profile|objective|about'
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            section_found = False
            for section_name, pattern in section_patterns.items():
                if re.match(f'^{pattern}:?$', line_lower):
                    current_section = section_name
                    sections[current_section] = []
                    section_found = True
                    break
            
            # Add content to current section
            if not section_found and current_section:
                sections[current_section].append(line)
        
        return sections
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        # Common technical skills patterns
        skill_patterns = [
            r'\b(Python|Java|JavaScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin)\b',
            r'\b(React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel)\b',
            r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|Linux)\b',
            r'\b(SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch)\b',
            r'\b(HTML|CSS|SASS|LESS|Bootstrap|Tailwind)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        return list(skills)
    
    def _extract_experience_entries(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract work experience entries"""
        # This is a simplified implementation
        # In production, you'd use more sophisticated parsing
        experience_entries = []
        
        # Look for patterns like "Job Title at Company (Date - Date)"
        job_pattern = r'(.+?)\s+at\s+(.+?)\s*\((.+?)\)'
        
        for line in lines:
            match = re.search(job_pattern, line)
            if match:
                experience_entries.append({
                    'job_title': match.group(1).strip(),
                    'company': match.group(2).strip(),
                    'date_range': match.group(3).strip()
                })
        
        return experience_entries
    
    def _extract_education_entries(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract education entries"""
        education_entries = []
        
        # Look for degree patterns
        degree_pattern = r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|MBA).*?(?:from\s+)?(.+?)(?:\s*\((.+?)\))?'
        
        for line in lines:
            match = re.search(degree_pattern, line, re.IGNORECASE)
            if match:
                education_entries.append({
                    'degree': match.group(1).strip(),
                    'institution': match.group(2).strip() if match.group(2) else '',
                    'date': match.group(3).strip() if match.group(3) else ''
                })
        
        return education_entries

class ResumeExporter:
    """Export resume data to various formats"""
    
    def __init__(self):
        self.export_formats = {
            'pdf': self.export_to_pdf,
            'docx': self.export_to_docx,
            'md': self.export_to_markdown,
            'html': self.export_to_html,
            'txt': self.export_to_text,
            'json': self.export_to_json
        }
    
    def export_resume(self, resume: Resume, format: str, output_path: str) -> str:
        """Export resume to specified format"""
        format = format.lower().replace('.', '')
        
        if format not in self.export_formats:
            raise ValueError(f"Unsupported export format: {format}")
        
        return self.export_formats[format](resume, output_path)
    
    def export_to_docx(self, resume: Resume, output_path: str) -> str:
        """Export resume to DOCX format (ATS-friendly)"""
        doc = Document()
        
        # Set document margins for ATS compatibility
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)
        
        # Header with contact information
        header = doc.add_heading(resume.contact_info.full_name, 0)
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Contact info
        contact_info = []
        if resume.contact_info.email:
            contact_info.append(resume.contact_info.email)
        if resume.contact_info.phone:
            contact_info.append(resume.contact_info.phone)
        if resume.contact_info.location:
            contact_info.append(resume.contact_info.location)
        
        if contact_info:
            contact_para = doc.add_paragraph(' | '.join(contact_info))
            contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # URLs
        urls = []
        if resume.contact_info.linkedin_url:
            urls.append(resume.contact_info.linkedin_url)
        if resume.contact_info.github_url:
            urls.append(resume.contact_info.github_url)
        if resume.contact_info.portfolio_url:
            urls.append(resume.contact_info.portfolio_url)
        
        if urls:
            url_para = doc.add_paragraph(' | '.join(urls))
            url_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Professional Summary
        if resume.professional_summary:
            doc.add_heading('Professional Summary', level=1)
            doc.add_paragraph(resume.professional_summary)
        
        # Work Experience
        if resume.work_experience:
            doc.add_heading('Professional Experience', level=1)
            for exp in resume.work_experience:
                # Job title and company
                job_header = f"{exp.job_title} | {exp.company}"
                if exp.location:
                    job_header += f" | {exp.location}"
                doc.add_paragraph(job_header, style='Heading 2')
                
                # Date range
                date_range = exp.start_date
                if exp.end_date:
                    date_range += f" - {exp.end_date}"
                doc.add_paragraph(date_range, style='Heading 3')
                
                # Description bullets
                for bullet in exp.description:
                    p = doc.add_paragraph(bullet, style='List Bullet')
        
        # Skills
        if resume.skills:
            doc.add_heading('Technical Skills', level=1)
            skills_by_category = {}
            for skill in resume.skills:
                category = skill.category.value.replace('_', ' ').title()
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.name)
            
            for category, skills in skills_by_category.items():
                doc.add_paragraph(f"{category}: {', '.join(skills)}")
        
        # Education
        if resume.education:
            doc.add_heading('Education', level=1)
            for edu in resume.education:
                edu_text = f"{edu.degree} | {edu.institution}"
                if edu.location:
                    edu_text += f" | {edu.location}"
                if edu.graduation_date:
                    edu_text += f" | {edu.graduation_date}"
                doc.add_paragraph(edu_text)
        
        # Projects
        if resume.projects:
            doc.add_heading('Projects', level=1)
            for project in resume.projects:
                project_header = project.name
                if project.url:
                    project_header += f" ({project.url})"
                doc.add_paragraph(project_header, style='Heading 2')
                doc.add_paragraph(project.description)
                if project.technologies:
                    doc.add_paragraph(f"Technologies: {', '.join(project.technologies)}")
        
        # Certifications
        if resume.certifications:
            doc.add_heading('Certifications', level=1)
            for cert in resume.certifications:
                cert_text = f"{cert.name} | {cert.issuer}"
                if cert.date_obtained:
                    cert_text += f" | {cert.date_obtained}"
                doc.add_paragraph(cert_text)
        
        doc.save(output_path)
        return output_path
    
    def export_to_markdown(self, resume: Resume, output_path: str) -> str:
        """Export resume to Markdown format"""
        md_content = []
        
        # Header
        md_content.append(f"# {resume.contact_info.full_name}")
        md_content.append("")
        
        # Contact info
        contact_info = []
        if resume.contact_info.email:
            contact_info.append(f"📧 {resume.contact_info.email}")
        if resume.contact_info.phone:
            contact_info.append(f"📞 {resume.contact_info.phone}")
        if resume.contact_info.location:
            contact_info.append(f"📍 {resume.contact_info.location}")
        
        if contact_info:
            md_content.extend(contact_info)
            md_content.append("")
        
        # URLs
        if resume.contact_info.linkedin_url:
            md_content.append(f"🔗 [LinkedIn]({resume.contact_info.linkedin_url})")
        if resume.contact_info.github_url:
            md_content.append(f"💻 [GitHub]({resume.contact_info.github_url})")
        if resume.contact_info.portfolio_url:
            md_content.append(f"🌐 [Portfolio]({resume.contact_info.portfolio_url})")
        
        if any([resume.contact_info.linkedin_url, resume.contact_info.github_url, resume.contact_info.portfolio_url]):
            md_content.append("")
        
        # Professional Summary
        if resume.professional_summary:
            md_content.append("## Professional Summary")
            md_content.append("")
            md_content.append(resume.professional_summary)
            md_content.append("")
        
        # Work Experience
        if resume.work_experience:
            md_content.append("## Professional Experience")
            md_content.append("")
            
            for exp in resume.work_experience:
                # Job header
                job_header = f"### {exp.job_title} | {exp.company}"
                if exp.location:
                    job_header += f" | {exp.location}"
                md_content.append(job_header)
                
                # Date range
                date_range = exp.start_date
                if exp.end_date:
                    date_range += f" - {exp.end_date}"
                md_content.append(f"*{date_range}*")
                md_content.append("")
                
                # Description
                for bullet in exp.description:
                    md_content.append(f"- {bullet}")
                md_content.append("")
        
        # Skills
        if resume.skills:
            md_content.append("## Technical Skills")
            md_content.append("")
            
            skills_by_category = {}
            for skill in resume.skills:
                category = skill.category.value.replace('_', ' ').title()
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.name)
            
            for category, skills in skills_by_category.items():
                md_content.append(f"**{category}:** {', '.join(skills)}")
            md_content.append("")
        
        # Education
        if resume.education:
            md_content.append("## Education")
            md_content.append("")
            
            for edu in resume.education:
                edu_header = f"### {edu.degree}"
                md_content.append(edu_header)
                md_content.append(f"**{edu.institution}**")
                if edu.location:
                    md_content.append(f"*{edu.location}*")
                if edu.graduation_date:
                    md_content.append(f"*Graduated: {edu.graduation_date}*")
                md_content.append("")
        
        # Projects
        if resume.projects:
            md_content.append("## Projects")
            md_content.append("")
            
            for project in resume.projects:
                project_header = f"### {project.name}"
                if project.url:
                    project_header = f"### [{project.name}]({project.url})"
                md_content.append(project_header)
                md_content.append(project.description)
                if project.technologies:
                    md_content.append(f"**Technologies:** {', '.join(project.technologies)}")
                md_content.append("")
        
        # Certifications
        if resume.certifications:
            md_content.append("## Certifications")
            md_content.append("")
            
            for cert in resume.certifications:
                cert_text = f"- **{cert.name}** | {cert.issuer}"
                if cert.date_obtained:
                    cert_text += f" | {cert.date_obtained}"
                md_content.append(cert_text)
            md_content.append("")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        return output_path
    
    def export_to_html(self, resume: Resume, output_path: str) -> str:
        """Export resume to HTML format"""
        # First export to markdown, then convert to HTML
        temp_md = output_path.replace('.html', '_temp.md')
        self.export_to_markdown(resume, temp_md)
        
        # Convert markdown to HTML
        with open(temp_md, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables'])
        
        # Add CSS styling for ATS-friendly appearance
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume.contact_info.full_name} - Resume</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #34495e;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        .contact-info {{
            text-align: center;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Clean up temp file
        os.remove(temp_md)
        
        return output_path
    
    def export_to_text(self, resume: Resume, output_path: str) -> str:
        """Export resume to plain text format (ATS-friendly)"""
        text_content = []
        
        # Header
        text_content.append(resume.contact_info.full_name.upper())
        text_content.append("=" * len(resume.contact_info.full_name))
        text_content.append("")
        
        # Contact info
        if resume.contact_info.email:
            text_content.append(f"Email: {resume.contact_info.email}")
        if resume.contact_info.phone:
            text_content.append(f"Phone: {resume.contact_info.phone}")
        if resume.contact_info.location:
            text_content.append(f"Location: {resume.contact_info.location}")
        if resume.contact_info.linkedin_url:
            text_content.append(f"LinkedIn: {resume.contact_info.linkedin_url}")
        if resume.contact_info.github_url:
            text_content.append(f"GitHub: {resume.contact_info.github_url}")
        text_content.append("")
        
        # Professional Summary
        if resume.professional_summary:
            text_content.append("PROFESSIONAL SUMMARY")
            text_content.append("-" * 20)
            text_content.append(resume.professional_summary)
            text_content.append("")
        
        # Work Experience
        if resume.work_experience:
            text_content.append("PROFESSIONAL EXPERIENCE")
            text_content.append("-" * 23)
            
            for exp in resume.work_experience:
                text_content.append(f"{exp.job_title} | {exp.company}")
                if exp.location:
                    text_content.append(f"Location: {exp.location}")
                
                date_range = exp.start_date
                if exp.end_date:
                    date_range += f" - {exp.end_date}"
                text_content.append(f"Duration: {date_range}")
                text_content.append("")
                
                for bullet in exp.description:
                    text_content.append(f"• {bullet}")
                text_content.append("")
        
        # Skills
        if resume.skills:
            text_content.append("TECHNICAL SKILLS")
            text_content.append("-" * 16)
            
            skills_by_category = {}
            for skill in resume.skills:
                category = skill.category.value.replace('_', ' ').title()
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.name)
            
            for category, skills in skills_by_category.items():
                text_content.append(f"{category}: {', '.join(skills)}")
            text_content.append("")
        
        # Education
        if resume.education:
            text_content.append("EDUCATION")
            text_content.append("-" * 9)
            
            for edu in resume.education:
                text_content.append(f"{edu.degree}")
                text_content.append(f"{edu.institution}")
                if edu.location:
                    text_content.append(f"Location: {edu.location}")
                if edu.graduation_date:
                    text_content.append(f"Graduated: {edu.graduation_date}")
                text_content.append("")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
        
        return output_path
    
    def export_to_json(self, resume: Resume, output_path: str) -> str:
        """Export resume to JSON format"""
        resume_dict = resume.model_dump()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(resume_dict, f, indent=2, default=str)
        
        return output_path
    
    def export_to_pdf(self, resume: Resume, output_path: str) -> str:
        """Export resume to PDF format (via HTML conversion)"""
        # For now, we'll create HTML and note that PDF conversion would require additional libraries
        html_path = output_path.replace('.pdf', '.html')
        self.export_to_html(resume, html_path)
        
        # In production, you would use libraries like:
        # - weasyprint
        # - reportlab
        # - pdfkit
        # For now, return HTML path with note
        
        return html_path  # Would return PDF path in production
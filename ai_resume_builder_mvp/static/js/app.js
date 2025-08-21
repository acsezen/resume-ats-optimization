// AI Resume Builder MVP - JavaScript functionality

class ResumeBuilder {
    constructor() {
        this.currentResume = null;
        this.currentScore = null;
        this.isOptimizing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFileUpload();
        this.setupFormValidation();
    }

    setupEventListeners() {
        // One-click optimization button
        const optimizeBtn = document.getElementById('optimize-btn');
        if (optimizeBtn) {
            optimizeBtn.addEventListener('click', () => this.optimizeResume());
        }

        // Export buttons
        document.querySelectorAll('.export-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const format = e.target.dataset.format;
                this.exportResume(format);
            });
        });

        // Job description input
        const jobDescInput = document.getElementById('job-description');
        if (jobDescInput) {
            jobDescInput.addEventListener('input', () => {
                this.debounce(() => this.analyzeJobDescription(), 1000);
            });
        }

        // Resume form inputs
        document.querySelectorAll('.resume-input').forEach(input => {
            input.addEventListener('input', () => {
                this.debounce(() => this.updateResumePreview(), 500);
            });
        });

        // ATS analysis button
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.analyzeATS());
        }
    }

    setupFileUpload() {
        const fileUpload = document.getElementById('file-upload');
        const fileInput = document.getElementById('file-input');

        if (!fileUpload || !fileInput) return;

        // Click to upload
        fileUpload.addEventListener('click', () => fileInput.click());

        // Drag and drop with modern animations
        fileUpload.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUpload.style.transform = 'scale(1.05)';
            fileUpload.style.borderColor = 'rgba(255, 255, 255, 0.8)';
            fileUpload.style.background = 'rgba(255, 255, 255, 0.15)';
        });

        fileUpload.addEventListener('dragleave', () => {
            fileUpload.style.transform = 'scale(1)';
            fileUpload.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            fileUpload.style.background = 'rgba(255, 255, 255, 0.05)';
        });

        fileUpload.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUpload.style.transform = 'scale(1)';
            fileUpload.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            fileUpload.style.background = 'rgba(255, 255, 255, 0.05)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    async handleFileUpload(file) {
        const allowedTypes = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/markdown',
            'text/plain'
        ];

        if (!allowedTypes.includes(file.type)) {
            this.showAlert('Please upload a PDF, DOCX, Markdown, or text file.', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB limit
            this.showAlert('File size must be less than 10MB.', 'error');
            return;
        }

        this.showLoading('Uploading and parsing resume...');

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/upload-resume', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.currentResume = result.resume;
                this.populateResumeForm(result.resume);
                this.updateResumePreview();
                this.showAlert('Resume uploaded and parsed successfully!', 'success');
            } else {
                this.showAlert(result.error || 'Failed to parse resume.', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showAlert('Failed to upload resume. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async optimizeResume() {
        if (this.isOptimizing) return;

        const jobDescription = document.getElementById('job-description')?.value;
        if (!jobDescription?.trim()) {
            this.showAlert('Please enter a job description for optimization.', 'warning');
            return;
        }

        if (!this.currentResume) {
            this.showAlert('Please upload a resume first.', 'warning');
            return;
        }

        this.isOptimizing = true;
        this.showLoading('AI is optimizing your resume...');
        
        const optimizeBtn = document.getElementById('optimize-btn');
        if (optimizeBtn) {
            optimizeBtn.disabled = true;
            optimizeBtn.innerHTML = '<span class="spinner"></span> Optimizing...';
        }

        try {
            const response = await fetch('/optimize-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resume: this.currentResume,
                    job_description: jobDescription
                })
            });

            const result = await response.json();

            if (result.success) {
                this.currentResume = result.optimized_resume;
                this.populateResumeForm(result.optimized_resume);
                this.updateResumePreview();
                this.displayOptimizationSuggestions(result.suggestions);
                this.showAlert('Resume optimized successfully!', 'success');
                
                // Automatically run ATS analysis
                setTimeout(() => this.analyzeATS(), 1000);
            } else {
                this.showAlert(result.error || 'Optimization failed.', 'error');
            }
        } catch (error) {
            console.error('Optimization error:', error);
            this.showAlert('Optimization failed. Please try again.', 'error');
        } finally {
            this.isOptimizing = false;
            this.hideLoading();
            
            if (optimizeBtn) {
                optimizeBtn.disabled = false;
                optimizeBtn.innerHTML = '🚀 One-Click Optimize';
            }
        }
    }

    async analyzeATS() {
        if (!this.currentResume) {
            this.showAlert('Please upload a resume first.', 'warning');
            return;
        }

        this.showLoading('Analyzing ATS compatibility...');

        try {
            const jobDescription = document.getElementById('job-description')?.value || '';
            
            const response = await fetch('/analyze-ats', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resume: this.currentResume,
                    job_description: jobDescription
                })
            });

            const result = await response.json();

            if (result.success) {
                this.currentScore = result.analysis;
                this.displayATSScore(result.analysis);
                this.displayRecommendations(result.analysis.ats_score.priority_recommendations);
                this.displayKeywordAnalysis(result.analysis.ats_score.keyword_analysis);
            } else {
                this.showAlert(result.error || 'ATS analysis failed.', 'error');
            }
        } catch (error) {
            console.error('ATS analysis error:', error);
            this.showAlert('ATS analysis failed. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async exportResume(format) {
        if (!this.currentResume) {
            this.showAlert('Please upload a resume first.', 'warning');
            return;
        }

        this.showLoading(`Exporting resume as ${format.toUpperCase()}...`);

        try {
            const response = await fetch('/export-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resume: this.currentResume,
                    format: format
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `resume.${format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showAlert(`Resume exported as ${format.toUpperCase()}!`, 'success');
            } else {
                const result = await response.json();
                this.showAlert(result.error || 'Export failed.', 'error');
            }
        } catch (error) {
            console.error('Export error:', error);
            this.showAlert('Export failed. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    populateResumeForm(resume) {
        // Contact Information
        this.setInputValue('full-name', resume.contact_info?.full_name);
        this.setInputValue('email', resume.contact_info?.email);
        this.setInputValue('phone', resume.contact_info?.phone);
        this.setInputValue('location', resume.contact_info?.location);
        this.setInputValue('linkedin-url', resume.contact_info?.linkedin_url);
        this.setInputValue('github-url', resume.contact_info?.github_url);
        this.setInputValue('portfolio-url', resume.contact_info?.portfolio_url);

        // Professional Summary
        this.setInputValue('professional-summary', resume.professional_summary);

        // Skills
        if (resume.skills && resume.skills.length > 0) {
            const skillsText = resume.skills.map(skill => skill.name).join(', ');
            this.setInputValue('skills', skillsText);
        }

        // Work Experience (simplified - just first entry for MVP)
        if (resume.work_experience && resume.work_experience.length > 0) {
            const exp = resume.work_experience[0];
            this.setInputValue('job-title', exp.job_title);
            this.setInputValue('company', exp.company);
            this.setInputValue('work-location', exp.location);
            this.setInputValue('start-date', exp.start_date);
            this.setInputValue('end-date', exp.end_date);
            
            if (exp.description && exp.description.length > 0) {
                this.setInputValue('job-description-text', exp.description.join('\n• '));
            }
        }

        // Education (simplified - just first entry for MVP)
        if (resume.education && resume.education.length > 0) {
            const edu = resume.education[0];
            this.setInputValue('degree', edu.degree);
            this.setInputValue('institution', edu.institution);
            this.setInputValue('edu-location', edu.location);
            this.setInputValue('graduation-date', edu.graduation_date);
        }
    }

    updateResumePreview() {
        const preview = document.getElementById('resume-preview');
        if (!preview) return;

        // Collect form data
        const resumeData = this.collectFormData();
        
        // Generate preview HTML
        const previewHTML = this.generatePreviewHTML(resumeData);
        preview.innerHTML = previewHTML;
    }

    collectFormData() {
        return {
            contact_info: {
                full_name: this.getInputValue('full-name'),
                email: this.getInputValue('email'),
                phone: this.getInputValue('phone'),
                location: this.getInputValue('location'),
                linkedin_url: this.getInputValue('linkedin-url'),
                github_url: this.getInputValue('github-url'),
                portfolio_url: this.getInputValue('portfolio-url')
            },
            professional_summary: this.getInputValue('professional-summary'),
            skills: this.getInputValue('skills')?.split(',').map(s => s.trim()).filter(s => s),
            work_experience: [{
                job_title: this.getInputValue('job-title'),
                company: this.getInputValue('company'),
                location: this.getInputValue('work-location'),
                start_date: this.getInputValue('start-date'),
                end_date: this.getInputValue('end-date'),
                description: this.getInputValue('job-description-text')?.split('\n').filter(s => s.trim())
            }],
            education: [{
                degree: this.getInputValue('degree'),
                institution: this.getInputValue('institution'),
                location: this.getInputValue('edu-location'),
                graduation_date: this.getInputValue('graduation-date')
            }]
        };
    }

    generatePreviewHTML(resumeData) {
        let html = '';

        // Header
        if (resumeData.contact_info.full_name) {
            html += `<h1>${resumeData.contact_info.full_name}</h1>`;
            
            const contactInfo = [];
            if (resumeData.contact_info.email) contactInfo.push(resumeData.contact_info.email);
            if (resumeData.contact_info.phone) contactInfo.push(resumeData.contact_info.phone);
            if (resumeData.contact_info.location) contactInfo.push(resumeData.contact_info.location);
            
            if (contactInfo.length > 0) {
                html += `<p style="text-align: center; margin-bottom: 1rem;">${contactInfo.join(' | ')}</p>`;
            }

            const urls = [];
            if (resumeData.contact_info.linkedin_url) urls.push(resumeData.contact_info.linkedin_url);
            if (resumeData.contact_info.github_url) urls.push(resumeData.contact_info.github_url);
            if (resumeData.contact_info.portfolio_url) urls.push(resumeData.contact_info.portfolio_url);
            
            if (urls.length > 0) {
                html += `<p style="text-align: center; margin-bottom: 1.5rem;">${urls.join(' | ')}</p>`;
            }
        }

        // Professional Summary
        if (resumeData.professional_summary) {
            html += `<h2>Professional Summary</h2>`;
            html += `<p>${resumeData.professional_summary}</p>`;
        }

        // Work Experience
        if (resumeData.work_experience[0].job_title) {
            html += `<h2>Professional Experience</h2>`;
            const exp = resumeData.work_experience[0];
            html += `<h3>${exp.job_title} | ${exp.company}</h3>`;
            
            if (exp.location || exp.start_date) {
                const details = [];
                if (exp.location) details.push(exp.location);
                if (exp.start_date) {
                    const dateRange = exp.end_date ? `${exp.start_date} - ${exp.end_date}` : `${exp.start_date} - Present`;
                    details.push(dateRange);
                }
                html += `<p><em>${details.join(' | ')}</em></p>`;
            }
            
            if (exp.description && exp.description.length > 0) {
                html += '<ul>';
                exp.description.forEach(bullet => {
                    if (bullet.trim()) {
                        html += `<li>${bullet.replace(/^[•\-\*]\s*/, '')}</li>`;
                    }
                });
                html += '</ul>';
            }
        }

        // Skills
        if (resumeData.skills && resumeData.skills.length > 0) {
            html += `<h2>Technical Skills</h2>`;
            html += `<p>${resumeData.skills.join(', ')}</p>`;
        }

        // Education
        if (resumeData.education[0].degree) {
            html += `<h2>Education</h2>`;
            const edu = resumeData.education[0];
            html += `<h3>${edu.degree}</h3>`;
            html += `<p>${edu.institution}`;
            if (edu.location) html += ` | ${edu.location}`;
            if (edu.graduation_date) html += ` | ${edu.graduation_date}`;
            html += '</p>';
        }

        return html || '<p style="color: #64748b; text-align: center; padding: 2rem;">Resume preview will appear here as you fill out the form.</p>';
    }

    displayATSScore(analysis) {
        const scoreContainer = document.getElementById('ats-score-container');
        if (!scoreContainer) return;

        const score = analysis.ats_score.overall_score;
        const level = analysis.ats_score.compatibility_level;
        
        let scoreClass = 'score-poor';
        let levelText = 'Poor';
        
        if (level === 'excellent') {
            scoreClass = 'score-excellent';
            levelText = 'Excellent';
        } else if (level === 'good') {
            scoreClass = 'score-good';
            levelText = 'Good';
        } else if (level === 'fair') {
            scoreClass = 'score-fair';
            levelText = 'Fair';
        }

        scoreContainer.innerHTML = `
            <div class="ats-score">
                <div class="score-circle ${scoreClass}">
                    ${Math.round(score)}
                </div>
                <div class="score-label">${levelText} ATS Compatibility</div>
                <div class="score-description">Your resume scores ${Math.round(score)}/100 for ATS compatibility</div>
            </div>
            
            <div class="mt-3">
                <div class="progress-label">
                    <span>Keyword Match</span>
                    <span>${Math.round(analysis.ats_score.keyword_score)}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${analysis.ats_score.keyword_score}%"></div>
                </div>
                
                <div class="progress-label">
                    <span>Formatting</span>
                    <span>${Math.round(analysis.ats_score.formatting_score)}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${analysis.ats_score.formatting_score}%"></div>
                </div>
                
                <div class="progress-label">
                    <span>Structure</span>
                    <span>${Math.round(analysis.ats_score.structure_score)}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${analysis.ats_score.structure_score}%"></div>
                </div>
                
                <div class="progress-label">
                    <span>Content Quality</span>
                    <span>${Math.round(analysis.ats_score.content_quality_score)}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${analysis.ats_score.content_quality_score}%"></div>
                </div>
            </div>
        `;
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendations-container');
        if (!container || !recommendations || recommendations.length === 0) return;

        const html = recommendations.map((rec, index) => `
            <div class="recommendation-item">
                <div class="recommendation-icon">💡</div>
                <div class="recommendation-text">${rec}</div>
                <div class="recommendation-priority priority-${index < 2 ? 'high' : index < 4 ? 'medium' : 'low'}">
                    ${index < 2 ? 'High' : index < 4 ? 'Medium' : 'Low'}
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <h3 class="mb-2">Recommendations</h3>
            <div class="recommendations">${html}</div>
        `;
    }

    displayKeywordAnalysis(keywordAnalysis) {
        const container = document.getElementById('keywords-container');
        if (!container || !keywordAnalysis) return;

        const matchedKeywords = keywordAnalysis.matched_keywords || [];
        const missingKeywords = keywordAnalysis.missing_keywords || [];

        let html = '<h3 class="mb-2">Keyword Analysis</h3>';
        
        if (matchedKeywords.length > 0) {
            html += '<h4 class="mb-1">Matched Keywords</h4>';
            html += '<div class="keywords mb-2">';
            matchedKeywords.forEach(keyword => {
                html += `<span class="keyword keyword-matched">${keyword}</span>`;
            });
            html += '</div>';
        }

        if (missingKeywords.length > 0) {
            html += '<h4 class="mb-1">Missing Keywords</h4>';
            html += '<div class="keywords mb-2">';
            missingKeywords.forEach(keyword => {
                html += `<span class="keyword keyword-missing">${keyword}</span>`;
            });
            html += '</div>';
        }

        container.innerHTML = html;
    }

    displayOptimizationSuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) return;

        const message = `Applied ${suggestions.length} AI optimizations:\n` +
            suggestions.map(s => `• ${s.section}: ${s.reasoning}`).join('\n');
        
        this.showAlert(message, 'success');
    }

    // Utility methods
    setInputValue(id, value) {
        const input = document.getElementById(id);
        if (input && value) {
            input.value = value;
        }
    }

    getInputValue(id) {
        const input = document.getElementById(id);
        return input ? input.value.trim() : '';
    }

    validateForm(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
        });

        return isValid;
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container') || document.body;
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        alertContainer.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    showLoading(message = 'Loading...') {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.innerHTML = `
                <div class="loading">
                    <span class="spinner"></span>
                    ${message}
                </div>
            `;
            loadingContainer.classList.remove('hidden');
        }
    }

    hideLoading() {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.classList.add('hidden');
        }
    }

    debounce(func, wait) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(func, wait);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.resumeBuilder = new ResumeBuilder();
});
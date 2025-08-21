# AI Resume Builder MVP 🤖📄

An AI-powered resume optimization tool that helps job seekers create ATS-compliant resumes with one-click enhancement. Built with FastHTML, OpenAI, and advanced prompting techniques.

![AI Resume Builder](https://img.shields.io/badge/AI-Powered-blue) ![ATS](https://img.shields.io/badge/ATS-Compatible-green) ![FastHTML](https://img.shields.io/badge/FastHTML-Framework-orange)

## 🚀 Features

### Core Functionality
- **📤 Multi-Format Import**: Upload resumes in PDF, DOCX, Markdown, or text format
- **🤖 One-Click AI Optimization**: Instantly optimize your resume with advanced AI prompts
- **📊 Real-Time ATS Analysis**: Get detailed compatibility scores and recommendations
- **📁 Multi-Format Export**: Download in PDF, DOCX, Markdown, HTML, text, or JSON
- **🎯 Keyword Matching**: Analyze and optimize for job description keywords
- **⚡ Live Preview**: See changes in real-time as you edit

### AI-Powered Features
- **Advanced Prompting**: Specialized prompts for different resume sections
- **Content Enhancement**: AI-generated bullet points with quantified achievements
- **Keyword Optimization**: Smart keyword integration for better ATS scores
- **Professional Summary**: AI-crafted summaries tailored to target roles
- **Skills Optimization**: Intelligent skill categorization and prioritization

### ATS Compatibility
- **Comprehensive Scoring**: 4-factor scoring system (Keywords, Formatting, Structure, Content)
- **Real-Time Analysis**: Instant feedback on ATS compatibility
- **Detailed Recommendations**: Prioritized suggestions for improvement
- **Industry Standards**: Based on Fortune 500 ATS requirements
- **Pass Rate Estimation**: Predict success rate across different ATS systems

## 🛠️ Technology Stack

- **Backend**: FastHTML (Python web framework)
- **AI/ML**: OpenAI GPT-4, PydanticAI for structured outputs
- **Document Processing**: PyPDF2, python-docx, markdown
- **Text Analysis**: scikit-learn, TF-IDF vectorization
- **Frontend**: Modern CSS3, Vanilla JavaScript
- **Data Models**: Pydantic for type safety and validation

## 📦 Installation

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (modern Python package manager)
- OpenAI API key (optional, for AI features)

### Quick Start with uv

1. **Install uv** (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**
```bash
git clone <repository-url>
cd ai_resume_builder_mvp
```

3. **Install dependencies**
```bash
uv sync
```

4. **Set up environment variables** (optional)
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

5. **Run the application**
```bash
uv run python main.py
# or use the convenience script
python scripts/start.py
# or use make
make run
```

6. **Open your browser**
```
http://localhost:8000
```

### Alternative Installation Methods

#### Using Make (Recommended for Development)
```bash
# Quick setup
make dev-setup

# Run the application
make run

# Run with AI features
OPENAI_API_KEY="your-key" make run
```

#### Using Docker
```bash
# Build and run
make docker

# Or manually
docker build -t ai-resume-builder-mvp .
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" ai-resume-builder-mvp
```

#### Traditional pip (if uv is not available)
```bash
pip install -r requirements.txt
python main.py
```

## 🎯 Usage Guide

### 1. Upload Your Resume
- Drag and drop or click to upload your resume
- Supported formats: PDF, DOCX, Markdown, Text
- AI automatically parses and structures your content

### 2. Add Target Job Description
- Paste the job description you're applying for
- AI analyzes requirements and keywords
- System identifies optimization opportunities

### 3. One-Click Optimization
- Click "🚀 One-Click Optimize" button
- AI enhances content with:
  - Keyword optimization
  - Quantified achievements
  - ATS-friendly formatting
  - Professional language

### 4. Review ATS Analysis
- Get detailed compatibility score (0-100)
- See keyword match analysis
- Review prioritized recommendations
- Track estimated pass rate

### 5. Export Optimized Resume
- Download in your preferred format
- All exports are ATS-compliant
- Ready for job applications

## 🧪 Testing

### Run Sample Tests
```bash
# Using uv
uv run python test_sample.py

# Using make
make test-sample
```

### Run Full Test Suite (when available)
```bash
# Using uv
uv run pytest

# Using make
make test
```

### Development Commands

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Run all quality checks
make check

# Clean temporary files
make clean

# Update dependencies
make update

# Show all available commands
make help
```

This will test:
- ATS analysis with sample data
- File processing and exports
- AI service availability
- Core functionality

## 📊 ATS Scoring System

The system uses a weighted scoring algorithm:

- **Keywords (40%)**: Match rate with job description
- **Formatting (25%)**: ATS-friendly structure and layout
- **Structure (20%)**: Logical organization and completeness
- **Content Quality (15%)**: Professional language and achievements

### Compatibility Levels
- **90-100**: Excellent - Ready for any ATS
- **75-89**: Good - Minor improvements recommended
- **60-74**: Fair - Several optimizations needed
- **Below 60**: Poor - Major restructuring required

## 🎨 Advanced Prompting Techniques

The system uses specialized prompts for different optimization tasks:

### Professional Summary Optimization
- Keyword integration strategies
- Value proposition frameworks
- Quantified impact statements
- Role alignment techniques

### Work Experience Enhancement
- STAR method implementation
- Action verb optimization
- Achievement quantification
- Industry-specific language

### Skills Section Optimization
- Keyword density analysis
- Skill categorization
- Relevance prioritization
- ATS-friendly formatting

## 🔧 Configuration

### Environment Variables
```bash
# Required for AI features
OPENAI_API_KEY=your-openai-api-key

# Optional: Custom port
PORT=8000
```

### File Upload Limits
- Maximum file size: 10MB
- Supported formats: PDF, DOCX, MD, TXT
- Processing timeout: 30 seconds

## 📁 Project Structure

```
ai_resume_builder_mvp/
├── main.py                 # FastHTML application
├── requirements.txt        # Python dependencies
├── test_sample.py         # Test suite
├── README.md              # This file
├── models/                # Data models
│   ├── resume_models.py   # Resume structure models
│   └── ats_models.py      # ATS analysis models
├── services/              # Business logic
│   ├── ai_service.py      # AI optimization service
│   └── ats_analyzer.py    # ATS compatibility analyzer
├── processors/            # File processing
│   └── file_processor.py  # Import/export handlers
├── static/                # Frontend assets
│   ├── css/style.css      # Modern CSS styling
│   └── js/app.js          # JavaScript functionality
├── templates/             # HTML templates (auto-generated)
├── uploads/               # Temporary file storage
└── exports/               # Export file storage
```

## 🚀 Development Roadmap

### Phase 1: MVP (Current)
- [x] Core resume builder functionality
- [x] AI-powered optimization
- [x] ATS compatibility analysis
- [x] Multi-format import/export
- [x] Real-time preview

### Phase 2: Enhanced Features
- [ ] User authentication and profiles
- [ ] Resume version history
- [ ] Advanced analytics dashboard
- [ ] Industry-specific templates
- [ ] Batch processing capabilities

### Phase 3: Enterprise Features
- [ ] Team collaboration tools
- [ ] Custom branding options
- [ ] API access for integrations
- [ ] Advanced reporting
- [ ] White-label solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for public methods
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastHTML team for the excellent framework
- ATS research from Fortune 500 companies
- Resume optimization best practices from HR professionals

## 📞 Support

For questions, issues, or feature requests:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed description
3. Include error logs and system information
4. Tag with appropriate labels

## 🔗 Related Projects

- [FastHTML](https://github.com/AnswerDotAI/fasthtml) - Modern Python web framework
- [PydanticAI](https://github.com/pydantic/pydantic-ai) - Structured AI outputs
- [OpenAI API](https://openai.com/api/) - AI language models

---

**Built with ❤️ for job seekers everywhere**

*Helping you land your dream job with AI-powered resume optimization*
# 🌍 Multilingual Academic Doubt Solver v2.0

A comprehensive, AI-powered multilingual academic doubt solving platform that supports **40+ languages** and provides intelligent answers to academic questions with automatic translation capabilities.

## ✨ **New Features in v2.0**

### 🚀 **Enhanced Multilingual Support**
- **40+ Languages**: English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Spanish, French, German, Arabic, Chinese, Japanese, Korean, and many more!
- **Smart Language Detection**: Automatic detection of user's language
- **Bidirectional Translation**: Translate questions and answers between any supported language
- **Academic Term Optimization**: Specialized translations for mathematical and scientific terms

### 🧠 **Advanced AI Capabilities**
- **Multiple QA Models**: DistilBERT with fallback to DialoGPT
- **Context-Aware Answers**: Intelligent context selection based on keywords
- **Confidence Scoring**: Quality metrics for every answer
- **Translation Quality Assessment**: Measure translation accuracy

### 📚 **Enhanced Educational Features**
- **Multi-Subject Support**: Math, Science, Social Studies, English, History, Geography
- **Class-Level Adaptation**: Content tailored for classes 1-12
- **Difficulty Levels**: Easy, Moderate, Hard questions
- **Interactive Quizzes**: Step-by-step navigation with progress tracking

### 🎯 **Improved User Experience**
- **Modern UI/UX**: Responsive design with beautiful animations
- **Real-time Language Detection**: Instant language identification
- **Progress Tracking**: Visual progress indicators for quizzes
- **Study Tips**: Language-specific study recommendations

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   AI Models     │
│   (HTML/CSS/JS) │◄──►│   (Routes)      │◄──►│   (Transformers)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Translation    │
                       │   Engine       │
                       │  (Multi-Backend)│
                       └─────────────────┘
```

## 🚀 **Quick Start**

### 1. **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/multilingual-doubt-solver.git
cd multilingual-doubt-solver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**

The application automatically detects your environment. For custom configuration:

```bash
# Set environment variables
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here
```

### 3. **Run the Application**

```bash
python app.py
```

Visit `http://localhost:5000` in your browser!

## 🌐 **Language Support**

### **Primary Languages (Full Academic Support)**
- **English (en)** - Base language with complete coverage
- **Hindi (hi)** - हिंदी - Full academic content
- **Tamil (ta)** - தமிழ் - Complete subject coverage
- **Telugu (te)** - తెలుగు - Full academic support
- **Bengali (bn)** - বাংলা - Complete subject coverage

### **Extended Language Support**
- **Marathi (mr)** - मराठी
- **Gujarati (gu)** - ગુજરાતી
- **Kannada (kn)** - ಕನ್ನಡ
- **Malayalam (ml)** - മലയാളം
- **Punjabi (pa)** - ਪੰਜਾਬੀ
- **Urdu (ur)** - اردو

### **International Languages**
- **Spanish (es)** - Español
- **French (fr)** - Français
- **German (de)** - Deutsch
- **Arabic (ar)** - العربية
- **Chinese (zh)** - 中文
- **Japanese (ja)** - 日本語
- **Korean (ko)** - 한국어

## 📚 **Academic Subjects**

### **Mathematics**
- **Classes 1-12**: Complete coverage from basic arithmetic to advanced calculus
- **Topics**: Algebra, Geometry, Trigonometry, Calculus, Statistics
- **Languages**: Full support in 11 Indian languages + English

### **Science**
- **Classes 1-12**: Comprehensive science education
- **Topics**: Physics, Chemistry, Biology, Environmental Science
- **Languages**: Full support in 11 Indian languages + English

### **Social Studies**
- **Classes 4-12**: History, Geography, Civics, Economics
- **Languages**: Full support in 11 Indian languages + English

### **English**
- **Classes 1-12**: Literature, Grammar, Writing Skills
- **Languages**: Full support in 11 Indian languages + English

## 🔧 **API Endpoints**

### **Core Functionality**
- `POST /ask` - Submit academic questions
- `GET /quiz_enhanced` - Enhanced quiz interface
- `POST /start_quiz` - Start a new quiz
- `POST /submit_quiz` - Submit quiz answers

### **Translation APIs**
- `POST /api/translate` - Translate text between languages
- `POST /api/detect_language` - Auto-detect text language
- `GET /api/study_tips/<subject>` - Get study tips in any language

### **Example API Usage**

```python
import requests

# Translate text
response = requests.post('/api/translate', json={
    'text': 'What is photosynthesis?',
    'source_lang': 'en',
    'target_lang': 'hi'
})

# Detect language
response = requests.post('/api/detect_language', json={
    'text': 'प्रकाश संश्लेषण क्या है?'
})
```

## 📁 **File Structure**

```
multilingual-doubt-solver/
├── app/
│   ├── __init__.py
│   ├── routes.py          # Enhanced API routes
│   ├── qa_model.py        # AI model integration
│   ├── translator.py       # Multi-backend translation
│   ├── data_loader.py     # Content loading utilities
│   └── utils.py           # Helper functions
├── templates/
│   ├── index.html         # Enhanced home page
│   ├── ask.html           # Question input interface
│   ├── result.html        # Answer display with metadata
│   ├── quiz_enhanced.html # Quiz selection interface
│   ├── quiz_questions.html # Interactive quiz interface
│   └── quiz_result.html   # Quiz results with feedback
├── data/                  # Academic content files
├── static/                # CSS and JavaScript assets
├── config.py              # Enhanced configuration
├── app.py                 # Main application
└── requirements.txt       # Dependencies
```

## 🎨 **Customization**

### **Adding New Languages**

1. **Update Configuration**
```python
# In config.py
LANGUAGES['new_lang'] = 'New Language Name'
```

2. **Add Language-Specific Content**
```python
# Create language-specific context files
FILE_PATHS['context_files']['math']['new_lang'] = 'data/math_new_lang.txt'
```

3. **Add Academic Terms**
```python
# In translator.py
ACADEMIC_TERMS['math']['new_lang'] = {
    'addition': 'translation_here',
    'subtraction': 'translation_here'
}
```

### **Adding New Subjects**

```python
# In config.py
ACADEMIC_SUBJECTS['new_subject'] = {
    'name': 'New Subject Name',
    'languages': ['en', 'hi', 'ta'],
    'difficulty_levels': ['easy', 'moderate', 'hard'],
    'class_range': [1, 12]
}
```

## 🔒 **Security Features**

- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Protection against abuse
- **Error Handling**: Secure error messages
- **Language Validation**: Safe language code handling

## 📊 **Performance Features**

- **Smart Caching**: Translation and model result caching
- **Async Processing**: Background task handling
- **Model Fallbacks**: Multiple AI model support
- **Optimized Queries**: Efficient context searching

## 🧪 **Testing**

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

## 🚀 **Deployment**

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### **Environment Variables**
```bash
FLASK_ENV=production
SECRET_KEY=your-production-secret
PORT=5000
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Areas for Contribution**
- 🆕 New language support
- 🔧 Bug fixes and improvements
- 📚 Additional academic content
- 🎨 UI/UX enhancements
- 🧪 Testing and documentation

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Hugging Face Transformers** for AI models
- **Google Translate** for translation services
- **NCERT** for educational content
- **Open Source Community** for inspiration and support

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/multilingual-doubt-solver/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/multilingual-doubt-solver/discussions)
- **Email**: support@yourdomain.com

---

**Made with ❤️ for global education accessibility**

*Empowering students worldwide to learn in their native language*


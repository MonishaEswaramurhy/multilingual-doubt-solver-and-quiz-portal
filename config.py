import os
from typing import Dict, List

# Application Configuration
APP_NAME = "Multilingual Academic Doubt Solver"
APP_VERSION = "2.0.0"
DEBUG = os.environ.get('FLASK_ENV') == 'development'

# Supported Languages with their codes and display names
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ar': 'Arabic',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'it': 'Italian',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'he': 'Hebrew',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'fa': 'Persian',
    'uk': 'Ukrainian',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian'
}

# Academic Subjects Configuration
ACADEMIC_SUBJECTS = {
    'math': {
        'name': 'Mathematics',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [1, 12]
    },
    'science': {
        'name': 'Science',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [1, 12]
    },
    'social': {
        'name': 'Social Studies',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [4, 12]
    },
    'english': {
        'name': 'English',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [1, 12]
    },
    'history': {
        'name': 'History',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [6, 12]
    },
    'geography': {
        'name': 'Geography',
        'languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
        'difficulty_levels': ['easy', 'moderate', 'hard'],
        'class_range': [6, 12]
    }
}

# Translation Configuration
TRANSLATION_CONFIG = {
    'default_source_language': 'en',
    'fallback_language': 'en',
    'supported_source_languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'],
    'translation_cache_enabled': True,
    'translation_cache_ttl': 3600,  # 1 hour
    'max_text_length': 5000,
    'batch_translation_size': 10
}

# AI Model Configuration
AI_MODEL_CONFIG = {
    'qa_model': 'distilbert-base-cased-distilled-squad',
    'fallback_qa_model': 'microsoft/DialoGPT-medium',
    'keyword_extraction_model': 'all-MiniLM-L6-v2',
    'max_context_length': 2000,
    'min_confidence_threshold': 0.3,
    'max_answer_length': 500
}

# Quiz Configuration
QUIZ_CONFIG = {
    'default_question_count': 5,
    'max_question_count': 20,
    'time_limit_per_question': 60,  # seconds
    'shuffle_questions': True,
    'shuffle_options': True,
    'show_explanations': True,
    'allow_review': True
}

# File Paths Configuration
FILE_PATHS = {
    'data_directory': 'data/',
    'context_files': {
        'math': {
            'en': 'data/ncert_math_class9.txt',
            'hi': 'data/ncert_math_class9_hi.txt',
            'ta': 'data/ncert_math_class9_ta.txt',
            'te': 'data/ncert_math_class9_te.txt',
            'bn': 'data/ncert_math_class9_bn.txt'
        },
        'science': {
            'en': 'data/ncert_science_class9.txt',
            'hi': 'data/ncert_science_class9_hi.txt',
            'ta': 'data/ncert_science_class9_ta.txt',
            'te': 'data/ncert_science_class9_te.txt',
            'bn': 'data/ncert_science_class9_bn.txt'
        },
        'social': {
            'en': 'data/ncert_social_class9.txt',
            'hi': 'data/ncert_social_class9_hi.txt',
            'ta': 'data/ncert_social_class9_ta.txt',
            'te': 'data/ncert_social_class9_te.txt',
            'bn': 'data/ncert_social_class9_bn.txt'
        },
        'english': {
            'en': 'data/ncert_english_class9.txt',
            'hi': 'data/ncert_english_class9_hi.txt',
            'ta': 'data/ncert_english_class9_ta.txt',
            'te': 'data/ncert_english_class9_te.txt',
            'bn': 'data/ncert_english_class9_bn.txt'
        }
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
    'file': 'app.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_caching': True,
    'cache_timeout': 300,  # 5 minutes
    'max_concurrent_requests': 10,
    'request_timeout': 30,  # seconds
    'enable_compression': True
}

def get_config(config_name: str = None):
    """Get configuration object based on environment"""
    class Config:
        # Basic Flask configuration
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
        DEBUG = DEBUG
        
        # Application specific configuration
        APP_NAME = APP_NAME
        APP_VERSION = APP_VERSION
        
        # Language and subject configuration
        LANGUAGES = LANGUAGES
        ACADEMIC_SUBJECTS = ACADEMIC_SUBJECTS
        
        # Feature configuration
        TRANSLATION_CONFIG = TRANSLATION_CONFIG
        AI_MODEL_CONFIG = AI_MODEL_CONFIG
        QUIZ_CONFIG = QUIZ_CONFIG
        FILE_PATHS = FILE_PATHS
        LOGGING_CONFIG = LOGGING_CONFIG
        PERFORMANCE_CONFIG = PERFORMANCE_CONFIG
        
        # Flask specific settings
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
        JSON_AS_ASCII = False  # Support for non-ASCII characters
        
    return Config

def get_supported_languages() -> Dict[str, str]:
    """Get supported languages dictionary"""
    return LANGUAGES

def get_academic_subjects() -> Dict[str, Dict]:
    """Get academic subjects configuration"""
    return ACADEMIC_SUBJECTS

def get_subject_languages(subject: str) -> List[str]:
    """Get supported languages for a specific subject"""
    return ACADEMIC_SUBJECTS.get(subject.lower(), {}).get('languages', ['en'])

def is_language_supported(language: str) -> bool:
    """Check if a language is supported"""
    return language in LANGUAGES

def get_language_name(language_code: str) -> str:
    """Get language name from language code"""
    return LANGUAGES.get(language_code, language_code.upper())

import logging
import requests
import json
from typing import Optional, Dict, List
import time
from urllib.parse import quote_plus

# Unofficial Google Translate endpoint (no external deps)
GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

# Supported languages with their codes and display names
SUPPORTED_LANGUAGES = {
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

# Academic subject-specific translation mappings
ACADEMIC_TERMS = {
    'math': {
        'en': {
            'addition': 'addition',
            'subtraction': 'subtraction',
            'multiplication': 'multiplication',
            'division': 'division',
            'fraction': 'fraction',
            'decimal': 'decimal',
            'percentage': 'percentage',
            'algebra': 'algebra',
            'geometry': 'geometry',
            'trigonometry': 'trigonometry',
            'calculus': 'calculus'
        },
        'hi': {
            'addition': 'जोड़',
            'subtraction': 'घटाव',
            'multiplication': 'गुणा',
            'division': 'भाग',
            'fraction': 'भिन्न',
            'decimal': 'दशमलव',
            'percentage': 'प्रतिशत',
            'algebra': 'बीजगणित',
            'geometry': 'ज्यामिति',
            'trigonometry': 'त्रिकोणमिति',
            'calculus': 'कैलकुलस'
        },
        'ta': {
            'addition': 'கூட்டல்',
            'subtraction': 'கழித்தல்',
            'multiplication': 'பெருக்கல்',
            'division': 'வகுத்தல்',
            'fraction': 'பின்னம்',
            'decimal': 'தசமம்',
            'percentage': 'சதவீதம்',
            'algebra': 'இயற்கணிதம்',
            'geometry': 'வடிவியல்',
            'trigonometry': 'முக்கோணவியல்',
            'calculus': 'நுண்கணிதம்'
        }
    },
    'science': {
        'en': {
            'atom': 'atom',
            'molecule': 'molecule',
            'cell': 'cell',
            'organism': 'organism',
            'ecosystem': 'ecosystem',
            'energy': 'energy',
            'force': 'force',
            'gravity': 'gravity',
            'electricity': 'electricity',
            'magnetism': 'magnetism'
        },
        'hi': {
            'atom': 'परमाणु',
            'molecule': 'अणु',
            'cell': 'कोशिका',
            'organism': 'जीव',
            'ecosystem': 'पारिस्थितिकी तंत्र',
            'energy': 'ऊर्जा',
            'force': 'बल',
            'gravity': 'गुरुत्वाकर्षण',
            'electricity': 'विद्युत',
            'magnetism': 'चुंबकत्व'
        },
        'ta': {
            'atom': 'அணு',
            'molecule': 'மூலக்கூறு',
            'cell': 'செல்',
            'organism': 'உயிரினம்',
            'ecosystem': 'சுற்றுச்சூழல் அமைப்பு',
            'energy': 'ஆற்றல்',
            'force': 'விசை',
            'gravity': 'ஈர்ப்பு விசை',
            'electricity': 'மின்சாரம்',
            'magnetism': 'காந்தவியல்'
        }
    }
}

class TranslationManager:
    """Manages multiple translation backends with fallback support"""
    
    def __init__(self):
        self.backends = ['google', 'microsoft', 'yandex']
        self.current_backend = 0
        self.retry_count = 0
        self.max_retries = 3
    
    def translate_with_fallback(self, text: str, src_lang: str = None, dest_lang: str = 'en') -> str:
        """Translate text using multiple backends with fallback"""
        if not text or src_lang == dest_lang:
            return text
        
        for attempt in range(self.max_retries):
            try:
                if self.current_backend == 0:  # Google Translate
                    return self._translate_google(text, src_lang, dest_lang)
                elif self.current_backend == 1:  # Microsoft Translator (placeholder)
                    return self._translate_microsoft(text, src_lang, dest_lang)
                elif self.current_backend == 2:  # Yandex (placeholder)
                    return self._translate_yandex(text, src_lang, dest_lang)
            except Exception as e:
                logging.warning(f"Translation backend {self.current_backend} failed: {e}")
                self.current_backend = (self.current_backend + 1) % len(self.backends)
                continue
        
        # If all backends fail, return original text
        logging.error("All translation backends failed")
        return text
    
    def _translate_google(self, text: str, src_lang: str, dest_lang: str) -> str:
        """Translate using Google Translate via the public endpoint."""
        try:
            params = {
                'client': 'gtx',
                'sl': src_lang or 'auto',
                'tl': dest_lang,
                'dt': 't',
                'q': text
            }
            resp = requests.get(GOOGLE_TRANSLATE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # data[0] contains translated segments
            return ''.join([seg[0] for seg in data[0]])
        except Exception as e:
            logging.error(f"Google translation failed: {e}")
            raise
    
    def _translate_microsoft(self, text: str, src_lang: str, dest_lang: str) -> str:
        """Placeholder for Microsoft Translator API"""
        # This would require Azure Cognitive Services subscription
        logging.info("Microsoft Translator not configured, falling back to Google")
        return self._translate_google(text, src_lang, dest_lang)
    
    def _translate_yandex(self, text: str, src_lang: str, dest_lang: str) -> str:
        """Placeholder for Yandex Translator API"""
        # This would require Yandex API key
        logging.info("Yandex Translator not configured, falling back to Google")
        return self._translate_google(text, src_lang, dest_lang)

# Initialize translation manager
translation_manager = TranslationManager()

def detect_language(text: str) -> str:
    """Detect the language of the input text with improved accuracy"""
    try:
        if not text or len(text.strip()) < 3:
            return 'en'
        
        # Use Google Translate auto-detection
        params = {
            'client': 'gtx',
            'sl': 'auto',
            'tl': 'en',
            'dt': 't',
            'q': text
        }
        resp = requests.get(GOOGLE_TRANSLATE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # The detected language is usually in data[2]
        detected_lang = data[2] if len(data) > 2 else 'en'

        # Normalize to supported languages
        if detected_lang in SUPPORTED_LANGUAGES:
            return detected_lang
        else:
            lang_mapping = {
                'zh-cn': 'zh', 'zh-tw': 'zh', 'zh-hans': 'zh', 'zh-hant': 'zh',
                'en-gb': 'en', 'en-us': 'en', 'en-au': 'en',
                'hi-in': 'hi', 'ta-in': 'ta', 'te-in': 'te', 'bn-in': 'bn'
            }
            return lang_mapping.get(detected_lang, 'en')

    except Exception as e:
        logging.error(f"Language detection failed: {e}")
        return 'en'

def translate_to_en(text: str, src_lang: str = None) -> str:
    """Translate text to English with academic term optimization"""
    if not text:
        return text
    
    try:
        if src_lang == 'en' or src_lang is None:
            return text
        
        # If source language not specified, detect it
        if src_lang is None:
            src_lang = detect_language(text)
            if src_lang == 'en':
                return text
        
        # Use translation manager with fallback
        translated_text = translation_manager.translate_with_fallback(text, src_lang, 'en')
        
        # Post-process for academic terms
        translated_text = _optimize_academic_terms(translated_text, 'en')
        
        return translated_text
        
    except Exception as e:
        logging.error(f"Translation to English failed: {e}")
        return text

def translate_from_en(text: str, dest_lang: str) -> str:
    """Translate text from English to target language with academic term optimization"""
    if not text:
        return text
    
    try:
        if dest_lang == 'en':
            return text
        
        # Pre-process for academic terms
        processed_text = _optimize_academic_terms(text, dest_lang)
        
        # Use translation manager with fallback
        translated_text = translation_manager.translate_with_fallback(processed_text, 'en', dest_lang)
        
        return translated_text
        
    except Exception as e:
        logging.error(f"Translation from English failed: {e}")
        return text

def translate_text(text: str, src_lang: str = None, dest_lang: str = 'en') -> str:
    """General translation function with enhanced features"""
    if not text:
        return text
    
    try:
        # If source language not specified, detect it
        if src_lang is None:
            src_lang = detect_language(text)
        
        # If source and destination are the same, return original text
        if src_lang == dest_lang:
            return text
        
        # Translate to English first if source is not English
        if src_lang != 'en':
            text = translate_to_en(text, src_lang)
        
        # Translate to destination language if not English
        if dest_lang != 'en':
            text = translate_from_en(text, dest_lang)
        
        return text
        
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return text

def _optimize_academic_terms(text: str, target_lang: str) -> str:
    """Optimize academic terms for better translation quality"""
    if target_lang not in ['en', 'hi', 'ta']:
        return text
    
    # Replace common academic terms with their proper translations
    for subject, terms in ACADEMIC_TERMS.items():
        if target_lang in terms:
            for term_en, term_local in terms[target_lang].items():
                # Use case-insensitive replacement
                import re
                pattern = re.compile(re.escape(term_en), re.IGNORECASE)
                text = pattern.sub(term_local, text)
    
    return text

def get_language_name(code: str) -> str:
    """Get language name from code"""
    return SUPPORTED_LANGUAGES.get(code, code.upper())

def get_supported_languages() -> Dict[str, str]:
    """Get list of supported languages"""
    return SUPPORTED_LANGUAGES

def get_language_family(code: str) -> str:
    """Get language family for better translation grouping"""
    language_families = {
        'indo-aryan': ['hi', 'bn', 'mr', 'gu', 'pa', 'ur'],
        'dravidian': ['ta', 'te', 'ml', 'kn'],
        'romance': ['es', 'fr', 'it', 'pt', 'ro'],
        'germanic': ['en', 'de', 'nl', 'sv', 'no', 'da'],
        'slavic': ['ru', 'uk', 'cs', 'pl', 'bg', 'hr', 'sk', 'sl'],
        'semitic': ['ar', 'he'],
        'sino-tibetan': ['zh', 'th'],
        'japonic': ['ja'],
        'koreanic': ['ko'],
        'turkic': ['tr'],
        'finnic': ['fi', 'et'],
        'baltic': ['lv', 'lt'],
        'celtic': ['ga', 'cy'],
        'uralic': ['hu']
    }
    
    for family, languages in language_families.items():
        if code in languages:
            return family
    
    return 'other'

def is_similar_language(lang1: str, lang2: str) -> bool:
    """Check if two languages are similar (same family)"""
    return get_language_family(lang1) == get_language_family(lang2)

def get_translation_quality_score(text: str, original_text: str, target_lang: str) -> float:
    """Calculate translation quality score (0-1)"""
    try:
        if not text or not original_text:
            return 0.0
        
        # Simple heuristic: longer translations tend to be better
        # This is a basic implementation - in production you'd use more sophisticated metrics
        original_length = len(original_text.strip())
        translated_length = len(text.strip())
        
        if original_length == 0:
            return 0.0
        
        # Length ratio (closer to 1 is better)
        length_ratio = min(translated_length / original_length, original_length / translated_length)
        
        # Basic quality indicators
        quality_score = length_ratio * 0.6  # 60% weight to length ratio
        
        # Bonus for maintaining structure
        if text.count('.') >= original_text.count('.') * 0.8:
            quality_score += 0.2
        
        # Bonus for maintaining question marks
        if text.count('?') >= original_text.count('?') * 0.8:
            quality_score += 0.2
        
        return min(quality_score, 1.0)
        
    except Exception as e:
        logging.error(f"Error calculating translation quality: {e}")
        return 0.5  # Default score

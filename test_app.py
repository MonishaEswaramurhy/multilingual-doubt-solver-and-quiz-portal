#!/usr/bin/env python3
"""
Simple test script for the Multilingual Academic Doubt Solver
"""

import requests
import json

def test_home_page():
    """Test the home page"""
    try:
        response = requests.get('http://localhost:5000/')
        print(f"Home page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Home page working")
        else:
            print("❌ Home page failed")
    except Exception as e:
        print(f"❌ Error accessing home page: {e}")

def test_ask_page():
    """Test the ask page"""
    try:
        response = requests.get('http://localhost:5000/ask')
        print(f"Ask page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Ask page working")
        else:
            print("❌ Ask page failed")
    except Exception as e:
        print(f"❌ Error accessing ask page: {e}")

def test_question_submission():
    """Test submitting a question"""
    try:
        data = {
            'subject': 'math',
            'lang': 'en',
            'question': 'What is mathematics?'
        }
        response = requests.post('http://localhost:5000/ask', data=data)
        print(f"Question submission status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Question submission working")
        else:
            print("❌ Question submission failed")
    except Exception as e:
        print(f"❌ Error submitting question: {e}")

def test_translation_api():
    """Test the translation API"""
    try:
        data = {
            'text': 'What is mathematics?',
            'source_lang': 'en',
            'target_lang': 'hi'
        }
        response = requests.post('http://localhost:5000/api/translate', json=data)
        print(f"Translation API status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Translation working: {result.get('translated_text', 'N/A')}")
        else:
            print("❌ Translation API failed")
    except Exception as e:
        print(f"❌ Error testing translation API: {e}")

def test_language_detection():
    """Test language detection"""
    try:
        data = {
            'text': 'गणित क्या है?'
        }
        response = requests.post('http://localhost:5000/api/detect_language', json=data)
        print(f"Language detection status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Language detection working: {result.get('detected_language', 'N/A')}")
        else:
            print("❌ Language detection failed")
    except Exception as e:
        print(f"❌ Error testing language detection: {e}")

if __name__ == "__main__":
    print("🧪 Testing Multilingual Academic Doubt Solver")
    print("=" * 50)
    
    test_home_page()
    print()
    
    test_ask_page()
    print()
    
    test_question_submission()
    print()
    
    test_translation_api()
    print()
    
    test_language_detection()
    print()
    
    print("🎯 Testing completed!")


from flask import Blueprint, render_template, request, jsonify, session
from app.translator import translate_to_en, translate_from_en, get_supported_languages, detect_language
from app.qa_model import get_answer, generate_mcq, generate_quiz_questions, get_study_tips
from random import shuffle
import logging

main_blueprint = Blueprint('main', __name__)

# Home page
@main_blueprint.route('/')
def index():
    languages = get_supported_languages()
    return render_template('index.html', languages=languages)

@main_blueprint.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'GET':
        languages = get_supported_languages()
        return render_template('ask.html', languages=languages)
    
    try:
        answer_lang = request.form.get('lang', 'en')  # Language for answer translation
        question = request.form.get('question', '').strip()
        subject = request.form.get('subject', 'science').lower()
        
        if not question:
            languages = get_supported_languages()
            return render_template('ask.html', error="Please enter a question", languages=languages)
        
        # Questions are always processed in English
        # Get answer using the enhanced QA model (always in English)
        answer_en, context_used, metadata = get_answer(question, subject, 'en')
        
        # Translate answer and context to user's language if needed
        if answer_lang != 'en':
            try:
                answer_local = translate_from_en(answer_en, answer_lang)
                context_local = translate_from_en(context_used, answer_lang)
            except Exception as e:
                logging.warning(f"Translation failed, using English: {e}")
                answer_local = answer_en
                context_local = context_used
        else:
            answer_local = answer_en
            context_local = context_used
        
        # Get study tips for the subject in user's language
        study_tips = get_study_tips(subject, answer_lang)
        
        return render_template(
            'result.html',
            question=question,
            answer=answer_local,
            context=context_local,
            lang=answer_lang,
            subject=subject,
            study_tips=study_tips,
            metadata=metadata
        )
        
    except Exception as e:
        logging.error(f"Error in ask route: {e}")
        languages = get_supported_languages()
        return render_template('ask.html', error="An error occurred. Please try again.", languages=languages)

# Quiz page
@main_blueprint.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        try:
            question = request.form.get('question', '').strip()
            if not question:
                return render_template('quiz_input.html', error="Please enter a question")
            
            answer, context, metadata = get_answer(question, 'science', 'en')
            options = generate_mcq(answer)
            shuffle(options)
            
            return render_template(
                'quiz.html',
                question=question,
                context=context,
                options=options,
                correct=answer
            )
        except Exception as e:
            logging.error(f"Error in quiz route: {e}")
            return render_template('quiz_input.html', error="An error occurred. Please try again.")
    
    classes = list(range(1, 13))
    languages = get_supported_languages()
    return render_template('quiz.html', classes=classes, languages=languages)

# Enhanced quiz selection page
@main_blueprint.route('/quiz_enhanced')
def quiz_enhanced():
    classes = list(range(1, 13))
    languages = get_supported_languages()
    subjects = ['Math', 'Science', 'Social Studies', 'English', 'History', 'Geography']
    difficulties = ['Easy', 'Moderate', 'Hard']
    
    return render_template('quiz_enhanced.html', 
                         classes=classes, 
                         languages=languages, 
                         subjects=subjects, 
                         difficulties=difficulties)

# Start quiz by reading Excel file with multilingual support
@main_blueprint.route('/start_quiz', methods=['POST'])
def start_quiz():
    try:
        subject = request.form.get('subject', '').strip()
        language = request.form.get('language', 'en').strip()
        selected_class = request.form.get('class', '').strip()
        difficulty = request.form.get('difficulty', 'easy').strip()
        
        if not all([subject, language, selected_class, difficulty]):
            return "Missing required parameters", 400
        
        filename = find_quiz_file(selected_class, subject, difficulty)
        if not filename:
            available = _list_quiz_files_for(selected_class, difficulty)
            if available:
                msg = (
                    f"Quiz file for class {selected_class}, difficulty {difficulty} not found for subject '{subject}'. "
                    f"Available files: " + ", ".join(os.path.basename(p) for p in available)
                )
            else:
                msg = (
                    f"No quiz files found for class {selected_class} and difficulty {difficulty}. "
                    f"Please add an Excel file like 'class{selected_class}{_normalize_subject(subject)}{difficulty}.xlsx' "
                    f"to the project root or 'data/' directory."
                )
            return msg, 404
        
        logging.info(f"[quiz] Start quiz using file: {filename}")
        
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            return f"Error reading quiz file: {e}", 500
        
        # Check if required columns exist
        required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'answer']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f"Quiz file is missing required columns: {missing_columns}", 500
        
        questions = []
        for _, row in df.iterrows():
            question_data = {
                'q': row['question'],
                'options': [row['option1'], row['option2'], row['option3'], row['option4']],
                'answer': row['answer']
            }
            
            # Translate question and options if language is not English
            if language != 'en':
                try:
                    question_data['q'] = translate_from_en(row['question'], language)
                    question_data['options'] = [translate_from_en(opt, language) for opt in question_data['options']]
                    question_data['answer'] = translate_from_en(row['answer'], language)
                except Exception as e:
                    logging.warning(f"Translation failed for question: {e}")
            
            questions.append(question_data)
        
        return render_template(
            'quiz_questions.html',
            questions=questions,
            subject=subject,
            selected_class=selected_class,
            difficulty=difficulty,
            language=language
        )
        
    except Exception as e:
        logging.error(f"Error in start_quiz: {e}")
        return "An error occurred while starting the quiz", 500

# Submit quiz and calculate score with multilingual support
@main_blueprint.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        subject = request.form.get("subject")
        selected_class = request.form.get("selected_class")
        difficulty = request.form.get("difficulty")
        language = request.form.get("language", "en")
        
        # Resolve the same Excel file again to access correct answers
        filepath = find_quiz_file(selected_class, subject, difficulty)
        if not filepath:
            available = _list_quiz_files_for(selected_class, difficulty)
            if available:
                return (
                    "Unable to locate the quiz file again when scoring. Found instead: "
                    + ", ".join(os.path.basename(p) for p in available)
                ), 404
            return "Quiz file not found!", 404
        
        logging.info(f"[quiz] Submit quiz using file: {filepath}")
        
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            return f"Error loading quiz file: {e}", 500
        
        score = 0
        user_answers = []
        correct_answers = df['answer'].tolist()
        questions = df['question'].tolist()
        
        # Compare submitted answers with correct ones
        for i in range(len(questions)):
            user_ans = request.form.get(f'q{i}')
            user_answers.append(user_ans)
            
            if user_ans and user_ans.strip().lower() == str(correct_answers[i]).strip().lower():
                score += 1
        
        # Calculate percentage
        percentage = (score / len(questions)) * 100 if questions else 0
        
        # Get performance feedback
        if percentage >= 80:
            feedback = "Excellent! You have a strong understanding of this topic."
        elif percentage >= 60:
            feedback = "Good job! Keep practicing to improve further."
        else:
            feedback = "Keep studying! Review the material and try again."
        
        # Translate feedback if needed
        if language != 'en':
            try:
                feedback = translate_from_en(feedback, language)
            except Exception as e:
                logging.warning(f"Failed to translate feedback: {e}")
        
        return render_template(
            'quiz_result.html',
            score=score,
            total=len(questions),
            percentage=percentage,
            feedback=feedback,
            user_answers=user_answers,
            correct_answers=correct_answers,
            questions=questions,
            language=language
        )
        
    except Exception as e:
        logging.error(f"Error in submit_quiz: {e}")
        return "An error occurred while processing your quiz", 500

# API endpoint for language detection
@main_blueprint.route('/api/detect_language', methods=['POST'])
def api_detect_language():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        detected_lang = detect_language(text)
        lang_name = get_supported_languages().get(detected_lang, detected_lang.upper())
        
        return jsonify({
            'detected_language': detected_lang,
            'language_name': lang_name,
            'confidence': 0.9  # Placeholder confidence score
        })
        
    except Exception as e:
        logging.error(f"Error in language detection API: {e}")
        return jsonify({'error': 'Language detection failed'}), 500

# API endpoint for getting study tips
@main_blueprint.route('/api/study_tips/<subject>')
def api_study_tips(subject):
    try:
        language = request.args.get('language', 'en')
        tips = get_study_tips(subject, language)
        return jsonify({'subject': subject, 'tips': tips, 'language': language})
    except Exception as e:
        logging.error(f"Error getting study tips: {e}")
        return jsonify({'error': 'Failed to get study tips'}), 500

# API endpoint for translation
@main_blueprint.route('/api/translate', methods=['POST'])
def api_translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if source_lang == 'auto':
            source_lang = detect_language(text)
        
        from app.translator import translate_text
        translated_text = translate_text(text, source_lang, target_lang)
        
        return jsonify({
            'original_text': text,
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang
        })
        
    except Exception as e:
        logging.error(f"Error in translation API: {e}")
        return jsonify({'error': 'Translation failed'}), 500

# Import required functions and modules
import pandas as pd
import os
from typing import Optional, List

def _list_quiz_files_for(class_str: str, difficulty: str) -> List[str]:
    """Return available quiz files for a given class and difficulty across root and data/."""
    possible_dirs = [".", "data"]
    matches: List[str] = []
    prefix = f"class{class_str}".lower()
    suffix = f"{difficulty}.xlsx".lower()
    for base in possible_dirs:
        try:
            for name in os.listdir(base):
                low = name.lower()
                if low.startswith(prefix) and low.endswith(suffix) and low.endswith(".xlsx"):
                    matches.append(os.path.join(base, name))
        except FileNotFoundError:
            continue
    return matches

def _normalize_subject(subject: str) -> str:
    mapping = {
        "maths": "math",
        "mathematics": "math",
        "cs": "computer",
        "comp": "computer",
        "cse": "computer",
        "sci": "science",
        "soc": "social",
        "socialstudies": "social",
        "bstudies": "businessstudies",
        "bst": "businessstudies",
        "eco": "economics",
        "acc": "accounts",
        "phy": "physics",
        "chem": "chemistry",
        "bio": "biology",
        "eng": "english",
        "evs": "evs",
        "history": "history",
    }
    s = (subject or "").strip().lower()
    return mapping.get(s, s)

def find_quiz_file(selected_class: str, subject: str, difficulty: str) -> Optional[str]:
    """Try to find the best matching quiz file."""
    normalized_subject = _normalize_subject(subject)
    
    exact_root = f"class{selected_class}{normalized_subject}{difficulty}.xlsx"
    exact_data = os.path.join("data", exact_root)
    if os.path.exists(exact_root):
        logging.info(f"[quiz] Using exact file: {exact_root}")
        return exact_root
    if os.path.exists(exact_data):
        logging.info(f"[quiz] Using exact file from data/: {exact_data}")
        return exact_data
    
    # Fuzzy find
    candidates = _list_quiz_files_for(selected_class, difficulty)
    logging.info(f"[quiz] Candidates for class={selected_class} difficulty={difficulty}: {candidates}")
    if not candidates:
        return None
    
    # Prefer a candidate that includes the subject keyword
    for path in candidates:
        if normalized_subject and normalized_subject in os.path.basename(path).lower():
            logging.info(f"[quiz] Fuzzy subject match: {path}")
            return path
    
    # Accept common variants for math specifically
    if normalized_subject == "math":
        for variant in ["mathe", "mathh", "mathm", "matheasy", "mathe", "mat"]:
            for path in candidates:
                if variant in os.path.basename(path).lower():
                    logging.info(f"[quiz] Fuzzy math variant match: {path}")
                    return path
    
    # Fall back to first available
    if candidates:
        logging.info(f"[quiz] Falling back to first candidate: {candidates[0]}")
        return candidates[0]
    return None

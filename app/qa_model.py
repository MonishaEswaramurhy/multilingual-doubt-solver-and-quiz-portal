from transformers import pipeline
from app.data_loader import load_context_file, split_into_chunks, find_best_context
from app.translator import translate_to_en, translate_from_en, detect_language
import random
from keybert import KeyBERT
import logging
import os

kw_model = KeyBERT()

# Initialize QA pipeline with a better model
try:
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    logging.info("Loaded DistilBERT QA model")
except Exception as e:
    logging.error(f"Failed to load QA model: {e}")
    qa_pipeline = None

# Subject-specific context files
SUBJECT_CONTEXTS = {
    'math': "data/test_context.txt",  # Use test context for now
    'science': "data/test_context.txt",
    'social': "data/test_context.txt",
    'english': "data/test_context.txt",
    'history': "data/test_context.txt",  # Added history
    'geography': "data/test_context.txt"  # Added geography
}

# Load contexts for different subjects
subject_contexts = {}
for subject, path in SUBJECT_CONTEXTS.items():
    try:
        if os.path.exists(path):
            full_text = load_context_file(path)
            if full_text:
                subject_contexts[subject] = split_into_chunks(full_text)
                logging.info(f"Loaded context for {subject}")
            else:
                logging.warning(f"Empty context file for {subject}")
        else:
            logging.warning(f"Context file not found: {path}")
    except Exception as e:
        logging.warning(f"Could not load context for {subject}: {e}")

# Create fallback context if no files are loaded
if not any(subject_contexts.values()):
    logging.warning("No context files loaded, creating fallback context")
    fallback_context = """
    This is a fallback context for the academic doubt solver. 
    The system is designed to help students with their academic questions.
    Please ensure that appropriate context files are available in the data directory.
    """
    fallback_chunks = split_into_chunks(fallback_context)
    for subject in SUBJECT_CONTEXTS.keys():
        subject_contexts[subject] = fallback_chunks


# Subject-specific fallback knowledge
SUBJECT_KNOWLEDGE = {
    'history': {
        'father of india': 'Mahatma Gandhi is often called the Father of India. He was a leader of the Indian independence movement against British rule.',
        'who is father of nation': 'Mahatma Gandhi is known as the Father of the Nation in India.',
        'gandhi': 'Mahatma Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist who led the successful campaign for India\'s independence.',
        'independence day': 'India gained independence from British rule on August 15, 1947.',
        'first prime minister': 'Jawaharlal Nehru was the first Prime Minister of independent India.',
        'partition': 'The partition of India in 1947 led to the creation of two independent nations: India and Pakistan.'
    },
    'geography': {
        'capital of india': 'New Delhi is the capital of India.',
        'largest state': 'Rajasthan is the largest state in India by area.',
        'longest river': 'The Ganges (Ganga) is considered the longest river in India.',
        'highest mountain': 'Kanchenjunga is the highest mountain peak in India.',
        'monsoon': 'Monsoon is the seasonal wind pattern that brings heavy rainfall to India during summer months.'
    },
    'math': {
        'equation of straight line': 'The general equation of a straight line is y = mx + c, where m is the slope and c is the y-intercept. Another form is Ax + By + C = 0.',
        'straight line equation': 'The general equation of a straight line is y = mx + c, where m is the slope and c is the y-intercept. Another form is Ax + By + C = 0.',
        'line equation': 'The general equation of a straight line is y = mx + c, where m is the slope and c is the y-intercept.',
        'quadratic equation': 'A quadratic equation has the form ax² + bx + c = 0. The solutions are given by the quadratic formula: x = (-b ± √(b² - 4ac)) / 2a.',
        'quadratic formula': 'The quadratic formula is x = (-b ± √(b² - 4ac)) / 2a, used to solve quadratic equations ax² + bx + c = 0.',
        'pythagorean theorem': 'The Pythagorean theorem states that in a right triangle, a² + b² = c², where c is the hypotenuse.',
        'pythagoras theorem': 'The Pythagorean theorem states that in a right triangle, a² + b² = c², where c is the hypotenuse.',
        'area of circle': 'The area of a circle is π × r², where r is the radius.',
        'circle area': 'The area of a circle is π × r², where r is the radius.',
        'area of triangle': 'The area of a triangle is ½ × base × height.',
        'triangle area': 'The area of a triangle is ½ × base × height.',
        'area of rectangle': 'The area of a rectangle is length × width.',
        'area of square': 'The area of a square is side², where side is the length of one side.',
        'slope of line': 'The slope of a line is the change in y divided by the change in x: m = (y₂ - y₁) / (x₂ - x₁).',
        'derivative': 'The derivative measures the rate of change of a function. For f(x) = xⁿ, the derivative is f\'(x) = nxⁿ⁻¹.',
        'integration': 'Integration is the reverse of differentiation. The integral of xⁿ is (xⁿ⁺¹)/(n+1) + C.',
        'integral': 'Integration is the reverse of differentiation. The integral of xⁿ is (xⁿ⁺¹)/(n+1) + C.',
        'linear equation': 'A linear equation in one variable has the form ax + b = 0, where a ≠ 0.',
        'factorization': 'Factorization is the process of writing a number or expression as a product of its factors.',
        'perimeter of circle': 'The perimeter (circumference) of a circle is 2πr, where r is the radius.',
        'circumference': 'The circumference of a circle is 2πr, where r is the radius.',
        'volume of sphere': 'The volume of a sphere is (4/3)πr³, where r is the radius.',
        'surface area of sphere': 'The surface area of a sphere is 4πr², where r is the radius.'
    },
    'science': {
        'photosynthesis': 'Photosynthesis is the process by which plants make their own food using sunlight, carbon dioxide, and water.',
        'gravity': 'Gravity is the force that pulls objects toward the center of the Earth.',
        'water cycle': 'The water cycle is the continuous movement of water through evaporation, condensation, and precipitation.',
        'atom': 'An atom is the smallest unit of matter that retains the properties of an element.',
        'molecule': 'A molecule is a group of atoms bonded together.',
        'photosynthesis process': 'Photosynthesis occurs in chloroplasts and converts carbon dioxide and water into glucose using sunlight.',
        'newton laws': 'Newton\'s first law states that objects at rest stay at rest unless acted upon by a force.',
        'density': 'Density is mass divided by volume, usually measured in g/cm³ or kg/m³.'
    }
}

def get_answer(question, subject='science', user_language='en'):
    """Get answer for a question with improved context filtering and fallback knowledge"""
    if not qa_pipeline:
        return "Sorry, the AI model is not available at the moment.", "", {}
    
    import traceback
    try:
        # Auto-detect language if not specified
        if user_language == 'auto':
            user_language = detect_language(question)

        # Translate question to English for better processing
        translated_question = (
            translate_to_en(question, user_language) if user_language != 'en' else question
        ).lower()

        # Check if we have direct knowledge for this subject and question
        subject_key = subject.lower()
        if subject_key in SUBJECT_KNOWLEDGE:
            for key, answer in SUBJECT_KNOWLEDGE[subject_key].items():
                if key in translated_question:
                    # Translate answer if needed
                    final_answer = translate_from_en(answer, user_language) if user_language != 'en' else answer
                    metadata = {
                        'confidence': 0.9,
                        'source_language': 'en',
                        'target_language': user_language,
                        'translation_quality': 0.9,
                        'keywords_found': [key],
                        'context_chunks_analyzed': 1,
                        'total_chunks_available': 1,
                        'source': 'built_in_knowledge'
                    }
                    return final_answer, f"Built-in knowledge: {answer}", metadata

        # Get context for the subject
        text_chunks = subject_contexts.get(subject.lower(), [])
        if not text_chunks:
            return "Sorry, no study material available for this subject.", "", {}

        # Extract keywords for better context filtering
        keywords = [kw[0] for kw in kw_model.extract_keywords(translated_question, top_n=5)]

        # Filter chunks based on keywords
        filtered_chunks = [chunk for chunk in text_chunks if any(k.lower() in chunk.lower() for k in keywords)]

        # If no relevant chunks found, use all chunks
        if not filtered_chunks:
            filtered_chunks = text_chunks

        # Find best context
        best_context = find_best_context(translated_question, filtered_chunks)

        # Get answer from QA pipeline
        result = qa_pipeline(question=translated_question, context=best_context)
        answer = result['answer']
        confidence = result.get('score', 0)

        # Translate answer if needed
        final_answer = translate_from_en(answer, user_language) if user_language != 'en' else answer

        # Prepare metadata
        metadata = {
            'confidence': confidence,
            'source_language': 'en',
            'target_language': user_language,
            'translation_quality': 0.8,  # Default quality score
            'keywords_found': keywords,
            'context_chunks_analyzed': len(filtered_chunks),
            'total_chunks_available': len(text_chunks)
        }

        # If confidence is too low, provide a more general response
        if confidence < 0.3:
            if user_language == 'en':
                answer_prefix = "Based on the available information, "
            elif user_language == 'hi':
                answer_prefix = "उपलब्ध जानकारी के आधार पर, "
            elif user_language == 'ta':
                answer_prefix = "கிடைக்கக்கூடிய தகவல்களின் அடிப்படையில், "
            elif user_language == 'te':
                answer_prefix = "అందుబాటులో ఉన్న సమాచారం ఆధారంగా, "
            elif user_language == 'bn':
                answer_prefix = "উপলব্ধ তথ্যের ভিত্তিতে, "
            else:
                answer_prefix = "Based on the available information, "

            final_answer = f"{answer_prefix}{final_answer}. However, you may want to verify this with your teacher or textbook."

        return final_answer, best_context, metadata

    except Exception as e:
        logging.error(f"Error in get_answer: {e}\n{traceback.format_exc()}")
        return "Sorry, I encountered an error while processing your question. Please try again.", "", {}


def generate_mcq(correct_answer, subject='general', difficulty='moderate'):
    """Generate multiple choice questions with distractors"""
    try:
        # Subject-specific distractors
        subject_distractors = {
            'math': [
                "A mathematical operation",
                "A geometric concept", 
                "An algebraic expression",
                "A numerical value"
            ],
            'science': [
                "A scientific process",
                "A natural phenomenon",
                "A chemical reaction",
                "A physical property"
            ],
            'social': [
                "A historical event",
                "A geographical feature",
                "A cultural practice",
                "A social institution"
            ],
            'english': [
                "A literary device",
                "A grammatical rule",
                "A writing technique",
                "A language feature"
            ],
            'general': [
                "An incorrect option 1",
                "An incorrect option 2",
                "An incorrect option 3",
                "An incorrect option 4"
            ]
        }
        
        # Get distractors for the subject
        distractors = subject_distractors.get(subject.lower(), subject_distractors['general'])

        # Always include correct answer
        options = distractors[:3]  # take first 3
        options.append(correct_answer)
        random.shuffle(options)
        
        return options
        
    except Exception as e:
        logging.error(f"Error generating MCQ: {e}")
        return [correct_answer, "Option 2", "Option 3", "Option 4"]


def generate_quiz_questions(subject, class_level, difficulty, count=5):
    """Generate quiz questions for a specific subject and class"""
    try:
        questions = []
        
        # Generate sample questions based on subject
        sample_questions = {
            'math': [
                "What is the formula for the area of a circle?",
                "What is the value of π (pi)?",
                "What is the square root of 16?",
                "What is 2 + 2 × 3?",
                "What is the perimeter of a square with side length 5?"
            ],
            'science': [
                "What is the chemical symbol for water?",
                "What is the largest planet in our solar system?",
                "What is the process by which plants make food?",
                "What is the hardest natural substance on Earth?",
                "What is the main component of air?"
            ]
        }
        
        subject_questions = sample_questions.get(subject.lower(), sample_questions['math'])
        
        for i in range(min(count, len(subject_questions))):
            question = subject_questions[i]
            answer = f"Answer {i+1}"  # Placeholder for correct answer
            
            questions.append({
                'question': question,
                'options': generate_mcq(answer, subject, difficulty),
                'correct_answer': answer,
                'explanation': f"This is the explanation for question {i+1}"
            })
        
        return questions
        
    except Exception as e:
        logging.error(f"Error generating quiz questions: {e}")
        return []


def get_study_tips(subject, language='en'):
    """Get study tips for a specific subject in the specified language"""
    tips = {
        'math': [
            "Practice regularly with different types of problems",
            "Understand the concepts before memorizing formulas",
            "Draw diagrams to visualize problems",
            "Check your work step by step"
        ],
        'science': [
            "Perform experiments to understand concepts",
            "Create mind maps for complex topics",
            "Relate concepts to real-world examples",
            "Review diagrams and charts regularly"
        ],
        'social': [
            "Create timelines for historical events",
            "Use maps to understand geography",
            "Connect current events to historical context",
            "Practice writing summaries of topics"
        ],
        'history': [
            "Create timelines for historical events",
            "Use maps to understand geography", 
            "Connect current events to historical context",
            "Practice writing summaries of topics"
        ],
        'english': [
            "Read regularly to improve vocabulary",
            "Practice writing essays and summaries",
            "Analyze literary works for themes and techniques",
            "Improve grammar through practice exercises"
        ],
        'geography': [
            "Use atlases and maps for visual learning",
            "Relate geographical concepts to current events",
            "Practice drawing maps and diagrams",
            "Study climate and weather patterns"
        ]
    }
    
    subject_tips = tips.get(subject.lower(), tips.get('math', []))
    
    # If language is not English, translate the tips
    if language != 'en':
        try:
            from app.translator import translate_from_en
            translated_tips = []
            for tip in subject_tips:
                translated_tip = translate_from_en(tip, language)
                translated_tips.append(translated_tip)
            return translated_tips
        except Exception as e:
            logging.error(f"Error translating study tips: {e}")
            return subject_tips
    
    return subject_tips

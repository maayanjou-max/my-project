"""
אפליקציית ווב לסוכן מידע תרופות
Drug Information Agent Web Application
"""

from flask import Flask, request, render_template, jsonify
import os
import sys
from enhanced_scraper import search_drug_information as search_drug_info
from conversational_agent import ask_drug_question
import logging

# הוספת נתיב לקבצים
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """עמוד הבית - ממשק חיפוש רגיל"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """ממשק שיחה חכם"""
    return render_template('chat.html')

@app.route('/search', methods=['POST'])
def search_drug():
    """חיפוש מידע על תרופה"""
    try:
        # קבלת שם התרופה מהבקשה
        data = request.get_json()
        drug_name = data.get('drug_name', '').strip()
        
        if not drug_name:
            return jsonify({
                'success': False,
                'message': 'יש להזין שם תרופה לחיפוש',
                'message_en': 'Please enter a drug name to search'
            }), 400
        
        logger.info(f"Searching for drug: {drug_name}")
        
        # חיפוש המידע
        result = search_drug_info(drug_name)
        
        if result.get('found', True):  # אם נמצא מידע
            return jsonify({
                'success': True,
                'data': result
            })
        else:  # אם לא נמצא מידע
            return jsonify({
                'success': False,
                'message': result.get('message'),
                'message_en': result.get('message_en'),
                'searched_names': result.get('searched_names', []),
                'trusted_sources': result.get('trusted_sources', [])
            })
    
    except Exception as e:
        logger.error(f"Error in drug search: {e}")
        return jsonify({
            'success': False,
            'message': 'אירעה שגיאה בחיפוש',
            'message_en': 'An error occurred during search',
            'error': str(e)
        }), 500

@app.route('/api/drug/<drug_name>')
def get_drug_info(drug_name):
    """API לקבלת מידע על תרופה"""
    try:
        result = search_drug_info(drug_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({
            'error': str(e),
            'message': 'שגיאה בחיפוש מידע'
        }), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """שאילת שאלה לסוכן השיחה החכם"""
    try:
        # קבלת השאלה מהבקשה
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'message': 'יש להזין שאלה',
                'message_en': 'Please enter a question'
            }), 400
        
        logger.info(f"Processing question: {question}")
        
        # עיבוד השאלה באמצעות הסוכן החכם
        result = ask_drug_question(question)
        
        if result.get('success', False):
            return jsonify({
                'success': True,
                'data': {
                    'question': result['original_question'],
                    'drug_name': result['drug_name'],
                    'question_types': result['question_types'],
                    'answer': result['answer']
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('message'),
                'suggestion': result.get('suggestion', ''),
                'error': result.get('error', '')
            })
    
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            'success': False,
            'message': 'אירעה שגיאה בעיבוד השאלה',
            'message_en': 'An error occurred while processing the question',
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """בדיקת תקינות השירות"""
    return jsonify({
        'status': 'healthy',
        'service': 'Drug Information Agent',
        'version': '2.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"""
    🏥 סוכן מידע תרופות / Drug Information Agent
    
    📡 השירות רץ על פורט: {port}
    🌐 כתובת: http://0.0.0.0:{port}
    🔍 מקורות מהימנים: MedlinePlus, MicroMedex, UpToDate
    
    לחיפוש תרופה: POST /search
    API: GET /api/drug/<drug_name>
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
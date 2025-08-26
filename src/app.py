"""
אפליקציית ווב לסוכן מידע תרופות
Drug Information Agent Web Application
"""

from flask import Flask, request, render_template, jsonify
import os
import sys
from advanced_scraper import search_drug_info_advanced as search_drug_info
import logging

# הוספת נתיב לקבצים
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """עמוד הבית"""
    return render_template('index.html')

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

@app.route('/health')
def health_check():
    """בדיקת תקינות השירות"""
    return jsonify({
        'status': 'healthy',
        'service': 'Drug Information Agent',
        'version': '1.0.0'
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
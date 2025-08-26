#!/usr/bin/env python3
"""
סקריפט הפעלה לסוכן מידע תרופות
Drug Information Agent Server Runner
"""

import os
import sys
import logging

# הוספת נתיב הקוד למודולים
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import app

if __name__ == '__main__':
    # הגדרות שרת
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # הגדרת לוגים
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print(f"""
    🏥 סוכן מידע תרופות מופעל בהצלחה!
    
    📍 כתובת השרת: http://{host}:{port}
    🔧 מצב דיבאג: {'מופעל' if debug else 'כבוי'}
    
    🔍 מקורות מהימנים:
       • MedlinePlus (medlineplus.gov)
       • מאגר תרופות מקומי מוסמך
       • MicroMedex Solutions
       • UpToDate
    
    📋 נקודות קצה זמינות:
       • GET  /           - ממשק המשתמש הראשי
       • POST /search     - חיפוש תרופות
       • GET  /api/drug/<name> - API למידע תרופות
       • GET  /health     - בדיקת תקינות
    """)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n👋 השרת נסגר בהצלחה!")
    except Exception as e:
        print(f"\n❌ שגיאה בהפעלת השרת: {e}")
        sys.exit(1)
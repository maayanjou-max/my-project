"""
סוכן שיחה חכם לתרופות - מבין שאלות ומשיב תשובות מדויקות
Conversational AI Agent for Drug Information
"""

import re
from typing import Dict, List, Optional, Tuple
from expanded_drug_database import ExpandedDrugDatabase
import logging

logger = logging.getLogger(__name__)

class DrugConversationalAgent:
    """סוכן שיחה חכם לתרופות"""
    
    def __init__(self):
        self.db = ExpandedDrugDatabase()
        self.question_patterns = self._build_question_patterns()
    
    def _build_question_patterns(self) -> Dict:
        """בניית תבניות זיהוי שאלות"""
        return {
            'pregnancy': {
                'patterns': [
                    r'(.*)(בהריון|הרי[הו]נ|הר[יה]ון|pregnant|pregnancy)(.*)',
                    r'(.*)(יכול[הת]? להיות|מותר|בטוח|safe).*(בהריון|הרי[הו]נ)',
                    r'(.*)(לקחת|לשתות).*(בהריון|pregnant)(.*)',
                ],
                'keywords': ['הריון', 'הרויון', 'הריונה', 'pregnant', 'pregnancy']
            },
            
            'breastfeeding': {
                'patterns': [
                    r'(.*)(הנק[הת]|מניק[הת]|breastfeeding|nursing)(.*)',
                    r'(.*)(מותר|בטוח|יכול[הת]).*(הנק[הת]|מניק[הת])',
                    r'(.*)(לתינוק|לבב[יא]|baby)(.*)',
                ],
                'keywords': ['הנקה', 'מניקה', 'breastfeeding', 'nursing', 'תינוק', 'בביא']
            },
            
            'timing': {
                'patterns': [
                    r'(.*)(מתי|when|איך|how).*(לקחת|לשתות|take)(.*)',
                    r'(.*)(לפני|אחרי|עם).*(אוכל|אכילה|food|meal)(.*)',
                    r'(.*)(על קיבה ריק[הת]|empty stomach)(.*)',
                    r'(.*)(זמן|time|timing)(.*)',
                ],
                'keywords': ['מתי', 'when', 'לפני', 'אחרי', 'עם', 'אוכל', 'קיבה']
            },
            
            'dosage': {
                'patterns': [
                    r'(.*)(כמה|how much|מינון|dose|dosage)(.*)',
                    r'(.*)(כמות|quantity|amount)(.*)',
                    r'(.*)(פעמים ביום|times per day|daily)(.*)',
                ],
                'keywords': ['מינון', 'כמה', 'כמות', 'dose', 'dosage', 'amount']
            },
            
            'side_effects': {
                'patterns': [
                    r'(.*)(תופע[ות]+|side effects|effects)(.*)',
                    r'(.*)(מה קורה|what happens|בעיות|problems)(.*)',
                    r'(.*)(מסוכן|dangerous|harmful|רע)(.*)',
                ],
                'keywords': ['תופעות', 'side effects', 'בעיות', 'מסוכן', 'רע']
            },
            
            'interactions': {
                'patterns': [
                    r'(.*)(עם|with).*(תרופ[הות]|medication|drug)(.*)',
                    r'(.*)(אלכוהול|alcohol|שתיי[הת])(.*)',
                    r'(.*)(אינטראקצי[הות]|interaction)(.*)',
                ],
                'keywords': ['אינטראקציות', 'עם תרופות', 'אלכוהול', 'interactions']
            },
            
            'general_info': {
                'patterns': [
                    r'(.*)(מה זה|what is|מידע|information)(.*)',
                    r'(.*)(איך עובד|how does it work|פעולה)(.*)',
                    r'(.*)(למה|why|מדוע|for what)(.*)',
                ],
                'keywords': ['מה זה', 'מידע', 'איך עובד', 'למה']
            }
        }
    
    def extract_drug_name(self, question: str) -> Optional[str]:
        """חילוץ שם התרופה מהשאלה"""
        # תחילה נחפש בתרופות הידועות במאגר
        all_drug_names = self.db.get_all_drug_names()
        
        # חיפוש השם הארוך ביותר שנמצא בשאלה מהמאגר
        found_drugs = []
        for drug_name in all_drug_names:
            if drug_name.lower() in question.lower():
                found_drugs.append(drug_name)
        
        if found_drugs:
            # החזר את השם הארוך ביותר (יותר ספציפי)
            return max(found_drugs, key=len)
        
        # אם לא נמצא במאגר, נסה לחלץ שם תרופה כללי מהשאלה
        import re
        
        # תבניות לזיהוי שמות תרופות
        drug_patterns = [
            r'(?:של|עם|את|על|האם|מותר|בטוח|לקחת|לשתות)\s+([א-ת\w]+)',
            r'([א-ת\w]+)\s+(?:בטוח|מותר|אסור)',
            r'תרופה\s+([א-ת\w]+)',
            r'([A-Za-z]+[a-z]{3,})',  # מילים באנגלית באורך סביר
            r'([א-ת]{4,})',  # מילים בעברית באורך סביר
        ]
        
        potential_drugs = set()
        for pattern in drug_patterns:
            matches = re.findall(pattern, question)
            for match in matches:
                if match and len(match) >= 3:  # לפחות 3 תווים
                    # סנן מילים נפוצות שאינן שמות תרופות
                    excluded_words = {
                        'הריון', 'הרויון', 'הנקה', 'מניקה', 'אוכל', 'תרופה', 'תרופות', 
                        'מותר', 'בטוח', 'אסור', 'לקחת', 'לשתות', 'מתי', 'איך', 'כמה',
                        'pregnant', 'pregnancy', 'breastfeeding', 'safe', 'allowed', 'take',
                        'when', 'how', 'much', 'with', 'without', 'food', 'meal'
                    }
                    
                    if match.lower() not in excluded_words:
                        potential_drugs.add(match)
        
        if potential_drugs:
            # החזר את השם הארוך ביותר
            return max(potential_drugs, key=len)
        
        return None
    
    def classify_question(self, question: str) -> List[str]:
        """זיהוי סוג השאלה"""
        question_types = []
        
        for q_type, patterns_info in self.question_patterns.items():
            # בדיקת תבניות
            for pattern in patterns_info['patterns']:
                if re.search(pattern, question, re.IGNORECASE):
                    question_types.append(q_type)
                    break
            
            # בדיקת מילות מפתח
            for keyword in patterns_info['keywords']:
                if keyword.lower() in question.lower():
                    if q_type not in question_types:
                        question_types.append(q_type)
        
        return question_types if question_types else ['general_info']
    
    def generate_answer(self, drug_name: str, question_types: List[str], original_question: str) -> str:
        """יצירת תשובה מקיפה"""
        drug_info = self.db.get_drug_info(drug_name)
        
        if not drug_info:
            return f"לא נמצא מידע אמין על התרופה '{drug_name}' במקורות הרפואיים המהימנים שלנו."
        
        answer_parts = []
        
        # כותרת
        answer_parts.append(f"**💊 {drug_info['generic_name']} ({drug_info['english_name']})**\n")
        
        # תשובה לפי סוגי השאלה
        for q_type in question_types:
            if q_type == 'pregnancy':
                pregnancy_info = drug_info['pregnancy']
                if pregnancy_info['safe']:
                    answer_parts.append(f"🤱 **בהריון**: ✅ בטוח - {pregnancy_info['details']}")
                else:
                    answer_parts.append(f"🤱 **בהריון**: ⚠️ להימנע - {pregnancy_info['details']}")
            
            elif q_type == 'breastfeeding':
                bf_info = drug_info['breastfeeding']
                if bf_info['safe']:
                    answer_parts.append(f"🍼 **בהנקה**: ✅ בטוח - {bf_info['details']}")
                else:
                    answer_parts.append(f"🍼 **בהנקה**: ⚠️ להימנע - {bf_info['details']}")
            
            elif q_type == 'timing':
                timing_info = drug_info['timing']
                answer_parts.append(f"🕐 **זמן נטילה**: {timing_info['with_food']}")
                answer_parts.append(f"⏰ **המלצה**: {timing_info['best_time']}")
            
            elif q_type == 'dosage':
                dosage_info = drug_info['dosage']
                answer_parts.append(f"💊 **מינון למבוגרים**: {dosage_info['adults']}")
                if 'children' in dosage_info:
                    answer_parts.append(f"👶 **מינון לילדים**: {dosage_info['children']}")
            
            elif q_type == 'side_effects':
                se_info = drug_info['side_effects']
                answer_parts.append(f"⚠️ **תופעות לוואי נפוצות**: {', '.join(se_info['common'])}")
                answer_parts.append(f"🚨 **תופעות חמורות**: {', '.join(se_info['serious'])}")
                answer_parts.append(f"⛔ **אזהרה**: {se_info['overdose_warning']}")
            
            elif q_type == 'interactions':
                int_info = drug_info['interactions']
                answer_parts.append(f"🍷 **אלכוהול**: {int_info['alcohol']}")
                answer_parts.append(f"💊 **תרופות אחרות**: {'; '.join(int_info['medications'])}")
            
            elif q_type == 'general_info':
                answer_parts.append(f"📋 **תיאור**: {drug_info['description']}")
                answer_parts.append(f"🎯 **שימושים**: {', '.join(drug_info['indications'])}")
        
        # הוספת מידע כללי חשוב
        if len(question_types) == 1 and question_types[0] != 'general_info':
            contraindications = drug_info.get('contraindications', [])
            if contraindications:
                answer_parts.append(f"\n❌ **התוויות נגד**: {', '.join(contraindications[:3])}")
        
        # מקורות
        sources = drug_info.get('sources', [])
        answer_parts.append(f"\n📚 **מקורות מהימנים**: {', '.join(sources)}")
        
        # אזהרה כללית
        answer_parts.append(f"\n⚕️ **חשוב**: המידע הוא למטרות הסברה בלבד ואינו תחליף לייעוץ רפואי מקצועי.")
        
        return "\n\n".join(answer_parts)
    
    def create_fallback_response(self, drug_name: str, question_types: List[str]) -> str:
        """יצירת תשובת fallback לתרופה לא ידועה"""
        response_parts = []
        
        response_parts.append(f"**💊 {drug_name}**")
        response_parts.append(f"📋 **מצטער, אין לי מידע מפורט על התרופה '{drug_name}' במאגר הנתונים שלי.**")
        
        # המלצות לפי סוג השאלה
        if 'pregnancy' in question_types:
            response_parts.append("🤱 **לגבי הריון**: חשוב מאוד להתייעץ עם רופא או רוקח לפני נטילת כל תרופה בהריון.")
        
        if 'breastfeeding' in question_types:
            response_parts.append("🍼 **לגבי הנקה**: יש להתייעץ עם רופא או רוקח על התאמת התרופה להנקה.")
        
        if 'timing' in question_types:
            response_parts.append("⏰ **לגבי זמן נטילה**: עיין בעלון המצורף לתרופה או התייעץ עם רוקח.")
        
        if 'dosage' in question_types:
            response_parts.append("💊 **לגבי מינון**: חשוב לפעול לפי הוראות הרופא והעלון המצורף.")
        
        if 'side_effects' in question_types:
            response_parts.append("⚠️ **לגבי תופעות לוואי**: קרא בעלון המצורף ויש לדווח לרופא על תופעות לוואי.")
        
        # מידע על התרופות הנתמכות
        supported_count = self.db.get_supported_drugs_count()
        response_parts.append(f"\n📚 **במאגר שלי יש מידע מפורט על {supported_count} תרופות נפוצות כמו:**")
        response_parts.append("פרצטמול, נורופן, אספירין, מטפורמין, דוקסיציקלין, אמוקסיצילין, דרלין, טרמדול, גבפנטין ועוד...")
        
        # המלצות כלליות
        response_parts.append("\n🎯 **המלצות:**")
        response_parts.append("• התייעץ עם רופא או רוקח מקצועי")
        response_parts.append("• קרא את עלון התרופה בקפידה")
        response_parts.append("• בדוק באתרים רפואיים מהימנים כמו MedlinePlus")
        
        response_parts.append("\n⚕️ **חשוב**: המידע שלי מוגבל לתרופות הנפוצות במאגר. לכל תרופה אחרת חשוב להתייעץ עם איש מקצוע רפואי.")
        
        return "\n\n".join(response_parts)

    def answer_question(self, question: str) -> Dict:
        """מענה על שאלה - הפונקציה העיקרית"""
        try:
            # חילוץ שם התרופה
            drug_name = self.extract_drug_name(question)
            
            if not drug_name:
                supported_count = self.db.get_supported_drugs_count()
                return {
                    'success': False,
                    'message': f'לא זיהיתי שם תרופה בשאלה. במאגר שלי יש מידע על {supported_count} תרופות נפוצות.',
                    'suggestion': 'דוגמאות לשאלות: "האם פרצטמול בטוח בהריון?", "מתי לוקחים דוקסילין?", "תופעות לוואי של דרלין?"',
                    'supported_drugs': ['פרצטמול', 'נורופן', 'אספירין', 'מטפורמין', 'דוקסילין', 'דרלין', 'טרמדול', 'גבפנטין', 'אמוקסיצילין', 'ביסופרולול']
                }
            
            # זיהוי סוג השאלה
            question_types = self.classify_question(question)
            
            # בדיקה אם התרופה במאגר
            drug_info = self.db.get_drug_info(drug_name)
            
            if drug_info:
                # יצירת תשובה מלאה
                answer = self.generate_answer(drug_name, question_types, question)
                return {
                    'success': True,
                    'drug_name': drug_name,
                    'question_types': question_types,
                    'answer': answer,
                    'original_question': question,
                    'found_in_database': True
                }
            else:
                # יצירת תשובת fallback
                fallback_answer = self.create_fallback_response(drug_name, question_types)
                return {
                    'success': True,
                    'drug_name': drug_name,
                    'question_types': question_types,
                    'answer': fallback_answer,
                    'original_question': question,
                    'found_in_database': False,
                    'fallback': True
                }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                'success': False,
                'message': 'אירעה שגיאה בעיבוד השאלה. אנא נסה שוב.',
                'error': str(e)
            }

# פונקציה עיקרית לשימוש
def ask_drug_question(question: str) -> Dict:
    """פונקציה עיקרית לשאילת שאלות על תרופות"""
    agent = DrugConversationalAgent()
    return agent.answer_question(question)
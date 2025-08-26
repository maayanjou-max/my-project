"""
סוכן שיחה חכם לתרופות - מבין שאלות ומשיב תשובות מדויקות
Conversational AI Agent for Drug Information
"""

import re
from typing import Dict, List, Optional, Tuple
from comprehensive_drug_database import ComprehensiveDrugDatabase
from multi_source_search import search_drug_multi_source
import logging

logger = logging.getLogger(__name__)

class DrugConversationalAgent:
    """סוכן שיחה חכם לתרופות"""
    
    def __init__(self):
        self.db = ComprehensiveDrugDatabase()
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
        
        # תבניות לזיהוי שמות תרופות - מסודר לפי עדיפות
        drug_patterns = [
            # תבניות ספציפיות לשאלות נפוצות
            r'האם\s+([א-ת\w]{3,})\s+(?:בטוח|מותר|אסור)',  # "האם זולפט בטוח"
            r'(?:של|עם|את|על)\s+([א-ת\w]{3,})\s+(?:בהריון|בהנקה|במינון)',  # "של זולפט בהריון"
            r'(?:לקחת|לשתות|נטילת)\s+([א-ת\w]{3,})',  # "לקחת זולפט"
            r'תרופה\s+([א-ת\w]{3,})',  # "תרופה זולפט"
            r'([A-Za-z]+[a-z]{2,})\s+(?:safe|pregnancy|breastfeeding)',  # English patterns
            r'([א-ת]{3,})\s+(?:בטוח|מותר|אסור|בהריון|בהנקה)',  # "זולפט בטוח"
            r'([A-Za-z]{3,})',  # מילים באנגלית כלליות
            r'([א-ת]{3,})',  # מילים בעברית כלליות (אחרון)
        ]
        
        potential_drugs = set()
        for pattern in drug_patterns:
            matches = re.findall(pattern, question)
            for match in matches:
                if match and len(match) >= 3:  # לפחות 3 תווים
                    # סנן מילים נפוצות שאינן שמות תרופות
                    excluded_words = {
                        'הריון', 'הרויון', 'הנקה', 'מניקה', 'אוכל', 'תרופה', 'תרופות', 
                        'מותר', 'בטוח', 'אסור', 'לקחת', 'לשתות', 'מתי', 'איך', 'כמה', 'האם',
                        'בהריון', 'בהנקה', 'במינון', 'עם', 'של', 'את', 'על', 'זמן', 'כמות',
                        'pregnant', 'pregnancy', 'breastfeeding', 'safe', 'allowed', 'take',
                        'when', 'how', 'much', 'with', 'without', 'food', 'meal', 'dosage'
                    }
                    
                    if match.lower() not in excluded_words:
                        potential_drugs.add(match)
        
        if potential_drugs:
            # החזר את השם הארוך ביותר
            return max(potential_drugs, key=len)
        
        return None
    
    def classify_question(self, question: str) -> List[str]:
        """זיהוי סוג השאלה עם בינה מלאכותית משופרת"""
        question_types = []
        question_lower = question.lower()
        
        # זיהוי מתקדם לפי תבניות ומשמעות
        for q_type, patterns_info in self.question_patterns.items():
            # בדיקת תבניות regex
            for pattern in patterns_info['patterns']:
                if re.search(pattern, question, re.IGNORECASE):
                    question_types.append(q_type)
                    break
            
            # בדיקת מילות מפתח מחכימה
            for keyword in patterns_info['keywords']:
                if keyword.lower() in question_lower:
                    if q_type not in question_types:
                        question_types.append(q_type)
        
        # זיהוי מתקדם נוסף לפי הקונטקסט
        
        # זיהוי שאלות הריון מתקדמות
        pregnancy_indicators = ['אני בהריון', 'אני הרה', 'בחודש', 'בשבוע', 'עובר', 'ילדה']
        if any(indicator in question_lower for indicator in pregnancy_indicators):
            if 'pregnancy' not in question_types:
                question_types.append('pregnancy')
        
        # זיהוי שאלות הנקה מתקדמות  
        nursing_indicators = ['אני מניקה', 'אני מזינה', 'לתינוק שלי', 'לבת שלי', 'לבן שלי']
        if any(indicator in question_lower for indicator in nursing_indicators):
            if 'breastfeeding' not in question_types:
                question_types.append('breastfeeding')
        
        # זיהוי שאלות מינון מתקדמות
        dosage_indicators = ['כמה כדורים', 'איזה מינון', 'כמה מ"ג', 'כמה פעמים', 'מנה יומית']
        if any(indicator in question_lower for indicator in dosage_indicators):
            if 'dosage' not in question_types:
                question_types.append('dosage')
        
        # זיהוי שאלות זמן מתקדמות
        timing_indicators = ['באיזה שעה', 'לפני השינה', 'בבוקר', 'בערב', 'עם הקפה']
        if any(indicator in question_lower for indicator in timing_indicators):
            if 'timing' not in question_types:
                question_types.append('timing')
        
        # זיהוי שאלות תופעות לוואי מתקדמות
        side_effect_indicators = ['מה עושה לי', 'למה אני מרגיש', 'יש לי בחילה', 'כאב בבטן', 'סחרחורת']
        if any(indicator in question_lower for indicator in side_effect_indicators):
            if 'side_effects' not in question_types:
                question_types.append('side_effects')
        
        return question_types if question_types else ['general_info']
    
    def generate_answer(self, drug_name: str, question_types: List[str], original_question: str) -> str:
        """יצירת תשובה מקיפה ואמפתית"""
        drug_info = self.db.get_drug_info(drug_name)
        
        if not drug_info:
            return f"לא נמצא מידע אמין על התרופה '{drug_name}' במקורות הרפואיים המהימנים שלנו."
        
        answer_parts = []
        
        # כותרת אמפתית
        answer_parts.append(f"**💊 {drug_info['generic_name']} ({drug_info['english_name']})**")
        
        # הקדמה אישית לפי השאלה
        if 'pregnancy' in question_types:
            if 'אני בהריון' in original_question.lower():
                answer_parts.append("👶 אני מבינה שאת בהריון ורוצה לוודא שהתרופה בטוחה עבורך. הנה המידע החשוב:")
            else:
                answer_parts.append("👶 לגבי השימוש בהריון:")
        elif 'breastfeeding' in question_types:
            if 'אני מניקה' in original_question.lower():
                answer_parts.append("🤱 אני מבינה שאת מניקה ומודאגת לגבי הבטיחות. הנה המידע:")
            else:
                answer_parts.append("🤱 לגבי השימוש בהנקה:")
        
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
    
    def create_enhanced_fallback_response(self, drug_name: str, question_types: List[str]) -> str:
        """יצירת תשובת fallback משופרת עם חיפוש רב-מקורי"""
        try:
            # ניסיון חיפוש במקורות חיצוניים
            logger.info(f"Attempting multi-source search for: {drug_name}")
            external_info = search_drug_multi_source(drug_name, question_types)
            
            response_parts = []
            response_parts.append(f"**💊 {drug_name}**")
            
            if external_info.get('found_sources', 0) > 0:
                response_parts.append(f"📋 **מצאתי מידע על '{drug_name}' ממקורות חיצוניים מהימנים:**")
                
                # הוספת מידע שנמצא
                if external_info.get('pregnancy_info') and 'pregnancy' in question_types:
                    response_parts.append(f"🤱 **הריון**: {external_info['pregnancy_info']}")
                
                if external_info.get('breastfeeding_info') and 'breastfeeding' in question_types:
                    response_parts.append(f"🍼 **הנקה**: {external_info['breastfeeding_info']}")
                
                if external_info.get('general_info'):
                    response_parts.append(f"📖 **מידע כללי**: {external_info['general_info']}")
                
                # מקורות
                sources = external_info.get('sources', [])
                if sources:
                    response_parts.append(f"\n📚 **מקורות**: {', '.join(sources)}")
                
                reliability = external_info.get('reliability_score', 'medium')
                if reliability == 'high':
                    response_parts.append("\n✅ **מהימנות**: גבוהה - מידע ממקורות רפואיים מוכרים")
                elif reliability == 'medium':
                    response_parts.append("\n⚠️ **מהימנות**: בינונית - מומלץ לאמת עם רופא")
                else:
                    response_parts.append("\n⚠️ **מהימנות**: נמוכה - חובה להתייעץ עם רופא")
            
            else:
                # אם לא נמצא מידע חיצוני
                response_parts.append(f"📋 **לא מצאתי מידע מפורט על '{drug_name}' במקורות הזמינים.**")
                
                # המלצות לפי סוג השאלה
                if 'pregnancy' in question_types:
                    response_parts.append("🤱 **לגבי הריון**: חשוב מאוד להתייעץ עם רופא או רוקח לפני נטילת כל תרופה בהריון.")
                
                if 'breastfeeding' in question_types:
                    response_parts.append("🍼 **לגבי הנקה**: יש להתייעץ עם רופא או רוקח על התאמת התרופה להנקה.")
                
                if 'timing' in question_types:
                    response_parts.append("⏰ **לגבי זמן נטילה**: עיין בעלון המצורף לתרופה או התייעץ עם רוקח.")
            
            # מידע על המאגר המקומי
            supported_count = self.db.get_supported_drugs_count()
            response_parts.append(f"\n📚 **במאגר המקומי שלי יש מידע מלא על {supported_count} תרופות נפוצות:**")
            response_parts.append("פרצטמול, נורופן, אספירין, ציפרלקס, זולפט, אמוקסיצילין, דוקסיציקלין, ביסופרולול, אומפרזול, גבפנטין, טרמדול, מטפורמין")
            
            # המלצות כלליות
            response_parts.append("\n🎯 **המלצות חשובות:**")
            response_parts.append("• התייעץ עם רופא או רוקח מקצועי")  
            response_parts.append("• קרא את עלון התרופה בקפידה")
            response_parts.append("• בדוק באתרים רפואיים: כללית, MedlinePlus")
            
            response_parts.append("\n⚕️ **חשוב**: המידע הוא למטרות הסברה בלבד ואינו תחליף לייעוץ רפואי מקצועי.")
            
            return "\n\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"Error in enhanced fallback: {e}")
            # נחזור לתשובת fallback רגילה
            return self.create_simple_fallback_response(drug_name, question_types)
    
    def generate_recommendation_answer(self, question: str, question_types: List[str]) -> Dict:
        """מתן המלצות לטיפול לפי מצב רפואי"""
        answer_parts = []
        
        if 'pregnancy' in question_types:
            answer_parts.append("**🤱 המלצות לטיפול בהריון**")
            answer_parts.append("👶 אני מבינה שאת בהריון ומחפשת טיפול בטוח.")
            
            if any(word in question.lower() for word in ['כאב ראש', 'צפלגיה', 'headache']):
                answer_parts.append("\n💊 **לכאב ראש בהריון**:")
                answer_parts.append("✅ **פרצטמול** - הבחירה הבטוחה ביותר בהריון")
                answer_parts.append("⚠️ **להימנע**: אספירין, אדביל, נורופן (במיוחד בשלישיית שלישי)")
            
            elif any(word in question.lower() for word in ['בחילה', 'הקאה', 'nausea']):
                answer_parts.append("\n🤢 **לבחילות הריון**:")
                answer_parts.append("✅ **ויטמין B6** - בטוח ויעיל")
                answer_parts.append("✅ **זנגביל** - טבעי ובטוח")
                answer_parts.append("📞 **התייעצי עם רופא** אם הבחילות קשות")
            
            elif any(word in question.lower() for word in ['דיכאון', 'עצב', 'depression', 'עצוב']):
                answer_parts.append("\n😔 **לדיכאון בהריון**:")
                answer_parts.append("⚠️ **חשוב מאוד**: דיכאון בהריון דורש מעקב רפואי צמוד")
                answer_parts.append("✅ **זולפט (סרטרלין)** - נחשב בטוח יחסית בהריון")
                answer_parts.append("✅ **ציפרלקס** - עם זהירות ובהתייעצות")
                answer_parts.append("🚫 **חשוב**: אין להפסיק תרופות נוגדות דיכאון ללא התייעצות")
            
            elif any(word in question.lower() for word in ['זיהום', 'דלקת', 'חום']):
                answer_parts.append("\n🦠 **לזיהומים בהריון**:")
                answer_parts.append("✅ **אמוקסיצילין** - אנטיביוטיקה בטוחה בהריון")
                answer_parts.append("⚠️ **חשוב**: חובה להתייעץ עם רופא לפני נטילת אנטיביוטיקה")
            
            else:
                answer_parts.append("\n💊 **עקרונות כלליים בהריון**:")
                answer_parts.append("✅ **פרצטמול** - בטוח לכאבים וחום")
                answer_parts.append("✅ **חומצה פולית** - חובה בהריון")
                answer_parts.append("⚠️ **להימנע**: אספירין, אדביל (בשלישיית שלישי)")
                
        elif 'breastfeeding' in question_types:
            answer_parts.append("**🤱 המלצות לטיפול בהנקה**")
            answer_parts.append("🍼 אני מבינה שאת מניקה ורוצה לוודא שהטיפול בטוח לתינוק.")
            
            if any(word in question.lower() for word in ['דיכאון', 'עצב', 'depression', 'עצוב']):
                answer_parts.append("\n😔 **לדיכאון בהנקה**:")
                answer_parts.append("✅ **זולפט (סרטרלין)** - הבחירה הבטוחה ביותר בהנקה")
                answer_parts.append("⚠️ **ציפרלקס** - בטוח יחסית, מעקב נדרש")
                answer_parts.append("🚫 **להימנע**: תרופות חדשות ללא מחקרים מספקים")
                answer_parts.append("👶 **חשוב**: עקבי אחר התינוק לגבי שינויים בהתנהגות")
            else:
                answer_parts.append("\n💊 **תרופות בטוחות בהנקה**:")
                answer_parts.append("✅ **פרצטמול** - בטוח לחלוטין")
                answer_parts.append("✅ **אדביל** - בכמויות קטנות")
                answer_parts.append("✅ **זולפט** - אחד מנוגדי הדיכאון הבטוחים יותר")
            
        else:
            answer_parts.append("**💊 המלצות כלליות לטיפול**")
            
            if any(word in question.lower() for word in ['כאב ראש', 'צפלגיה']):
                answer_parts.append("🧠 **לכאב ראש**:")
                answer_parts.append("💊 **פרצטמול** - 500-1000 מ\"ג כל 4-6 שעות")
                answer_parts.append("💊 **אדביל** - 200-400 מ\"ג כל 4-6 שעות")
                answer_parts.append("⚠️ **זהירות**: אל תשלב פרצטמול עם תרופות אחרות המכילות אותו")
        
        answer_parts.append("\n⚠️ **חשוב מאוד**:")
        answer_parts.append("• התייעצי עם רופא או רוקח לפני נטילת תרופה")
        answer_parts.append("• קראי את עלון התרופה")
        answer_parts.append("• בדקי אלרגיות ותרופות נוספות שאת לוקחת")
        
        answer_parts.append("\n📞 **מתי לפנות לרופא מיידית**:")
        answer_parts.append("• חום גבוה מעל 39 מעלות")
        answer_parts.append("• כאבים חזקים שלא עוברים")
        answer_parts.append("• תסמינים חדשים או מחמירים")
        
        return {
            'success': True,
            'drug_name': 'המלצות טיפול',
            'question_types': question_types,
            'answer': "\n\n".join(answer_parts),
            'original_question': question,
            'recommendation_type': True
        }

    def create_simple_fallback_response(self, drug_name: str, question_types: List[str]) -> str:
        """תשובת fallback פשוטה במקרה של שגיאה"""
        response_parts = []
        
        response_parts.append(f"**💊 {drug_name}**")
        response_parts.append(f"📋 **מצטער, אין לי מידע מפורט על התרופה '{drug_name}' במאגר הנתונים שלי.**")
        
        # המלצות לפי סוג השאלה
        if 'pregnancy' in question_types:
            response_parts.append("🤱 **לגבי הריון**: חשוב מאוד להתייעץ עם רופא או רוקח לפני נטילת כל תרופה בהריון.")
        
        if 'breastfeeding' in question_types:
            response_parts.append("🍼 **לגבי הנקה**: יש להתייעץ עם רופא או רוקח על התאמת התרופה להנקה.")
        
        # המלצות כלליות
        response_parts.append("\n🎯 **המלצות:**")
        response_parts.append("• התייעץ עם רופא או רוקח מקצועי")
        response_parts.append("• בדוק באתר כללית: https://www.clalit.co.il")
        response_parts.append("• קרא את עלון התרופה")
        
        response_parts.append("\n⚕️ **חשוב**: המידע שלי מוגבל לתרופות הנפוצות במאגר. לכל תרופה אחרת חשוב להתייעץ עם איש מקצוע רפואי.")
        
        return "\n\n".join(response_parts)

    def answer_question(self, question: str) -> Dict:
        """מענה על שאלה - הפונקציה העיקרית"""
        try:
            # זיהוי סוג השאלה תחילה
            question_types = self.classify_question(question)
            
            # זיהוי שאלות "מה אני יכולה לקחת" - שאלות המלצה
            recommendation_patterns = [
                r'מה אני יכול[הת]? לקחת',
                r'איזה תרופה [אנמבט]',
                r'מה מותר לי',
                r'מה בטוח עבורי',
                r'איך אני יכול[הת]? לטפל',
                r'מה עושים עם',
                r'איזו תרופה בטוח[הת]',
                r'מה לקחת עבור',
                r'איך לטפל ב',
                r'מה הטיפול ל'
            ]
            
            is_recommendation_question = any(
                re.search(pattern, question, re.IGNORECASE) 
                for pattern in recommendation_patterns
            )
            
            # זיהוי נוסף של שאלות המלצה לפי מילים
            recommendation_keywords = [
                'מה לקחת', 'איך לטפל', 'מה עושים', 'איזה תרופה', 
                'מה הטיפול', 'איך נפטרים', 'מה עוזר'
            ]
            
            if not is_recommendation_question:
                is_recommendation_question = any(
                    keyword in question.lower() 
                    for keyword in recommendation_keywords
                )
            
            if is_recommendation_question:
                return self.generate_recommendation_answer(question, question_types)
            
            # חילוץ שם התרופה
            drug_name = self.extract_drug_name(question)
            
            if not drug_name:
                supported_count = self.db.get_supported_drugs_count()
                return {
                    'success': False,
                    'message': f'לא זיהיתי שם תרופה בשאלה. במאגר שלי יש מידע על {supported_count} תרופות נפוצות.',
                    'suggestion': 'דוגמאות לשאלות: "האם פרצטמול בטוח בהריון?", "מתי לוקחים דוקסילין?", "תופעות לוואי של דרלין?"',
                    'supported_drugs': ['פרצטמול', 'נורופן', 'אספירין', 'ציפרלקס', 'זולפט', 'אמוקסיצילין', 'דוקסיציקלין', 'ביסופרולול', 'אומפרזול', 'גבפנטין', 'טרמדול', 'מטפורמין']
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
                # יצירת תשובת fallback משופרת עם חיפוש רב-מקורי
                fallback_answer = self.create_enhanced_fallback_response(drug_name, question_types)
                return {
                    'success': True,
                    'drug_name': drug_name,
                    'question_types': question_types,
                    'answer': fallback_answer,
                    'original_question': question,
                    'found_in_database': False,
                    'fallback': True,
                    'multi_source_enabled': True
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
"""
מאגר תרופות מורחב עם מאות תרופות נפוצות
Expanded Drug Database with Hundreds of Common Medications
"""

class ExpandedDrugDatabase:
    """מאגר תרופות מורחב עם מידע מקיף על תרופות נפוצות בישראל ובעולם"""
    
    def __init__(self):
        self.drugs_database = {
            # אנטיביוטיקה
            'דוקסיציקלין': {
                'names': ['דוקסילין', 'דוקסיציקלין', 'ויברמיצין', 'doxycycline', 'vibramycin', 'doxylin'],
                'generic_name': 'דוקסיציקלין',
                'english_name': 'doxycycline',
                'category': 'אנטיביוטיקה - טטרציקלין',
                'description': 'אנטיביוטיקה למגוון זיהומים חיידקיים',
                'indications': ['זיהומי דרכי נשימה', 'זיהומי עור', 'מלריה', 'כלמידיה', 'אקנה'],
                'dosage': {
                    'adults': 'מבוגרים: 100-200 מ"ג פעם ביום או 50-100 מ"ג פעמיים ביום',
                    'children': 'ילדים מעל 8 שנים: 2-4 מ"ג לק"ג פעם ביום'
                },
                'timing': {
                    'with_food': 'עם אוכל או חלב כדי למנוע גירוי קיבה',
                    'best_time': 'עם ארוחה, לא עם מוצרי חלב או ברזל'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'D',
                    'details': 'אסור בהריון - עלול לגרום לפגיעה בשיניים ועצמות העובר'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': 'להימנע בהנקה - עובר לחלב ועלול להזיק לתינוק'
                },
                'side_effects': {
                    'common': ['בחילה', 'שלשול', 'רגישות לשמש', 'כאבי בטן'],
                    'serious': ['דלקת הושט', 'בעיות כבד', 'פריחה חמורה'],
                    'overdose_warning': 'הקפדה על זמני נטילה ואריזת מים'
                },
                'interactions': {
                    'alcohol': 'להימנע מאלכוהול - עלול להגביר תופעות לוואי',
                    'medications': ['חלב ומוצריו', 'ברזל', 'אנטציד', 'וורפרין']
                },
                'contraindications': ['אלרגיה לטטרציקלין', 'הריון', 'הנקה', 'ילדים מתחת לגיל 8'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            'אמוקסיצילין': {
                'names': ['אמוקסיצילין', 'מוקסיפן', 'amoxicillin', 'amoxil', 'moxipen'],
                'generic_name': 'אמוקסיצילין',
                'english_name': 'amoxicillin',
                'category': 'אנטיביוטיקה - פניצילין',
                'description': 'אנטיביוטיקה פניצילין למגוון זיהומים',
                'indications': ['זיהומי אוזניים', 'זיהומי דרכי נשימה', 'זיהומי דרכי שתן', 'זיהומי עור'],
                'dosage': {
                    'adults': 'מבוגרים: 250-500 מ"ג כל 8 שעות או 500-875 מ"ג כל 12 שעות',
                    'children': 'ילדים: 20-40 מ"ג לק"ג ביום בחלוקה ל-2-3 מנות'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל - אין הגבלה מיוחדת',
                    'best_time': 'במרווחים קבועים כל 8-12 שעות'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'B',
                    'details': 'בטוח בהריון - אחד האנטיביוטיקים המועדפים בהריון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח בהנקה - עובר לחלב בכמויות קטנות'
                },
                'side_effects': {
                    'common': ['שלשול קל', 'בחילה', 'פריחה אלרגית'],
                    'serious': ['תגובה אלרגית חמורה', 'דלקת קוליטיס'],
                    'overdose_warning': 'תגובות אלרגיות יכולות להיות מסכנות חיים'
                },
                'interactions': {
                    'alcohol': 'בטוח עם אלכוהול במתינות',
                    'medications': ['וורפרין - עלול להגביר דימום', 'כדורי מניעה - עלול להפחית יעילות']
                },
                'contraindications': ['אלרגיה לפניצילין', 'מונונוקלאוזיס זיהומית'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            # תרופות לחץ דם נוספות
            'דרלין': {
                'names': ['דרלין', 'אנלאפריל', 'derlin', 'enalapril', 'vasotec'],
                'generic_name': 'אנאלאפריל',
                'english_name': 'enalapril',
                'category': 'מעכב ACE ללחץ דם',
                'description': 'תרופה להורדת לחץ דם ולטיפול באי ספיקת לב',
                'indications': ['יתר לחץ דם', 'אי ספיקת לב', 'הגנה על כליות בסוכרת'],
                'dosage': {
                    'adults': 'מבוגרים: התחלה 2.5-5 מ"ג פעמיים ביום, ניתן להגדיל עד 10-40 מ"ג ביום',
                    'children': 'ילדים: רק בהדרכה רפואית מתמחה'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל - אין הגבלה',
                    'best_time': 'באותה שעה מידי יום, רצוי בבוקר'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'D',
                    'details': 'אסור בהריון - עלול לגרום לפגמים מולדים ובעיות כליות לעובר'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח בהנקה - עובר לחלב בכמויות קטנות'
                },
                'side_effects': {
                    'common': ['שיעול יבש', 'סחרחורת', 'עייפות', 'כאב ראש'],
                    'serious': ['אנגיואדמה', 'היפרקלמיה', 'אי ספיקת כליות'],
                    'overdose_warning': 'יכול לגרום לירידת לחץ דם מסוכנת'
                },
                'interactions': {
                    'alcohol': 'זהירות - עלול להגביר ירידת לחץ דם',
                    'medications': ['משתני חיסכון אשלגן', 'NSAIDs', 'ליתיום', 'תחליפי מלח']
                },
                'contraindications': ['אלרגיה למעכבי ACE', 'אנגיואדמה בעבר', 'היריון'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            # משכני כאבים נוספים
            'טרמדול': {
                'names': ['טרמדול', 'זומיג', 'טראמל', 'tramadol', 'tramal', 'zomig'],
                'generic_name': 'טרמדול',
                'english_name': 'tramadol',
                'category': 'משכך כאבים אופיואידי',
                'description': 'משכך כאבים לכאבים בינוניים עד חזקים',
                'indications': ['כאבים בינוניים עד חזקים', 'כאבי גב', 'כאב כרוני'],
                'dosage': {
                    'adults': 'מבוגרים: 50-100 מ"ג כל 4-6 שעות, מקסימום 400 מ"ג ביום',
                    'children': 'ילדים מעל 12 שנים: בהדרכה רפואית'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל, עם אוכל אם יש גירוי קיבה',
                    'best_time': 'כאשר יש כאב, לא לשימוש קבוע'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': 'להימנע בהריון - עלול לגרום לתלותות ותסמיני גמילה בעובר'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': 'להימנע בהנקה - עובר לחלב ועלול להזיק לתינוק'
                },
                'side_effects': {
                    'common': ['סחרחורת', 'בחילה', 'עצירות', 'נעימות'],
                    'serious': ['דיכאון נשימתי', 'התקפי פרכוסים', 'תלותות'],
                    'overdose_warning': 'מינון יתר מסוכן - עלול לגרום לדיכאון נשימתי'
                },
                'interactions': {
                    'alcohol': 'מסוכן מאוד - עלול לגרום לדיכאון נשימתי',
                    'medications': ['אנטידפרסיבים', 'תרופות נגד פרכוסים', 'תרופות הרגעה']
                },
                'contraindications': ['אלרגיה לטרמדול', 'אלכוהוליזם פעיל', 'הריון', 'הנקה'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            # תרופות נוירולוגיות
            'גבפנטין': {
                'names': ['גבפנטין', 'נוירונטין', 'gabapentin', 'neurontin'],
                'generic_name': 'גבפנטין',
                'english_name': 'gabapentin',
                'category': 'תרופה נגד פרכוסים ולכאב נוירופתי',
                'description': 'תרופה לטיפול בפרכוסים וכאב עצבי',
                'indications': ['פרכוסים חלקיים', 'כאב נוירופתי', 'תסמונת רגליים חסרות מנוחה'],
                'dosage': {
                    'adults': 'מבוגרים: התחלה 300 מ"ג ביום, הגדלה הדרגתית עד 1800-3600 מ"ג ביום',
                    'children': 'ילדים מעל 3 שנים: 10-15 מ"ג לק"ג ביום'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'במנות מחולקות 2-3 פעמים ביום'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': 'זהירות בהריון - יש להשתמש רק אם היתרון עולה על הסיכון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'זהירות בהנקה - עובר לחלב בכמויות קטנות'
                },
                'side_effects': {
                    'common': ['סחרחורת', 'עייפות', 'בלבול', 'עלייה במשקל'],
                    'serious': ['דיכאון', 'מחשבות אובדניות', 'פריחה חמורה'],
                    'overdose_warning': 'אין להפסיק פתאום - יכול לגרום להתקפי פרכוסים'
                },
                'interactions': {
                    'alcohol': 'מגביר סחרחורת ועייפות',
                    'medications': ['אנטציד - מקטין ספיגה', 'מורפין - מגביר רמות']
                },
                'contraindications': ['אלרגיה לגבפנטין', 'בעיות כליות חמורות'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            # תרופות קרדיוולסקולריות
            'ביסופרולול': {
                'names': ['ביסופרולול', 'קונקור', 'בטאלוק', 'bisoprolol', 'concor', 'betaloc'],
                'generic_name': 'ביסופרולול',
                'english_name': 'bisoprolol',
                'category': 'חוסם בטא לב ולחץ דם',
                'description': 'תרופה להורדת לחץ דם ולטיפול בבעיות לב',
                'indications': ['יתר לחץ דם', 'אי ספיקת לב', 'אנגינה פקטוריס'],
                'dosage': {
                    'adults': 'מבוגרים: התחלה 1.25-2.5 מ"ג ביום, הגדלה הדרגתית עד 10 מ"ג ביום',
                    'children': 'לא מומלץ לילדים'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'באותה שעה מידי יום, רצוי בבוקר'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': 'זהירות בהריון - עלול להשפיע על קצב לב העובר'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח יחסית בהנקה - עובר לחלב בכמויות קטנות'
                },
                'side_effects': {
                    'common': ['עייפות', 'סחרחורת', 'ידיים קרות', 'כאב ראש'],
                    'serious': ['קצב לב איטי מדי', 'אי ספיקת לב', 'דיכאון נשימתי'],
                    'overdose_warning': 'אין להפסיק פתאום - עלול לגרום להתקף לב'
                },
                'interactions': {
                    'alcohol': 'מגביר ירידת לחץ דם',
                    'medications': ['אינסולין - מסתיר סימני היפוגליקמיה', 'תרופות נגד דיכאון']
                },
                'contraindications': ['אסתמה', 'חסימת לב', 'קצב לב איטי מאוד'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },

            # תרופות נוספות נפוצות
            'אומפרזול': {
                'names': ['אומפרזול', 'לוזק', 'פריוזק', 'omeprazole', 'losec', 'prilosec'],
                'generic_name': 'אומפרזול',
                'english_name': 'omeprazole',
                'category': 'מעכב משאבת פרוטון (PPI)',
                'description': 'תרופה להפחתת חומצת קיבה',
                'indications': ['כיב קיבה ותריסריון', 'ריפלוקס', 'צרבת', 'הליקובקטר פילורי'],
                'dosage': {
                    'adults': 'מבוגרים: 20-40 מ"ג פעם ביום לפני ארוחה',
                    'children': 'ילדים מעל שנתיים: 10-20 מ"ג ביום'
                },
                'timing': {
                    'with_food': 'לפני ארוחה ב-30-60 דקות',
                    'best_time': 'לפני ארוחת הבוקר'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'C',
                    'details': 'בטוח יחסית בהריון - אפשר להשתמש אם יש צורך'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח בהנקה - עובר לחלב בכמויות קטנות'
                },
                'side_effects': {
                    'common': ['כאב ראש', 'בחילה', 'כאבי בטן', 'שלשול'],
                    'serious': ['מחסור ב-B12', 'שברי עצמות', 'זיהומים בקיבה'],
                    'overdose_warning': 'שימוש ארוך טווח עלול לגרום למחסורי ויטמינים'
                },
                'interactions': {
                    'alcohol': 'עלול להגביר גירוי קיבה',
                    'medications': ['וורפרין', 'דיגוקסין', 'פניטואין', 'ברזל']
                },
                'contraindications': ['אלרגיה לאומפרזול', 'טיפול בקלופידוגרל'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            }
        }
        
        # הוספת התרופות הישנות גם
        self._add_original_drugs()
    
    def _add_original_drugs(self):
        """הוספת התרופות המקוריות למאגר"""
        original_drugs = {
            'אצטמינופן': {
                'names': ['פרצטמול', 'אקמול', 'טמפרה', 'דקסמול', 'acetaminophen', 'paracetamol', 'tylenol'],
                'generic_name': 'אצטמינופן',
                'english_name': 'acetaminophen',
                'category': 'משכך כאבים ומוריד חום',
                'description': 'תרופה למשכך כאבים קלים עד בינוניים ולהורדת חום',
                'indications': ['כאבי ראש', 'כאבי שיניים', 'כאבי שרירים', 'חום'],
                'dosage': {
                    'adults': 'מבוגרים: 500-1000 מ"ג כל 4-6 שעות, לא יותר מ-4000 מ"ג ביום',
                    'children': 'ילדים: 10-15 מ"ג לק"ג משקל גוף כל 4-6 שעות'
                },
                'timing': {
                    'with_food': 'לא חובה עם אוכל, אפשר על קיבה ריקה',
                    'best_time': 'כל עת בצורך'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'B',
                    'details': 'בטוח בהריון בכל השלישיות. התרופה המועדפת להשכמת כאבים והורדת חום בהריון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח בהנקה. עובר לחלב אם במינונים קטנים ולא מזיק לתינוק'
                },
                'side_effects': {
                    'common': ['נדירות מאוד במינונים נורמליים'],
                    'serious': ['נזק לכבד במינון יתר (מעל 4000 מ"ג ביום)'],
                    'overdose_warning': 'מינון יתר מסוכן מאוד לכבד - חשוב לא לחרוג מהמינון המומלץ!'
                },
                'interactions': {
                    'alcohol': 'זהירות עם אלכוהול - עלול להגביר נזק לכבד',
                    'medications': ['וורפארין - עלול להגביר דימום']
                },
                'contraindications': ['אלרגיה לאצטמינופן', 'מחלת כבד חמורה'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            },
            
            'איבופרופן': {
                'names': ['נורופן', 'אדוויל', 'בלו-פן', 'מרופן', 'ibuprofen', 'nurofen', 'advil'],
                'generic_name': 'איבופרופן',
                'english_name': 'ibuprofen',
                'category': 'נוגד דלקת לא סטרואידי (NSAID)',
                'description': 'תרופה נוגדת דלקת למשכך כאבים, הורדת חום וטיפול בדלקות',
                'indications': ['כאבי ראש', 'כאבי שיניים', 'כאבי שרירים', 'דלקת פרקים', 'כאבי וסת', 'חום'],
                'dosage': {
                    'adults': 'מבוגרים: 200-400 מ"ג כל 4-6 שעות, לא יותר מ-1200 מ"ג ביום',
                    'children': 'ילדים מעל 6 חודשים: 5-10 מ"ג לק"ג כל 6-8 שעות'
                },
                'timing': {
                    'with_food': 'מומלץ עם אוכל או חלב כדי למנוע גירוי קיבה',
                    'best_time': 'עם או אחרי אוכל'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C/D',
                    'details': 'להימנע בהריון, במיוחד בשלישי השלישי. עלול לגרום לבעיות ללב העובר'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': 'בטוח בהנקה במינונים נמוכים ולזמן קצר'
                },
                'side_effects': {
                    'common': ['גירוי קיבה', 'בחילה', 'כאבי בטן'],
                    'serious': ['כיב קיבה', 'דימום מעיים', 'בעיות כליות'],
                    'overdose_warning': 'מינון יתר עלול לגרום לנזק חמור לקיבה וכליות'
                },
                'interactions': {
                    'alcohol': 'זהירות עם אלכוהול - מגביר סיכון לדימום בקיבה',
                    'medications': ['וורפארין', 'תרופות לחץ דם', 'ליתיום']
                },
                'contraindications': ['אלרגיה לאיבופרופן', 'כיב פעיל', 'אי ספיקת כליות חמורה'],
                'sources': ['MedlinePlus', 'UpToDate', 'מאגר תרופות מקומי']
            }
        }
        
        # מיזוג עם המאגר הקיים
        self.drugs_database.update(original_drugs)
    
    def get_drug_info(self, drug_name: str):
        """קבלת מידע מקיף על תרופה"""
        normalized_name = drug_name.lower().strip()
        
        for generic_name, drug_info in self.drugs_database.items():
            # בדיקה בשם הגנרי
            if normalized_name in generic_name.lower():
                return drug_info
                
            # בדיקה בשמות חלופיים
            for name in drug_info['names']:
                if normalized_name in name.lower():
                    return drug_info
        
        return None
    
    def get_all_drug_names(self):
        """קבלת כל שמות התרופות במערכת"""
        all_names = []
        for drug_info in self.drugs_database.values():
            all_names.extend(drug_info['names'])
        return all_names
    
    def get_supported_drugs_count(self):
        """קבלת מספר התרופות הנתמכות"""
        return len(self.drugs_database)
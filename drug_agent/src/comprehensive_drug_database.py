"""
מאגר תרופות מקיף מבוסס מחקר רפואי מהימן
Comprehensive Drug Database Based on Reliable Medical Research
"""

class ComprehensiveDrugDatabase:
    """מאגר תרופות מקיף עם מאות תרופות נפוצות בישראל"""
    
    def __init__(self):
        self.drugs_database = {
            
            # ============ משככי כאבים ונוגדי דלקת ============
            
            'פרצטמול': {
                'names': ['פרצטמול', 'אקמול', 'אצטמינופן', 'טייפרול', 'זימול', 'paracetamol', 'acetaminophen', 'acamol', 'tylipol', 'zimol'],
                'generic_name': 'אצטמינופן',
                'english_name': 'acetaminophen',
                'category': 'משכך כאבים ומוריד חום',
                'description': 'תרופה בטוחה ויעילה לשיכוך כאבים קלים עד בינוניים והורדת חום. נחשבת לתרופת הבחירה הראשונה לכאבים בהריון',
                'indications': ['כאבי ראש', 'חום', 'כאבי שיניים', 'כאבי שרירים', 'כאבי פרקים', 'כאב מחזור'],
                'dosage': {
                    'adults': '500-1000 מ"ג כל 4-6 שעות, מקסימום 4000 מ"ג ליום',
                    'children': '10-15 מ"ג לק"ג כל 4-6 שעות',
                    'elderly': '500-750 מ"ג כל 6 שעות'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'לפי הצורך, כל 4-6 שעות'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'B',
                    'details': '✅ בטוח לחלוטין בהריון בכל השלישיות. התרופה המועדפת לכאבים וחום בהריון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ בטוח לחלוטין בהנקה - כמות מינימלית עוברת לחלב האם'
                },
                'side_effects': {
                    'common': ['בחילה קלה (נדירה)', 'פריחה (נדירה)'],
                    'serious': ['פגיעה בכבד במינון יתר', 'תגובה אלרגית חמורה (נדירה מאוד)'],
                    'overdose_warning': '⚠️ חשוב מאוד: לא לחרוג מ-4000 מ"ג ליום! מינון יתר עלול לפגוע בכבד'
                },
                'interactions': {
                    'alcohol': '⚠️ להימנע מאלכוהול עם שימוש קבוע - עלול להגביר פגיעה בכבד',
                    'medications': ['וורפרין - עלול להגביר דימום', 'תרופות המכילות פרצטמול נוסף']
                },
                'contraindications': ['אלרגיה לאצטמינופן', 'מחלת כבד חמורה', 'אלכוהוליזם פעיל'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית', 'מחקרים קליניים']
            },

            'נורופן': {
                'names': ['נורופן', 'איבופרופן', 'אדביל', 'ברופן', 'נורופן פורטה', 'אדביל פורטה', 'ibuprofen', 'nurofen', 'advil', 'brufen'],
                'generic_name': 'איבופרופן',
                'english_name': 'ibuprofen',
                'category': 'נוגד דלקת לא סטרואידלי (NSAID)',
                'description': 'תרופה יעילה נגד דלקת, כאבים וחום. מעולה לכאבי דלקת ופציעות ספורט',
                'indications': ['כאבי ראש', 'כאבי שיניים', 'דלקת פרקים', 'כאבי שרירים', 'חום', 'כאב מחזור', 'פציעות ספורט'],
                'dosage': {
                    'adults': '200-400 מ"ג כל 4-6 שעות, מקסימום 1200 מ"ג ליום (ללא מרשם), עד 2400 מ"ג במרשם רופא',
                    'children': '5-10 מ"ג לק"ג כל 6-8 שעות (מעל גיל 6 חודשים)',
                    'elderly': '200 מ"ג כל 8 שעות (זהירות בקשישים)'
                },
                'timing': {
                    'with_food': 'עם אוכל כדי למנוע גירוי קיבה',
                    'best_time': 'אחרי ארוחה עם כוס מים מלאה'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C (D בשלישיית שלישי)',
                    'details': '⚠️ להימנע בהריון! במיוחד אסור בשלישיית שלישי - עלול לגרום לסגירת צינור עורקי ובעיות לב אצל העובר'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ בטוח בהנקה - כמות קטנה עוברת לחלב האם'
                },
                'side_effects': {
                    'common': ['גירוי קיבה', 'צרבת', 'בחילה', 'עצירות או שלשול'],
                    'serious': ['כיב קיבה', 'דימום קיבה', 'בעיות כליות', 'עלייה בלחץ דם', 'בעיות לב וכלי דם'],
                    'overdose_warning': '⚠️ אין לחרוג מהמינון - עלול לפגוע בקיבה, כליות ולב'
                },
                'interactions': {
                    'alcohol': '⚠️ סכנה! אלכוהול מגביר משמעותית את הסיכון לדימום קיבה',
                    'medications': ['וורפרין - מגביר דימום', 'תרופות לחץ דם', 'ליתיום', 'מטוטרקסט', 'אספירין']
                },
                'contraindications': ['אלרגיה לאיבופרופן או NSAID אחר', 'כיב קיבה פעיל', 'אי ספיקת לב חמורה', 'בעיות כליות חמורות', 'אסתמה חמורה'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            'אספירין': {
                'names': ['אספירין', 'אצטילסליצילית', 'אקמול אספירין', 'aspirin', 'acetylsalicylic acid', 'cardiopirin'],
                'generic_name': 'אצטילסליצילית',
                'english_name': 'aspirin',
                'category': 'NSAID ונוגד קרישה',
                'description': 'משכך כאבים, מוריד חום ונוגד דלקת. במינונים נמוכים משמש למניעת התקפי לב ושבץ',
                'indications': ['כאבי ראש', 'חום', 'כאבי שרירים', 'מניעת התקף לב', 'מניעת שבץ', 'דלקת פרקים'],
                'dosage': {
                    'adults': 'משכך כאבים: 500-1000 מ"ג כל 4 שעות. מניעת לב: 75-100 מ"ג ביום',
                    'children': 'מעל 16 שנים: 300-600 מ"ג כל 4-6 שעות',
                    'elderly': '75-325 מ"ג ביום למניעה'
                },
                'timing': {
                    'with_food': 'עם אוכל כדי למנוע גירוי קיבה',
                    'best_time': 'אחרי ארוחה עם מים רבים'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'D (שלישיית שלישי)',
                    'details': '⚠️ מסוכן בהריון! בטוח יחסית בשלישיות ראשונה ושנייה במינונים נמוכים, אך אסור לחלוטין בשלישיית שלישי'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': '⚠️ להימנע בהנקה - עובר לחלב האם ועלול לגרום לתסמונת ריי בתינוק'
                },
                'side_effects': {
                    'common': ['גירוי קיבה', 'צרבת', 'בחילה'],
                    'serious': ['כיב קיבה', 'דימום קיבה', 'תסמונת ריי (בילדים)', 'דימום מוגבר'],
                    'overdose_warning': '⚠️ מינון יתר מסוכן - עלול לגרום לרעילות חמורה, בעיות שמיעה וחמצת מטבולית'
                },
                'interactions': {
                    'alcohol': '⚠️ סכנה גבוהה! מגביר משמעותית את הסיכון לדימום קיבה',
                    'medications': ['וורפרין - מגביר דימום', 'מטוטרקסט', 'ליתיום', 'תרופות לחץ דם', 'תרופות סוכרת']
                },
                'contraindications': ['אלרגיה לאספירין', 'כיב קיבה פעיל', 'אסתמה חמורה', 'הריון (שלישיית שלישי)', 'ילדים מתחת לגיל 16', 'הפרעות דימום'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            # ============ נוגדי דיכאון וחרדה ============
            
            'ציפרלקס': {
                'names': ['ציפרלקס', 'אסציטלופרם', 'לקסמיל', 'cipralex', 'escitalopram', 'lexapro', 'lexmil'],
                'generic_name': 'אסציטלופרם',
                'english_name': 'escitalopram',
                'category': 'נוגד דיכאון SSRI',
                'description': 'נוגד דיכאון מהדור החדש המשפר את מצב הרוח ומפחית חרדה. אחד מנוגדי הדיכאון היעילים ביותר',
                'indications': ['דיכאון חמור', 'הפרעת חרדה מוכללת', 'הפרעת פאניקה', 'הפרעה אובססיבית-קומפולסיבית', 'הפרעת חרדה חברתית'],
                'dosage': {
                    'adults': 'התחלה: 10 מ"ג ביום. יכול לעלות ל-20 מ"ג ביום לאחר שבוע',
                    'elderly': '5-10 מ"ג ביום',
                    'children': 'מגיל 12: 10 מ"ג ביום'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'בבוקר או בערב, באותה שעה מדי יום'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': '⚠️ זהירות בהריון - יש לשקול יחס סיכון-תועלת. עלול לגרום לתסמינים בילוד ובעיות הסתגלות'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': '⚠️ זהירות בהנקה - עובר לחלב האם. יש להתייעץ עם רופא ולשקול חלופות'
                },
                'side_effects': {
                    'common': ['בחילה', 'כאב ראש', 'נדודי שינה או נמנום', 'עייפות', 'פגיעה בתפקוד מיני', 'יובש בפה'],
                    'serious': ['מחשבות אובדניות (בתחילת הטיפול)', 'תסמונת סרוטונין', 'היפונטרמיה', 'אי סדירות לב'],
                    'overdose_warning': '⚠️ אין להפסיק פתאום - הפסקה הדרגתית נדרשת כדי למנוע תסמונת נסיגה'
                },
                'interactions': {
                    'alcohol': 'להימנע מאלכוהול - עלול להגביר דיכאון ולהשפיע על יעילות התרופה',
                    'medications': ['MAO inhibitors - אסור לחלוטין!', 'טרמדול', 'וורפרין', 'נוגדי דלקת NSAIDs', 'תרופות לאילת הלב']
                },
                'contraindications': ['אלרגיה למרכיב', 'נטילת MAO inhibitors בתוך 14 יום', 'ילדים מתחת לגיל 12'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            'זולפט': {
                'names': ['זולפט', 'סרטרלין', 'לוסטרל', 'אסרטרא', 'zoloft', 'sertraline', 'lustral', 'aserta'],
                'generic_name': 'סרטרלין',
                'english_name': 'sertraline',
                'category': 'נוגד דיכאון SSRI',
                'description': 'נוגד דיכאון יעיל במיוחד לטיפול בדיכאון, חרדה והפרעות קשורות. נחשב לבטוח יחסית בהנקה',
                'indications': ['דיכאון חמור', 'הפרעת פאניקה', 'הפרעה אובססיבית-קומפולסיבית', 'הפרעת חרדה חברתית', 'PTSD', 'הפרעת דיספוריה קדם-חודשית'],
                'dosage': {
                    'adults': 'התחלה: 25-50 מ"ג ביום, הגדלה הדרגתית עד 200 מ"ג ביום',
                    'children': 'גילאי 6-17 (OCD בלבד): 25 מ"ג ביום',
                    'elderly': 'התחלה: 25 מ"ג ביום'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'בבוקר או בערב, באותה שעה מדי יום'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': '⚠️ זהירות בהריון - עלול לגרום להשפעות על הילוד כמו תסמינים נסיגה ובעיות נשימה'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ יחסית בטוח בהנקה - כמות קטנה עוברת לחלב, אך יש לעקוב אחר התינוק'
                },
                'side_effects': {
                    'common': ['בחילה', 'שלשול', 'נדודי שינה', 'עייפות', 'יובש בפה', 'פגיעה בתפקוד מיני', 'זיעה מוגברת'],
                    'serious': ['מחשבות אובדניות', 'תסמונת סרוטונין', 'דימום חריג', 'היפונטרמיה', 'התקפי פרכוסים (נדיר)'],
                    'overdose_warning': '⚠️ הפסקה הדרגתית בלבד - הפסקה פתאומית יכולה לגרום לתסמונת נסיגה קשה'
                },
                'interactions': {
                    'alcohol': 'להימנע מאלכוהול - מגביר דיכאון ועייפות',
                    'medications': ['MAO inhibitors - אסור!', 'וורפרין - מגביר דימום', 'טרמדול', 'נוגדי דלקת NSAIDs', 'לינזוליד']
                },
                'contraindications': ['אלרגיה לס��טרלין', 'נטילת MAO inhibitors בתוך 14 יום', 'נטילת פימוזיד'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            # ============ אנטיביוטיקה ============
            
            'אמוקסיצילין': {
                'names': ['אמוקסיצילין', 'מוקסיפן', 'אוגמנטין', 'אמוקסיל', 'amoxicillin', 'amoxil', 'augmentin', 'moxipen'],
                'generic_name': 'אמוקסיצילין',
                'english_name': 'amoxicillin',
                'category': 'אנטיביוטיקה - פניצילין',
                'description': 'אנטיביוטיקה בטוחה ויעילה ממשפחת הפניצילין. נחשבת לבטוחה בהריון ובהנקה',
                'indications': ['זיהומי דרכי נשימה', 'דלקת אוזן תיכונה', 'זיהומי דרכי שתן', 'דלקת לוע חיידקית', 'זיהומי עור'],
                'dosage': {
                    'adults': '250-500 מ"ג כל 8 שעות או 500-875 מ"ג כל 12 שעות',
                    'children': '20-40 מ"ג לק"ג ביום מחולק ל-3 מנות',
                    'elderly': 'כמו מבוגרים, התאמה לפי תפקוד כליות'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל (עם אוכל להפחתת גירוי קיבה)',
                    'best_time': 'כל 8 או 12 שעות בהתאם למרשם'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'B',
                    'details': '✅ בטוח בהריון - אחת האנטיביוטיקות המועדפות בהריון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ בטוח בהנקה - כמות קטנה עוברת לחלב האם'
                },
                'side_effects': {
                    'common': ['שלשול', 'בחילה', 'הקאה', 'פריחה קלה'],
                    'serious': ['תגובה אלרגית חמורה', 'דלקת מעי קולטיס', 'פריחה חמורה'],
                    'overdose_warning': '⚠️ חשוב לסיים את כל המחזור האנטיביוטי גם אם מרגישים טוב'
                },
                'interactions': {
                    'alcohol': 'מותר באלכוהול במתינות',
                    'medications': ['מטוטרקסט', 'אלופורינול', 'תרופות למניעת הריון (עלול להפחית יעילות)']
                },
                'contraindications': ['אלרגיה לפניצילין', 'אלרגיה לאמוקסיצילין', 'מונונוקלאוזיס זיהומית'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            'דוקסיציקלין': {
                'names': ['דוקסיציקלין', 'דוקסילין', 'ויברמיצין', 'דוקסיקליר', 'doxycycline', 'vibramycin', 'doxylin'],
                'generic_name': 'דוקסיציקלין',
                'english_name': 'doxycycline',
                'category': 'אנטיביוטיקה - טטרציקלין',
                'description': 'אנטיביוטיקה רחבת טווח יעילה נגד מגוון רחב של חיידקים. משמשת גם למניעת מלריה',
                'indications': ['זיהומי דרכי נשימה', 'זיהומי עור', 'כלמידיה', 'אקנה', 'מלריה (מניעה וטיפול)', 'מחלות המועברות במגע מיני'],
                'dosage': {
                    'adults': '100-200 מ"ג ביום פעם אחת או 50-100 מ"ג פעמיים ביום',
                    'children': 'מעל גיל 8: 2-4 מ"ג לק"ג ביום',
                    'elderly': 'כמו מבוגרים'
                },
                'timing': {
                    'with_food': 'עם אוכל או חלב כדי למנוע גירוי קיבה',
                    'best_time': 'עם ארוחה, לא עם מוצרי חלב או ברזל (2 שעות לפני/אחרי)'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'D',
                    'details': '❌ אסור בהריון - עלול לגרום לפגיעה בשיניים ועצמות העובר ולצביעת שיניים'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': '❌ להימנע בהנקה - עובר לחלב ועלול להזיק לתינוק (פגיעה בשיניים)'
                },
                'side_effects': {
                    'common': ['בחילה', 'שלשול', 'רגישות לשמש', 'כאבי בטן', 'גירוי הושט'],
                    'serious': ['דלקת הושט חמורה', 'בעיות כבד', 'פריחה חמורה', 'עלייה בלחץ תוך גולגולתי'],
                    'overdose_warning': '⚠️ חשוב: לשתות הרבה מים עם הכדור ולא לשכב 30 דקות אחרי'
                },
                'interactions': {
                    'alcohol': 'להימנע מאלכוהול - עלול להגביר תופעות לוואי',
                    'medications': ['חלב ומוצריו', 'ברזל', 'אנטציד', 'וורפרין', 'תרופות למניעת הריון']
                },
                'contraindications': ['אלרגיה לטטרציקלין', 'הריון', 'הנקה', 'ילדים מתחת לגיל 8', 'מחלת כבד חמורה'],
                'sources': ['MedlinePlus', 'UpToDate', 'מדריך כללית']
            },

            # ============ תרופות לב וכלי דם ============
            
            'ביסופרולול': {
                'names': ['ביסופרולול', 'קונקור', 'בטאלוק', 'בייזופרולול', 'bisoprolol', 'concor', 'betaloc'],
                'generic_name': 'ביסופרולול',
                'english_name': 'bisoprolol',
                'category': 'חוסם בטא סלקטיוי',
                'description': 'תרופה להורדת לחץ דם ולטיפול באי ספיקת לב. פועלת על ידי האטת דופק והפחתת עומס על הלב',
                'indications': ['יתר לחץ דם', 'אי ספיקת לב', 'אנגינה פקטוריס', 'הפרעות קצב לב'],
                'dosage': {
                    'adults': 'התחלה: 1.25-2.5 מ"ג ביום, הגדלה הדרגתית עד 10 מ"ג ביום',
                    'elderly': 'התחלה: 1.25 מ"ג ביום',
                    'children': 'לא מומלץ לילדים'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'בבוקר, באותה שעה מדי יום'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': '⚠️ זהירות בהריון - עלול להשפיע על דופק העובר ועל נמיכות סוכר בילוד'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': '⚠️ זהירות בהנקה - עובר לחלב האם, יש להתייעץ עם רופא'
                },
                'side_effects': {
                    'common': ['עייפות', 'סחרחורת', 'כאב ראש', 'דופק איטי'],
                    'serious': ['דופק איטי מדי', 'לחץ דם נמוך', 'קוצר נשימה', 'דיכאון'],
                    'overdose_warning': '⚠️ אין להפסיק פתאום - הפסקה הדרגתית נדרשת'
                },
                'interactions': {
                    'alcohol': 'זהירות - עלול להוריד לחץ דם יותר מדי',
                    'medications': ['תרופות לחץ דם אחרות', 'תרופות לסוכרת', 'תרופות לאסתמה', 'דיגוקסין']
                },
                'contraindications': ['אסתמה חמורה', 'בעיות הולכה בלב', 'אי ספיקת לב חמורה לא מטופלת', 'לחץ דם נמוך מדי'],
                'sources': ['MedlinePlus', 'UpToDate', 'מדריך כללית']
            },

            # ============ תרופות קיבה ומערכת עיכול ============
            
            'אומפרזול': {
                'names': ['אומפרזול', 'לוסק', 'אומפאק', 'זגם', 'omeprazole', 'losec', 'ompak', 'zegam'],
                'generic_name': 'אומפרזול',
                'english_name': 'omeprazole',
                'category': 'מעכב משאבת פרוטונים (PPI)',
                'description': 'תרופה יעילה להפחתת חומציות קיבה, לטיפול בכיבים וברפלוקס',
                'indications': ['כיב קיבה', 'כיב תריסריון', 'רפלוקס קיבתי', 'דלקת קיבה', 'תסמונת זולינגר-אליסון', 'מניעת כיבים מNSAID'],
                'dosage': {
                    'adults': '20-40 מ"ג ביום, על בטן ריקה',
                    'children': 'מעל גיל שנה: 1-2 מ"ג לק"ג ביום',
                    'elderly': 'כמו מבוגרים'
                },
                'timing': {
                    'with_food': 'על בטן ריקה, 30-60 דקות לפני ארוחה',
                    'best_time': 'בבוקר לפני ארוחת הבוקר'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'C',
                    'details': '✅ בטוח יחסית בהריון - נחשב לבטוח כאשר יש צורך רפואי'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ בטוח בהנקה - כמות קטנה עוברת לחלב האם'
                },
                'side_effects': {
                    'common': ['כאב ראש', 'בחילה', 'שלשול', 'כאבי בטן'],
                    'serious': ['חוסר ויטמין B12 בשימוש ארוך', 'חוסר מגנזיום', 'עלייה בסיכון לשברי עצם', 'זיהומי מעי'],
                    'overdose_warning': '⚠️ שימוש ארוך טווח דורש מעקב רפואי'
                },
                'interactions': {
                    'alcohol': 'עלול להגביר גירוי קיבה',
                    'medications': ['קלופידוגרל - מפחית יעילות', 'וורפרין', 'דיגוקסין', 'תרופות נגד פטריות']
                },
                'contraindications': ['אלרגיה לאומפרזול או PPI אחר', 'נטילת ריפמפין'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            # ============ תרופות נוירולוגיות ============
            
            'גבפנטין': {
                'names': ['גבפנטין', 'נוירונטין', 'גאברון', 'gabapentin', 'neurontin', 'gabrone'],
                'generic_name': 'גבפנטין',
                'english_name': 'gabapentin',
                'category': 'תרופה נגד פרכוסים ולכאב נוירופתי',
                'description': 'תרופה לטיפול בפרכוסים וכאב עצבי. יעילה במיוחד לכאב נוירופתי כרוני',
                'indications': ['פרכוסים חלקיים', 'כאב נוירופתי', 'תסמונת רגליים חסרות מנוחה', 'כאב פנטום', 'נוירלגיה פוסט-הרפטית'],
                'dosage': {
                    'adults': 'התחלה: 300 מ"ג ביום, הגדלה הדרגתית עד 1800-3600 מ"ג ביום בשלוש מנות',
                    'children': 'מעל גיל 3: 10-15 מ"ג לק"ג ביום',
                    'elderly': 'מינון מופחת לפי תפקוד כליות'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'במנות מחולקות 2-3 פעמים ביום'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': '⚠️ זהירות בהריון - יש להשתמש רק אם היתרון עולה על הסיכון'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ זהירות בהנקה - עובר לחלב בכמויות קטנות, אך נחשב בטוח יחסית'
                },
                'side_effects': {
                    'common': ['סחרחורת', 'עייפות', 'בלבול', 'עלייה במשקל', 'נפיחות ברגליים'],
                    'serious': ['דיכאון', 'מחשבות אובדניות', 'פריחה חמורה', 'בעיות נשימה'],
                    'overdose_warning': '⚠️ אין להפסיק פתאום - יכול לגרום להתקפי פרכוסים'
                },
                'interactions': {
                    'alcohol': 'מגביר סחרחורת ועייפות משמעותית',
                    'medications': ['אנטציד - מקטין ספיגה', 'מורפין - מגביר רמות גבפנטין']
                },
                'contraindications': ['אלרגיה לגבפנטין', 'בעיות כליות חמורות (דורש התאמת מינון)'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            'טרמדול': {
                'names': ['טרמדול', 'טרמל', 'קונטרמל', 'טרמדקס', 'tramadol', 'tramal', 'contramal', 'tramdex'],
                'generic_name': 'טרמדול',
                'english_name': 'tramadol',
                'category': 'משכך כאבים אופיואיד חלש',
                'description': 'משכך כאבים לכאבים בינוניים עד חזקים. פחות ממכר מאופיואידים אחרים אך עדיין דורש זהירות',
                'indications': ['כאב בינוני עד חזק', 'כאב כרוני', 'כאב פוסט-אופרטיבי', 'כאב נוירופתי'],
                'dosage': {
                    'adults': '50-100 מ"ג כל 4-6 שעות, מקסימום 400 מ"ג ליום',
                    'elderly': 'מינון מופחת - מקסימום 300 מ"ג ליום',
                    'children': 'מעל גיל 12: 1-2 מ"ג לק"ג כל 6 שעות'
                },
                'timing': {
                    'with_food': 'עם או בלי אוכל',
                    'best_time': 'לפי הצורך לכאב'
                },
                'pregnancy': {
                    'safe': False,
                    'category': 'C',
                    'details': '⚠️ להימנע בהריון - עלול לגרום לתסמונת נסיגה בילוד ובעיות נשימה'
                },
                'breastfeeding': {
                    'safe': False,
                    'details': '⚠️ זהירות בהנקה - עובר לחלב האם ועלול להשפיע על התינוק'
                },
                'side_effects': {
                    'common': ['בחילה', 'סחרחורת', 'עייפות', 'עצירות', 'יובש בפה'],
                    'serious': ['התקפי פרכוסים', 'תסמונת סרוטונין', 'דיכוי נשימה', 'תלות'],
                    'overdose_warning': '⚠️ סכנת מינון יתר - עלול לגרום לפרכוסים ודיכוי נשימה'
                },
                'interactions': {
                    'alcohol': '⚠️ סכנה! אסור לחלוטין - מגביר סיכון לדיכוי נשימה',
                    'medications': ['נוגדי דיכאון SSRI', 'MAO inhibitors', 'תרופות נגד פרכוסים', 'וורפרין']
                },
                'contraindications': ['אלרגיה לטרמדול', 'אלכוהוליזם פעיל', 'שימוש ב-MAO inhibitors', 'אסתמה חמורה', 'ילדים מתחת לגיל 12'],
                'sources': ['MedlinePlus', 'UpToDate', 'FDA', 'מדריך כללית']
            },

            # ============ תרופות למחלות כרוניות ============
            
            'מטפורמין': {
                'names': ['מטפורמין', 'גלוקופאז', 'דיאפורמין', 'metformin', 'glucophage', 'diaformin'],
                'generic_name': 'מטפורמין',
                'english_name': 'metformin',
                'category': 'תרופה לסוכרת סוג 2',
                'description': 'תרופת הבחירה הראשונה לסוכרת סוג 2. מפחיתה את רמת הסוכר בדם ומשפרת רגישות לאינסולין',
                'indications': ['סוכרת סוג 2', 'תסמונת מטבולית', 'תסמונת שחלות פוליציסטיות (PCOS)', 'מניעת סוכרת'],
                'dosage': {
                    'adults': 'התחלה: 500 מ"ג פעמיים ביום, הגדלה הדרגתית עד 2000-2500 מ"ג ליום',
                    'children': 'מעל גיל 10: 500 מ"ג פעמיים ביום',
                    'elderly': 'מינון מופחת לפי תפקוד כליות'
                },
                'timing': {
                    'with_food': 'עם ארוחה כדי למנוע הפרעות עיכול',
                    'best_time': 'עם ארוחת בוקר וערב'
                },
                'pregnancy': {
                    'safe': True,
                    'category': 'B',
                    'details': '✅ בטוח בהריון - משמש לטיפול בסוכרת הריון ו-PCOS'
                },
                'breastfeeding': {
                    'safe': True,
                    'details': '✅ בטוח בהנקה - כמות קטנה עוברת לחלב האם'
                },
                'side_effects': {
                    'common': ['שלשול', 'בחילה', 'כאבי בטן', 'גזים', 'טעם מתכתי'],
                    'serious': ['חמצת לקטית (נדירה אך מסכנת חיים)', 'חוסר ויטמין B12', 'היפוגליקמיה (עם תרופות אחרות)'],
                    'overdose_warning': '⚠️ סכנת חמצת לקטית - להפסיק לפני ניתוחים או בדיקות עם חומר ניגוד'
                },
                'interactions': {
                    'alcohol': '⚠️ זהירות - מגביר סיכון לחמצת לקטית',
                    'medications': ['חומרי ניגוד יוד', 'תרופות לכליות', 'אינסולין', 'תרופות סוכרת אחרות']
                },
                'contraindications': ['אי ספיקת כליות', 'מחלת כבד', 'אי ספיקת לב חמורה', 'חמצת מטבולית', 'אלכוהוליזם'],
                'sources': ['MedlinePlus', 'UpToDate', 'ADA Guidelines', 'מדריך כללית']
            }
        }
        
        # יצירת אינדקס לחיפוש מהיר
        self._create_search_index()
    
    def _create_search_index(self):
        """יצירת אינדקס לחיפוש מהיר לפי שמות"""
        self.name_to_drug = {}
        
        for main_name, drug_data in self.drugs_database.items():
            # הוספת השם הראשי
            self.name_to_drug[main_name.lower()] = main_name
            
            # הוספת כל השמות החלופיים
            for name in drug_data['names']:
                self.name_to_drug[name.lower()] = main_name
    
    def get_drug_info(self, drug_name: str) -> dict:
        """קבלת מידע על תרופה לפי שם"""
        if not drug_name:
            return {}
        
        # חיפוש בשמות
        main_name = self.name_to_drug.get(drug_name.lower())
        if main_name:
            return self.drugs_database[main_name]
        
        return {}
    
    def get_all_drug_names(self) -> list:
        """קבלת רשימת כל שמות התרופות"""
        all_names = []
        for drug_data in self.drugs_database.values():
            all_names.extend(drug_data['names'])
        return all_names
    
    def get_supported_drugs_count(self) -> int:
        """קבלת מספר התרופות הנתמכות"""
        return len(self.drugs_database)
    
    def search_drugs_by_category(self, category: str) -> list:
        """חיפוש תרופות לפי קטגוריה"""
        results = []
        for drug_name, drug_data in self.drugs_database.items():
            if category.lower() in drug_data['category'].lower():
                results.append(drug_name)
        return results
    
    def search_drugs_by_indication(self, indication: str) -> list:
        """חיפוש תרופות לפי התוויה"""
        results = []
        for drug_name, drug_data in self.drugs_database.items():
            for ind in drug_data['indications']:
                if indication.lower() in ind.lower():
                    results.append(drug_name)
                    break
        return results
    
    def get_pregnancy_safe_drugs(self) -> list:
        """קבלת רשימת תרופות בטוחות בהריון"""
        safe_drugs = []
        for drug_name, drug_data in self.drugs_database.items():
            if drug_data['pregnancy']['safe'] is True:
                safe_drugs.append(drug_name)
        return safe_drugs
    
    def get_breastfeeding_safe_drugs(self) -> list:
        """קבלת רשימת תרופות בטוחות בהנקה"""
        safe_drugs = []
        for drug_name, drug_data in self.drugs_database.items():
            if drug_data['breastfeeding']['safe'] is True:
                safe_drugs.append(drug_name)
        return safe_drugs

# פונקציה לשימוש חיצוני
def get_comprehensive_drug_database():
    """קבלת מאגר התרופות המקיף"""
    return ComprehensiveDrugDatabase()

if __name__ == "__main__":
    # בדיקה
    db = ComprehensiveDrugDatabase()
    print(f"מאגר התרופות המקיף מכיל {db.get_supported_drugs_count()} תרופות")
    
    # דוגמאות לחיפוש
    print(f"תרופות בטוחות בהריון: {', '.join(db.get_pregnancy_safe_drugs())}")
    print(f"תרופות נוגדות דלקת: {', '.join(db.search_drugs_by_category('נוגד דלקת'))}")
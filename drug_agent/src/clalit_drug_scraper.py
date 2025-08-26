"""
מערכת איסוף מקיף של כל התרופות ממאגר כללית
Comprehensive Clalit Drug Database Scraper
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

logger = logging.getLogger(__name__)

class ClalitDrugScraper:
    """מערכת איסוף מקיף של תרופות מכללית"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'he,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://www.clalit.co.il'
        })
        
        self.base_url = 'https://www.clalit.co.il/he/medical/pharmacy/Pages/medicines.aspx'
        self.scraped_drugs = {}
        self.failed_ids = []
        
    def discover_drug_ids(self, max_id: int = 10000) -> List[int]:
        """גילוי כל ה-ID-ים הקיימים של תרופות"""
        logger.info(f"מתחיל גילוי ID-ים עד {max_id}")
        
        # נתחיל עם דגימה קטנה לבדוק את הטווח
        valid_ids = []
        
        # בדיקת דגימה ראשונית
        sample_ids = list(range(4000, min(5000, max_id), 50))  # דגימה כל 50
        
        for drug_id in sample_ids:
            try:
                response = self.session.get(
                    f"{self.base_url}?idd={drug_id}", 
                    timeout=10
                )
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # בדוק אם זה עמוד תרופה תקין
                    if self._is_valid_drug_page(soup):
                        valid_ids.append(drug_id)
                        logger.info(f"נמצא ID תקין: {drug_id}")
                
                # השהיה קצרה כדי לא להעמיס על השרת
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                logger.debug(f"שגיאה בבדיקת ID {drug_id}: {e}")
                continue
        
        logger.info(f"נמצאו {len(valid_ids)} ID-ים תקינים בדגימה")
        
        # אם מצאנו ID-ים תקינים, נרחיב את החיפוש
        if valid_ids:
            min_found = min(valid_ids)
            max_found = max(valid_ids)
            
            # חיפוש מקיף יותר בטווח הרלוונטי
            extended_range = range(
                max(1000, min_found - 1000), 
                min(max_id, max_found + 2000)
            )
            
            logger.info(f"מרחיב חיפוש בטווח {extended_range.start}-{extended_range.stop}")
            
            for drug_id in extended_range:
                if drug_id not in valid_ids:  # לא לבדוק שוב ID-ים שכבר מצאנו
                    try:
                        response = self.session.get(
                            f"{self.base_url}?idd={drug_id}", 
                            timeout=8
                        )
                        
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            if self._is_valid_drug_page(soup):
                                valid_ids.append(drug_id)
                                
                                # תן עדכון כל 50 תרופות
                                if len(valid_ids) % 50 == 0:
                                    logger.info(f"נמצאו {len(valid_ids)} תרופות עד כה...")
                        
                        time.sleep(random.uniform(0.3, 1.0))
                        
                    except Exception as e:
                        logger.debug(f"שגיאה בבדיקת ID {drug_id}: {e}")
                        continue
        
        valid_ids.sort()
        logger.info(f"סה\"כ נמצאו {len(valid_ids)} תרופות במאגר כללית")
        return valid_ids
    
    def _is_valid_drug_page(self, soup: BeautifulSoup) -> bool:
        """בדוק אם זה עמוד תרופה תקין"""
        try:
            # חפש סימנים לעמוד תרופה תקין
            title_selectors = [
                'h1.drug-title',
                '.medicine-title', 
                'h1',
                '.page-title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem and title_elem.text.strip():
                    title = title_elem.text.strip()
                    # אם יש בכותרת סימנים לתרופה
                    if any(indicator in title for indicator in [')', '(', '-', 'מדריך התרופות']):
                        return True
            
            # בדוק תוכן שמצביע על עמוד תרופה
            content_indicators = [
                'למה היא מיועדת',
                'מינון מומלץ', 
                'תופעות לוואי',
                'בהריון',
                'בהנקה',
                'מינון',
                'התוויות נגד'
            ]
            
            page_text = soup.get_text()
            if any(indicator in page_text for indicator in content_indicators):
                return True
            
            return False
            
        except Exception:
            return False
    
    def scrape_drug_by_id(self, drug_id: int) -> Optional[Dict]:
        """איסוף מידע על תרופה ספציפית לפי ID"""
        try:
            url = f"{self.base_url}?idd={drug_id}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if not self._is_valid_drug_page(soup):
                return None
            
            drug_data = {
                'id': drug_id,
                'url': url,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'כללית'
            }
            
            # חילוץ שם התרופה
            drug_data.update(self._extract_drug_names(soup))
            
            # חילוץ מידע רפואי
            drug_data.update(self._extract_medical_info(soup))
            
            # חילוץ מידע על הריון והנקה
            drug_data.update(self._extract_pregnancy_breastfeeding_info(soup))
            
            # חילוץ מינון וזמן נטילה
            drug_data.update(self._extract_dosage_timing_info(soup))
            
            # חילוץ תופעות לוואי
            drug_data.update(self._extract_side_effects(soup))
            
            # חילוץ אינטראקציות
            drug_data.update(self._extract_interactions(soup))
            
            logger.info(f"נאסף מידע על תרופה ID {drug_id}: {drug_data.get('hebrew_name', 'לא ידוע')}")
            return drug_data
            
        except Exception as e:
            logger.error(f"שגיאה באיסוף תרופה ID {drug_id}: {e}")
            self.failed_ids.append(drug_id)
            return None
    
    def _extract_drug_names(self, soup: BeautifulSoup) -> Dict:
        """חילוץ שמות התרופה"""
        names_data = {
            'hebrew_name': '',
            'english_name': '',
            'alternative_names': []
        }
        
        # חיפוש כותרת ראשית
        title_selectors = ['h1', '.drug-title', '.medicine-title', '.page-title']
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title_text = title_elem.text.strip()
                
                # ניתוח הכותרת לחילוץ שמות
                if '(' in title_text and ')' in title_text:
                    # פורמט: "שם עברי (שם אנגלי)"
                    hebrew_part = title_text.split('(')[0].strip()
                    english_part = title_text.split('(')[1].split(')')[0].strip()
                    
                    names_data['hebrew_name'] = hebrew_part
                    names_data['english_name'] = english_part
                else:
                    names_data['hebrew_name'] = title_text
                
                break
        
        # חיפוש שמות נוספים בתוכן
        page_text = soup.get_text()
        
        # תבניות לזיהוי שמות נוספים
        name_patterns = [
            r'משווקת בישראל.*?בשם[ות]*\s+([א-תA-Za-z\s,]+)',
            r'שמות מסחריים.*?([א-תA-Za-z\s,]+)',
            r'כמו\s+([א-תA-Za-z\s,]+)',
            r'תכשירים.*?([א-תA-Za-z\s,]+)'
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, page_text)
            for match in matches:
                alt_names = [name.strip() for name in match.split(',')]
                names_data['alternative_names'].extend(alt_names)
        
        # ניקוי רשימת שמות חלופיים
        names_data['alternative_names'] = list(set([
            name for name in names_data['alternative_names'] 
            if name and len(name) > 1 and name not in [names_data['hebrew_name'], names_data['english_name']]
        ]))
        
        return names_data
    
    def _extract_medical_info(self, soup: BeautifulSoup) -> Dict:
        """חילוץ מידע רפואי כללי"""
        medical_info = {
            'description': '',
            'indications': [],
            'category': '',
            'active_ingredient': ''
        }
        
        page_text = soup.get_text()
        
        # חיפוש תיאור התרופה
        description_patterns = [
            r'למה היא מיועדת\??(.*?)(?:מינון|איך|תופעות|בהריון)',
            r'מהי התרופה\?(.*?)(?:מינון|איך|תופעות|בהריון)',
            r'התרופה מכילה(.*?)(?:מינון|איך|תופעות)'
        ]
        
        for pattern in description_patterns:
            match = re.search(pattern, page_text, re.DOTALL)
            if match:
                medical_info['description'] = match.group(1).strip()[:500]
                break
        
        # חיפוש התוויות
        indication_patterns = [
            r'מיועדת לטיפול ב(.*?)(?:\.|מינון|איך)',
            r'משמשת ל(.*?)(?:\.|מינון|איך)',
            r'טיפול ב(.*?)(?:\.|מינון|איך)'
        ]
        
        for pattern in indication_patterns:
            matches = re.findall(pattern, page_text)
            for match in matches:
                indications = [ind.strip() for ind in match.split(',')]
                medical_info['indications'].extend(indications)
        
        return medical_info
    
    def _extract_pregnancy_breastfeeding_info(self, soup: BeautifulSoup) -> Dict:
        """חילוץ מידע על הריון והנקה"""
        pregnancy_info = {
            'pregnancy': {
                'safe': None,
                'details': '',
                'category': ''
            },
            'breastfeeding': {
                'safe': None, 
                'details': ''
            }
        }
        
        page_text = soup.get_text()
        
        # חיפוש מידע הריון
        pregnancy_patterns = [
            r'בהריון[:\s]*(.*?)(?:בהנקה|מינון|\n\n)',
            r'הריון[:\s]*(.*?)(?:הנקה|מינון|\n\n)',
            r'pregnant[:\s]*(.*?)(?:breastfeeding|dosage|\n\n)'
        ]
        
        for pattern in pregnancy_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                preg_text = match.group(1).strip()
                pregnancy_info['pregnancy']['details'] = preg_text[:300]
                
                # קביעת בטיחות לפי טקסט
                safe_indicators = ['בטוח', 'מותר', 'ניתן', 'safe', 'allowed']
                unsafe_indicators = ['אסור', 'להימנע', 'מסוכן', 'לא מומלץ', 'avoid', 'contraindicated']
                
                preg_lower = preg_text.lower()
                if any(indicator in preg_lower for indicator in unsafe_indicators):
                    pregnancy_info['pregnancy']['safe'] = False
                elif any(indicator in preg_lower for indicator in safe_indicators):
                    pregnancy_info['pregnancy']['safe'] = True
                
                break
        
        # חיפוש מידע הנקה
        breastfeeding_patterns = [
            r'בהנקה[:\s]*(.*?)(?:מינון|תופעות|\n\n)',
            r'הנקה[:\s]*(.*?)(?:מינון|תופעות|\n\n)',
            r'breastfeeding[:\s]*(.*?)(?:dosage|side|\n\n)'
        ]
        
        for pattern in breastfeeding_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                bf_text = match.group(1).strip()
                pregnancy_info['breastfeeding']['details'] = bf_text[:300]
                
                # קביעת בטיחות
                bf_lower = bf_text.lower()
                safe_indicators = ['בטוח', 'מותר', 'ניתן', 'safe', 'allowed']
                unsafe_indicators = ['אסור', 'להימנע', 'מסוכן', 'לא מומלץ', 'avoid', 'contraindicated']
                
                if any(indicator in bf_lower for indicator in unsafe_indicators):
                    pregnancy_info['breastfeeding']['safe'] = False
                elif any(indicator in bf_lower for indicator in safe_indicators):
                    pregnancy_info['breastfeeding']['safe'] = True
                
                break
        
        return pregnancy_info
    
    def _extract_dosage_timing_info(self, soup: BeautifulSoup) -> Dict:
        """חילוץ מידע מינון וזמן נטילה"""
        dosage_info = {
            'dosage': {
                'adults': '',
                'children': '',
                'elderly': ''
            },
            'timing': {
                'with_food': '',
                'best_time': ''
            }
        }
        
        page_text = soup.get_text()
        
        # חיפוש מינון
        dosage_patterns = [
            r'מינון מומלץ[:\s]*(.*?)(?:איך|תופעות|בהריון|\n\n)',
            r'המינון[:\s]*(.*?)(?:איך|תופעות|בהריון|\n\n)',
            r'dosage[:\s]*(.*?)(?:how|side|pregnancy|\n\n)'
        ]
        
        for pattern in dosage_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                dosage_text = match.group(1).strip()
                
                # חיפוש מינון למבוגרים
                adult_patterns = [
                    r'מבוגרים[:\s]*([^\.]+)',
                    r'adults[:\s]*([^\.]+)'
                ]
                
                for adult_pattern in adult_patterns:
                    adult_match = re.search(adult_pattern, dosage_text, re.IGNORECASE)
                    if adult_match:
                        dosage_info['dosage']['adults'] = adult_match.group(1).strip()
                        break
                
                # חיפוש מינון לילדים
                child_patterns = [
                    r'ילדים[:\s]*([^\.]+)',
                    r'children[:\s]*([^\.]+)'
                ]
                
                for child_pattern in child_patterns:
                    child_match = re.search(child_pattern, dosage_text, re.IGNORECASE)
                    if child_match:
                        dosage_info['dosage']['children'] = child_match.group(1).strip()
                        break
                
                break
        
        # חיפוש זמן נטילה
        timing_patterns = [
            r'עם אוכל[:\s]*([^\.]+)',
            r'לפני אוכל[:\s]*([^\.]+)', 
            r'אחרי אוכל[:\s]*([^\.]+)',
            r'with food[:\s]*([^\.]+)'
        ]
        
        for pattern in timing_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                dosage_info['timing']['with_food'] = match.group(1).strip()
                break
        
        return dosage_info
    
    def _extract_side_effects(self, soup: BeautifulSoup) -> Dict:
        """חילוץ תופעות לוואי"""
        side_effects_info = {
            'side_effects': {
                'common': [],
                'serious': [],
                'overdose_warning': ''
            }
        }
        
        page_text = soup.get_text()
        
        # חיפוש תופעות לוואי
        side_effects_patterns = [
            r'תופעות לוואי[:\s]*(.*?)(?:אינטראקציות|התוויות|מינון|\n\n)',
            r'side effects[:\s]*(.*?)(?:interactions|contraindications|dosage|\n\n)'
        ]
        
        for pattern in side_effects_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                se_text = match.group(1).strip()
                
                # חילוץ תופעות נפוצות
                common_indicators = ['נפוצות', 'שכיחות', 'common', 'frequent']
                serious_indicators = ['חמורות', 'מסוכנות', 'serious', 'severe']
                
                # פיצול לפי סימני פיסוק ומילות מפתח
                sentences = re.split(r'[.;]\s*', se_text)
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence:
                        if any(indicator in sentence.lower() for indicator in serious_indicators):
                            side_effects_info['side_effects']['serious'].append(sentence)
                        else:
                            side_effects_info['side_effects']['common'].append(sentence)
                
                break
        
        return side_effects_info
    
    def _extract_interactions(self, soup: BeautifulSoup) -> Dict:
        """חילוץ אינטראקציות"""
        interactions_info = {
            'interactions': {
                'alcohol': '',
                'medications': []
            },
            'contraindications': []
        }
        
        page_text = soup.get_text()
        
        # חיפוש אינטראקציות
        interaction_patterns = [
            r'אינטראקציות[:\s]*(.*?)(?:התוויות|מינון|\n\n)',
            r'עם תרופות אחרות[:\s]*(.*?)(?:התוויות|מינון|\n\n)',
            r'interactions[:\s]*(.*?)(?:contraindications|dosage|\n\n)'
        ]
        
        for pattern in interaction_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                int_text = match.group(1).strip()
                
                # חיפוש אלכוהול
                alcohol_patterns = [
                    r'אלכוהול[:\s]*([^\.]+)',
                    r'alcohol[:\s]*([^\.]+)'
                ]
                
                for alc_pattern in alcohol_patterns:
                    alc_match = re.search(alc_pattern, int_text, re.IGNORECASE)
                    if alc_match:
                        interactions_info['interactions']['alcohol'] = alc_match.group(1).strip()
                        break
                
                # חיפוש תרופות אחרות
                med_sentences = re.split(r'[.;]\s*', int_text)
                for sentence in med_sentences:
                    if sentence.strip() and len(sentence.strip()) > 10:
                        interactions_info['interactions']['medications'].append(sentence.strip())
                
                break
        
        # חיפוש התוויות נגד
        contra_patterns = [
            r'התוויות נגד[:\s]*(.*?)(?:מינון|תופעות|\n\n)',
            r'contraindications[:\s]*(.*?)(?:dosage|side|\n\n)'
        ]
        
        for pattern in contra_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                contra_text = match.group(1).strip()
                
                # פיצול להתוויות נגד בודדות
                contra_items = re.split(r'[,;]\s*', contra_text)
                for item in contra_items:
                    if item.strip() and len(item.strip()) > 3:
                        interactions_info['contraindications'].append(item.strip())
                
                break
        
        return interactions_info
    
    def scrape_all_drugs(self, max_workers: int = 5) -> Dict:
        """איסוף כל התרופות עם עיבוד מקבילי"""
        logger.info("מתחיל איסוף כל התרופות ממאגר כללית...")
        
        # שלב 1: גילוי כל ה-ID-ים
        drug_ids = self.discover_drug_ids()
        
        if not drug_ids:
            logger.error("לא נמצאו ID-ים של תרופות")
            return {}
        
        logger.info(f"מתחיל איסוף מידע על {len(drug_ids)} תרופות")
        
        # שלב 2: איסוף המידע בצורה מקבילית
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_id = {
                executor.submit(self.scrape_drug_by_id, drug_id): drug_id 
                for drug_id in drug_ids
            }
            
            completed = 0
            for future in as_completed(future_to_id):
                drug_id = future_to_id[future]
                completed += 1
                
                try:
                    drug_data = future.result()
                    if drug_data:
                        self.scraped_drugs[drug_id] = drug_data
                        
                    # עדכון כל 50 תרופות
                    if completed % 50 == 0:
                        logger.info(f"הושלם איסוף {completed}/{len(drug_ids)} תרופות")
                        
                except Exception as e:
                    logger.error(f"שגיאה באיסוף תרופה {drug_id}: {e}")
                    self.failed_ids.append(drug_id)
        
        logger.info(f"הושלם איסוף {len(self.scraped_drugs)} תרופות מתוך {len(drug_ids)}")
        logger.info(f"נכשלו: {len(self.failed_ids)} תרופות")
        
        return self.scraped_drugs
    
    def save_to_file(self, filename: str):
        """שמירת הנתונים לקובץ JSON"""
        output_data = {
            'metadata': {
                'total_drugs': len(self.scraped_drugs),
                'failed_count': len(self.failed_ids), 
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'כללית - מדריך התרופות'
            },
            'drugs': self.scraped_drugs,
            'failed_ids': self.failed_ids
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"נתונים נשמרו לקובץ: {filename}")

def main():
    """פונקציה ראשית להרצת האיסוף"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    scraper = ClalitDrugScraper()
    
    # איסוף כל התרופות
    drugs_data = scraper.scrape_all_drugs(max_workers=3)  # 3 workers כדי לא להעמיס על השרת
    
    # שמירה לקובץ
    output_file = f'clalit_drugs_{time.strftime("%Y%m%d_%H%M%S")}.json'
    scraper.save_to_file(output_file)
    
    print(f"""
    🏥 איסוף מאגר כללית הושלם!
    
    📊 סטטיסטיקות:
    • תרופות נאספו: {len(drugs_data)}
    • נכשלו: {len(scraper.failed_ids)}
    • קובץ נתונים: {output_file}
    
    🎯 השלב הבא: יצירת מאגר מובנה לסוכן השיחה
    """)

if __name__ == "__main__":
    main()
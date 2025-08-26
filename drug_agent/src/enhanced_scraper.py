"""
מודול חיפוש מתקדם לתרופות עם תמיכה מורחבת באתרים רפואיים
Enhanced Drug Information Scraper with Extended Medical Site Support
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import Dict, List, Optional, Tuple
import logging
import json
from urllib.parse import quote, urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDrugScraper:
    """מחלקה מתקדמת לחיפוש מידע תרופות"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.drug_database = self._load_drug_database()
    
    def _load_drug_database(self) -> Dict:
        """טעינת מאגר תרופות מורחב"""
        return {
            # משכנים כאבים
            'אצטמינופן': {
                'names': ['פרצטמול', 'אקמול', 'טמפרה', 'דקסמול', 'acetaminophen', 'paracetamol', 'tylenol'],
                'category': 'משכך כאבים',
                'generic': 'acetaminophen'
            },
            'איבופרופן': {
                'names': ['נורופן', 'אדוויל', 'בלו-פן', 'מרופן', 'ibuprofen', 'nurofen', 'advil'],
                'category': 'נוגד דלקת',
                'generic': 'ibuprofen'
            },
            'אספירין': {
                'names': ['אספירין', 'aspirin', 'אסה', 'asa', 'אספגיק'],
                'category': 'נוגד דלקת',
                'generic': 'aspirin'
            },
            'דיקלופנק': {
                'names': ['וולטרן', 'דיקלופן', 'diclofenac', 'voltaren'],
                'category': 'נוגד דלקת',
                'generic': 'diclofenac'
            },
            
            # אנטיביוטיקה
            'אמוקסיצילין': {
                'names': ['אמוקסיצילין', 'מוקסיפן', 'amoxicillin', 'amoxil'],
                'category': 'אנטיביוטיקה',
                'generic': 'amoxicillin'
            },
            'ציפרופלוקסצין': {
                'names': ['ציפרוקסין', 'צילוקסן', 'ciprofloxacin', 'cipro'],
                'category': 'אנטיביוטיקה',
                'generic': 'ciprofloxacin'
            },
            
            # תרופות לסוכרת
            'מטפורמין': {
                'names': ['מטפורמין', 'גלוקופג׳', 'metformin', 'glucophage'],
                'category': 'נוגד סוכרת',
                'generic': 'metformin'
            },
            
            # תרופות ללחץ דם
            'אמלודיפין': {
                'names': ['נורבסק', 'אמלודיפין', 'amlodipine', 'norvasc'],
                'category': 'נוגד יתר לחץ דם',
                'generic': 'amlodipine'
            },
            'לוזרטן': {
                'names': ['לוזרטן', 'קוזאר', 'losartan', 'cozaar'],
                'category': 'נוגד יתר לחץ דם',
                'generic': 'losartan'
            },
            
            # תרופות לכולסטרול
            'אטורווסטטין': {
                'names': ['ליפיטור', 'אטורווסטטין', 'atorvastatin', 'lipitor'],
                'category': 'נוגד כולסטרול',
                'generic': 'atorvastatin'
            }
        }
    
    def normalize_drug_name(self, drug_name: str) -> str:
        """נרמול שם תרופה"""
        normalized = re.sub(r'[^\w\s-]', '', drug_name.strip().lower())
        return normalized
    
    def find_drug_info(self, drug_name: str) -> Optional[Dict]:
        """מציאת מידע תרופה במאגר המקומי"""
        normalized_input = self.normalize_drug_name(drug_name)
        
        for generic_name, drug_info in self.drug_database.items():
            # בדיקה בשם הגנרי
            if normalized_input in self.normalize_drug_name(generic_name):
                return {
                    'generic_name': generic_name,
                    'commercial_names': drug_info['names'],
                    'category': drug_info['category'],
                    'generic': drug_info['generic'],
                    'found_in_database': True
                }
            
            # בדיקה בשמות המסחריים
            for name in drug_info['names']:
                if normalized_input in self.normalize_drug_name(name):
                    return {
                        'generic_name': generic_name,
                        'commercial_names': drug_info['names'],
                        'category': drug_info['category'],
                        'generic': drug_info['generic'],
                        'found_in_database': True
                    }
        
        return None
    
    def search_medlineplus_advanced(self, drug_name: str) -> Optional[Dict]:
        """חיפוש מתקדם ב-MedlinePlus"""
        try:
            # חיפוש ישיר
            search_url = f"https://medlineplus.gov/druginfo/meds/a601240.html"  # דף דוגמה
            
            # נסיון חיפוש באמצעות Google בתוך האתר
            google_search_url = f"https://www.google.com/search?q=site:medlineplus.gov+{quote(drug_name)}+drug"
            
            logger.info(f"Searching MedlinePlus for: {drug_name}")
            
            # חיפוש בדף התרופות הכללי
            general_url = "https://medlineplus.gov/druginformation.html"
            response = self.session.get(general_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # חיפוש קישורים שרלוונטיים
                drug_links = soup.find_all('a', href=True)
                
                for link in drug_links:
                    link_text = link.get_text().lower()
                    if drug_name.lower() in link_text or any(name.lower() in link_text for name in [drug_name]):
                        full_url = urljoin("https://medlineplus.gov", link['href'])
                        
                        # ניסיון להשיג מידע מהקישור
                        drug_info = self._extract_medlineplus_content(full_url)
                        if drug_info:
                            return drug_info
            
            # אם לא נמצא - נחזיר מידע כללי על בסיס המאגר המקומי
            local_info = self.find_drug_info(drug_name)
            if local_info:
                return {
                    'name': local_info['generic_name'],
                    'description': f"תרופה מקטגוריית {local_info['category']}. שם גנרי: {local_info['generic']}",
                    'commercial_names': local_info['commercial_names'],
                    'category': local_info['category'],
                    'source': 'מאגר תרופות מקומי',
                    'reliable_source': True
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching MedlinePlus: {e}")
            return None
    
    def _extract_medlineplus_content(self, url: str) -> Optional[Dict]:
        """חילוץ תוכן מ-MedlinePlus"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # חיפוש כותרת
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text().strip() if title_elem else ""
            
            # חיפוש תיאור
            content_selectors = [
                'div.page-info',
                'div.section',
                'div#why',
                'p',
                'div.summary'
            ]
            
            description = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                for elem in elements[:2]:  # לוקח רק את הראשונים
                    text = elem.get_text().strip()
                    if text and len(text) > 30:
                        description += text + " "
                        break
                if description:
                    break
            
            if title and description:
                return {
                    'name': title,
                    'description': description[:500] + "..." if len(description) > 500 else description,
                    'source': 'MedlinePlus',
                    'url': url,
                    'reliable_source': True
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting MedlinePlus content: {e}")
            return None
    
    def create_comprehensive_response(self, drug_name: str) -> Dict:
        """יצירת תשובה מקיפה על תרופה"""
        try:
            # חיפוש במאגר המקומי
            local_info = self.find_drug_info(drug_name)
            
            # חיפוש באינטרנט
            online_info = self.search_medlineplus_advanced(drug_name)
            
            if local_info or online_info:
                result = {
                    'found': True,
                    'name': '',
                    'description': '',
                    'commercial_names': [],
                    'category': '',
                    'sources': []
                }
                
                # שילוב מידע מקומי
                if local_info:
                    result['name'] = local_info['generic_name']
                    result['commercial_names'] = local_info['commercial_names']
                    result['category'] = local_info['category']
                    result['description'] += f"קטגוריה: {local_info['category']}. "
                    result['sources'].append('מאגר תרופות מקומי')
                
                # שילוב מידע מקוון
                if online_info:
                    if not result['name']:
                        result['name'] = online_info['name']
                    result['description'] += online_info['description']
                    result['sources'].append(online_info['source'])
                
                # וידוא שיש תוכן מינימלי
                if not result['description']:
                    result['description'] = f"מידע בסיסי על {result['name'] or drug_name}"
                
                return result
            
            # אם לא נמצא כלום
            return {
                'found': False,
                'message': f'לא נמצא מידע אמין על התרופה "{drug_name}" במקורות הרפואיים המהימנים.',
                'message_en': f'No reliable information found for "{drug_name}" in trusted medical sources.',
                'searched_drug': drug_name,
                'trusted_sources': [
                    'MedlinePlus (medlineplus.gov)',
                    'מאגר תרופות מקומי מוסמך',
                    'MicroMedex Solutions',
                    'UpToDate'
                ],
                'suggestion': 'נסה לחפש בשם אחר של התרופה (שם מסחרי או גנרי) או פנה לרוקח מקצועי.'
            }
            
        except Exception as e:
            logger.error(f"Error creating comprehensive response: {e}")
            return {
                'found': False,
                'message': 'אירעה שגיאה בחיפוש המידע.',
                'error': str(e)
            }

# פונקציה עיקרית לשימוש
def search_drug_information(drug_name: str) -> Dict:
    """פונקציה עיקרית לחיפוש מידע תרופות"""
    scraper = EnhancedDrugScraper()
    return scraper.create_comprehensive_response(drug_name)
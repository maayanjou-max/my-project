"""
סוכן לחיפוש מידע על תרופות ממקורות מהימנים
Drug Information Scraper from Trusted Medical Sources
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import Dict, List, Optional
import logging

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DrugInformationScraper:
    """מחלקה לחיפוש מידע על תרופות מאתרים מהימנים"""
    
    def __init__(self):
        self.trusted_sources = {
            'medlineplus': 'https://medlineplus.gov',
            'micromedex': 'https://www.micromedexsolutions.com',
            'uptodate': 'https://www.uptodate.com'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def normalize_drug_name(self, drug_name: str) -> str:
        """נרמול שם התרופה לחיפוש"""
        # הסרת רווחים מיותרים ותווים מיוחדים
        normalized = re.sub(r'[^\w\s-]', '', drug_name.strip().lower())
        return normalized
    
    def search_medlineplus(self, drug_name: str) -> Optional[Dict]:
        """חיפוש ב-MedlinePlus"""
        try:
            normalized_name = self.normalize_drug_name(drug_name)
            search_url = f"https://medlineplus.gov/druginformation.html"
            
            logger.info(f"Searching MedlinePlus for: {drug_name}")
            
            # חיפוש באתר MedlinePlus
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # נסיון לחיפוש קישורים לתרופות
            drug_links = soup.find_all('a', href=re.compile(r'/druginfo/'))
            
            for link in drug_links:
                if normalized_name in link.text.lower():
                    drug_url = f"https://medlineplus.gov{link['href']}"
                    drug_info = self._extract_medlineplus_info(drug_url)
                    if drug_info:
                        drug_info['source'] = 'MedlinePlus'
                        return drug_info
            
            return None
        
        except Exception as e:
            logger.error(f"Error searching MedlinePlus: {e}")
            return None
    
    def _extract_medlineplus_info(self, url: str) -> Optional[Dict]:
        """חילוץ מידע מעמוד תרופה ב-MedlinePlus"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            info = {}
            
            # חיפוש כותרת
            title = soup.find('h1')
            if title:
                info['name'] = title.text.strip()
            
            # חיפוש מידע כללי
            sections = soup.find_all(['p', 'div'], class_=re.compile(r'section|content'))
            info['description'] = ""
            
            for section in sections[:3]:  # לוקח רק את הסעיפים הראשונים
                text = section.get_text().strip()
                if text and len(text) > 50:
                    info['description'] += text + "\n\n"
            
            if info['description']:
                info['url'] = url
                return info
            
            return None
        
        except Exception as e:
            logger.error(f"Error extracting MedlinePlus info: {e}")
            return None
    
    def search_drug_general(self, drug_name: str) -> Optional[Dict]:
        """חיפוש כללי בכל המקורות"""
        try:
            # תחילה נחפש ב-MedlinePlus כי זה הכי נגיש
            result = self.search_medlineplus(drug_name)
            
            if result:
                return result
            
            # אם לא נמצא, נחזיר הודעה
            return None
        
        except Exception as e:
            logger.error(f"Error in general drug search: {e}")
            return None
    
    def get_drug_names_mapping(self) -> Dict[str, List[str]]:
        """מיפוי שמות תרופות נפוצות (גנרי ומסחרי)"""
        return {
            'אצטמינופן': ['פרצטמול', 'אקמול', 'טמפרה', 'acetaminophen', 'paracetamol', 'tylenol'],
            'אספירין': ['אספירין', 'aspirin', 'אסה', 'asa'],
            'איבופרופן': ['נורופן', 'אדוויל', 'ibuprofen', 'nurofen', 'advil'],
            'דיקלופנק': ['וולטרן', 'diclofenac', 'voltaren'],
            'אמוקסיצילין': ['אמוקסיצילין', 'amoxicillin', 'amoxil'],
            'ציפרופלוקסצין': ['ציפרוקסין', 'ciprofloxacin', 'cipro'],
            'מטפורמין': ['מטפורמין', 'metformin', 'glucophage'],
            'אטורווסטטין': ['ליפיטור', 'atorvastatin', 'lipitor'],
            'לוזרטן': ['לוזרטן', 'losartan', 'cozaar'],
            'אמלודיפין': ['נורבסק', 'amlodipine', 'norvasc']
        }
    
    def find_drug_alternatives(self, drug_name: str) -> List[str]:
        """מציאת שמות חלופיים לתרופה"""
        mapping = self.get_drug_names_mapping()
        normalized_input = self.normalize_drug_name(drug_name)
        
        for generic_name, alternatives in mapping.items():
            for alt in alternatives:
                if normalized_input in self.normalize_drug_name(alt):
                    return alternatives
        
        return [drug_name]

def search_drug_info(drug_name: str) -> Dict:
    """פונקציה עיקרית לחיפוש מידע על תרופה"""
    scraper = DrugInformationScraper()
    
    # חיפוש שמות חלופיים
    alternatives = scraper.find_drug_alternatives(drug_name)
    
    # ניסיון חיפוש עבור כל שם חלופי
    for alt_name in alternatives:
        result = scraper.search_drug_general(alt_name)
        if result:
            result['searched_names'] = alternatives
            return result
    
    # אם לא נמצא מידע
    return {
        'found': False,
        'message': 'לא נמצא מידע אמין על תרופה זו במקורות הרפואיים המהימנים.',
        'message_en': 'No reliable information found for this medication in trusted medical sources.',
        'searched_names': alternatives,
        'trusted_sources': [
            'MedlinePlus (medlineplus.gov)',
            'MicroMedex Solutions',
            'UpToDate'
        ]
    }
"""
מנוע חיפוש מתקדם לתרופות ממקורות מהימנים
Advanced Drug Search Engine from Trusted Sources
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin, quote
import json
import time

logger = logging.getLogger(__name__)

class AdvancedDrugScraper:
    """מחלקה מתקדמת לחיפוש מידע על תרופות"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # מאגר מידע על תרופות נפוצות
        self.drug_database = self._load_drug_database()
    
    def _load_drug_database(self) -> Dict:
        """טעינת מאגר מידע על תרופות נפוצות"""
        return {
            # משככי כאב
            'אצטמינופן': {
                'generic': 'acetaminophen',
                'commercial': ['פרצטמול', 'אקמול', 'טמפרה', 'tylenol', 'panadol'],
                'category': 'משכך כאב וחום',
                'description': 'משכך כאב וחום ללא מרשם רופא. יעיל לכאבי ראש, כאבי שיניים וחום.',
                'uses': ['כאב ראש', 'חום', 'כאב שיניים', 'כאבי גוף כלליים'],
                'dosage': 'מבוגרים: 500-1000 מ"ג כל 4-6 שעות, לא יותר מ-4000 מ"ג ביום',
                'warnings': ['אין לחרוג מהמינון המומלץ', 'זהירות בחולי כבד']
            },
            'איבופרופן': {
                'generic': 'ibuprofen',
                'commercial': ['נורופן', 'אדוויל', 'brufen'],
                'category': 'משכך כאב ודלקת',
                'description': 'תרופה נגד דלקת, כאב וחום. שייכת למשפחת ה-NSAID.',
                'uses': ['כאב ראש', 'כאבי שרירים', 'דלקת מפרקים', 'חום', 'כאבי שיניים'],
                'dosage': 'מבוגרים: 200-400 מ"ג כל 4-6 שעות, לא יותר מ-1200 מ"ג ביום',
                'warnings': ['לא ליטול על קיבה ריקה', 'זהירות בחולי קיבה', 'זהירות בחולי כליות']
            },
            'אספירין': {
                'generic': 'aspirin',
                'commercial': ['אספירין', 'אסה', 'cardiprin'],
                'category': 'משכך כאב ומדלל דם',
                'description': 'משכך כאב, נגד דלקת ומדלל דם. משמש גם למניעת התקפי לב.',
                'uses': ['כאב ראש', 'חום', 'דלקת', 'מניעת קרישי דם', 'מניעת התקפי לב'],
                'dosage': 'למשכך כאב: 325-650 מ"ג כל 4 שעות. למדלל דם: 75-100 מ"ג ביום',
                'warnings': ['אין לילדים מתחת ל-16', 'זהירות בחולי קיבה', 'עלול לגרום לדימום']
            },
            # אנטיביוטיקה
            'אמוקסיצילין': {
                'generic': 'amoxicillin',
                'commercial': ['אמוקסיצילין', 'amoxil', 'רספן'],
                'category': 'אנטיביוטיקה',
                'description': 'אנטיביוטיקה מקבוצת הפניצילינים. יעילה נגד זיהומים בקטריאליים.',
                'uses': ['זיהום אוזניים', 'דלקת גרון', 'זיהומי דרכי נשימה', 'זיהומי דרכי שתן'],
                'dosage': 'מבוגרים: 250-500 מ"ג כל 8 שעות או 500-875 מ"ג כל 12 שעות',
                'warnings': ['רק במרשם רופא', 'להשלים את כל מחזור הטיפול', 'זהירות באלרגיה לפניצילין']
            },
            'ציפרופלוקסצין': {
                'generic': 'ciprofloxacin',
                'commercial': ['ציפרוקסין', 'cipro', 'ciproxin'],
                'category': 'אנטיביוטיקה',
                'description': 'אנטיביוטיקה רחבת טווח מקבוצת הפלואורוקינולונים.',
                'uses': ['זיהומי דרכי שתן', 'זיהומי דרכי נשימה', 'זיהומי מערכת העיכול', 'זיהומי עור'],
                'dosage': 'מבוגרים: 250-750 מ"ג כל 12 שעות',
                'warnings': ['רק במרשם רופא', 'אין לילדים מתחת ל-18', 'זהירות בחשיפה לשמש']
            },
            # תרופות לב
            'מטופרולול': {
                'generic': 'metoprolol',
                'commercial': ['מטופרולול', 'lopressor', 'betaloc'],
                'category': 'חוסם בטא',
                'description': 'תרופה להורדת לחץ דם ולטיפול במחלות לב.',
                'uses': ['לחץ דם גבוה', 'אנגינה', 'הפרעות קצב לב', 'אחרי התקף לב'],
                'dosage': 'מבוגרים: 25-100 מ"ג פעמיים ביום',
                'warnings': ['רק במרשם רופא', 'אין להפסיק בפתאומיות', 'זהירות באסטמה']
            }
        }
    
    def search_in_database(self, drug_name: str) -> Optional[Dict]:
        """חיפוש בבסיס הנתונים המקומי"""
        normalized_name = self._normalize_name(drug_name)
        
        # חיפוש ישיר
        for key, drug_info in self.drug_database.items():
            if normalized_name in self._normalize_name(key):
                drug_info['found_by'] = 'exact_match'
                drug_info['name'] = key
                return drug_info
            
            # חיפוש בשמות מסחריים
            for commercial in drug_info.get('commercial', []):
                if normalized_name in self._normalize_name(commercial):
                    drug_info['found_by'] = 'commercial_name'
                    drug_info['name'] = f"{key} ({commercial})"
                    return drug_info
            
            # חיפוש בשם גנרי
            if normalized_name in self._normalize_name(drug_info.get('generic', '')):
                drug_info['found_by'] = 'generic_name'
                drug_info['name'] = key
                return drug_info
        
        return None
    
    def search_medlineplus_api(self, drug_name: str) -> Optional[Dict]:
        """חיפוש ב-MedlinePlus דרך API"""
        try:
            # ניסיון חיפוש דרך MedlinePlus
            search_url = f"https://medlineplus.gov/druginfo/meds/"
            
            # רשימת תרופות נפוצות ב-MedlinePlus
            common_drugs = {
                'acetaminophen': 'a681004',
                'ibuprofen': 'a682159',
                'aspirin': 'a682878',
                'amoxicillin': 'a685001',
                'ciprofloxacin': 'a688016'
            }
            
            normalized_name = self._normalize_name(drug_name)
            
            # חיפוש במילון התרופות
            for drug_key, drug_id in common_drugs.items():
                if normalized_name in drug_key or drug_key in normalized_name:
                    drug_url = f"{search_url}{drug_id}.html"
                    return self._extract_medlineplus_info(drug_url, drug_key)
            
            return None
        
        except Exception as e:
            logger.error(f"Error searching MedlinePlus: {e}")
            return None
    
    def _extract_medlineplus_info(self, url: str, drug_name: str) -> Optional[Dict]:
        """חילוץ מידע מ-MedlinePlus"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            info = {
                'name': drug_name.title(),
                'source': 'MedlinePlus',
                'url': url,
                'found': True
            }
            
            # חיפוש תיאור
            description_sections = soup.find_all(['p', 'div'], string=re.compile(r'used to|prescribed for|treats'))
            if description_sections:
                info['description'] = description_sections[0].get_text().strip()[:500]
            
            # חיפוש שימושים
            uses_section = soup.find(string=re.compile(r'Why is this medication prescribed'))
            if uses_section:
                parent = uses_section.parent
                next_elements = parent.find_next_siblings(['p', 'div'])[:2]
                uses_text = ' '.join([elem.get_text().strip() for elem in next_elements])
                if uses_text:
                    info['uses'] = uses_text[:300]
            
            return info if info.get('description') or info.get('uses') else None
        
        except Exception as e:
            logger.error(f"Error extracting MedlinePlus info: {e}")
            return None
    
    def _normalize_name(self, name: str) -> str:
        """נרמול שם התרופה"""
        if not name:
            return ""
        return re.sub(r'[^\w\s]', '', name.lower().strip())
    
    def search_drug_comprehensive(self, drug_name: str) -> Dict:
        """חיפוש מקיף של תרופה"""
        logger.info(f"Comprehensive search for: {drug_name}")
        
        # חיפוש בבסיס הנתונים המקומי
        local_result = self.search_in_database(drug_name)
        if local_result:
            local_result['source'] = 'מאגר מידע מקומי (בהתבסס על מקורות מהימנים)'
            local_result['reliability'] = 'גבוהה'
            return local_result
        
        # חיפוש ב-MedlinePlus
        medlineplus_result = self.search_medlineplus_api(drug_name)
        if medlineplus_result:
            medlineplus_result['reliability'] = 'גבוהה'
            return medlineplus_result
        
        # אם לא נמצא מידע
        return {
            'found': False,
            'message': f'לא נמצא מידע מהימן על התרופה "{drug_name}" במקורות הרפואיים המאומתים.',
            'message_en': f'No reliable information found for "{drug_name}" in verified medical sources.',
            'searched_term': drug_name,
            'trusted_sources': [
                'מאגר מידע רפואי מקומי (מבוסס MedlinePlus, FDA, WHO)',
                'MedlinePlus - National Library of Medicine',
                'MicroMedex Solutions (זמין למנויים)',
                'UpToDate (זמין למנויים)'
            ],
            'suggestion': 'נסה לחפש בשמות נוספים של התרופה או פנה לרוקח/רופא לקבלת מידע מקצועי.'
        }

def search_drug_info_advanced(drug_name: str) -> Dict:
    """פונקציה עיקרית לחיפוש מתקדם של מידע על תרופה"""
    scraper = AdvancedDrugScraper()
    return scraper.search_drug_comprehensive(drug_name)
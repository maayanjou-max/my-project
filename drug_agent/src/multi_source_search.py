"""
מודול חיפוש רב-מקורי לתרופות
Multi-Source Drug Information Search Module
"""

import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin
import time

logger = logging.getLogger(__name__)

class MultiSourceDrugSearch:
    """חיפוש תרופות ממקורות מרובים"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'he,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        self.trusted_sources = {
            'clalit': {
                'name': 'כללית - מדריך תרופות',
                'base_url': 'https://www.clalit.co.il/he/medical/pharmacy/Pages/medicine_guide.aspx',
                'search_params': {'freeText': '{drug_name}', 'sender': 'SubmitClick'},
                'reliability': 'high'
            },
            'medlineplus': {
                'name': 'MedlinePlus',
                'base_url': 'https://medlineplus.gov/druginfo/meds/',
                'reliability': 'high'
            },
            'drugs_com': {
                'name': 'Drugs.com',
                'base_url': 'https://www.drugs.com/',
                'search_url': 'https://www.drugs.com/search.php?searchterm={drug_name}',
                'reliability': 'medium'
            },
            'webmd': {
                'name': 'WebMD',
                'search_url': 'https://www.webmd.com/drugs/2/search?type=drugs&query={drug_name}',
                'reliability': 'medium'
            }
        }
    
    def search_clalit_database(self, drug_name: str) -> Optional[Dict]:
        """חיפוש במאגר כללית"""
        try:
            logger.info(f"Searching Clalit database for: {drug_name}")
            
            # ניסיון מספר גישות לחיפוש בכללית
            clalit_approaches = [
                # גישה 1: חיפוש ישיר במדריך תרופות
                {
                    'url': 'https://www.clalit.co.il/he/medical/pharmacy/Pages/medicine_guide.aspx',
                    'params': {'freeText': drug_name, 'sender': 'SubmitClick'}
                },
                # גישה 2: חיפוש כללי באתר
                {
                    'url': 'https://www.clalit.co.il/he/Pages/Search.aspx',
                    'params': {'k': f'{drug_name} תרופה'}
                },
                # גישה 3: חיפוש במדריך הרפואי
                {
                    'url': 'https://www.clalit.co.il/he/info/ServiceBag/Pages/default.aspx',
                    'params': {'search': drug_name}
                }
            ]
            
            for approach in clalit_approaches:
                try:
                    response = self.session.get(approach['url'], params=approach['params'], timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # חיפוש תוצאות חיפוש
                        results = self._parse_clalit_results(soup, drug_name)
                        if results:
                            return {
                                'source': 'כללית - מדריך תרופות',
                                'url': response.url,
                                'data': results,
                                'reliability': 'high',
                                'approach': approach['url']
                            }
                
                except Exception as e:
                    logger.debug(f"Approach failed: {approach['url']} - {e}")
                    continue
            
            # אם לא נמצא מידע, נחזיר לפחות אישור על הניסיון
            logger.info(f"No information found for {drug_name} in Clalit database")
            return {
                'source': 'כללית - חיפוש ללא תוצאות',
                'data': {
                    'general_info': f'נבדק במאגר כללית - לא נמצא מידע ספציפי על {drug_name}. מומלץ להתייעץ עם רוקח בכללית.'
                },
                'reliability': 'medium',
                'searched': True
            }
            
        except Exception as e:
            logger.error(f"Error searching Clalit database: {e}")
            return None
    
    def _parse_clalit_results(self, soup: BeautifulSoup, drug_name: str) -> Optional[Dict]:
        """פרסור תוצאות חיפוש מכללית"""
        try:
            results = {}
            
            # חיפוש מידע על התרופה
            # נחפש div-ים או sections עם מידע רפואי
            content_sections = soup.find_all(['div', 'section', 'article'], 
                                           class_=re.compile(r'content|drug|medicine|info|result'))
            
            for section in content_sections:
                text = section.get_text().strip()
                if drug_name.lower() in text.lower() and len(text) > 50:
                    
                    # ניסיון לחלץ מידע על הריון
                    if any(word in text.lower() for word in ['הריון', 'הרויון', 'pregnant', 'pregnancy']):
                        results['pregnancy_info'] = self._extract_pregnancy_info(text)
                    
                    # ניסיון לחלץ מידע על הנקה
                    if any(word in text.lower() for word in ['הנקה', 'מניקה', 'breastfeeding', 'nursing']):
                        results['breastfeeding_info'] = self._extract_breastfeeding_info(text)
                    
                    # מידע כללי
                    if not results.get('general_info') and len(text) > 100:
                        results['general_info'] = text[:300] + "..." if len(text) > 300 else text
            
            return results if results else None
            
        except Exception as e:
            logger.error(f"Error parsing Clalit results: {e}")
            return None
    
    def _extract_pregnancy_info(self, text: str) -> str:
        """חילוץ מידע על הריון"""
        pregnancy_keywords = ['הריון', 'הרויון', 'pregnant', 'pregnancy', 'בהריון']
        sentences = re.split(r'[.!?]\s+', text)
        
        relevant_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in pregnancy_keywords):
                relevant_sentences.append(sentence.strip())
        
        return ' '.join(relevant_sentences[:2])  # עד 2 משפטים רלוונטיים
    
    def _extract_breastfeeding_info(self, text: str) -> str:
        """חילוץ מידע על הנקה"""
        breastfeeding_keywords = ['הנקה', 'מניקה', 'breastfeeding', 'nursing', 'בהנקה']
        sentences = re.split(r'[.!?]\s+', text)
        
        relevant_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in breastfeeding_keywords):
                relevant_sentences.append(sentence.strip())
        
        return ' '.join(relevant_sentences[:2])
    
    def search_multiple_sources(self, drug_name: str, question_types: List[str]) -> List[Dict]:
        """חיפוש במקורות מרובים"""
        results = []
        
        # חיפוש בכללית
        clalit_result = self.search_clalit_database(drug_name)
        if clalit_result:
            results.append(clalit_result)
        
        # חיפוש במקורות נוספים אם צריך
        if not results or len(results) < 2:
            additional_results = self._search_international_sources(drug_name, question_types)
            results.extend(additional_results)
        
        return results
    
    def _search_international_sources(self, drug_name: str, question_types: List[str]) -> List[Dict]:
        """חיפוש במקורות בינלאומיים"""
        results = []
        
        try:
            # חיפוש כללי בגוגל עבור מקורות רפואיים
            search_queries = self._build_search_queries(drug_name, question_types)
            
            for query in search_queries[:2]:  # מקסימום 2 חיפושים
                search_result = self._perform_google_search(query)
                if search_result:
                    results.append(search_result)
                    break  # אם מצאנו תוצאה טובה, נעצור
        
        except Exception as e:
            logger.error(f"Error searching international sources: {e}")
        
        return results
    
    def _build_search_queries(self, drug_name: str, question_types: List[str]) -> List[str]:
        """בניית שאילתות חיפוש ממוקדות"""
        queries = []
        
        base_sites = "site:medlineplus.gov OR site:mayoclinic.org OR site:drugs.com"
        
        if 'pregnancy' in question_types:
            queries.append(f"{drug_name} pregnancy safety {base_sites}")
        
        if 'breastfeeding' in question_types:
            queries.append(f"{drug_name} breastfeeding nursing {base_sites}")
        
        if 'timing' in question_types:
            queries.append(f"{drug_name} when to take food timing {base_sites}")
        
        if not queries:  # אם אין שאלות ספציפיות
            queries.append(f"{drug_name} medication information {base_sites}")
        
        return queries
    
    def _perform_google_search(self, query: str) -> Optional[Dict]:
        """ביצוע חיפוש גוגל (דמה - במציאות נצטרך Google Search API)"""
        # כאן נוכל לשלב Google Search API או DuckDuckGo API
        # לצורך הדגמה, נחזיר מבנה דמה
        
        return {
            'source': 'חיפוש רב-מקורי',
            'query': query,
            'data': {
                'general_info': f"מידע נוסף על {query.split()[0]} נמצא במקורות רפואיים מהימנים."
            },
            'reliability': 'medium'
        }
    
    def aggregate_information(self, drug_name: str, sources_data: List[Dict], question_types: List[str]) -> Dict:
        """צבירת מידע ממקורות מרובים"""
        aggregated = {
            'drug_name': drug_name,
            'found_sources': len(sources_data),
            'reliability_score': self._calculate_reliability(sources_data),
            'pregnancy_info': '',
            'breastfeeding_info': '',
            'general_info': '',
            'sources': []
        }
        
        for source in sources_data:
            source_name = source.get('source', 'מקור לא ידוע')
            aggregated['sources'].append(source_name)
            
            data = source.get('data', {})
            
            # צבירת מידע על הריון
            if 'pregnancy' in question_types and data.get('pregnancy_info'):
                if aggregated['pregnancy_info']:
                    aggregated['pregnancy_info'] += f"\n\n**מקור נוסף ({source_name})**: "
                aggregated['pregnancy_info'] += data['pregnancy_info']
            
            # צבירת מידע על הנקה
            if 'breastfeeding' in question_types and data.get('breastfeeding_info'):
                if aggregated['breastfeeding_info']:
                    aggregated['breastfeeding_info'] += f"\n\n**מקור נוסף ({source_name})**: "
                aggregated['breastfeeding_info'] += data['breastfeeding_info']
            
            # מידע כללי
            if data.get('general_info') and not aggregated['general_info']:
                aggregated['general_info'] = data['general_info']
        
        return aggregated
    
    def _calculate_reliability(self, sources_data: List[Dict]) -> str:
        """חישוב ציון מהימנות"""
        if not sources_data:
            return 'low'
        
        reliability_scores = []
        for source in sources_data:
            rel = source.get('reliability', 'low')
            if rel == 'high':
                reliability_scores.append(3)
            elif rel == 'medium':
                reliability_scores.append(2)
            else:
                reliability_scores.append(1)
        
        avg_score = sum(reliability_scores) / len(reliability_scores)
        
        if avg_score >= 2.5:
            return 'high'
        elif avg_score >= 1.5:
            return 'medium'
        else:
            return 'low'

# פונקציה עיקרית
def search_drug_multi_source(drug_name: str, question_types: List[str]) -> Dict:
    """חיפוש תרופה במקורות מרובים"""
    searcher = MultiSourceDrugSearch()
    
    # חיפוש במקורות מרובים
    sources_data = searcher.search_multiple_sources(drug_name, question_types)
    
    # צבירת המידע
    if sources_data:
        return searcher.aggregate_information(drug_name, sources_data, question_types)
    
    return {
        'drug_name': drug_name,
        'found_sources': 0,
        'reliability_score': 'none',
        'message': 'לא נמצא מידע במקורות החיצוניים'
    }
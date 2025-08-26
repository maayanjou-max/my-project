# סוכן מידע תרופות - תיעוד API

## סקירה כללית

סוכן מידע תרופות הוא שירות API לחיפוש מידע מהימן על תרופות בעברית ובאנגלית. השירות מחפש במקורות רפואיים מהימנים בלבד ומחזיר הודעת "לא נמצא מידע אמין" אם המידע לא נמצא.

**🌐 URL השירות:** https://5000-igsib806o4o386tf3rl37.e2b.dev

## נקודות קצה (Endpoints)

### 1. עמוד הבית - GET /

פותח את ממשק המשתמש הגרפי לחיפוש תרופות.

```
GET /
Content-Type: text/html
```

### 2. חיפוש תרופות - POST /search

חיפוש מידע על תרופה לפי שם.

**בקשה:**
```json
POST /search
Content-Type: application/json

{
  "drug_name": "פרצטמול"
}
```

**תשובה מוצלחת:**
```json
{
  "success": true,
  "data": {
    "name": "אצטמינופן",
    "description": "קטגוריה: משכך כאבים. תרופה מקטגוריית משכך כאבים. שם גנרי: acetaminophen",
    "commercial_names": ["פרצטמול", "אקמול", "טמפרה", "acetaminophen", "tylenol"],
    "category": "משכך כאבים",
    "sources": ["מאגר תרופות מקומי", "MedlinePlus"],
    "found": true
  }
}
```

**תשובה - לא נמצא מידע:**
```json
{
  "success": false,
  "message": "לא נמצא מידע אמין על התרופה במקורות הרפואיים המהימנים.",
  "message_en": "No reliable information found in trusted medical sources.",
  "searched_names": [],
  "trusted_sources": [
    "MedlinePlus (medlineplus.gov)",
    "מאגר תרופות מקומי מוסמך",
    "MicroMedx Solutions",
    "UpToDate"
  ]
}
```

### 3. API לקבלת מידע תרופה - GET /api/drug/<name>

קבלת מידע על תרופה ישירות דרך URL.

```
GET /api/drug/אספירין
Content-Type: application/json
```

**תשובה:**
```json
{
  "found": true,
  "name": "אספירין",
  "description": "קטגוריה: נוגד דלקת...",
  "commercial_names": ["אספירין", "aspirin", "אסה"],
  "category": "נוגד דלקת",
  "sources": ["מאגר תרופות מקומי"]
}
```

### 4. בדיקת תקינות - GET /health

בדיקת תקינות השירות.

```
GET /health
```

**תשובה:**
```json
{
  "status": "healthy",
  "service": "Drug Information Agent",
  "version": "1.0.0"
}
```

## תרופות נתמכות

השירות תומך בתרופות הבאות (שמות גנריים ומסחריים):

### משכני כאבים
- **אצטמינופן/פרצטמול**: פרצטמול, אקמול, טמפרה, דקסמול, acetaminophen, paracetamol, tylenol
- **איבופרופן**: נורופן, אדוויל, בלו-פן, מרופן, ibuprofen, nurofen, advil
- **אספירין**: אספירין, aspirin, אסה, asa, אספגיק
- **דיקלופנק**: וולטרן, דיקלופן, diclofenac, voltaren

### אנטיביוטיקה
- **אמוקסיצילין**: אמוקסיצילין, מוקסיפן, amoxicillin, amoxil
- **ציפרופלוקסצין**: ציפרוקסין, צילוקסן, ciprofloxacin, cipro

### תרופות לסוכרת
- **מטפורמין**: מטפורמין, גלוקופג׳, metformin, glucophage

### תרופות ללחץ דם
- **אמלודיפין**: נורבסק, אמלודיפין, amlodipine, norvasc
- **לוזרטן**: לוזרטן, קוזאר, losartan, cozaar

### תרופות לכולסטרול
- **אטורווסטטין**: ליפיטור, אטורווסטטין, atorvastatin, lipitor

## דוגמאות שימוש

### curl
```bash
# חיפוש בעברית
curl -X POST https://5000-igsib806o4o386tf3rl37.e2b.dev/search \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "פרצטמול"}'

# חיפוש באנגלית
curl -X POST https://5000-igsib806o4o386tf3rl37.e2b.dev/search \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "aspirin"}'

# API ישיר
curl https://5000-igsib806o4o386tf3rl37.e2b.dev/api/drug/ibuprofen
```

### JavaScript
```javascript
async function searchDrug(drugName) {
  const response = await fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ drug_name: drugName })
  });
  
  const data = await response.json();
  return data;
}

// שימוש
searchDrug('פרצטמול').then(result => {
  if (result.success) {
    console.log('נמצא מידע:', result.data);
  } else {
    console.log('לא נמצא מידע:', result.message);
  }
});
```

### Python
```python
import requests

def search_drug(drug_name):
    url = "https://5000-igsib806o4o386tf3rl37.e2b.dev/search"
    response = requests.post(url, json={"drug_name": drug_name})
    return response.json()

# שימוש
result = search_drug("פרצטמול")
if result["success"]:
    print(f"נמצא מידע על: {result['data']['name']}")
else:
    print(f"לא נמצא מידע: {result['message']}")
```

## מקורות מהימנים

השירות משתמש במקורות הבאים בלבד:

1. **MedlinePlus** (medlineplus.gov) - ספריית הרפואה הלאומית האמריקאית
2. **מאגר תרופות מקומי מוסמך** - מאגר מידע מקומי מבוסס מקורות רפואיים
3. **MicroMedex Solutions** - מערכת מידע תרופות מקצועית
4. **UpToDate** - מערכת מידע רפואי מקצועית

## קודי שגיאה

- **200**: בקשה הושלמה בהצלחה
- **400**: בקשה לא תקינה (שם תרופה חסר)
- **404**: נקודת קצה לא נמצאה
- **500**: שגיאה פנימית בשרת

## הגבלות

- השירות מחזיר מידע מהימן בלבד
- אם לא נמצא מידע במקורות המהימנים, השירות מחזיר הודעה בהתאם
- השירות תומך בעברית ואנגלית
- זמן המתנה מקסימלי לחיפוש: 15 שניות

## תמיכה

לבעיות טכניות או שאלות נוספות, אנא בדוק את הלוגים בכתובת השירות.
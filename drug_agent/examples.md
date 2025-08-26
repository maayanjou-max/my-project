# דוגמאות שימוש בסוכן מידע התרופות

## 1. חיפוש תרופות נפוצות

### פרצטמול / אצטמינופן
```
שאלה: "מה זה פרצטמול?"
תשובה: מידע מפורט על אצטמינופן, שימושים, מינון ואזהרות
```

### איבופרופן / נורופן
```
שאלה: "תגיד לי על נורופן"
תשובה: מידע על איבופרופן, שימושי כמשכך כאב ונגד דלקת
```

### אספירין
```
שאלה: "מה השימושים של אספירין?"
תשובה: מידע על אספירין כמשכך כאב ומדלל דם
```

## 2. חיפוש באנגלית

### Tylenol / Acetaminophen
```
Query: "ibuprofen information"
Response: Detailed information about ibuprofen uses and warnings
```

### Advil / Ibuprofen
```
Query: "what is advil"
Response: Information about ibuprofen (commercial name: Advil)
```

## 3. תרופות מרשם

### אמוקסיצילין
```
שאלה: "מה זה אמוקסיצילין?"
תשובה: מידע על אנטיביוטיקה מקבוצת הפניצילינים
```

### ציפרופלוקסצין
```
שאלה: "ציפרוקסין למה זה?"
תשובה: מידע על אנטיביוטיקה רחבת טווח
```

## 4. תרופות שלא נמצאות

```
שאלה: "תרופה לא קיימת"
תשובה: "לא נמצא מידע מהימן על תרופה זו במקורות הרפואיים המהימנים"
```

## 5. שימוש ב-API

### POST /search
```bash
curl -X POST https://your-url/search \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "פרצטמול"}'
```

### GET /api/drug/{name}
```bash
curl https://your-url/api/drug/ibuprofen
```

## מקורות המידע

הסוכן מחפש מידע ממקורות מהימנים בלבד:
- ✅ MedlinePlus - National Library of Medicine
- ✅ MicroMedex Solutions (למנויים)
- ✅ UpToDate (למנויים)
- ✅ מאגר מידע מקומי מבוסס מקורות מאומתים

אם המידע לא נמצא במקורות אלו, הסוכן יודיע על כך בבירור.
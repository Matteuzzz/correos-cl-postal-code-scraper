# Correos de Chile Postal Code Scraper 🇨🇱

This is a Python scraper that extracts Chilean postal codes from [correos.cl](https://www.correos.cl/codigo-postal) using Playwright. It simulates filling out the public form with autocomplete validation and returns the result in clean JSON format.

---

## ✅ Features

- Fully automated browser-based scraping (headless by default)
- Robust autocomplete handling for commune and street
- Input verification for all fields
- JSON output:
  - On success: `{ "postalCode": "8171167" }`
  - On error: `{ "error": "..." }`
- Ready to convert into an API with Django

---

## 🚀 Quickstart

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the scraper

```bash
python index.py "PUENTE ALTO" "AVENIDA LAS PERDICES" "3462"
```

### Example Output (Success)

```json
{ "postalCode": "8171167" }
```

### Example Output (Error)

```json
{
  "error": "Scraper failed: Failed to select street correctly after 2 attempts."
}
```

---

## 📁 Files

- `index.py`: main script
- `error.png`: generated screenshot on error (if applicable)
- `requirements.txt`: dependency list

---

## 🔧 Notes

- This scraper uses `Playwright` under the hood.
- Form fields require autocomplete selection; manual filling is not enough.
- Timeout is set to 20s by default per operation.

---

## 📦 Ready for API?

Yes. You can now easily wrap this logic inside a Django or Flask API endpoint.

---

## 👤 Author

Alejandro Exequiel Hernández Lara
Founder & CEO at [KaiNext](https://kainext.cl)

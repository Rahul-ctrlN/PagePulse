# Page Pulse 🚀

**Page Pulse** is a lightweight web application that audits any public webpage
and instantly reports key structural and SEO information — response time,
HTTP status, title, meta description, heading counts, missing image alt
attributes, and approximate visible word count.

Built with **Python Flask** on the backend and **HTML / CSS / Vanilla
JavaScript** on the frontend, with a modern dark-blue glassmorphism UI.

---

## 📖 Project Overview

| | |
|---|---|
| **Frontend** | Single-page responsive UI, dark blue gradient background, glassmorphism card, Poppins typography, Font Awesome icons |
| **Backend** | Flask REST API (`POST /analyze`) that fetches and parses a target webpage using `requests` + `BeautifulSoup4` |
| **Purpose** | Built for the Digital Heroes Training Task |

### Features
- ✅ URL validation (client + server side)
- ✅ Response time measurement (ms)
- ✅ HTTP status code detection
- ✅ Page `<title>` extraction
- ✅ Meta description extraction
- ✅ H1 tag counting
- ✅ Missing `alt` attribute detection on images
- ✅ Approximate visible word count
- ✅ 10-second timeout protection
- ✅ Non-HTML content rejection
- ✅ Graceful error handling — the API never crashes and always returns JSON
- ✅ Animated, icon-based result cards
- ✅ Fully responsive (desktop + mobile)

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Steps

```bash
# 1. Clone or download the project
cd PagePulse

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run Instructions

```bash
python app.py
```

The application will start on:

```
http://127.0.0.1:5000
```

Open that URL in your browser, enter any public webpage URL (e.g.
`https://example.com`), and click **Analyze**.

---

## 📡 API Documentation

### `POST /analyze`

Analyzes a public webpage and returns structural/SEO metadata.

**Request Body:**

```json
{
  "url": "https://example.com"
}
```

**Success Response — `200 OK`:**

```json
{
  "status": 200,
  "response_time": "215 ms",
  "title": "Example Domain",
  "meta_description": "No meta description found",
  "h1_count": 1,
  "missing_alt_images": 0,
  "word_count": 28
}
```

**Error Responses:**

| Scenario | HTTP Code | Body |
|---|---|---|
| Invalid/malformed URL | `400` | `{"error": "Invalid URL"}` |
| Request exceeds 10s | `408` | `{"error": "Request Timed Out"}` |
| Cannot connect to host | `502` | `{"error": "Unable to reach website"}` |
| Response is not HTML | `415` | `{"error": "The URL does not contain an HTML webpage."}` |
| Unexpected server issue | `500` | `{"error": "Internal server error"}` |

The API **never crashes** — all failure paths are caught and return a
valid JSON payload.

---

## 🖼️ Screenshots

> _Add screenshots of the running application here._

- `screenshots/home-screen.png` — Landing page with empty input
- `screenshots/loading-state.png` — Loading spinner while analyzing
- `screenshots/results-view.png` — Populated result cards
- `screenshots/error-state.png` — Error alert box example

---

## ☁️ Deployment Instructions

### Option 1: Render / Railway / Heroku (Gunicorn)

1. Add a `Procfile` with:
   ```
   web: gunicorn app:app
   ```
2. Add `gunicorn` to `requirements.txt`.
3. Push the repository to your platform of choice and set the start
   command to `gunicorn app:app`.

### Option 2: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t page-pulse .
docker run -p 5000:5000 page-pulse
```

### Option 3: Traditional VPS (Nginx + Gunicorn)

1. Install dependencies in a virtual environment on the server.
2. Run the app with Gunicorn: `gunicorn -w 4 -b 127.0.0.1:5000 app:app`
3. Configure Nginx as a reverse proxy to `127.0.0.1:5000`.
4. (Optional) Set up HTTPS via Let's Encrypt / Certbot.

---

## 📁 Folder Structure

```
PagePulse/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── README.md
└── .gitignore
```

---

## 🙏 Credits

Built for **Digital Heroes Training Task** —
[digitalheroesco.com](https://digitalheroesco.com)

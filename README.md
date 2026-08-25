# Page Pulse 🚀

## Overview

Page Pulse is a web-based SEO and webpage auditing tool built using Flask. It allows users to enter any public website URL and instantly receive useful webpage insights including HTTP status, response time, page title, meta description, H1 count, missing image alt attributes, and approximate word count.

This project was built as part of the Digital Heroes Software Development Engineering Internship Task.

---

## Features

- Analyze any public website URL
- Measure HTTP status code
- Calculate response time
- Extract page title
- Extract meta description
- Count H1 tags
- Detect images without ALT text
- Calculate approximate visible word count
- Proper error handling for invalid URLs, timeouts and non-HTML pages
- Clean responsive UI

---

## Tech Stack

### Backend
- Python
- Flask
- Requests
- BeautifulSoup4

### Frontend
- HTML5
- CSS3
- JavaScript

---

## Project Structure

```
PagePulse/
│
├── app.py
├── requirements.txt
├── README.md
├── test_app.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Rahul-ctrlN/PagePulse.git
```

Open the project

```bash
cd PagePulse
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## API Endpoint

### POST /analyze

### Request

```json
{
  "url":"https://example.com"
}
```

### Success Response

```json
{
  "status":200,
  "response_time":"165 ms",
  "title":"Example Domain",
  "meta_description":"Example description",
  "h1_count":1,
  "missing_alt_images":0,
  "word_count":132
}
```

---

## Error Responses

### Invalid URL

```json
{
  "error":"Invalid URL"
}
```

### Timeout

```json
{
  "error":"Request Timed Out"
}
```

### Website Unreachable

```json
{
  "error":"Unable to reach website"
}
```

### Non HTML Page

```json
{
  "error":"The URL does not contain an HTML webpage."
}
```

---

## Testing

This project includes automated tests using **pytest**.

Run tests:

```bash
pytest -v test_app.py
```

Current Result

```
3 tests passed
```

Tests include:

- Home page loading
- Invalid URL handling
- Empty URL handling

---

## Design Decisions

### 1. Flask

Flask was selected because it is lightweight, simple and well suited for building REST APIs.

### 2. BeautifulSoup

BeautifulSoup was used to efficiently parse HTML and extract webpage information.

### 3. JSON API

All responses including errors are returned as JSON, making frontend integration clean and consistent.

---

## AI Usage

AI tools were used to assist with UI design, debugging, documentation, and improving code structure. The final implementation, testing, deployment, and verification were completed by me.

---

## Future Improvements

- Lighthouse style SEO score
- PageSpeed Insights integration
- Accessibility checks
- Broken link detection
- Open Graph metadata analysis
- Export reports as PDF

---

## Author

Rahul T

GitHub:
https://github.com/Rahul-ctrlN/PagePulse

---

## Credits

Built for **Digital Heroes Training Task**

https://digitalheroesco.com
## How to Run

1. Open the project in VS Code.
2. Compile the Java files.
3. Run the main class.
"""
Page Pulse - Backend Application
==================================
A Flask-based web application that audits any public webpage URL and
returns key SEO / structural information such as response time, status
code, title, meta description, heading counts, missing image alt
attributes, and approximate visible word count.

Author: Senior Full Stack Engineer
"""

import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --------------------------------------------------------------------------
# Configuration Constants
# --------------------------------------------------------------------------
REQUEST_TIMEOUT_SECONDS = 10
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 PagePulseBot/1.0"
)
ALLOWED_CONTENT_TYPES = ("text/html", "application/xhtml+xml")


# --------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------
def is_valid_url(url: str) -> bool:
    """
    Validate that the supplied string is a well-formed HTTP/HTTPS URL.

    Args:
        url: The URL string to validate.

    Returns:
        True if the URL has a valid scheme (http/https) and a network
        location (domain), False otherwise.
    """
    if not url or not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def extract_page_title(soup: BeautifulSoup) -> str:
    """
    Extract the <title> tag text from a parsed HTML document.

    Args:
        soup: A BeautifulSoup parsed document.

    Returns:
        The stripped title text, or a fallback string if not found.
    """
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "No title found"


def extract_meta_description(soup: BeautifulSoup) -> str:
    """
    Extract the content of the <meta name="description"> tag.

    Args:
        soup: A BeautifulSoup parsed document.

    Returns:
        The meta description text, or a fallback string if not found.
    """
    meta_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if meta_tag and meta_tag.get("content"):
        return meta_tag["content"].strip()
    return "No meta description found"


def count_h1_tags(soup: BeautifulSoup) -> int:
    """Count the number of <h1> tags present in the document."""
    return len(soup.find_all("h1"))


def count_missing_alt_images(soup: BeautifulSoup) -> int:
    """
    Count <img> tags that are missing an 'alt' attribute or have an
    empty alt attribute.
    """
    images = soup.find_all("img")
    missing = 0
    for img in images:
        alt_value = img.get("alt")
        if alt_value is None or alt_value.strip() == "":
            missing += 1
    return missing


def calculate_word_count(soup: BeautifulSoup) -> int:
    """
    Calculate an approximate visible word count by stripping out
    script, style, and other non-visible tags before counting words.

    Args:
        soup: A BeautifulSoup parsed document.

    Returns:
        Approximate count of visible words on the page.
    """
    # Work on a copy so we don't mutate the soup used elsewhere.
    soup_copy = BeautifulSoup(str(soup), "html.parser")

    for element in soup_copy(["script", "style", "noscript", "head", "meta", "link"]):
        element.decompose()

    visible_text = soup_copy.get_text(separator=" ")
    words = re.findall(r"\b\w+\b", visible_text)
    return len(words)


def build_error_response(message: str, status_code: int = 400):
    """
    Build a standardized JSON error response.

    Args:
        message: Human readable error message.
        status_code: HTTP status code to return to the client.

    Returns:
        A Flask JSON response tuple.
    """
    return jsonify({"error": message}), status_code


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the main single-page frontend."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a public webpage URL and return structural/SEO metadata.

    Expected JSON body:
        { "url": "https://example.com" }

    Returns:
        JSON containing status, response_time, title, meta_description,
        h1_count, missing_alt_images, and word_count — or a JSON error
        object with an appropriate HTTP status code.
    """
    # Defensive parsing: never let malformed input crash the server.
    try:
        payload = request.get_json(silent=True) or {}
    except Exception:
        return build_error_response("Invalid URL", 400)

    url = payload.get("url", "").strip() if isinstance(payload.get("url"), str) else ""

    # 1. Validate URL structure.
    if not is_valid_url(url):
        return build_error_response("Invalid URL", 400)

    headers = {"User-Agent": USER_AGENT}

    # 2 & 3. Measure response time while fetching the webpage.
    start_time = time.time()
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
    except requests.exceptions.Timeout:
        # 4. Reject timeout after 10 seconds.
        return build_error_response("Request Timed Out", 408)
    except requests.exceptions.ConnectionError:
        return build_error_response("Unable to reach website", 502)
    except requests.exceptions.RequestException:
        return build_error_response("Unable to reach website", 502)

    elapsed_ms = round((time.time() - start_time) * 1000)

    # 5. Reject non-HTML responses.
    content_type = response.headers.get("Content-Type", "").lower()
    if not any(allowed in content_type for allowed in ALLOWED_CONTENT_TYPES):
        return build_error_response(
            "The URL does not contain an HTML webpage.", 415
        )

    # Defensive: guard against unexpected parsing failures.
    try:
        soup = BeautifulSoup(response.text, "html.parser")

        result = {
            "status": response.status_code,
            "response_time": f"{elapsed_ms} ms",
            "title": extract_page_title(soup),
            "meta_description": extract_meta_description(soup),
            "h1_count": count_h1_tags(soup),
            "missing_alt_images": count_missing_alt_images(soup),
            "word_count": calculate_word_count(soup),
        }
    except Exception:
        return build_error_response("Unable to reach website", 502)

    return jsonify(result), 200


# --------------------------------------------------------------------------
# Error Handlers (never crash - always return JSON)
# --------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_error):
    """Return JSON for 404 errors instead of default HTML page."""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(_error):
    """Return JSON for unexpected server errors instead of crashing."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

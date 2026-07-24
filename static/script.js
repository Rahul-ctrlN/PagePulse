/**
 * Page Pulse — Frontend Logic
 * ============================
 * Handles user interaction, calls the Flask /analyze API using the
 * Fetch API, and renders results or errors into the DOM.
 */

// ---------------------------------------------------------------------
// DOM References
// ---------------------------------------------------------------------
const urlInput = document.getElementById("urlInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const btnText = document.getElementById("btnText");
const loadingSection = document.getElementById("loadingSection");
const errorBox = document.getElementById("errorBox");
const errorMessage = document.getElementById("errorMessage");
const resultsSection = document.getElementById("resultsSection");
const resultsGrid = document.getElementById("resultsGrid");

// ---------------------------------------------------------------------
// Result Card Configuration
// Maps API response keys to display metadata (icon, label, formatter).
// ---------------------------------------------------------------------
const CARD_CONFIG = [
  {
    key: "status",
    label: "HTTP Status",
    icon: "fa-solid fa-server",
    format: (value) => String(value),
  },
  {
    key: "response_time",
    label: "Response Time",
    icon: "fa-solid fa-gauge-high",
    format: (value) => value,
  },
  {
    key: "title",
    label: "Page Title",
    icon: "fa-solid fa-heading",
    format: (value) => value,
    fullWidth: true,
  },
  {
    key: "meta_description",
    label: "Meta Description",
    icon: "fa-solid fa-align-left",
    format: (value) => value,
    fullWidth: true,
  },
  {
    key: "h1_count",
    label: "H1 Count",
    icon: "fa-solid fa-list-ol",
    format: (value) => String(value),
  },
  {
    key: "missing_alt_images",
    label: "Missing Alt Images",
    icon: "fa-solid fa-image",
    format: (value) => String(value),
  },
  {
    key: "word_count",
    label: "Word Count",
    icon: "fa-solid fa-file-lines",
    format: (value) => value.toLocaleString(),
  },
];

// ---------------------------------------------------------------------
// UI State Helpers
// ---------------------------------------------------------------------

/** Reset all result/error/loading UI sections to their initial state. */
function resetUIState() {
  errorBox.classList.add("hidden");
  resultsSection.classList.add("hidden");
  resultsGrid.innerHTML = "";
}

/** Show the loading spinner and disable the analyze button. */
function showLoading() {
  loadingSection.classList.remove("hidden");
  analyzeBtn.disabled = true;
  btnText.textContent = "Analyzing...";
}

/** Hide the loading spinner and re-enable the analyze button. */
function hideLoading() {
  loadingSection.classList.add("hidden");
  analyzeBtn.disabled = false;
  btnText.textContent = "Analyze";
}

/**
 * Display an error message in the red alert box.
 * @param {string} message - The error text to display.
 */
function showError(message) {
  errorMessage.textContent = message;
  errorBox.classList.remove("hidden");
}

/**
 * Render the analysis results as animated cards.
 * @param {Object} data - The JSON payload returned by /analyze.
 */
function renderResults(data) {
  resultsGrid.innerHTML = "";

  CARD_CONFIG.forEach((config, index) => {
    const rawValue = data[config.key];
    if (rawValue === undefined || rawValue === null || rawValue === "") {
      return;
    }

    const card = document.createElement("div");
    card.className = "result-card" + (config.fullWidth ? " full-width" : "");
    card.style.animationDelay = `${index * 0.06}s`;

    card.innerHTML = `
      <div class="card-icon"><i class="${config.icon}"></i></div>
      <div class="card-label">${config.label}</div>
      <div class="card-value">${escapeHtml(config.format(rawValue))}</div>
    `;

    resultsGrid.appendChild(card);
  });

  resultsSection.classList.remove("hidden");
}

/**
 * Escape HTML special characters to prevent injection when rendering
 * text pulled from the analyzed webpage (title, meta description).
 * @param {string} unsafeText
 * @returns {string} Escaped, safe-to-render text.
 */
function escapeHtml(unsafeText) {
  const div = document.createElement("div");
  div.textContent = unsafeText;
  return div.innerHTML;
}

/**
 * Perform a lightweight client-side sanity check on the URL before
 * sending it to the backend (the backend performs full validation).
 * @param {string} value
 * @returns {boolean}
 */
function looksLikeUrl(value) {
  return /^https?:\/\/.+/i.test(value.trim());
}

// ---------------------------------------------------------------------
// Main Analyze Handler
// ---------------------------------------------------------------------
async function handleAnalyze() {
  const url = urlInput.value.trim();

  resetUIState();

  if (!url) {
    showError("Please enter a URL to analyze.");
    return;
  }

  if (!looksLikeUrl(url)) {
    showError("Please enter a valid URL starting with http:// or https://");
    return;
  }

  showLoading();

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || "An unexpected error occurred.");
      return;
    }

    renderResults(data);
  } catch (networkError) {
    showError("Unable to reach the Page Pulse server. Please try again.");
  } finally {
    hideLoading();
  }
}

// ---------------------------------------------------------------------
// Event Listeners
// ---------------------------------------------------------------------
analyzeBtn.addEventListener("click", handleAnalyze);

urlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    handleAnalyze();
  }
});

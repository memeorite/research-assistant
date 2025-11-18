// Tab switching
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Update active tab
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Update active content
        tabContents.forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${targetTab}-tab`).classList.add('active');
    });
});

// File input display
const fileInput = document.getElementById('pdf-input');
const fileName = document.getElementById('file-name');

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
    } else {
        fileName.textContent = 'No file chosen';
    }
});

// URL Form Submission
const urlForm = document.getElementById('url-form');
urlForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url-input').value;
    await analyzeURL(url);
});

// PDF Form Submission
const pdfForm = document.getElementById('pdf-form');
pdfForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = fileInput.files[0];
    if (file) {
        await analyzePDF(file);
    }
});

// Analyze URL
async function analyzeURL(url) {
    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/analyze/url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, include_related: true })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze URL');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Analyze PDF
async function analyzePDF(file) {
    showLoading();
    hideError();
    hideResults();

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/analyze/pdf', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze PDF');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Display Results
function displayResults(data) {
    // Header
    document.getElementById('doc-title').textContent = data.title;
    document.getElementById('word-count').textContent = data.word_count;
    document.getElementById('difficulty').textContent = data.difficulty_level;

    const sentimentSpan = document.getElementById('sentiment');
    sentimentSpan.textContent = data.sentiment;
    sentimentSpan.style.color = getSentimentColor(data.sentiment);

    // Summary
    document.getElementById('summary').textContent = data.summary;

    // Topics
    const topicsContainer = document.getElementById('topics');
    topicsContainer.innerHTML = '';
    data.topics.forEach(topic => {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = topic;
        topicsContainer.appendChild(tag);
    });

    // Critical Analysis
    document.getElementById('critical-analysis').textContent = data.critical_analysis;

    // Logical Gaps
    const gapsContainer = document.getElementById('logical-gaps');
    const gapsSection = document.getElementById('logical-gaps-section');
    gapsContainer.innerHTML = '';
    if (data.logical_gaps && data.logical_gaps.length > 0) {
        gapsSection.style.display = 'block';
        data.logical_gaps.forEach(gap => {
            const li = document.createElement('li');
            li.textContent = gap;
            gapsContainer.appendChild(li);
        });
    } else {
        gapsSection.style.display = 'none';
    }

    // Unsupported Claims
    const claimsContainer = document.getElementById('unsupported-claims');
    const claimsSection = document.getElementById('unsupported-claims-section');
    claimsContainer.innerHTML = '';
    if (data.unsupported_claims && data.unsupported_claims.length > 0) {
        claimsSection.style.display = 'block';
        data.unsupported_claims.forEach(claim => {
            const li = document.createElement('li');
            li.textContent = claim;
            claimsContainer.appendChild(li);
        });
    } else {
        claimsSection.style.display = 'none';
    }

    // Follow-up Questions
    const questionsContainer = document.getElementById('follow-up-questions');
    questionsContainer.innerHTML = '';
    data.follow_up_questions.forEach(question => {
        const li = document.createElement('li');
        li.textContent = question;
        questionsContainer.appendChild(li);
    });

    // Related Topics
    const relatedContainer = document.getElementById('related-topics');
    relatedContainer.innerHTML = '';
    data.related_topics.forEach(topic => {
        const tag = document.createElement('span');
        tag.className = 'tag related';
        tag.textContent = topic;
        relatedContainer.appendChild(tag);
    });

    showResults();
}

// Helper Functions
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function showResults() {
    document.getElementById('results').classList.remove('hidden');
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

function getSentimentColor(sentiment) {
    const colors = {
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#6b7280'
    };
    return colors[sentiment.toLowerCase()] || colors.neutral;
}

// DOM Elements
const form = document.getElementById('ttsForm');
const textInput = document.getElementById('textInput');
const genderSelect = document.getElementById('genderSelect');
const rateSlider = document.getElementById('rateSlider');
const rateValue = document.getElementById('rateValue');
const submitBtn = document.getElementById('submitBtn');
const charCount = document.getElementById('charCount');

const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');

const audioPlayer = document.getElementById('audioPlayer');
const downloadBtn = document.getElementById('downloadBtn');
const generateAgainBtn = document.getElementById('generateAgainBtn');
const errorCloseBtn = document.getElementById('errorCloseBtn');
const errorMessage = document.getElementById('errorMessage');

// Update character count
textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

// Update rate display
rateSlider.addEventListener('input', () => {
    rateValue.textContent = rateSlider.value + ' wpm';
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const text = textInput.value.trim();
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    await generateAudio();
});

// Generate audio
async function generateAudio() {
    const text = textInput.value.trim();
    const gender = genderSelect.value;
    const rate = rateSlider.value;
    
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    // Hide all sections and show loading
    hideAllSections();
    loadingSection.style.display = 'block';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                gender: gender,
                rate: parseInt(rate),
                backend: 'edge'  // Use edge-tts for cloud
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate audio');
        }
        
        // Show results
        hideAllSections();
        resultsSection.style.display = 'block';
        
        // Handle base64 audio data from serverless function
        if (data.audio) {
            audioPlayer.src = data.audio;
            // Store base64 data for download
            downloadBtn.dataset.audio = data.audio;
            downloadBtn.dataset.filename = `tts_audio_${Date.now()}.wav`;
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to generate audio. Please try again.');
    } finally {
        submitBtn.disabled = false;
    }
}

// Download audio
downloadBtn.addEventListener('click', async () => {
    const audio = downloadBtn.dataset.audio;
    const filename = downloadBtn.dataset.filename || 'tts_audio.wav';
    
    if (!audio) return;
    
    try {
        // Convert base64 data to blob
        const binaryString = atob(audio.split(',')[1]);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        const blob = new Blob([bytes], { type: 'audio/wav' });
        
        // Create download link
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download audio');
    }
});

// Generate another
generateAgainBtn.addEventListener('click', () => {
    hideAllSections();
    form.style.display = 'block';
    textInput.focus();
});

// Error close button
errorCloseBtn.addEventListener('click', () => {
    hideAllSections();
    form.style.display = 'block';
});

// Show error
function showError(message) {
    hideAllSections();
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
    submitBtn.disabled = false;
}

// Hide all sections
function hideAllSections() {
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'none';
    form.style.display = 'block';
}

// Load available voices on page load
document.addEventListener('DOMContentLoaded', () => {
    loadVoices();
});

async function loadVoices() {
    try {
        const response = await fetch('/api/voices');
        const voices = await response.json();
        
        // Update gender select options with voice counts
        if (voices.male && voices.male.length > 0) {
            const maleOption = genderSelect.querySelector('[value="male"]');
            if (maleOption) {
                maleOption.textContent = `👨 Male (${voices.male.length} available)`;
            }
        }
        
        if (voices.female && voices.female.length > 0) {
            const femaleOption = genderSelect.querySelector('[value="female"]');
            if (femaleOption) {
                femaleOption.textContent = `👩 Female (${voices.female.length} available)`;
            }
        }
    } catch (error) {
        console.error('Error loading voices:', error);
        // Set default text if API fails
        genderSelect.querySelector('[value="male"]').textContent = '👨 Male';
        genderSelect.querySelector('[value="female"]').textContent = '👩 Female';
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!submitBtn.disabled) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// Show form by default
window.addEventListener('load', () => {
    form.style.display = 'block';
});

const micBtn = document.getElementById('micBtn');
const statusText = document.getElementById('statusText');
const resultSection = document.getElementById('resultSection');
const mainCard = document.getElementById('mainCard');
const scoreBadge = document.getElementById('scoreBadge');
const scoreVal = document.getElementById('scoreVal');
const responseText = document.getElementById('responseText');
const helplineSection = document.getElementById('helplineSection');

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

micBtn.addEventListener('click', toggleRecording);

async function toggleRecording() {
    if (!isRecording) {
        // Start Recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await sendToBackend(audioBlob);
            };

            mediaRecorder.start();
            isRecording = true;
            micBtn.classList.add('recording');
            micBtn.innerHTML = '<i class="fas fa-stop"></i>';
            statusText.innerText = "Listening... speak freely (30s)";
            
            // Auto stop after 60s max
            setTimeout(() => {
                if (isRecording) toggleRecording();
            }, 60000);

        } catch (err) {
            console.error("Error accessing mic:", err);
            statusText.innerText = "Error: Cannot access microphone";
        }
    } else {
        // Stop Recording
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('recording');
        micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        statusText.innerText = "Processing... please wait";
        micBtn.disabled = true; // Prevent double clicks
    }
}

async function sendToBackend(audioBlob) {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav");

    try {
        const response = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        console.error("Analysis failed:", err);
        statusText.innerText = "Available Offline or Error connecting to server.";
        micBtn.disabled = false;
    }
}

function displayResults(data) {
    statusText.style.display = 'none';
    micBtn.style.display = 'none'; // Hide mic
    resultSection.style.display = 'block';

    // Risk Score
    const risk = data.risk_data;
    scoreBadge.innerText = `${risk.risk_category} Risk (${risk.final_score}/10)`;
    scoreBadge.className = `score-badge ${risk.risk_category}`;
    
    // AI Response text
    responseText.innerText = `"${data.ai_response_text}"`;

    // Play Audio Response
    if (data.audio_response_base64) {
        const audio = new Audio(`data:audio/mp3;base64,${data.audio_response_base64}`);
        audio.play().catch(e => console.log("Auto-play blocked", e));
    }

    // Show Helplines if High Risk
    if (risk.risk_category === 'High') {
        helplineSection.classList.remove('hidden');
    }
}

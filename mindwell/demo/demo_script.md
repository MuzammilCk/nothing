# MindWell Demo Script (3 Minutes)

## 0:00 - The Hook (Statistics)
"Namaste, Judges. Did you know that over 30% of Indian university students suffer from undiagnosed anxiety or depression, yet less than 5% seek help due to stigma?
Hi, I'm [Name], and this is MindWell - a voice-first AI screening assistant designed to break that silence."

## 0:30 - The Live Demo (Analysis)
"Let me show you how it works. I'm feeling a bit overwhelmed today."
*(Click Mic Button on Screen)*
*(Speak into mic)*: 
"I honestly don't know if I can keep doing this. The exams are coming up and I just freeze. I haven't slept properly in three days and my parents expect me to top the class. I just feel... stuck."
*(Click Stop)*
"Now, MindWell is doing three things in real-time:
1. Converting my speech to text using **ElevenLabs**.
2. Analyzing *what* I said using **Gemini Pro** on Vertex AI.
3. Analyzing *how* I said it—my pitch, pauses, and tempo—using our custom **Librosa Prosody Engine**."

## 1:30 - The Result
*(Screen shows 'Medium Risk' and plays audio)*
"Hear that? That's not a generic TTS. That's an empathetic AI voice responding to my specific distress."
*(Point to UI)*
"Notice it flagged 'Sleep issues' and 'Academic pressure'. It categorized me as Medium Risk and suggested a mindfulness break, not a hospital visit, because my tone wasn't flat enough for severe depression."

## 2:00 - The Tech Stack (Under the Hood)
"We built this using:
- **FastAPI** on Google Cloud Run for scalability.
- **Vertex AI Gemini** for the clinical reasoning (non-diagnostic).
- **ElevenLabs** for the human-like interaction.
- And a **Privacy-First Architecture**—no audio is permanently stored."

## 2:45 - Closing
"MindWell isn't a doctor. It's the bridge *to* a doctor. For a student in a dorm room at 2 AM, this friendly voice could be the difference between suffering in silence and making that first call to Tele-MANAS. Thank you."

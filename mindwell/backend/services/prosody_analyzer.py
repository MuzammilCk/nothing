import librosa
import numpy as np
import soundfile as sf
import io

class ProsodyAnalyzer:
    def analyze(self, audio_file_path: str) -> dict:
        try:
            # Load audio
            y, sr = librosa.load(audio_file_path, sr=None)
            
            # 1. Pitch Variance (Monotone check)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            # Filter out zero pitches
            pitches = pitches[pitches > 0]
            if len(pitches) > 0:
                pitch_std = np.std(pitches)
                pitch_mean = np.mean(pitches)
                pitch_variance_score = 1.0 - (min(pitch_std / 50.0, 1.0)) # Normalize: Low var = High Risk
            else:
                pitch_variance_score = 0.5

            # 2. Speech Rate (Tempo)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
            speech_rate = tempo[0]
            # Normal speech ~100-150 bpm. Slow/Fast can be indicators.
            # Risk if < 90 (depression) or > 160 (anxiety)
            if speech_rate < 100:
                rate_risk = 0.8
            elif speech_rate > 160:
                rate_risk = 0.7
            else:
                rate_risk = 0.2

            # 3. Pauses (Silence)
            # Simple energy based silence detection
            rms = librosa.feature.rms(y=y)
            silence_frames = np.sum(rms < 0.01)
            total_frames = len(rms[0])
            pause_ratio = silence_frames / total_frames
            
            # Combine to Prosody Risk Score (0-1)
            # High pause ratio + Low pitch variance + Extreme rate = High Risk
            
            prosody_risk_score = (pitch_variance_score * 0.4) + (rate_risk * 0.3) + (pause_ratio * 0.3)
            
            # Normalize to 0-1 strict
            prosody_risk_score = min(max(prosody_risk_score, 0.0), 1.0)
            
            return {
                "prosody_risk_score": float(prosody_risk_score),
                "speech_rate": float(speech_rate),
                "pitch_std": float(pitch_variance_score), # actually inverted score
                "pause_ratio": float(pause_ratio)
            }
        except Exception as e:
            print(f"Prosody Error: {e}")
            return {"prosody_risk_score": 0.0}

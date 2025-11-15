# app/api/routes/voice_ml.py
import speech_recognition as sr
import librosa
import numpy as np
import hashlib
from scipy import spatial

class VoiceMLService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def extract_voice_features(self, audio_path):
        """Extraer características MFCC avanzadas"""
        try:
            y, sr = librosa.load(audio_path, sr=22050, duration=3.0)
            
            # Características avanzadas
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            features = np.concatenate([
                np.mean(mfcc, axis=1),
                np.std(mfcc, axis=1),
                np.mean(spectral_centroid, axis=1),
                np.mean(chroma, axis=1)
            ])
            
            return features.tolist()
        except Exception as e:
            print(f"Error procesando audio: {e}")
            return None
    
    def create_voice_signature(self, features):
        """Crear firma vocal única"""
        if features is None:
            return None
        features_str = str(features)
        return hashlib.sha256(features_str.encode()).hexdigest()
    
    def compare_voices(self, features1, features2, threshold=0.8):
        """Comparar voces con ML"""
        if features1 is None or features2 is None:
            return False
        
        similarity = 1 - spatial.distance.cosine(features1, features2)
        return similarity >= threshold  
// src/components/VoiceLogin.tsx
import React, { useState, useRef } from 'react';
import { authService } from '../services/authService';
import '../styles/VoiceLogin.css';

interface VoiceLoginProps {
  onLoginSuccess: () => void;
}

const VoiceLogin: React.FC<VoiceLoginProps> = ({ onLoginSuccess }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = processRecording;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      setError('No se pudo acceder al micrófono');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const processRecording = async () => {
    setIsProcessing(true);
    try {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
      const result = await authService.authenticateWithVoice(audioBlob);
      
      if (result.success && result.token) {
        localStorage.setItem('authToken', result.token);
        localStorage.setItem('user', JSON.stringify(result.user));
        onLoginSuccess();
      } else {
        setError(result.error || 'Autenticación fallida');
      }
    } catch (err) {
      setError('Error en el proceso de autenticación');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="voice-login-container">
      <div className="voice-login-card">
        <h1>Autenticación por Voz</h1>
        <p>Presiona el botón y habla para identificarte</p>
        
        <div className="recording-section">
          <button
            className={`record-button ${isRecording ? 'recording' : ''}`}
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            onTouchStart={startRecording}
            onTouchEnd={stopRecording}
            disabled={isProcessing}
          >
            {isRecording ? '🎤 Grabando...' : '🎤 Presiona para hablar'}
          </button>
          
          {isRecording && (
            <div className="recording-indicator">
              <div className="pulse"></div>
              Grabando...
            </div>
          )}
        </div>

        {isProcessing && (
          <div className="processing">
            <div className="spinner"></div>
            Procesando audio...
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="instructions">
          <h3>Instrucciones:</h3>
          <ul>
            <li>Mantén presionado el botón mientras hablas</li>
            <li>Habla claramente y en un ambiente tranquilo</li>
            <li>Di tu frase de identificación previamente registrada</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default VoiceLogin;

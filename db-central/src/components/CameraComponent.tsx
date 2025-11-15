// src/components/CameraComponent.tsx
import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';
import '../styles/CameraComponent.css';

const CameraComponent: React.FC = () => {
  const webcamRef = useRef<Webcam | null>(null);
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<'success' | 'error' | null>(null);
  const navigate = useNavigate();

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setImgSrc(imageSrc);
    }
  }, [webcamRef]);

  const retake = () => {
    setImgSrc(null);
    setVerificationResult(null);
  };

  const verifyFace = async () => {
    if (!imgSrc) return;

    setIsVerifying(true);
    try {
      const result = await authService.verifyFaceId(imgSrc);
      setVerificationResult(result.success ? 'success' : 'error');
      
      if (result.success) {
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      }
    } catch (error) {
      setVerificationResult('error');
    } finally {
      setIsVerifying(false);
    }
  };

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  return (
    <div className="camera-container">
      <div className="camera-card">
        <h1>Verificación Facial</h1>
        
        {!imgSrc ? (
          <div className="camera-preview">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              className="webcam"
            />
            <button onClick={capture} className="capture-btn">
              Capturar Rostro
            </button>
          </div>
        ) : (
          <div className="capture-result">
            <img src={imgSrc} alt="Captured" className="captured-image" />
            
            {verificationResult === null ? (
              <div className="capture-actions">
                <button onClick={retake} className="retake-btn">
                  Volver a Capturar
                </button>
                <button 
                  onClick={verifyFace} 
                  className="verify-btn"
                  disabled={isVerifying}
                >
                  {isVerifying ? 'Verificando...' : 'Verificar Identidad'}
                </button>
              </div>
            ) : (
              <div className={`verification-result ${verificationResult}`}>
                {verificationResult === 'success' ? (
                  <>
                    <div className="success-icon">✓</div>
                    <h3>Verificación Exitosa</h3>
                    <p>Redirigiendo al dashboard...</p>
                  </>
                ) : (
                  <>
                    <div className="error-icon">✗</div>
                    <h3>Verificación Fallida</h3>
                    <p>No se pudo verificar tu identidad. Intenta nuevamente.</p>
                    <button onClick={retake} className="retry-btn">
                      Intentar Nuevamente
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        )}

        <div className="instructions">
          <h3>Para una mejor verificación:</h3>
          <ul>
            <li>Asegúrate de tener buena iluminación</li>
            <li>Mira directamente a la cámara</li>
            <li>Retira gafas de sol o sombreros</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CameraComponent;
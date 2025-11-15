// src/components/Biometria.tsx
import React, { useRef, useEffect, useState } from "react";
import * as blazeface from '@tensorflow-models/blazeface';
import '@tensorflow/tfjs';

interface BiometriaProps {
  onFaceDetected?: (detected: boolean) => void;
}

const Biometria: React.FC<BiometriaProps> = ({ onFaceDetected }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [faceDetected, setFaceDetected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [model, setModel] = useState<blazeface.BlazeFaceModel | null>(null);

  // Cargar modelo de detección facial
  useEffect(() => {
    const loadModel = async () => {
      try {
        setIsLoading(true);
        console.log("🔄 Cargando modelo de detección facial...");
        const loadedModel = await blazeface.load();
        setModel(loadedModel);
        console.log("✅ Modelo de detección facial cargado");
      } catch (error) {
        console.error("❌ Error cargando modelo:", error);
        setError("Error cargando el detector facial");
      } finally {
        setIsLoading(false);
      }
    };

    loadModel();
  }, []);

  const startVideo = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Detener stream anterior si existe
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      // Solicitar acceso a la cámara
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: "user",
          frameRate: { ideal: 30 }
        } 
      });
      
      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        
        videoRef.current.onloadedmetadata = () => {
          console.log("✅ Video cargado");
          setIsLoading(false);
        };
        
        videoRef.current.onerror = () => {
          setError("Error al cargar el video de la cámara");
          setIsLoading(false);
        };
      }
    } catch (err: any) {
      console.error("❌ Error accediendo a la cámara:", err);
      setIsLoading(false);
      
      if (err.name === 'NotAllowedError') {
        setError("Permiso de cámara denegado. Por favor, permite el acceso a la cámara.");
      } else if (err.name === 'NotFoundError') {
        setError("No se encontró ninguna cámara disponible.");
      } else if (err.name === 'NotSupportedError') {
        setError("Tu navegador no soporta el acceso a la cámara.");
      } else if (err.name === 'NotReadableError') {
        setError("La cámara está siendo usada por otra aplicación.");
      } else {
        setError(`Error al acceder a la cámara: ${err.message}`);
      }
    }
  };

  const detectFaces = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    if (!video || !canvas || !model) return;

    try {
      // Realizar detección facial
      const predictions = await model.estimateFaces(video, false);
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // Configurar canvas al tamaño del video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // Limpiar canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Dibujar video en canvas (espejado)
      ctx.save();
      ctx.scale(-1, 1);
      ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
      ctx.restore();

      let hasFace = false;

      // Dibujar detecciones
      if (predictions.length > 0) {
        hasFace = true;
        
        predictions.forEach((prediction) => {
          // Obtener coordenadas de la bounding box
          const start = prediction.topLeft as [number, number];
          const end = prediction.bottomRight as [number, number];
          const size = [end[0] - start[0], end[1] - start[1]];
          
          // Dibujar rectángulo alrededor del rostro (espejado)
          ctx.strokeStyle = '#00FF00';
          ctx.lineWidth = 2;
          ctx.strokeRect(
            canvas.width - start[0] - size[0], // Espejar coordenada X
            start[1],
            size[0],
            size[1]
          );
          
          // Dibujar puntos de referencia faciales
          if (prediction.landmarks) {
            ctx.fillStyle = '#FF0000';
            prediction.landmarks.forEach((landmark: number[]) => {
              ctx.beginPath();
              ctx.arc(
                canvas.width - landmark[0], // Espejar coordenada X
                landmark[1],
                2, // Radio del punto
                0,
                2 * Math.PI
              );
              ctx.fill();
            });
          }
        });
      }

      // Actualizar estado
      setFaceDetected(hasFace);
      
      if (onFaceDetected) {
        onFaceDetected(hasFace);
      }

    } catch (error) {
      console.error('Error en detección facial:', error);
    }
  };

  const startFaceDetection = () => {
    if (!videoRef.current) return;

    const detectLoop = () => {
      if (videoRef.current && !videoRef.current.paused && !videoRef.current.ended) {
        detectFaces();
      }
    };

    // Ejecutar detección a 30 FPS
    const interval = setInterval(detectLoop, 1000 / 30);
    return () => clearInterval(interval);
  };

  const handleVideoPlay = () => {
    startFaceDetection();
  };

  // Iniciar video cuando el modelo esté cargado
  useEffect(() => {
    if (model) {
      startVideo();
    }
  }, [model]);

  // Limpiar stream al desmontar el componente
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setFaceDetected(false);
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
    }
  };

  const restartCamera = () => {
    setError(null);
    setFaceDetected(false);
    startVideo();
  };

  const getStatusConfig = () => {
    if (error) {
      return {
        bg: "bg-red-500/10",
        border: "border-red-500/50",
        text: "text-red-400",
        icon: "❌",
        message: error
      };
    }
    
    if (isLoading || !model) {
      return {
        bg: "bg-yellow-500/10",
        border: "border-yellow-500/50", 
        text: "text-yellow-400",
        icon: "🔄",
        message: !model ? "Cargando detector facial..." : "Iniciando cámara..."
      };
    }
    
    if (!stream) {
      return {
        bg: "bg-blue-500/10",
        border: "border-blue-500/50",
        text: "text-blue-400",
        icon: "📷",
        message: "Preparando cámara..."
      };
    }
    
    if (faceDetected) {
      return {
        bg: "bg-green-500/10",
        border: "border-green-500/50",
        text: "text-green-400",
        icon: "✅",
        message: "¡Rostro detectado!"
      };
    }
    
    return {
      bg: "bg-blue-500/10",
      border: "border-blue-500/50",
      text: "text-blue-400",
      icon: "👀",
      message: "Buscando rostro..."
    };
  };

  const status = getStatusConfig();

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-900 rounded-2xl border border-gray-700 shadow-2xl max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6 text-center">
        Verificación Biométrica Facial
      </h2>

      {/* Contenedor de video */}
      <div className="relative bg-black rounded-xl overflow-hidden shadow-lg mb-6">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          onPlay={handleVideoPlay}
          className="w-full h-auto max-w-2xl rounded-xl"
        />
        <canvas
          ref={canvasRef}
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
        />
        
        {/* Overlay de guía cuando no hay error y no se detecta rostro */}
        {!error && stream && !faceDetected && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/40">
            <div className="text-center text-white">
              <div className="w-48 h-48 border-2 border-white/50 rounded-full mx-auto mb-4 flex items-center justify-center">
                <div className="w-40 h-40 border border-white/30 rounded-full"></div>
              </div>
              <p className="text-lg font-semibold">Coloca tu rostro dentro del círculo</p>
            </div>
          </div>
        )}

        {/* Loading overlay */}
        {isLoading && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center rounded-xl">
            <div className="text-center text-white">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
              <p className="text-lg">
                {!model ? "Cargando detector facial..." : "Iniciando cámara..."}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Controles de cámara */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={restartCamera}
          disabled={isLoading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors font-medium"
        >
          <span>🔄</span>
          Reiniciar Cámara
        </button>
        {stream && (
          <button
            onClick={stopCamera}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors font-medium"
          >
            <span>⏹️</span>
            Detener Cámara
          </button>
        )}
      </div>

      {/* Indicador de estado */}
      <div className={`w-full max-w-md p-4 rounded-lg border-2 ${status.bg} ${status.border} ${status.text} mb-4`}>
        <div className="flex items-center justify-center gap-3">
          <span className="text-xl">{status.icon}</span>
          <span className="font-semibold text-center">{status.message}</span>
        </div>
        
        {/* Botón de reintento para errores */}
        {error && (
          <div className="mt-3 text-center">
            <button
              onClick={restartCamera}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm font-medium"
            >
              Reintentar Conexión
            </button>
          </div>
        )}
      </div>

      {/* Información de detección */}
      {faceDetected && (
        <div className="mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
          <p className="text-green-400 text-center">
            ✅ Rostro detectado correctamente
          </p>
        </div>
      )}

      {/* Instrucciones */}
      <div className="text-center text-gray-400 text-sm space-y-1">
        <p className="font-medium text-gray-300 mb-2">Para mejor detección:</p>
        <p>• Asegúrate de tener buena iluminación frontal</p>
        <p>• Mira directamente a la cámara</p>
        <p>• Mantén el rostro centrado en el marco</p>
        <p>• El detector seguirá tu rostro en tiempo real</p>
      </div>
    </div>
  );
};

export default Biometria;
import React, { useRef, useEffect, useState } from "react";
import * as faceapi from "face-api.js";

const Biometria: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [faceDetected, setFaceDetected] = useState(false);

  useEffect(() => {
    const loadModelsAndStartVideo = async () => {
      // Carga los modelos
      await faceapi.nets.tinyFaceDetector.loadFromUri("/models");

      if (videoRef.current) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
          videoRef.current.srcObject = stream;
        } catch (err) {
          console.error("Error accediendo a la cámara:", err);
        }
      }
    };

    loadModelsAndStartVideo();
  }, []);

  const handleVideoPlay = () => {
    const interval = setInterval(async () => {
      if (!videoRef.current || !canvasRef.current) return;

      // Detectar caras
      const detections = await faceapi.detectAllFaces(
        videoRef.current,
        new faceapi.TinyFaceDetectorOptions()
      );

      // Ajustar canvas al tamaño del video
      const canvas = canvasRef.current;
      const displaySize = {
        width: videoRef.current.width,
        height: videoRef.current.height,
      };
      faceapi.matchDimensions(canvas, displaySize);
      const resizedDetections = faceapi.resizeResults(detections, displaySize);

      // Dibujar detecciones
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        faceapi.draw.drawDetections(canvas, resizedDetections);
      }

      // Actualizar estado
      setFaceDetected(resizedDetections.length > 0);
    }, 200);

    return () => clearInterval(interval);
  };

  return (
    <div style={{ position: "relative", width: 960, height: 720, margin: "0 auto" }}>
      <video
        ref={videoRef}
        autoPlay
        muted
        onPlay={handleVideoPlay}
        width={960}
        height={720}
        style={{ borderRadius: 12, border: "3px solid gray" }}
      />
      <canvas
        ref={canvasRef}
        width={960}
        height={720}
        style={{ position: "absolute", top: 0, left: 0 }}
      />
      <p
        style={{
          color: faceDetected ? "lime" : "red",
          fontWeight: "bold",
          fontSize: 24,
          textAlign: "center",
          marginTop: -2,
        }}
      >
        {faceDetected ? "¡Cara detectada!" : "No se detecta cara"}
      </p>
    </div>
  );
};

export default Biometria;

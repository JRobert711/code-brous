// src/types/index.ts
export interface User {
    id: string;
    name: string;
    email: string;
  }
  
  export interface Drone {
    id: string;
    name: string;
    status: 'active' | 'inactive' | 'maintenance';
    battery: number;
    location: {
      lat: number;
      lng: number;
    };
  }
  
  export interface VoiceAuthResponse {
    success: boolean;
    user?: User;
    token?: string;
    error?: string;
  }
  
  export interface CameraCapture {
    id: string;
    timestamp: Date;
    imageData: string;
  }
// src/services/authService.ts
import axios from 'axios';
import type { VoiceAuthResponse, User } from '../types';

const API_BASE_URL = 'http://localhost:3001/api'; // Ajusta según tu backend

export const authService = {
  async authenticateWithVoice(audioBlob: Blob): Promise<VoiceAuthResponse> {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'voice-auth.wav');

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/voice`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error('Error en autenticación por voz');
    }
  },

  async verifyFaceId(imageData: string): Promise<{ success: boolean; user?: User }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/face`, {
        image: imageData
      });
      return response.data;
    } catch (error) {
      throw new Error('Error en verificación facial');
    }
  },

  logout(): void {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
};
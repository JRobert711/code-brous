import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Tipos para TypeScript
export interface Ciudadano {
  id: number;
  nombre: string;
  identificacion: string;
  email?: string;
  telefono?: string;
  fecha_creacion: string;
}

export interface Drone {
  id: number;
  modelo: string;
  estado: string;
  ubicacion?: string;
  bateria?: number;
}

export interface BiometricData {
  id: number;
  ciudadano_id: number;
  tipo: string;
  datos: string;
  fecha_registro: string;
}

export interface DashboardStats {
  totalCiudadanos: number;
  dronesActivos: number;
  totalDrones: number;
  registrosBiometricos: number;
  ciudadanosRecientes: number;
}

// Servicios para cada módulo
export const ciudadanoService = {
  getAll: () => api.get<Ciudadano[]>('/api/ciudadanos'),
  getById: (id: number) => api.get<Ciudadano>(`/api/ciudadanos/${id}`),
  create: (ciudadano: Omit<Ciudadano, 'id' | 'fecha_creacion'>) => 
    api.post<Ciudadano>('/api/ciudadanos', ciudadano),
  update: (id: number, ciudadano: Omit<Ciudadano, 'id' | 'fecha_creacion'>) => 
    api.put<Ciudadano>(`/api/ciudadanos/${id}`, ciudadano),
  delete: (id: number) => api.delete(`/api/ciudadanos/${id}`),
};

export const droneService = {
  getAll: () => api.get<Drone[]>('/api/drones'),
  create: (drone: Omit<Drone, 'id'>) => 
    api.post<Drone>('/api/drones', drone),
};

export const biometriaService = {
  getAll: () => api.get<BiometricData[]>('/api/biometria'),
  getByCiudadano: (ciudadanoId: number) => 
    api.get<BiometricData[]>(`/api/biometria/${ciudadanoId}`),
};

export const dashboardService = {
  getStats: () => api.get<DashboardStats>('/api/dashboard/stats'),
};

export default api;
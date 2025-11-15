import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token a las requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token');
      localStorage.removeItem('usuario');
      window.location.href = '/login';
    }
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// ========== TIPOS PARA TYPESCRIPT ==========

export interface Usuario {
  id: number;
  dui: string;
  nombres: string;
  apellidos: string;
  email?: string;
  telefono?: string;
  fecha_nacimiento?: string;
  direccion?: string;
  sector: string;
  nivel_acceso: number;
  created_at: string;
  is_active?: boolean;
}

export interface UsuarioCreate {
  dui: string;
  nombres: string;
  apellidos: string;
  email?: string;
  telefono?: string;
  fecha_nacimiento?: string;
  direccion?: string;
  sector: string;
  password: string;
}

export interface UsuarioCompleto extends Usuario {
  permisos: string[];
  historial_medico?: HistorialMedico;
  vacunas?: Vacuna[];
  operaciones?: Operacion[];
  medicamentos?: Medicamento[];
  titulos_academicos?: TituloAcademico[];
  certificaciones?: Certificacion[];
  cursos_especializados?: CursoEspecializado[];
  experiencia_laboral?: ExperienciaLaboral[];
  habilidades_verificadas?: HabilidadVerificada[];
  contribuciones_isss?: ContribucionISSS[];
  antecedentes_penales?: AntecedentePenal[];
  licencias_conducir?: LicenciaConducir[];
  multas_sanciones?: MultaSancion[];
  pensiones?: Pension[];
  subsidios?: Subsidio[];
  ayudas_estatales?: AyudaEstatal[];
}

// ========== MÓDULO SALUD ==========
export interface HistorialMedico {
  id: number;
  usuario_id: number;
  grupo_sanguineo?: string;
  alergias?: string;
  enfermedades_cronicas?: string;
  discapacidades?: string;
}

export interface Vacuna {
  id: number;
  usuario_id: number;
  nombre: string;
  fecha_aplicacion: string;
  lote?: string;
  centro_salud: string;
}

export interface Operacion {
  id: number;
  usuario_id: number;
  tipo_operacion: string;
  fecha: string;
  hospital: string;
  descripcion?: string;
}

export interface Medicamento {
  id: number;
  usuario_id: number;
  nombre: string;
  dosis: string;
  frecuencia: string;
  fecha_inicio: string;
  fecha_fin?: string;
  recetado_por: string;
}

// ========== MÓDULO EDUCACIÓN ==========
export interface TituloAcademico {
  id: number;
  usuario_id: number;
  nivel_educativo: string;
  institucion: string;
  titulo: string;
  año_graduacion: number;
  promedio?: number;
}

export interface Certificacion {
  id: number;
  usuario_id: number;
  nombre: string;
  institucion: string;
  fecha_emision: string;
  fecha_expiracion?: string;
}

export interface CursoEspecializado {
  id: number;
  usuario_id: number;
  nombre_curso: string;
  institucion: string;
  horas: number;
  fecha_completacion: string;
}

// ========== MÓDULO LABORAL ==========
export interface ExperienciaLaboral {
  id: number;
  usuario_id: number;
  empresa: string;
  puesto: string;
  fecha_inicio: string;
  fecha_fin?: string;
  responsabilidades?: string;
  salario_final?: number;
}

export interface HabilidadVerificada {
  id: number;
  usuario_id: number;
  habilidad: string;
  nivel: string;
  verificada_por: string;
  fecha_verificacion: string;
}

export interface ContribucionISSS {
  id: number;
  usuario_id: number;
  empleador: string;
  meses_cotizados: number;
  ultima_contribucion: string;
  monto_actual?: number;
}

// ========== MÓDULO JUDICIAL ==========
export interface AntecedentePenal {
  id: number;
  usuario_id: number;
  delito: string;
  fecha_delito: string;
  sentencia: string;
  estado: string;
  observaciones?: string;
}

export interface LicenciaConducir {
  id: number;
  usuario_id: number;
  categoria: string;
  fecha_emision: string;
  fecha_expiracion: string;
  restricciones?: string;
  puntos: number;
}

export interface MultaSancion {
  id: number;
  usuario_id: number;
  tipo: string;
  motivo: string;
  monto: number;
  fecha: string;
  estado: string;
}

// ========== MÓDULO SERVICIOS SOCIALES ==========
export interface Pension {
  id: number;
  usuario_id: number;
  tipo_pension: string;
  monto_mensual: number;
  fecha_inicio: string;
  entidad_emisora: string;
}

export interface Subsidio {
  id: number;
  usuario_id: number;
  tipo_subsidio: string;
  monto: number;
  fecha_asignacion: string;
  fecha_vencimiento?: string;
}

export interface AyudaEstatal {
  id: number;
  usuario_id: number;
  programa: string;
  beneficio: string;
  fecha_asignacion: string;
  vigente: boolean;
}

// ========== DASHBOARD ==========
export interface DashboardStats {
  totalUsuarios: number;
  usuariosActivos: number;
  registrosSalud: number;
  registrosEducacion: number;
  registrosLaborales: number;
  registrosJudiciales: number;
  registrosServiciosSociales: number;
}

// ========== AUTENTICACIÓN ==========
export interface LoginRequest {
  dui: string;
  password: string;
  captcha_token: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: Usuario;
  permisos: string[];
}

export interface RegisterRequest extends UsuarioCreate {}

// ========== SERVICIOS DE API ==========

// Servicio de Autenticación
export const authService = {
  login: (credenciales: LoginRequest) => 
    api.post<LoginResponse>('/api/auth/login', credenciales),
  
  register: (usuario: RegisterRequest) => 
    api.post<Usuario>('/api/auth/register', usuario),
  
  getMe: () => 
    api.get<Usuario>('/api/auth/me'),
  
  logout: () => 
    api.post('/api/auth/logout'),
  
  getTestTokens: () => 
    api.get('/api/auth/test-tokens'),
};

// Servicio de Usuarios
export const usuarioService = {
  getAll: (sector?: string) => 
    api.get<Usuario[]>('/api/usuarios', { params: { sector } }),
  
  getById: (id: number) => 
    api.get<UsuarioCompleto>(`/api/usuarios/${id}`),
  
  updateInfoBasica: (id: number, info: Partial<Usuario>) => 
    api.put(`/api/usuarios/${id}/info-basica`, info),
};

// Servicio de Salud
export const saludService = {
  // Historial Médico
  getHistorialMedico: (usuarioId: number) => 
    api.get<HistorialMedico>(`/api/salud/${usuarioId}/historial`),
  
  updateHistorialMedico: (usuarioId: number, historial: HistorialMedico) => 
    api.put(`/api/salud/${usuarioId}/historial`, historial),
  
  // Vacunas
  getVacunas: (usuarioId: number) => 
    api.get<Vacuna[]>(`/api/salud/${usuarioId}/vacunas`),
  
  addVacuna: (usuarioId: number, vacuna: Omit<Vacuna, 'id'>) => 
    api.post(`/api/salud/${usuarioId}/vacunas`, vacuna),
  
  // Operaciones
  getOperaciones: (usuarioId: number) => 
    api.get<Operacion[]>(`/api/salud/${usuarioId}/operaciones`),
  
  // Medicamentos
  getMedicamentos: (usuarioId: number) => 
    api.get<Medicamento[]>(`/api/salud/${usuarioId}/medicamentos`),
};

// Servicio de Educación
export const educacionService = {
  // Títulos Académicos
  getTitulos: (usuarioId: number) => 
    api.get<TituloAcademico[]>(`/api/educacion/${usuarioId}/titulos`),
  
  addTitulo: (usuarioId: number, titulo: Omit<TituloAcademico, 'id'>) => 
    api.post(`/api/educacion/${usuarioId}/titulos`, titulo),
  
  // Certificaciones
  getCertificaciones: (usuarioId: number) => 
    api.get<Certificacion[]>(`/api/educacion/${usuarioId}/certificaciones`),
  
  addCertificacion: (usuarioId: number, certificacion: Omit<Certificacion, 'id'>) => 
    api.post(`/api/educacion/${usuarioId}/certificaciones`, certificacion),
  
  // Cursos
  getCursos: (usuarioId: number) => 
    api.get<CursoEspecializado[]>(`/api/educacion/${usuarioId}/cursos`),
  
  addCurso: (usuarioId: number, curso: Omit<CursoEspecializado, 'id'>) => 
    api.post(`/api/educacion/${usuarioId}/cursos`, curso),
};

// Servicio Laboral
export const laboralService = {
  // Experiencia Laboral
  getExperiencia: (usuarioId: number) => 
    api.get<ExperienciaLaboral[]>(`/api/laboral/${usuarioId}/experiencia`),
  
  addExperiencia: (usuarioId: number, experiencia: Omit<ExperienciaLaboral, 'id'>) => 
    api.post(`/api/laboral/${usuarioId}/experiencia`, experiencia),
  
  // Habilidades
  getHabilidades: (usuarioId: number) => 
    api.get<HabilidadVerificada[]>(`/api/laboral/${usuarioId}/habilidades`),
  
  addHabilidad: (usuarioId: number, habilidad: Omit<HabilidadVerificada, 'id'>) => 
    api.post(`/api/laboral/${usuarioId}/habilidades`, habilidad),
  
  // ISSS
  getContribucionesISSS: (usuarioId: number) => 
    api.get<ContribucionISSS[]>(`/api/laboral/${usuarioId}/isss`),
  
  addContribucionISSS: (usuarioId: number, contribucion: Omit<ContribucionISSS, 'id'>) => 
    api.post(`/api/laboral/${usuarioId}/isss`, contribucion),
};

// Servicio Judicial
export const judicialService = {
  // Antecedentes Penales
  getAntecedentes: (usuarioId: number) => 
    api.get<AntecedentePenal[]>(`/api/judicial/${usuarioId}/antecedentes`),
  
  addAntecedente: (usuarioId: number, antecedente: Omit<AntecedentePenal, 'id'>) => 
    api.post(`/api/judicial/${usuarioId}/antecedentes`, antecedente),
  
  // Licencias de Conducir
  getLicencias: (usuarioId: number) => 
    api.get<LicenciaConducir[]>(`/api/judicial/${usuarioId}/licencias`),
  
  addLicencia: (usuarioId: number, licencia: Omit<LicenciaConducir, 'id'>) => 
    api.post(`/api/judicial/${usuarioId}/licencias`, licencia),
  
  // Multas
  getMultas: (usuarioId: number) => 
    api.get<MultaSancion[]>(`/api/judicial/${usuarioId}/multas`),
  
  addMulta: (usuarioId: number, multa: Omit<MultaSancion, 'id'>) => 
    api.post(`/api/judicial/${usuarioId}/multas`, multa),
};

// Servicio de Servicios Sociales
export const serviciosSocialesService = {
  // Pensiones
  getPensiones: (usuarioId: number) => 
    api.get<Pension[]>(`/api/servicios-sociales/${usuarioId}/pensiones`),
  
  addPension: (usuarioId: number, pension: Omit<Pension, 'id'>) => 
    api.post(`/api/servicios-sociales/${usuarioId}/pensiones`, pension),
  
  // Subsidios
  getSubsidios: (usuarioId: number) => 
    api.get<Subsidio[]>(`/api/servicios-sociales/${usuarioId}/subsidios`),
  
  addSubsidio: (usuarioId: number, subsidio: Omit<Subsidio, 'id'>) => 
    api.post(`/api/servicios-sociales/${usuarioId}/subsidios`, subsidio),
  
  // Ayudas Estatales
  getAyudas: (usuarioId: number) => 
    api.get<AyudaEstatal[]>(`/api/servicios-sociales/${usuarioId}/ayudas`),
  
  addAyuda: (usuarioId: number, ayuda: Omit<AyudaEstatal, 'id'>) => 
    api.post(`/api/servicios-sociales/${usuarioId}/ayudas`, ayuda),
};

// Servicio del Dashboard
export const dashboardService = {
  getStats: () => 
    api.get<DashboardStats>('/api/dashboard/stats'),
};

// Utilidades para manejo de tokens
export const tokenUtils = {
  setToken: (token: string) => {
    localStorage.setItem('access_token', token);
  },
  
  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },
  
  removeToken: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('usuario');
  },
  
  setUsuario: (usuario: Usuario) => {
    localStorage.setItem('usuario', JSON.stringify(usuario));
  },
  
  getUsuario: (): Usuario | null => {
    const usuarioStr = localStorage.getItem('usuario');
    return usuarioStr ? JSON.parse(usuarioStr) : null;
  },
  
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};

export default api;
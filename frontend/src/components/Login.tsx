// src/components/Login.tsx
import React, { useState } from 'react';
import { authService, tokenUtils, Usuario } from '../services/api';
import { useNavigate } from 'react-router-dom';

interface LoginFormState {
  document_type: 'dui' | 'nit' | 'carnet_menoridad' | 'carnet_recien_nacido' | 'carnet_escolar' | string;
  document_value: string;
  password: string;
}

const Login: React.FC = () => {
  const [formData, setFormData] = useState<LoginFormState>({
    document_type: 'dui',
    document_value: '',
    password: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [debugInfo, setDebugInfo] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setDebugInfo('');

    try {
      console.log('📨 Enviando al backend:', formData);
      setDebugInfo('Conectando con el servidor...');

      // Construimos el payload exactamente como lo espera el backend
      const payload = {
        document_type: formData.document_type,
        document_value: formData.document_value,
        password: formData.password
      };

      // TypeScript puede tirar si authService.login espera otra interfaz.
      // Para evitar romper todo, casteamos a any aquí asumiendo que authService
      // espera un objeto compatible en runtime (mejor: actualizar la definición en services/api).
      const response = await authService.login(payload as any);

      console.log('✅ Login exitoso:', response.data);
      setDebugInfo('Login exitoso, guardando token...');

      // Guardar token y usuario en utilidades
      tokenUtils.setToken(response.data.access_token);
      tokenUtils.setUsuario(response.data.usuario);

      console.log('🔑 Token guardado:', response.data.access_token);
      console.log('👤 Usuario guardado:', response.data.usuario);
      setDebugInfo('Redirigiendo al dashboard...');

      // Redirigir al dashboard
      navigate('/dashboard');
    } catch (err: any) {
      console.error('❌ Error de login:', err);
      console.error('❌ Respuesta del error:', err?.response);

      let errorMessage = 'Error al iniciar sesión';

      if (err?.response) {
        errorMessage = err.response.data?.detail || `Error ${err.response.status}`;
        setDebugInfo(`Status: ${err.response.status}, Mensaje: ${errorMessage}`);
      } else if (err?.request) {
        errorMessage = 'No se pudo conectar con el servidor';
        setDebugInfo('No hay respuesta del servidor');
      } else {
        errorMessage = err?.message || errorMessage;
        setDebugInfo(`Error: ${err?.message}`);
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const usarTokenPrueba = async (token: string, sector: string, nombres: string) => {
    console.log('🔑 Usando token de prueba:', token);
    setDebugInfo(`Usando token: ${token}`);

    try {
      tokenUtils.setToken(token);

      // Crear usuario de prueba
      const usuarioPrueba: Usuario = {
        id: parseInt(token.replace('test_token_', '')) || 0,
        dui: '00000000-0',
        nombres: nombres,
        apellidos: 'de Prueba',
        email: 'test@email.com',
        sector: sector,
        nivel_acceso:
          sector === 'admin'
            ? 7
            : sector === 'medico'
            ? 6
            : sector === 'judicial'
            ? 5
            : sector === 'educativo'
            ? 4
            : sector === 'laboral'
            ? 3
            : sector === 'servicios_sociales'
            ? 2
            : 1,
        created_at: new Date().toISOString(),
        telefono: '+503 0000-0000'
      };

      tokenUtils.setUsuario(usuarioPrueba);

      console.log('👤 Usuario de prueba creado:', usuarioPrueba);
      setDebugInfo('Token aplicado, redirigiendo...');

      // Comprobar token con una request 'me' opcional
      try {
        const testResponse = await authService.getMe();
        console.log('✅ Token válido, usuario:', testResponse.data);
      } catch (testError) {
        console.warn('⚠️ El token podría no ser válido, pero continuamos...', testError);
      }

      navigate('/dashboard');
    } catch (err) {
      console.error('❌ Error usando token de prueba:', err);
      setError('Error al usar el token de prueba');
      setDebugInfo('Error al aplicar el token');
    }
  };

  // Función para probar la conexión con el backend
  const probarConexionBackend = async () => {
    try {
      setDebugInfo('Probando conexión con el backend...');
      const response = await fetch('http://localhost:8000/api/health');
      const data = await response.json();
      console.log('✅ Backend respondió:', data);
      setDebugInfo(`Backend: ${data.status} - ${data.system}`);
    } catch (err) {
      console.error('❌ Backend no responde:', err);
      setDebugInfo('❌ Backend no disponible - Verifica que esté corriendo en puerto 8000');
      setError('El backend no está disponible. Ejecuta: uvicorn app.main:app --reload --port 8000');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/50 border border-gray-700 rounded-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">🏛️ Sistema Nacional</h1>
          <p className="text-gray-400">Iniciar Sesión</p>
        </div>

        {/* Botón para probar conexión */}
        <button
          onClick={probarConexionBackend}
          className="w-full bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg text-sm mb-4 transition-colors"
        >
          🔍 Probar Conexión Backend
        </button>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-400 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {debugInfo && (
          <div className="bg-blue-500/20 border border-blue-500/50 text-blue-400 p-3 rounded-lg mb-4 text-sm">
            {debugInfo}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Tipo de Documento</label>
            <select
              value={formData.document_type}
              onChange={(e) => setFormData({ ...formData, document_type: e.target.value })}
              className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white"
            >
              <option value="dui">DUI</option>
              <option value="nit">NIT</option>
              <option value="carnet_menoridad">Carnet de Minoridad</option>
              <option value="carnet_recien_nacido">Carnet de Recién Nacido</option>
              <option value="carnet_escolar">Carnet Escolar</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Número de Documento</label>
            <input
              type="text"
              value={formData.document_value}
              onChange={(e) => setFormData({ ...formData, document_value: e.target.value })}
              className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="Ingrese su identificación"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Contraseña</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="••••••••"
              required
            />
            <p className="text-xs text-gray-400 mt-1">Usa "password123" para usuarios de prueba</p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>

        {/* Acceso Rápido (Desarrollo) */}
        <div className="mt-8 pt-6 border-t border-gray-700">
          <h3 className="text-sm font-medium text-gray-300 mb-3">Acceso Rápido (Desarrollo)</h3>
          <div className="space-y-2">
            <button
              onClick={() => usarTokenPrueba('test_token_5', 'admin', 'Administrador')}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              👑 Admin (Nivel 7) - Acceso Total
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_2', 'medico', 'Médico')}
              className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🏥 Médico (Nivel 6) - Módulo Salud
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_3', 'judicial', 'Judicial')}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              ⚖️ Judicial (Nivel 5) - Módulo Judicial
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_4', 'educativo', 'Educador')}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🎓 Educativo (Nivel 4) - Módulo Educación
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_6', 'laboral', 'Laboral')}
              className="w-full bg-yellow-600 hover:bg-yellow-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              💼 Laboral (Nivel 3) - Módulo Laboral
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_7', 'servicios_sociales', 'Servicios Sociales')}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🏛️ Servicios Sociales (Nivel 2) - Módulo Social
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_1', 'ciudadano', 'Ciudadano')}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              👤 Ciudadano (Nivel 1) - Acceso Básico
            </button>
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">Sistema de Identidad Nacional v1.0</p>
        </div>
      </div>
    </div>
  );
};

export default Login;

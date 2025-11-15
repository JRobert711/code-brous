import React, { useState } from 'react';
import { authService, tokenUtils, Usuario } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    dui: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authService.login(formData);
      
      // Guardar token y usuario
      tokenUtils.setToken(response.data.access_token);
      tokenUtils.setUsuario(response.data.usuario);
      
      // Redirigir al dashboard
      navigate('/');
      
    } catch (error: any) {
      console.error('Error de login:', error);
      setError(error.response?.data?.detail || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  const usarTokenPrueba = (token: string, sector: string, nombres: string) => {
    tokenUtils.setToken(token);
    
    // Para tokens de prueba, también necesitamos simular el usuario
    const usuarioPrueba: Usuario = {
      id: parseInt(token.replace('test_token_', '')),
      dui: "00000000-0",
      nombres: nombres,
      apellidos: "de Prueba",
      email: "test@email.com",
      sector: sector,
      nivel_acceso: sector === 'admin' ? 7 : 
                    sector === 'medico' ? 6 :
                    sector === 'judicial' ? 5 :
                    sector === 'educativo' ? 4 :
                    sector === 'laboral' ? 3 :
                    sector === 'servicios_sociales' ? 2 : 1,
      created_at: new Date().toISOString(),
      telefono: "+503 0000-0000"
    };
    tokenUtils.setUsuario(usuarioPrueba);
    
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/50 border border-gray-700 rounded-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">🏛️ Sistema Nacional</h1>
          <p className="text-gray-400">Iniciar Sesión</p>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-400 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              DUI
            </label>
            <input
              type="text"
              value={formData.dui}
              onChange={(e) => setFormData({...formData, dui: e.target.value})}
              className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="00000000-0"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Contraseña
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="••••••••"
              required
            />
            <p className="text-xs text-gray-400 mt-1">
              Usa "password123" para usuarios de prueba
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>

        {/* Tokens de prueba para desarrollo */}
        <div className="mt-8 pt-6 border-t border-gray-700">
          <h3 className="text-sm font-medium text-gray-300 mb-3">Acceso Rápido (Desarrollo)</h3>
          <div className="space-y-2">
            <button
              onClick={() => usarTokenPrueba('test_token_999', 'admin', 'Administrador')}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🔑 Admin (Acceso Total)
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_1', 'ciudadano', 'Ciudadano')}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              👤 Ciudadano (Acceso Básico)
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_2', 'medico', 'Médico')}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🏥 Médico (Acceso Salud)
            </button>
            <button
              onClick={() => usarTokenPrueba('test_token_4', 'educativo', 'Educador')}
              className="w-full bg-yellow-600 hover:bg-yellow-700 text-white py-2 rounded-lg text-sm transition-colors"
            >
              🎓 Educativo (Acceso Educación)
            </button>
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            Sistema de Identidad Nacional v1.0
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
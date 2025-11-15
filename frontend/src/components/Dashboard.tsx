import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  // Datos de ejemplo para estadísticas
  const stats = {
    totalCiudadanos: '6,542,000',
    registrosHoy: '1,247',
    dronesActivos: '12',
    reconocimientosExitosos: '98.7%',
    alertasSeguridad: '3'
  };

  const modules = [
    {
      title: "GESTIÓN DE CIUDADANOS",
      description: "Registro y administración de identidades digitales",
      icon: "👤",
      path: "/ciudadanos",
      color: "from-blue-600 to-cyan-500",
      stats: "6.5M+ registros"
    },
    {
      title: "BIOMETRÍA AVANZADA",
      description: "Autenticación por voz, rostro y huellas digitales",
      icon: "🎙️",
      path: "/biometria",
      color: "from-purple-600 to-pink-500",
      stats: "98.7% precisión"
    },
    {
      title: "VIGILANCIA CON DRONES",
      description: "Monitoreo en tiempo real y reconocimiento facial",
      icon: "🚁",
      path: "/drones",
      color: "from-green-600 to-emerald-500",
      stats: "12 drones activos"
    },
    {
      title: "EXPEDIENTES DIGITALES",
      description: "Historial médico, educativo y laboral unificado",
      icon: "📁",
      path: "/expedientes",
      color: "from-orange-600 to-red-500",
      stats: "10.2M+ documentos"
    },
    {
      title: "REPORTES DE SEGURIDAD",
      description: "Análisis y reportes de actividades de seguridad",
      icon: "📊",
      path: "/reportes",
      color: "from-indigo-600 to-blue-500",
      stats: "247 alertas/mes"
    },
    {
      title: "ADMINISTRACIÓN",
      description: "Configuración y gestión del sistema central",
      icon: "⚙️",
      path: "/admin",
      color: "from-gray-600 to-slate-500",
      stats: "Sistema activo"
    }
  ];

  return (
    <div className="min-h-screen py-8">
      {/* Encabezado Principal */}
      <section className="max-w-7xl mx-auto mb-12">
        <div className="bg-gradient-to-r from-[#006DFF] via-[#0047AB] to-[#003366] rounded-2xl shadow-2xl p-10 text-white text-center relative overflow-hidden">
          {/* Efectos de fondo */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-cyan-400/10 rounded-full blur-2xl"></div>
          
          <h2 className="text-5xl font-extrabold tracking-tight mb-4 relative z-10">
            SISTEMA DE IDENTIDAD DIGITAL NACIONAL
          </h2>
          <p className="text-xl opacity-90 mb-8 leading-relaxed max-w-3xl mx-auto relative z-10">
            Plataforma centralizada de gestión ciudadana con biometría avanzada 
            y vigilancia inteligente para El Salvador
          </p>

          {/* Estadísticas Rápidas */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8 relative z-10">
            {Object.entries(stats).map(([key, value]) => (
              <div key={key} className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold text-white">{value}</div>
                <div className="text-sm text-gray-300 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').toLowerCase()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Módulos del Sistema */}
      <section className="max-w-7xl mx-auto">
        <h3 className="text-3xl font-bold text-white text-center mb-8">MÓDULOS PRINCIPALES</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((module, index) => (
            <Link
              key={index}
              to={module.path}
              className="group relative bg-gradient-to-br from-gray-900/80 to-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-600/50 hover:border-[#006DFF] transition-all duration-300 hover:transform hover:scale-105 hover:shadow-2xl hover:shadow-[#006DFF]/20"
            >
              {/* Efecto de gradiente en hover */}
              <div className={`absolute inset-0 bg-gradient-to-r ${module.color} opacity-0 group-hover:opacity-10 rounded-2xl transition-opacity duration-300`}></div>
              
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-4xl">{module.icon}</span>
                  <div className="text-sm font-semibold text-gray-400 bg-gray-700/50 px-3 py-1 rounded-full">
                    {module.stats}
                  </div>
                </div>
                
                <h4 className="text-xl font-bold text-white mb-3 group-hover:text-cyan-200 transition-colors">
                  {module.title}
                </h4>
                
                <p className="text-gray-300 text-sm leading-relaxed mb-4">
                  {module.description}
                </p>
                
                <div className="flex items-center text-cyan-400 font-semibold text-sm">
                  Acceder al módulo
                  <svg 
                    className="w-4 h-4 ml-2 transform group-hover:translate-x-1 transition-transform" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Alertas y Notificaciones */}
      <section className="max-w-7xl mx-auto mt-12">
        <div className="bg-gradient-to-r from-red-600/20 to-orange-600/20 backdrop-blur-sm rounded-2xl p-6 border border-red-500/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <div>
                <h4 className="text-lg font-bold text-white">ALERTAS DE SEGURIDAD ACTIVAS</h4>
                <p className="text-gray-300 text-sm">
                  {stats.alertasSeguridad} incidentes requieren atención inmediata
                </p>
              </div>
            </div>
            <Link 
              to="/alertas" 
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
            >
              Ver Alertas
            </Link>
          </div>
        </div>
      </section>

      {/* Información Adicional */}
      <section className="max-w-7xl mx-auto mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 backdrop-blur-sm rounded-2xl p-6 border border-cyan-500/30">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-8 h-8 bg-cyan-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">✓</span>
            </div>
            <h4 className="text-lg font-bold text-white">Sistema Operativo</h4>
          </div>
          <p className="text-gray-300 text-sm">
            Todos los módulos funcionando correctamente. Sin interrupciones reportadas.
          </p>
        </div>

        <div className="bg-gradient-to-br from-green-600/20 to-emerald-600/20 backdrop-blur-sm rounded-2xl p-6 border border-emerald-500/30">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">📈</span>
            </div>
            <h4 className="text-lg font-bold text-white">Rendimiento</h4>
          </div>
          <p className="text-gray-300 text-sm">
            Tiempo de respuesta: 124ms. Capacidad utilizada: 67%.
          </p>
        </div>

        <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">🛡️</span>
            </div>
            <h4 className="text-lg font-bold text-white">Seguridad</h4>
          </div>
          <p className="text-gray-300 text-sm">
            Protocolos de seguridad activos. Cifrado AES-256 implementado.
          </p>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
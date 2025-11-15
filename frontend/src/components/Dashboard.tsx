// src/components/Dashboard.tsx
import { useEffect, useState } from 'react';
import { 
  ciudadanoService, 
  droneService, 
  Ciudadano, 
  Drone,
} from '../services/api';

interface DashboardStats {
  totalCiudadanos: number;
  dronesActivos: number;
  totalDrones: number;
  registrosBiometricos: number;
  ciudadanosRecientes: number;
}

const Dashboard = () => {
  const [ciudadanos, setCiudadanos] = useState<Ciudadano[]>([]);
  const [drones, setDrones] = useState<Drone[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    totalCiudadanos: 0,
    dronesActivos: 0,
    totalDrones: 0,
    registrosBiometricos: 0,
    ciudadanosRecientes: 0
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [ciudadanosRes, dronesRes] = await Promise.all([
          ciudadanoService.getAll(),
          droneService.getAll()
        ]);
        
        setCiudadanos(ciudadanosRes.data);
        setDrones(dronesRes.data);

        // Calcular estadísticas básicas
        const ahora = new Date();
        const ultimaSemana = new Date(ahora.setDate(ahora.getDate() - 7));
        
        const ciudadanosRecientes = ciudadanosRes.data.filter((c: Ciudadano) => 
          c.fecha_creacion && new Date(c.fecha_creacion) > ultimaSemana
        ).length;

        setStats({
          totalCiudadanos: ciudadanosRes.data.length,
          dronesActivos: dronesRes.data.filter((d: Drone) => d.estado === 'activo').length,
          totalDrones: dronesRes.data.length,
          registrosBiometricos: 0, // Placeholder por ahora
          ciudadanosRecientes
        });

      } catch (error) {
        console.error('Error cargando datos del dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const Card = ({ title, value, subtitle, icon, color }: { 
    title: string; 
    value: number; 
    subtitle: string; 
    icon: string; 
    color: string;
  }) => (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-xl border border-gray-700 shadow-lg">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-gray-400 text-sm font-medium mb-2">{title}</p>
          <p className={`text-3xl font-bold ${color} mb-1`}>{value}</p>
          <p className="text-gray-500 text-sm">{subtitle}</p>
        </div>
        <div className="text-2xl">{icon}</div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <div className="text-lg text-gray-300">Cargando datos del sistema...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Panel de Control</h1>
          <p className="text-gray-400">Resumen general del sistema de vigilancia</p>
        </div>
        <div className="text-sm text-gray-400">
          Última actualización: <span className="text-green-400">Ahora</span>
        </div>
      </div>

      {/* Estadísticas Principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card 
          title="Ciudadanos Registrados" 
          value={stats.totalCiudadanos}
          subtitle="Total en el sistema"
          icon="👥"
          color="text-blue-400"
        />
        
        <Card 
          title="Drones Activos" 
          value={stats.dronesActivos}
          subtitle={`de ${stats.totalDrones} totales`}
          icon="🚁"
          color="text-green-400"
        />
        
        <Card 
          title="Registros Biométricos" 
          value={stats.registrosBiometricos}
          subtitle="Huellas y reconocimiento"
          icon="🔒"
          color="text-purple-400"
        />
        
        <Card 
          title="Nuevos Esta Semana" 
          value={stats.ciudadanosRecientes}
          subtitle="Registros recientes"
          icon="🆕"
          color="text-yellow-400"
        />
      </div>

      {/* Grid Inferior */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Drones Activos */}
        <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Drones en Operación</h2>
            <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">
              {stats.dronesActivos} activos
            </span>
          </div>
          <div className="space-y-3">
            {drones.slice(0, 6).map((drone) => (
              <div 
                key={drone.id} 
                className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${
                    drone.estado === 'activo' ? 'bg-green-500' : 
                    drone.estado === 'mantenimiento' ? 'bg-yellow-500' : 'bg-red-500'
                  }`}></div>
                  <div>
                    <p className="font-medium text-white">{drone.modelo}</p>
                    <p className="text-sm text-gray-400">{drone.ubicacion || 'Ubicación no disponible'}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                    drone.estado === 'activo' 
                      ? 'bg-green-500/20 text-green-400' 
                      : drone.estado === 'mantenimiento'
                      ? 'bg-yellow-500/20 text-yellow-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    {drone.estado}
                  </span>
                </div>
              </div>
            ))}
            {drones.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <div className="text-4xl mb-2">🚁</div>
                <p>No hay drones registrados</p>
              </div>
            )}
          </div>
        </div>

        {/* Ciudadanos Recientes */}
        <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Ciudadanos Recientes</h2>
            <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm">
              {stats.ciudadanosRecientes} nuevos
            </span>
          </div>
          <div className="space-y-3">
            {ciudadanos.slice(0, 6).map((ciudadano) => (
              <div 
                key={ciudadano.id} 
                className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                    <span className="text-blue-400 font-semibold">
                      {ciudadano.nombre.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-white">{ciudadano.nombre}</p>
                    <p className="text-sm text-gray-400">ID: {ciudadano.identificacion}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-400">
                    {ciudadano.fecha_creacion ? 
                      new Date(ciudadano.fecha_creacion).toLocaleDateString() : 
                      'Fecha no disponible'
                    }
                  </p>
                </div>
              </div>
            ))}
            {ciudadanos.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <div className="text-4xl mb-2">👥</div>
                <p>No hay ciudadanos registrados</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gray-800/30 rounded-xl border border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Acciones Rápidas</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="bg-blue-600 text-white p-4 rounded-lg text-center opacity-50 cursor-not-allowed">
            <div className="text-2xl mb-2">➕</div>
            <p className="text-sm">Nuevo Ciudadano</p>
          </button>
          <button className="bg-green-600 text-white p-4 rounded-lg text-center opacity-50 cursor-not-allowed">
            <div className="text-2xl mb-2">🚁</div>
            <p className="text-sm">Registrar Drone</p>
          </button>
          <button className="bg-purple-600 text-white p-4 rounded-lg text-center opacity-50 cursor-not-allowed">
            <div className="text-2xl mb-2">🔒</div>
            <p className="text-sm">Biometría</p>
          </button>
          <button className="bg-orange-600 text-white p-4 rounded-lg text-center opacity-50 cursor-not-allowed">
            <div className="text-2xl mb-2">📊</div>
            <p className="text-sm">Generar Reporte</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
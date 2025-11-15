import { useEffect, useState } from 'react';
import { 
  usuarioService, 
  dashboardService,
  Usuario,
  DashboardStats
} from '../services/api';

const Dashboard = () => {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    totalUsuarios: 0,
    usuariosActivos: 0,
    registrosSalud: 0,
    registrosEducacion: 0,
    registrosLaborales: 0,
    registrosJudiciales: 0,
    registrosServiciosSociales: 0
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [usuariosRes] = await Promise.all([
          usuarioService.getAll()
        ]);
        
        setUsuarios(usuariosRes.data);

        // Calcular estadísticas básicas
        const ahora = new Date();
        const ultimaSemana = new Date(ahora.setDate(ahora.getDate() - 7));
        
        const usuariosRecientes = usuariosRes.data.filter((u: Usuario) => 
          u.created_at && new Date(u.created_at) > ultimaSemana
        ).length;

        const usuariosActivos = usuariosRes.data.filter((u: Usuario) => 
          u.is_active !== false
        ).length;

        // Por ahora usamos datos estáticos para los registros de módulos
        // En un sistema real, estos vendrían del backend
        setStats({
          totalUsuarios: usuariosRes.data.length,
          usuariosActivos,
          registrosSalud: 45, // Placeholder
          registrosEducacion: 23, // Placeholder
          registrosLaborales: 67, // Placeholder
          registrosJudiciales: 12, // Placeholder
          registrosServiciosSociales: 34 // Placeholder
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
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-xl border border-gray-700 shadow-lg hover:shadow-xl transition-all duration-300">
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
          <p className="text-gray-400">Sistema Nacional de Identidad - Resumen General</p>
        </div>
        <div className="text-sm text-gray-400">
          Última actualización: <span className="text-green-400">Ahora</span>
        </div>
      </div>

      {/* Estadísticas Principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card 
          title="Usuarios Registrados" 
          value={stats.totalUsuarios}
          subtitle="Total en el sistema"
          icon="👥"
          color="text-blue-400"
        />
        
        <Card 
          title="Usuarios Activos" 
          value={stats.usuariosActivos}
          subtitle="Activos en la plataforma"
          icon="✅"
          color="text-green-400"
        />
        
        <Card 
          title="Registros de Salud" 
          value={stats.registrosSalud}
          subtitle="Historial médico"
          icon="🏥"
          color="text-red-400"
        />
        
        <Card 
          title="Registros Educativos" 
          value={stats.registrosEducacion}
          subtitle="Títulos y certificaciones"
          icon="🎓"
          color="text-purple-400"
        />
      </div>

      {/* Segunda Fila de Estadísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card 
          title="Registros Laborales" 
          value={stats.registrosLaborales}
          subtitle="Experiencia y habilidades"
          icon="💼"
          color="text-yellow-400"
        />
        
        <Card 
          title="Registros Judiciales" 
          value={stats.registrosJudiciales}
          subtitle="Antecedentes y licencias"
          icon="⚖️"
          color="text-orange-400"
        />
        
        <Card 
          title="Servicios Sociales" 
          value={stats.registrosServiciosSociales}
          subtitle="Pensiones y subsidios"
          icon="🏛️"
          color="text-indigo-400"
        />
      </div>

      {/* Grid Inferior */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Usuarios por Sector */}
        <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Usuarios por Sector</h2>
            <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm">
              {stats.totalUsuarios} total
            </span>
          </div>
          <div className="space-y-3">
            {Object.entries(
              usuarios.reduce((acc: {[key: string]: number}, usuario) => {
                acc[usuario.sector] = (acc[usuario.sector] || 0) + 1;
                return acc;
              }, {})
            ).map(([sector, count]) => (
              <div 
                key={sector} 
                className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg hover:bg-gray-700/50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${
                    sector === 'ciudadano' ? 'bg-blue-500' : 
                    sector === 'medico' ? 'bg-green-500' : 
                    sector === 'educativo' ? 'bg-purple-500' :
                    sector === 'judicial' ? 'bg-orange-500' :
                    sector === 'laboral' ? 'bg-yellow-500' :
                    sector === 'servicios_sociales' ? 'bg-indigo-500' :
                    'bg-red-500'
                  }`}></div>
                  <div>
                    <p className="font-medium text-white capitalize">
                      {sector.replace('_', ' ')}
                    </p>
                    <p className="text-sm text-gray-400">
                      {count} usuario{count !== 1 ? 's' : ''}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-400">
                    {((count / stats.totalUsuarios) * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
            {usuarios.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <div className="text-4xl mb-2">👥</div>
                <p>No hay usuarios registrados</p>
              </div>
            )}
          </div>
        </div>

        {/* Usuarios Recientes */}
        <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Usuarios Recientes</h2>
            <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">
              {usuarios.filter(u => {
                const unaSemanaAtras = new Date();
                unaSemanaAtras.setDate(unaSemanaAtras.getDate() - 7);
                return u.created_at && new Date(u.created_at) > unaSemanaAtras;
              }).length} nuevos
            </span>
          </div>
          <div className="space-y-3">
            {usuarios
              .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
              .slice(0, 6)
              .map((usuario) => (
              <div 
                key={usuario.id} 
                className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg hover:bg-gray-700/50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                    <span className="text-blue-400 font-semibold">
                      {usuario.nombres.charAt(0)}{usuario.apellidos.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-white">
                      {usuario.nombres} {usuario.apellidos}
                    </p>
                    <p className="text-sm text-gray-400">
                      {usuario.dui} • {usuario.sector}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-400">
                    {usuario.created_at ? 
                      new Date(usuario.created_at).toLocaleDateString() : 
                      'Fecha no disponible'
                    }
                  </p>
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium mt-1 ${
                    usuario.is_active === false 
                      ? 'bg-red-500/20 text-red-400' 
                      : 'bg-green-500/20 text-green-400'
                  }`}>
                    {usuario.is_active === false ? 'Inactivo' : 'Activo'}
                  </span>
                </div>
              </div>
            ))}
            {usuarios.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <div className="text-4xl mb-2">👥</div>
                <p>No hay usuarios registrados</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gray-800/30 rounded-xl border border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Acciones Rápidas</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button 
            className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg text-center transition-colors"
            onClick={() => {/* Navegar a registro de usuario */}}
          >
            <div className="text-2xl mb-2">👤</div>
            <p className="text-sm">Nuevo Usuario</p>
          </button>
          <button 
            className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg text-center transition-colors"
            onClick={() => {/* Navegar a módulo salud */}}
          >
            <div className="text-2xl mb-2">🏥</div>
            <p className="text-sm">Módulo Salud</p>
          </button>
          <button 
            className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg text-center transition-colors"
            onClick={() => {/* Navegar a módulo educación */}}
          >
            <div className="text-2xl mb-2">🎓</div>
            <p className="text-sm">Módulo Educación</p>
          </button>
          <button 
            className="bg-orange-600 hover:bg-orange-700 text-white p-4 rounded-lg text-center transition-colors"
            onClick={() => {/* Navegar a reportes */}}
          >
            <div className="text-2xl mb-2">📊</div>
            <p className="text-sm">Generar Reporte</p>
          </button>
        </div>
      </div>

      {/* Información del Sistema */}
      <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Estado del Sistema</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-300">Backend: </span>
            <span className="text-green-400">Operacional</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-300">Base de datos: </span>
            <span className="text-green-400">Conectada</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-300">Autenticación: </span>
            <span className="text-green-400">Activa</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
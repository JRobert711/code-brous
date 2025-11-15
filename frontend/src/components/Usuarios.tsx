import React, { useEffect, useState } from 'react';
import { usuarioService, Usuario, authService, UsuarioCreate } from '../services/api';

const Usuarios: React.FC = () => {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState<UsuarioCreate>({
    dui: '',
    nombres: '',
    apellidos: '',
    email: '',
    telefono: '',
    fecha_nacimiento: '',
    direccion: '',
    sector: 'ciudadano',
    password: 'password123'
  });

  // Cargar usuarios al iniciar
  useEffect(() => {
    fetchUsuarios();
  }, []);

  const fetchUsuarios = async () => {
    try {
      setLoading(true);
      const response = await usuarioService.getAll();
      setUsuarios(response.data);
    } catch (error) {
      console.error('Error cargando usuarios:', error);
      alert('Error al cargar los usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        // Actualizar usuario existente (solo info básica)
        await usuarioService.updateInfoBasica(editingId, formData);
        alert('Usuario actualizado exitosamente');
      } else {
        // Crear nuevo usuario usando authService.register
        await authService.register(formData);
        alert('Usuario creado exitosamente');
      }
      
      resetForm();
      fetchUsuarios();
    } catch (error: any) {
      console.error('Error guardando usuario:', error);
      alert(error.response?.data?.detail || 'Error al guardar el usuario');
    }
  };

  const handleEdit = (usuario: Usuario) => {
    setFormData({
      dui: usuario.dui,
      nombres: usuario.nombres,
      apellidos: usuario.apellidos,
      email: usuario.email || '',
      telefono: usuario.telefono || '',
      fecha_nacimiento: usuario.fecha_nacimiento || '',
      direccion: usuario.direccion || '',
      sector: usuario.sector,
      password: 'password123'
    });
    setEditingId(usuario.id);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      try {
        alert('Funcionalidad de eliminar no implementada en el backend');
      } catch (error) {
        console.error('Error eliminando usuario:', error);
        alert('Error al eliminar el usuario');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      dui: '',
      nombres: '',
      apellidos: '',
      email: '',
      telefono: '',
      fecha_nacimiento: '',
      direccion: '',
      sector: 'ciudadano',
      password: 'password123'
    });
    setEditingId(null);
    setShowForm(false);
  };

  // Filtrar usuarios basado en la búsqueda
  const filteredUsuarios = usuarios.filter(usuario =>
    usuario.nombres.toLowerCase().includes(searchTerm.toLowerCase()) ||
    usuario.apellidos.toLowerCase().includes(searchTerm.toLowerCase()) ||
    usuario.dui.includes(searchTerm) ||
    usuario.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Estadísticas
  const stats = {
    total: usuarios.length,
    activos: usuarios.filter(u => u.is_active !== false).length,
    porSector: usuarios.reduce((acc: {[key: string]: number}, usuario) => {
      acc[usuario.sector] = (acc[usuario.sector] || 0) + 1;
      return acc;
    }, {})
  };

  if (loading) {
    return (
      <div className="text-white flex justify-center items-center h-64">
        <div className="text-lg">Cargando usuarios...</div>
      </div>
    );
  }

  return (
    <div className="text-white p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Gestión de Usuarios</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          + Nuevo Usuario
        </button>
      </div>

      {/* Tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Total Registrados</h3>
          <p className="text-3xl font-bold text-blue-400">{stats.total}</p>
          <p className="text-gray-300 mt-2">Usuarios en el sistema</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Usuarios Activos</h3>
          <p className="text-3xl font-bold text-green-400">{stats.activos}</p>
          <p className="text-gray-300 mt-2">Activos en la plataforma</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Ciudadanos</h3>
          <p className="text-3xl font-bold text-purple-400">{stats.porSector.ciudadano || 0}</p>
          <p className="text-gray-300 mt-2">Usuarios base</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Búsqueda</h3>
          <div className="mt-2">
            <input
              type="text"
              placeholder="Buscar usuario..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 text-white placeholder-gray-400"
            />
          </div>
        </div>
      </div>

      {/* Formulario de creación/edición */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-600 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">
              {editingId ? 'Editar Usuario' : 'Nuevo Usuario'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">DUI</label>
                  <input
                    type="text"
                    value={formData.dui}
                    onChange={(e) => setFormData({...formData, dui: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                    required
                    placeholder="00000000-0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Sector</label>
                  <select
                    value={formData.sector}
                    onChange={(e) => setFormData({...formData, sector: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                    required
                  >
                    <option value="ciudadano">Ciudadano</option>
                    <option value="medico">Médico</option>
                    <option value="educativo">Educativo</option>
                    <option value="judicial">Judicial</option>
                    <option value="laboral">Laboral</option>
                    <option value="servicios_sociales">Servicios Sociales</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nombres</label>
                  <input
                    type="text"
                    value={formData.nombres}
                    onChange={(e) => setFormData({...formData, nombres: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Apellidos</label>
                  <input
                    type="text"
                    value={formData.apellidos}
                    onChange={(e) => setFormData({...formData, apellidos: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Teléfono</label>
                  <input
                    type="tel"
                    value={formData.telefono}
                    onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Fecha de Nacimiento</label>
                  <input
                    type="date"
                    value={formData.fecha_nacimiento}
                    onChange={(e) => setFormData({...formData, fecha_nacimiento: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Dirección</label>
                  <input
                    type="text"
                    value={formData.direccion}
                    onChange={(e) => setFormData({...formData, direccion: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  />
                </div>
              </div>

              {!editingId && (
                <div>
                  <label className="block text-sm font-medium mb-2">Contraseña</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                    required
                    placeholder="Mínimo 8 caracteres"
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    La contraseña por defecto es "password123"
                  </p>
                </div>
              )}

              <div className="flex space-x-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition-colors"
                >
                  {editingId ? 'Actualizar' : 'Crear'}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-3 rounded-lg font-semibold transition-colors"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tabla de usuarios */}
      <div className="bg-gray-800/50 rounded-xl border border-gray-600 overflow-hidden">
        <div className="p-4 border-b border-gray-600">
          <h3 className="text-xl font-semibold">Lista de Usuarios</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-left p-4 font-semibold">ID</th>
                <th className="text-left p-4 font-semibold">Nombre Completo</th>
                <th className="text-left p-4 font-semibold">DUI</th>
                <th className="text-left p-4 font-semibold">Sector</th>
                <th className="text-left p-4 font-semibold">Email</th>
                <th className="text-left p-4 font-semibold">Teléfono</th>
                <th className="text-left p-4 font-semibold">Estado</th>
                <th className="text-left p-4 font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsuarios.map((usuario) => (
                <tr key={usuario.id} className="border-b border-gray-600 hover:bg-gray-700/50">
                  <td className="p-4">{usuario.id}</td>
                  <td className="p-4 font-medium">
                    {usuario.nombres} {usuario.apellidos}
                  </td>
                  <td className="p-4 font-mono">{usuario.dui}</td>
                  <td className="p-4">
                    <span className={`inline-block px-2 py-1 rounded text-xs font-medium capitalize ${
                      usuario.sector === 'ciudadano' ? 'bg-blue-500/20 text-blue-400' :
                      usuario.sector === 'medico' ? 'bg-green-500/20 text-green-400' :
                      usuario.sector === 'educativo' ? 'bg-purple-500/20 text-purple-400' :
                      usuario.sector === 'judicial' ? 'bg-orange-500/20 text-orange-400' :
                      usuario.sector === 'laboral' ? 'bg-yellow-500/20 text-yellow-400' :
                      usuario.sector === 'servicios_sociales' ? 'bg-indigo-500/20 text-indigo-400' :
                      'bg-red-500/20 text-red-400'
                    }`}>
                      {usuario.sector.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="p-4">{usuario.email || '-'}</td>
                  <td className="p-4">{usuario.telefono || '-'}</td>
                  <td className="p-4">
                    <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                      usuario.is_active === false 
                        ? 'bg-red-500/20 text-red-400' 
                        : 'bg-green-500/20 text-green-400'
                    }`}>
                      {usuario.is_active === false ? 'Inactivo' : 'Activo'}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(usuario)}
                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDelete(usuario.id)}
                        className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
                      >
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredUsuarios.length === 0 && (
            <div className="text-center p-8 text-gray-400">
              {searchTerm ? 'No se encontraron usuarios' : 'No hay usuarios registrados'}
            </div>
          )}
        </div>
      </div>

      {/* Distribución por Sectores */}
      <div className="mt-8 bg-gray-800/50 rounded-xl border border-gray-600 p-6">
        <h3 className="text-xl font-semibold mb-4">Distribución por Sectores</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(stats.porSector).map(([sector, count]) => (
            <div key={sector} className="bg-gray-700/30 p-4 rounded-lg">
              <p className="text-sm text-gray-400 capitalize">{sector.replace('_', ' ')}</p>
              <p className="text-2xl font-bold text-white">{count}</p>
              <p className="text-xs text-gray-500">
                {((count / stats.total) * 100).toFixed(1)}% del total
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Usuarios;
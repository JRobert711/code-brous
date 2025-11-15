import React, { useEffect, useState } from 'react';
import { ciudadanoService, Ciudadano } from '../services/api';

const Ciudadanos: React.FC = () => {
  const [ciudadanos, setCiudadanos] = useState<Ciudadano[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    identificacion: '',
    email: '',
    telefono: ''
  });

  // Cargar ciudadanos al iniciar
  useEffect(() => {
    fetchCiudadanos();
  }, []);

  const fetchCiudadanos = async () => {
    try {
      setLoading(true);
      const response = await ciudadanoService.getAll();
      setCiudadanos(response.data);
    } catch (error) {
      console.error('Error cargando ciudadanos:', error);
      alert('Error al cargar los ciudadanos');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        // Actualizar ciudadano existente
        await ciudadanoService.update(editingId, formData);
      } else {
        // Crear nuevo ciudadano
        await ciudadanoService.create(formData);
      }
      
      resetForm();
      fetchCiudadanos();
      alert(editingId ? 'Ciudadano actualizado exitosamente' : 'Ciudadano creado exitosamente');
    } catch (error) {
      console.error('Error guardando ciudadano:', error);
      alert('Error al guardar el ciudadano');
    }
  };

  const handleEdit = (ciudadano: Ciudadano) => {
    setFormData({
      nombre: ciudadano.nombre,
      identificacion: ciudadano.identificacion,
      email: ciudadano.email || '',
      telefono: ciudadano.telefono || ''
    });
    setEditingId(ciudadano.id);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este ciudadano?')) {
      try {
        await ciudadanoService.delete(id);
        fetchCiudadanos();
        alert('Ciudadano eliminado exitosamente');
      } catch (error) {
        console.error('Error eliminando ciudadano:', error);
        alert('Error al eliminar el ciudadano');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      identificacion: '',
      email: '',
      telefono: ''
    });
    setEditingId(null);
    setShowForm(false);
  };

  // Filtrar ciudadanos basado en la búsqueda
  const filteredCiudadanos = ciudadanos.filter(ciudadano =>
    ciudadano.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ciudadano.identificacion.includes(searchTerm) ||
    ciudadano.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="text-white flex justify-center items-center h-64">
        <div className="text-lg">Cargando ciudadanos...</div>
      </div>
    );
  }

  return (
    <div className="text-white p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Gestión de Ciudadanos</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          + Nuevo Ciudadano
        </button>
      </div>

      {/* Tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Total Registrados</h3>
          <p className="text-3xl font-bold text-blue-400">{ciudadanos.length}</p>
          <p className="text-gray-300 mt-2">Ciudadanos en el sistema</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Expedientes</h3>
          <p className="text-3xl font-bold text-green-400">{ciudadanos.length}</p>
          <p className="text-gray-300 mt-2">Historial completo</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-2">Búsqueda</h3>
          <div className="mt-2">
            <input
              type="text"
              placeholder="Buscar ciudadano..."
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
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-600 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">
              {editingId ? 'Editar Ciudadano' : 'Nuevo Ciudadano'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Nombre completo</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                  className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Identificación</label>
                <input
                  type="text"
                  value={formData.identificacion}
                  onChange={(e) => setFormData({...formData, identificacion: e.target.value})}
                  className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white"
                  required
                />
              </div>
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

      {/* Tabla de ciudadanos */}
      <div className="bg-gray-800/50 rounded-xl border border-gray-600 overflow-hidden">
        <div className="p-4 border-b border-gray-600">
          <h3 className="text-xl font-semibold">Lista de Ciudadanos</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-left p-4 font-semibold">ID</th>
                <th className="text-left p-4 font-semibold">Nombre</th>
                <th className="text-left p-4 font-semibold">Identificación</th>
                <th className="text-left p-4 font-semibold">Email</th>
                <th className="text-left p-4 font-semibold">Teléfono</th>
                <th className="text-left p-4 font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredCiudadanos.map((ciudadano) => (
                <tr key={ciudadano.id} className="border-b border-gray-600 hover:bg-gray-700/50">
                  <td className="p-4">{ciudadano.id}</td>
                  <td className="p-4 font-medium">{ciudadano.nombre}</td>
                  <td className="p-4">{ciudadano.identificacion}</td>
                  <td className="p-4">{ciudadano.email || '-'}</td>
                  <td className="p-4">{ciudadano.telefono || '-'}</td>
                  <td className="p-4">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(ciudadano)}
                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDelete(ciudadano.id)}
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
          {filteredCiudadanos.length === 0 && (
            <div className="text-center p-8 text-gray-400">
              {searchTerm ? 'No se encontraron ciudadanos' : 'No hay ciudadanos registrados'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Ciudadanos;
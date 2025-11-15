import React from 'react';

const Admin: React.FC = () => {
  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">Administración del Sistema</h1>
      <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
        <h3 className="text-xl font-semibold mb-4">Panel de Control</h3>
        <p className="text-gray-300">Configuración y gestión del sistema IDN</p>
      </div>
    </div>
  );
};

export default Admin;
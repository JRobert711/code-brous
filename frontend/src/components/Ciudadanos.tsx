import React from 'react';

const Ciudadanos: React.FC = () => {
  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">Gestión de Ciudadanos</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-4">Registro Civil</h3>
          <p className="text-gray-300">Gestión de identidades digitales</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-4">Expedientes</h3>
          <p className="text-gray-300">Historial completo de ciudadanos</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-4">Búsqueda</h3>
          <p className="text-gray-300">Localizar información ciudadana</p>
        </div>
      </div>
    </div>
  );
};

export default Ciudadanos;
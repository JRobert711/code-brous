import React from 'react';

const Drones: React.FC = () => {
  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">Monitoreo con Drones</h1>
      <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
        <h3 className="text-xl font-semibold mb-4">Vigilancia en Tiempo Real</h3>
        <p className="text-gray-300">12 drones activos - 98.7% operativos</p>
      </div>
    </div>
  );
};

export default Drones;
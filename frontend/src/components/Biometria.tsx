import React from 'react';

const Biometria: React.FC = () => {
  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">Sistema Biométrico</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-4">Reconocimiento Facial</h3>
          <p className="text-gray-300">Autenticación por Face ID</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-600">
          <h3 className="text-xl font-semibold mb-4">Autenticación por Voz</h3>
          <p className="text-gray-300">Verificación mediante voz</p>
        </div>
      </div>
    </div>
  );
};

export default Biometria;
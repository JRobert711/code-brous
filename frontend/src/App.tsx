import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/common/Layout';
import Dashboard from './components/Dashboard';

// Importar todos los componentes de módulos
import Ciudadanos from './components/Ciudadanos';
import Biometria from './components/Biometria';
import Drones from './components/Drones';
import Reportes from './components/Reportes';
import Admin from './components/Admin';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/ciudadanos" element={<Ciudadanos />} />
          <Route path="/biometria" element={<Biometria />} />
          <Route path="/drones" element={<Drones />} />
          <Route path="/reportes" element={<Reportes />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
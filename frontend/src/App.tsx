import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/common/Layout';
import Dashboard from './components/Dashboard';
import Login from './components/Login';

// Importar todos los componentes de módulos
import Usuarios from './components/Usuarios';
import Biometria from './components/Biometria';
import Drones from './components/Drones';
import Reportes from './components/Reportes';
import Admin from './components/Admin';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/usuarios" element={<Usuarios />} />
          <Route path="/biometria" element={<Biometria />} />
          <Route path="/drones" element={<Drones />} />
          <Route path="/reportes" element={<Reportes />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/dashboard" element={< Dashboard/>} />
          
          
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
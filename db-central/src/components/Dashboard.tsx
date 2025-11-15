// src/components/Dashboard.tsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import type { User } from '../types';
import '../styles/Dashboard.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const user: User = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Panel de Control</h1>
        <div className="user-info">
          <span>Bienvenido, {user.name}</span>
          <button onClick={handleLogout} className="logout-btn">
            Cerrar Sesión
          </button>
        </div>
      </header>

      <div className="dashboard-grid">
        <Link to="/camera" className="dashboard-card">
          <div className="card-icon">📷</div>
          <h3>Verificación Facial</h3>
          <p>Verifica tu identidad con Face ID</p>
        </Link>

        <Link to="/drones" className="dashboard-card">
          <div className="card-icon">🚁</div>
          <h3>Monitoreo de Drones</h3>
          <p>Supervisa flota de drones en tiempo real</p>
        </Link>

        <div className="dashboard-card">
          <div className="card-icon">📊</div>
          <h3>Reportes</h3>
          <p>Genera reportes de actividad</p>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">⚙️</div>
          <h3>Configuración</h3>
          <p>Ajusta preferencias del sistema</p>
        </div>
      </div>

      <div className="quick-stats">
        <h2>Estadísticas Rápidas</h2>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-number">12</span>
            <span className="stat-label">Drones Activos</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">98%</span>
            <span className="stat-label">Eficiencia</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">24/7</span>
            <span className="stat-label">Operación</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

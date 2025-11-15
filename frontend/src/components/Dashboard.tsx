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
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">🚁</div>
            <div className="title">
              <h1>Sistema de Monitoreo</h1>
              <p>Ministerio de Seguridad Nacional</p>
            </div>
          </div>
          <div className="user-info">
            <div className="user-details">
              <span className="user-name">Bienvenido, {user.name || 'Usuario'}</span>
              <span className="user-role">Operador Autorizado</span>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <div className="dashboard-main">
        <div className="sidebar">
          <nav className="sidebar-nav">
            <Link to="/dashboard" className="nav-item active">
              <span className="nav-icon">📊</span>
              <span className="nav-text">Dashboard</span>
            </Link>
            <Link to="/camera" className="nav-item">
              <span className="nav-icon">📷</span>
              <span className="nav-text">Verificación Facial</span>
            </Link>
            <Link to="/drones" className="nav-item">
              <span className="nav-icon">🚁</span>
              <span className="nav-text">Monitoreo de Drones</span>
            </Link>
            <div className="nav-item">
              <span className="nav-icon">📋</span>
              <span className="nav-text">Reportes</span>
            </div>
            <div className="nav-item">
              <span className="nav-icon">⚙️</span>
              <span className="nav-text">Configuración</span>
            </div>
          </nav>
        </div>

        <div className="dashboard-content">
          <div className="content-header">
            <h2>Panel de Control Principal</h2>
            <div className="status-indicators">
              <div className="status-item online">
                <span className="status-dot"></span>
                Sistema Online
              </div>
              <div className="status-item active">
                <span className="status-dot"></span>
                12 Drones Activos
              </div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">🚁</div>
              <div className="stat-info">
                <h3>Total Drones</h3>
                <span className="stat-number">24</span>
                <span className="stat-label">Unidades registradas</span>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">🟢</div>
              <div className="stat-info">
                <h3>En Operación</h3>
                <span className="stat-number">12</span>
                <span className="stat-label">Misiones activas</span>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">⚡</div>
              <div className="stat-info">
                <h3>Eficiencia</h3>
                <span className="stat-number">98%</span>
                <span className="stat-label">Tasa de éxito</span>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">🕒</div>
              <div className="stat-info">
                <h3>Uptime</h3>
                <span className="stat-number">99.9%</span>
                <span className="stat-label">Disponibilidad</span>
              </div>
            </div>
          </div>

          <div className="quick-actions">
            <h3>Acciones Rápidas</h3>
            <div className="actions-grid">
              <Link to="/camera" className="action-card">
                <div className="action-icon">📷</div>
                <h4>Verificación Facial</h4>
                <p>Verificar identidad con Face ID</p>
              </Link>
              
              <Link to="/drones" className="action-card">
                <div className="action-icon">🚁</div>
                <h4>Control de Drones</h4>
                <p>Monitoreo en tiempo real</p>
              </Link>
              
              <div className="action-card">
                <div className="action-icon">📡</div>
                <h4>Desplegar Flota</h4>
                <p>Iniciar misión coordinada</p>
              </div>
              
              <div className="action-card">
                <div className="action-icon">🚨</div>
                <h4>Modo Emergencia</h4>
                <p>Protocolos de seguridad</p>
              </div>
            </div>
          </div>

          <div className="recent-activity">
            <h3>Actividad Reciente</h3>
            <div className="activity-list">
              <div className="activity-item">
                <div className="activity-icon success">✓</div>
                <div className="activity-content">
                  <p>Drone DJI-004 completó patrulla zona norte</p>
                  <span className="activity-time">Hace 5 minutos</span>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon warning">⚠</div>
                <div className="activity-content">
                  <p>Batería baja en Drone AUTEL-007</p>
                  <span className="activity-time">Hace 12 minutos</span>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon info">ℹ</div>
                <div className="activity-content">
                  <p>Nuevo operador autenticado: Carlos Rodríguez</p>
                  <span className="activity-time">Hace 25 minutos</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
// src/components/DroneMonitor.tsx
import React, { useState, useEffect } from 'react';
import type { Drone } from '../types';
import '../styles/DroneMonitor.css';

const DroneMonitor: React.FC = () => {
  const [drones, setDrones] = useState<Drone[]>([]);
  const [selectedDrone, setSelectedDrone] = useState<Drone | null>(null);

  // Datos simulados - en una app real esto vendría de una API
  useEffect(() => {
    const mockDrones: Drone[] = [
      {
        id: '1',
        name: 'DJI Mavic 3',
        status: 'active',
        battery: 85,
        location: { lat: 40.7128, lng: -74.0060 }
      },
      {
        id: '2',
        name: 'Autel Evo II',
        status: 'active',
        battery: 45,
        location: { lat: 34.0522, lng: -118.2437 }
      },
      {
        id: '3',
        name: 'Parrot Anafi',
        status: 'maintenance',
        battery: 100,
        location: { lat: 41.8781, lng: -87.6298 }
      },
      {
        id: '4',
        name: 'Skydio 2',
        status: 'inactive',
        battery: 0,
        location: { lat: 29.7604, lng: -95.3698 }
      }
    ];

    setDrones(mockDrones);
  }, []);

  const getStatusColor = (status: Drone['status']) => {
    switch (status) {
      case 'active': return '#4CAF50';
      case 'inactive': return '#f44336';
      case 'maintenance': return '#FF9800';
      default: return '#757575';
    }
  };

  const getBatteryColor = (battery: number) => {
    if (battery > 70) return '#4CAF50';
    if (battery > 30) return '#FF9800';
    return '#f44336';
  };

  return (
    <div className="drone-monitor-container">
      <header className="monitor-header">
        <h1>Monitoreo de Drones</h1>
        <div className="status-summary">
          <span className="active-count">
            {drones.filter(d => d.status === 'active').length} Activos
          </span>
          <span className="total-count">
            {drones.length} Total
          </span>
        </div>
      </header>

      <div className="monitor-content">
        <div className="drones-list">
          <h2>Flota de Drones</h2>
          {drones.map(drone => (
            <div 
              key={drone.id}
              className={`drone-card ${selectedDrone?.id === drone.id ? 'selected' : ''}`}
              onClick={() => setSelectedDrone(drone)}
            >
              <div className="drone-header">
                <h3>{drone.name}</h3>
                <span 
                  className="status-badge"
                  style={{ backgroundColor: getStatusColor(drone.status) }}
                >
                  {drone.status}
                </span>
              </div>
              
              <div className="drone-info">
                <div className="battery-info">
                  <span>Batería:</span>
                  <div className="battery-bar">
                    <div 
                      className="battery-level"
                      style={{ 
                        width: `${drone.battery}%`,
                        backgroundColor: getBatteryColor(drone.battery)
                      }}
                    ></div>
                  </div>
                  <span>{drone.battery}%</span>
                </div>
                
                <div className="location-info">
                  <span>Ubicación:</span>
                  <span>{drone.location.lat.toFixed(4)}, {drone.location.lng.toFixed(4)}</span>
                </div>
              </div>

              <div className="drone-actions">
                <button className="action-btn view">Ver Detalles</button>
                <button 
                  className="action-btn control"
                  disabled={drone.status !== 'active'}
                >
                  Controlar
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="monitor-panel">
          {selectedDrone ? (
            <div className="drone-details">
              <h2>Detalles del Drone</h2>
              <div className="detail-section">
                <h3>Información General</h3>
                <div className="detail-item">
                  <span>Nombre:</span>
                  <span>{selectedDrone.name}</span>
                </div>
                <div className="detail-item">
                  <span>Estado:</span>
                  <span className="status-text" style={{ color: getStatusColor(selectedDrone.status) }}>
                    {selectedDrone.status}
                  </span>
                </div>
                <div className="detail-item">
                  <span>Batería:</span>
                  <span style={{ color: getBatteryColor(selectedDrone.battery) }}>
                    {selectedDrone.battery}%
                  </span>
                </div>
              </div>

              <div className="detail-section">
                <h3>Ubicación</h3>
                <div className="map-placeholder">
                  📍 Lat: {selectedDrone.location.lat.toFixed(6)}
                  <br />
                  📍 Lng: {selectedDrone.location.lng.toFixed(6)}
                </div>
              </div>

              <div className="detail-section">
                <h3>Acciones</h3>
                <div className="action-buttons">
                  <button className="btn primary">Iniciar Vuelo</button>
                  <button className="btn secondary">Programar Ruta</button>
                  <button className="btn warning">Regreso a Base</button>
                  <button className="btn danger">Emergencia</button>
                </div>
              </div>
            </div>
          ) : (
            <div className="no-selection">
              <h3>Selecciona un drone</h3>
              <p>Haz clic en un drone de la lista para ver sus detalles y controles</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DroneMonitor;
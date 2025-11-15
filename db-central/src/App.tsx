import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import VoiceLogin from './components/VoiceLogin.tsx';
import Dashboard from './components/Dashboard';
import DroneMonitor from './components/DroneMonitor';
import './styles/App.css';

const CameraComponent: React.FC = () => {
  return <div>Camera</div>;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              isAuthenticated ? 
              <Navigate to="/dashboard" /> : 
              <VoiceLogin onLoginSuccess={() => setIsAuthenticated(true)} />
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              isAuthenticated ? 
              <Dashboard /> : 
              <Navigate to="/" />
            } 
          />
          <Route 
            path="/camera" 
            element={
              isAuthenticated ? 
              <CameraComponent /> : 
              <Navigate to="/" />
            } 
          />
          <Route 
            path="/drones" 
            element={
              isAuthenticated ? 
              <DroneMonitor /> : 
              <Navigate to="/" />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
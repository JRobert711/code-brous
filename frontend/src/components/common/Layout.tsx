import React from "react";
import { Link, useLocation } from "react-router-dom";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A1428] via-[#1E3A5F] to-[#006DFF] flex flex-col text-white overflow-hidden">
      {/* Fondo con efectos de partículas */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-[#006DFF] rounded-full blur-[120px] opacity-20"></div>
        <div className="absolute bottom-1/3 right-1/3 w-[400px] h-[400px] bg-[#003366] rounded-full blur-[90px] opacity-25"></div>
        <div className="absolute top-1/2 left-1/2 w-[300px] h-[300px] bg-[#0047AB] rounded-full blur-[70px] opacity-15"></div>
      </div>

      {/* HEADER - Estilo Ministerio */}
      <header className="bg-[#0A1428]/95 backdrop-blur-md border-b border-[#006DFF]/30 text-white pt-4 pb-3 relative z-10 shadow-2xl">
        <div className="container mx-auto px-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            {/* Logo y Título */}
            <div className="flex items-center justify-center lg:justify-start mb-4 lg:mb-0">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-r from-[#006DFF] to-[#0047AB] rounded-lg flex items-center justify-center shadow-lg">
                  <span className="text-white font-bold text-lg">IDN</span>
                </div>
                <div className="text-center lg:text-left">
                  <h1 className="text-xl font-bold text-white">IDENTIDAD DIGITAL NACIONAL</h1>
                  <p className="text-sm text-gray-300">Ministerio de Seguridad Pública y Justicia</p>
                </div>
              </div>
            </div>

            {/* Navegación */}
            <nav className="flex flex-wrap gap-2 justify-center lg:justify-end relative">
              {[
                { path: "/", label: "INICIO" },
                { path: "/ciudadanos", label: "CIUDADANOS" },
                { path: "/biometria", label: "BIOMETRÍA" },
                { path: "/drones", label: "VIGILANCIA" },
                { path: "/reportes", label: "REPORTES" },
                { path: "/admin", label: "ADMINISTRACIÓN" },
              ].map(({ path, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-300 transform hover:scale-105 border ${
                    isActive(path)
                      ? "bg-gradient-to-r from-[#006DFF] to-[#0047AB] text-white shadow-lg shadow-[#006DFF]/40 border-transparent"
                      : "bg-transparent text-white border-[#006DFF]/50 hover:bg-[#006DFF]/20 hover:border-[#006DFF] hover:shadow-lg hover:shadow-[#006DFF]/20"
                  }`}
                >
                  {label}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Barra de Estado */}
      <div className="bg-[#003366]/80 backdrop-blur-sm border-b border-[#006DFF]/20 py-2 relative z-10">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400">Sistema Operativo</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Drones Conectados: <strong>12</strong></span>
              </div>
            </div>
            <div className="text-gray-300">
              {new Date().toLocaleDateString('es-SV', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </div>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <main className="flex-1 container mx-auto px-6 py-8 relative z-10">
        <div className="backdrop-blur-md bg-[#0A1428]/70 rounded-2xl border border-[#006DFF]/30 shadow-2xl p-8 transition-all duration-500 hover:border-[#006DFF]/50 hover:shadow-[0_0_40px_rgba(0,109,255,0.3)]">
          {children}
        </div>
      </main>

      {/* FOOTER */}
      <footer className="bg-[#0A1428]/95 backdrop-blur-md border-t border-[#006DFF]/30 text-white py-6 relative z-10">
        <div className="container mx-auto px-6">
          <div className="flex flex-col lg:flex-row items-center justify-between">
            {/* Información Institucional */}
            <div className="text-center lg:text-left mb-4 lg:mb-0">
              <h3 className="font-bold text-lg mb-2">Sistema de Identidad Digital Nacional</h3>
              <p className="text-gray-400 text-sm">
                Ministerio de Seguridad Pública y Justicia • El Salvador, Centroamérica
              </p>
            </div>

            {/* Enlaces Legales */}
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <Link to="/privacidad" className="text-gray-400 hover:text-white transition-colors">
                Política de Privacidad
              </Link>
              <Link to="/terminos" className="text-gray-400 hover:text-white transition-colors">
                Términos de Servicio
              </Link>
              <Link to="/contacto" className="text-gray-400 hover:text-white transition-colors">
                Contacto
              </Link>
            </div>

            {/* Estado del Sistema */}
            <div className="flex items-center space-x-2 mt-4 lg:mt-0">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-green-400 text-sm">Sistema en Línea</span>
            </div>
          </div>
          
          {/* Derechos de Autor */}
          <div className="border-t border-[#006DFF]/20 mt-4 pt-4 text-center">
            <p className="text-gray-500 text-xs">
              © 2024 Gobierno de El Salvador. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
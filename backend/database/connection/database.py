# backend/database/connection/database.py
import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="../db-central/idn_sv.db"):
        # Asegurar que la carpeta existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Crear todas las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dui TEXT UNIQUE NOT NULL,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                email TEXT,
                fecha_nacimiento DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de perfiles de voz
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                voice_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabla de drones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                estado TEXT DEFAULT 'activo',
                ubicacion_lat REAL,
                ubicacion_lng REAL,
                bateria INTEGER DEFAULT 100,
                ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de logs de seguridad
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                accion TEXT NOT NULL,
                descripcion TEXT,
                ip_address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar datos de ejemplo
        self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
        print("✅ Base de datos SQLite inicializada correctamente")
    
    def insert_sample_data(self, cursor):
        """Insertar datos de ejemplo"""
        try:
            # Usuarios de ejemplo
            usuarios = [
                ('12345678-9', 'Juan Carlos', 'Pérez García', 'juan.perez@example.com', '1990-05-15'),
                ('98765432-1', 'María Elena', 'López Martínez', 'maria.lopez@example.com', '1985-08-22'),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO usuarios (dui, nombres, apellidos, email, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?)
            ''', usuarios)
            
            # Drones de ejemplo
            drones = [
                ('DRONE-001', 'activo', 13.6929, -89.2182, 85),
                ('DRONE-002', 'activo', 13.7000, -89.2000, 92),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO drones (nombre, estado, ubicacion_lat, ubicacion_lng, bateria)
                VALUES (?, ?, ?, ?, ?)
            ''', drones)
            
            print("✅ Datos de ejemplo insertados")
        except Exception as e:
            print(f"⚠️ Error insertando datos de ejemplo: {e}")

    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(self.db_path)

# Instancia global de la base de datos
db_manager = DatabaseManager()
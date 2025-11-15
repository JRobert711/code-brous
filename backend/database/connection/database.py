# backend/database/connection/database.py
import sqlite3
import os
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_path="../db-central/idn_sv.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de usuarios con varios tipos de identificación
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Aquí permitimos TODOS los tipos de identificación
                tipo_identificacion TEXT NOT NULL,
                numero_identificacion TEXT NOT NULL UNIQUE,

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
        
        # Tabla logs
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
        
        # Insertar datos iniciales
        self.insert_sample_data(cursor)

        conn.commit()
        conn.close()
        print("✅ Base de datos actualizada con soporte para múltiples identificaciones.")
    
    def insert_sample_data(self, cursor):
        try:
            usuarios = [
                # (tipo_identificacion, numero_identificacion, nombres, apellidos, email, fecha_nacimiento)
                ('DUI', '12345678-9', 'Juan Carlos', 'Pérez García', 'juan.perez@example.com', '1990-05-15'),
                ('DUI', '98765432-1', 'María Elena', 'López Martínez', 'maria.lopez@example.com', '1985-08-22'),

                # Ejemplos de otros métodos
                ('NIT', '0614-250786-102-3', 'Pedro Antonio', 'Ramírez Torres', 'pedro.ramirez@example.com', '1986-07-25'),
                ('CARNET_MENORIDAD', 'MN-202455', 'Lucas Andrés', 'Gómez Ruiz', None, '2011-03-14'),
                ('CARNET_RECIEN_NACIDO', 'RN-998877', 'Bebé', 'Recien Nacido', None, '2024-01-12'),
                ('CARNET_ESCOLAR', 'CE-55221', 'Valeria Sofía', 'Martínez López', 'valeria.martinez@example.com', '2008-11-20'),
                ('LICENCIA', 'B1234567', 'Carlos Alberto', 'Hernández Díaz', 'carlos.hernandez@example.com', '1992-04-10'),
                ('PASAPORTE', 'A12345678', 'Ana Patricia', 'Morales Pérez', 'ana.morales@example.com', '1994-12-01'),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO usuarios 
                (tipo_identificacion, numero_identificacion, nombres, apellidos, email, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', usuarios)

            drones = [
                ('DRONE-001', 'activo', 13.6929, -89.2182, 85),
                ('DRONE-002', 'activo', 13.7000, -89.2000, 92),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO drones (nombre, estado, ubicacion_lat, ubicacion_lng, bateria)
                VALUES (?, ?, ?, ?, ?)
            ''', drones)

        except Exception as e:
            print(f"⚠️ Error al insertar datos iniciales: {e}")

    def get_connection(self):
        return sqlite3.connect(self.db_path)

db_manager = DatabaseManager()

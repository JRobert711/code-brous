import sqlite3
import os

def init_database():
    """Crear base de datos inicial"""
    conn = sqlite3.connect("idn_sv.db")
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
    
    # Datos de ejemplo
    usuarios = [
        ('12345678-9', 'Juan Carlos', 'Pérez García', 'juan.perez@example.com', '1990-05-15'),
        ('98765432-1', 'María Elena', 'López Martínez', 'maria.lopez@example.com', '1985-08-22'),
    ]
    
    for usuario in usuarios:
        cursor.execute(
            "INSERT OR IGNORE INTO usuarios (dui, nombres, apellidos, email, fecha_nacimiento) VALUES (?, ?, ?, ?, ?)",
            usuario
        )
    
    drones = [
        ('DRONE-001', 'activo', 13.6929, -89.2182, 85),
        ('DRONE-002', 'activo', 13.7000, -89.2000, 92),
    ]
    
    for drone in drones:
        cursor.execute(
            "INSERT OR IGNORE INTO drones (nombre, estado, ubicacion_lat, ubicacion_lng, bateria) VALUES (?, ?, ?, ?, ?)",
            drone
        )
    
    conn.commit()
    conn.close()
    print("✅ Base de datos SQLite creada con datos de ejemplo")

if __name__ == "__main__":
    init_database()
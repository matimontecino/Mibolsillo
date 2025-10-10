# registrar_usuario.py
import sys
import os
sys.path.insert(0, os.path.abspath("."))

from app.SQL.SQL import SessionLocal
from app.SQL.security.hash import hash_password
from sqlalchemy import text

def crear_usuario(nombre: str, email: str, password: str):
    db = SessionLocal()
    try:
        # Hashea la contraseña
        hashed_pw = hash_password(password)
        
        # Inserta en la base de datos
        query = text("""
            INSERT INTO usuarios (nombre, email, password, activo)
            VALUES (:nombre, :email, :password, TRUE)
            RETURNING id, email;
        """)
        
        result = db.execute(query, {
            "nombre": nombre,
            "email": email,
            "password": hashed_pw
        })
        
        usuario = result.fetchone()
        db.commit()
        
        print(f"✅ Usuario creado: {usuario.email} (ID: {usuario.id})")
        print(f"🔒 Contraseña hasheada: {hashed_pw[:30]}...")
        
    except Exception as e:
        db.rollback()
        print("❌ Error al crear usuario:", e)
    finally:
        db.close()

# Ejecuta el registro
if __name__ == "__main__":
    crear_usuario(
        nombre="Matías",
        email="matias@example.com",
        password="miClave123"
    )
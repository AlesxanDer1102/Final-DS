# User service modificado para usar PostgreSQL y FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="User Service")
# Coneccion a la base de datos PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres-service"),
        database=os.getenv("DB_NAME", "parcial_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "12345")
    )
# Modelo del usuario
class User(BaseModel):
    id: int      # Identificador único del usuario
    name: str    # Nombre del usuario
    email: str   # Correo electrónico del usuario
# Endpoint para crear usuario
@app.post("/users/", response_model=User)
def create_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
                   (user.id, user.name, user.email))
        conn.commit()
        return user
    except psycopg2.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        cur.close()
        conn.close()
# Endpoint para listar usuarios
@app.get("/users/")
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, email FROM users")
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cur.fetchall()]
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    finally:
        cur.close()
        conn.close()
# Endpoint para obtener un usuario por ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": row[0], "name": row[1], "email": row[2]}
    finally:
        cur.close()
        conn.close()
# Endpoint para eliminar un usuario
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return {"detail": "User deleted"}
    finally:
        cur.close()
        conn.close()
# Endpoint de health check
@app.get("/health")
def health():
    return {"status": "ok"}
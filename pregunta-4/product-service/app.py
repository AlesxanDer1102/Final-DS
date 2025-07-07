# Product service modificado para usar PostgreSQL y FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="Product Service")
# Coneccion a la base de datos PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres-service"),
        database=os.getenv("DB_NAME", "parcial_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "12345")
    )
# Modelo del producto
class Product(BaseModel):
    id: int
    name: str
    quantity: int
# Endpoint para crear producto
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products (id, name, quantity) VALUES (%s, %s, %s)",
                   (product.id, product.name, product.quantity))
        conn.commit()
        return product
    except psycopg2.IntegrityError:
        raise HTTPException(status_code=400, detail="Product already exists")
    finally:
        cur.close()
        conn.close()
# Endpoint para listar productos
@app.get("/products/")
def list_products():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, quantity FROM products")
        products = [{"id": row[0], "name": row[1], "quantity": row[2]} for row in cur.fetchall()]
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products
    finally:
        cur.close()
        conn.close()
# Endpoint para obtener un producto por ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, quantity FROM products WHERE id = %s", (product_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": row[0], "name": row[1], "quantity": row[2]}
    finally:
        cur.close()
        conn.close()
# Endpoint para actualizar un producto
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        return {"detail": "Product deleted"}
    finally:
        cur.close()
        conn.close()
# Endpoint de hellth check
@app.get("/health")
def health():
    return {"status": "ok"}
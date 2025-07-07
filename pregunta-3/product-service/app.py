from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Product Service")

# "Base de datos" en memoria usando un diccionario
products: Dict[int, Dict] = {}

class Product(BaseModel):
    id: int        # Identificador único del producto
    name: str      # Nombre del producto
    quantity: int  # Cantidad de productos disponibles

@app.post("/products/", response_model=Product)
def create_product(product: Product):
    # Comprueba si el producto ya existe
    if product.id in products:
        raise HTTPException(status_code=400, detail="Product already exists")
    # Guarda el producto en la "base de datos"
    products[product.id] = product.dict()
    return product

@app.get("/products/", response_model=List[Product])
def list_products():
    # Verifica si hay productos en la "base de datos"
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    # Devuelve la lista de productos
    return list(products.values())

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    # Verifica si el producto existe
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    # Devuelve el producto encontrado
    return products[product_id]

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    # Comprueba si el producto existe antes de eliminar
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    # Elimina el producto  de la "base de datos"
    del products[product_id]
    return {"detail": "Product deleted"}

# Punto de comprobación de salud del servicio
@app.get("/health")
def health():
    return {"status": "ok"}
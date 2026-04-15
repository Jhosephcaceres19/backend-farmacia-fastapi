from fastapi import FastAPI
from pydantic import BaseModel, field_validator


app = FastAPI()

producto = []

class Producto(BaseModel):
    nombre:str
    price: float
    score: int
    description: str |None = None

    @field_validator("nombre")
    def validar_nombre(cls, value):
        if len(value) < 3:
            raise ValueError("El producto debe tener mas de 3 caracteeres")
        return value
    
    @field_validator("description")
    def validar_descripcion(cls, value):
        if len(value) < 3:
            raise ValueError("La descripcion debe tener mas de 3 caracteres")
        return value
    
    @field_validator("price")
    def validar_precio(cls, value):
        if value < 0 :
            raise ValueError("El precio debe ser mayo que 0")
        return value
    
    @field_validator("score")
    def validar_cantidad(cls, value):
        if value < 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        
@app.post("/produto")
async def crear_producto(product:Producto):
    producto.append(product)
    return product


@app.get("/producto")
async def ver_producto():
    return{
        "Produtos": producto
    }


@app.put("/producto/{id}")
async def actualizar_producto(id:int, product:Producto):
    if id < 0 or id>=len(producto):
        return{"error": "producto no encontrado"}
    
    producto[id] = product
    return product


@app.delete("producto/{id}")
async def eliminar_producto(id:int):
    if id < 0 or id >= len(producto):
        return{"error":"No se encontro el producto"}
    producto_eliminado = producto.pop(id)
    return{
        "Producto eliminaod": producto_eliminado
    }


@app.get("producto/{id}")
async def obtener_un_producto(id:int):
    if id < 0 or len(producto):
        return {"error": "Producto no encontrado"}
    return producto[id]
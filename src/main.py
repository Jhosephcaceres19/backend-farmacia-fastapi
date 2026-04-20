from fastapi import FastAPI, Depends
from pydantic import BaseModel, field_validator
from src.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from src.model import Farmacia




app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        if  value is not None and len(value) < 3:
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
        return value
    



        
@app.post("/producto")
async def crear_producto(product:Producto, db: Session = Depends(get_db)):
    nuevo =  Farmacia(**product.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.get("/producto")
async def ver_producto(db:Session = Depends(get_db)):
    return db.query(Farmacia).all()


@app.put("/producto/{id}")
async def actualizar_producto(id: int, product: Producto, db: Session = Depends(get_db)):
    producto_db = db.query(Farmacia).filter(Farmacia.id == id).first()

    if not producto_db:
        return {"error": "Producto no encontrado"}

    for key, value in product.model_dump().items():
        setattr(producto_db, key, value)

    db.commit()
    db.refresh(producto_db)

    return producto_db


@app.delete("/producto/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Farmacia).filter(Farmacia.id == id).first()

    if not producto:
        return {"error": "Producto no encontrado"}

    db.delete(producto)
    db.commit()

    return {"mensaje": "Producto eliminado"}


@app.get("/producto/{id}")
async def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Farmacia).filter(Farmacia.id == id).first()

    if not producto:
        return {"error": "Producto no encontrado"}

    return producto
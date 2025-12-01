from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# ¡No más código complejo para ObjectId!

class Titulo(BaseModel):
    model_config = {"populate_by_name": True}
    numero_titulo: str = Field(alias="nmroDeTitulo")
    ano_expedicion: int = Field(alias="anoDeExpedicion")
    tipo_titulo: str = Field(alias="tipoDeTitulo")

class Pago(BaseModel):
    monto: float
    fecha: datetime
    concepto: str

class Curso(BaseModel):
    model_config = {"populate_by_name": True}
    id_curso: str = Field(alias="idCurso")
    nombre_curso: str = Field(alias="nombreCurso")

class EstudianteCreate(BaseModel):
    model_config = {"populate_by_name": True}
    usuario: str = Field(..., alias="registro")
    contrasena: str
    ci: str = Field(..., alias="CI")
    extension: str
    nombre: str
    celular: str
    carrera: str
    correo: EmailStr
    fecha_nacimiento: datetime = Field(..., alias="fechaNacimiento")
    domicilio: str
    foto: Optional[str] = None
    lista_de_cursos: List[Curso] = Field(default=[], alias="listaDeCursos")
    lista_de_pagos: List[Pago] = Field(default=[], alias="listaDePagos")
    lista_de_titulos: List[Titulo] = Field(default=[], alias="listaDeTitulos")

class EstudianteUpdate(BaseModel):
    model_config = {"populate_by_name": True}
    nombre: Optional[str] = None
    celular: Optional[str] = None
    carrera: Optional[str] = None
    correo: Optional[EmailStr] = None
    domicilio: Optional[str] = None
    foto: Optional[str] = None
    lista_de_cursos: Optional[List[Curso]] = Field(None, alias="listaDeCursos")
    lista_de_pagos: Optional[List[Pago]] = Field(None, alias="listaDePagos")
    lista_de_titulos: Optional[List[Titulo]] = Field(None, alias="listaDeTitulos")

class EstudianteResponse(BaseModel):
    model_config = {"populate_by_name": True}
    # --- LA MAGIA ESTÁ AQUÍ: El ID ahora es un simple string ---
    id: str = Field(alias="_id") 
    
    usuario: str = Field(..., alias="registro")
    ci: str = Field(..., alias="CI")
    extension: str
    nombre: str
    celular: str
    carrera: str
    correo: EmailStr
    fecha_nacimiento: datetime = Field(alias="fechaNacimiento")
    domicilio: str
    foto: Optional[str] = None
    lista_de_cursos: List[Curso] = Field(alias="listaDeCursos")
    lista_de_pagos: List[Pago] = Field(alias="listaDePagos")
    lista_de_titulos: List[Titulo] = Field(alias="listaDeTitulos")
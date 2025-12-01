from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from bson import ObjectId

from ..db.database import estudiante_collection
from ..schemas.estudiante_schema import (
    EstudianteCreate,
    EstudianteUpdate,
    EstudianteResponse,
)

router = APIRouter()

@router.post("/", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
async def create_estudiante(estudiante: EstudianteCreate = Body(...)):
    estudiante_dict = estudiante.model_dump(by_alias=True)
    if await estudiante_collection.find_one({"registro": estudiante_dict["registro"]}):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
    if await estudiante_collection.find_one({"CI": estudiante_dict["CI"]}):
        raise HTTPException(status_code=400, detail="La Cédula de Identidad ya está registrada.")

    new_estudiante = await estudiante_collection.insert_one(estudiante_dict)
    created_estudiante = await estudiante_collection.find_one({"_id": new_estudiante.inserted_id})
    
    # Convertimos el ObjectId a string antes de devolverlo
    created_estudiante["_id"] = str(created_estudiante["_id"])
    return created_estudiante

@router.get("/", response_model=List[EstudianteResponse])
async def get_all_estudiantes():
    estudiantes = await estudiante_collection.find().to_list(1000)
    # Convertimos el ObjectId de cada estudiante a string
    for est in estudiantes:
        est["_id"] = str(est["_id"])
    return estudiantes

@router.get("/{id}", response_model=EstudianteResponse)
async def get_estudiante_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"El ID '{id}' no es válido.")
    
    estudiante = await estudiante_collection.find_one({"_id": ObjectId(id)})
    if estudiante is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID '{id}' no encontrado.")
    
    # Convertimos el ObjectId a string antes de devolverlo
    estudiante["_id"] = str(estudiante["_id"])
    return estudiante

@router.put("/{id}", response_model=EstudianteResponse)
async def update_estudiante(id: str, estudiante_update: EstudianteUpdate = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"El ID '{id}' no es válido.")
    update_data = estudiante_update.model_dump(by_alias=True, exclude_unset=True)
    if len(update_data) < 1:
        raise HTTPException(status_code=400, detail="El cuerpo de la solicitud no puede estar vacío.")

    await estudiante_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    updated_student = await estudiante_collection.find_one({"_id": ObjectId(id)})
    if updated_student is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID '{id}' no encontrado.")
        
    # Convertimos el ObjectId a string antes de devolverlo
    updated_student["_id"] = str(updated_student["_id"])
    return updated_student

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estudiante(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"El ID '{id}' no es válido.")
    
    delete_result = await estudiante_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID '{id}' no encontrado.")
    return
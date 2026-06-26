from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import  engine, get_db
from typing import List
import models,schemas,crud

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.post("/patients/",response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate,db:Session = Depends(get_db)):
    regular_patient =  crud.create_patient(db,patient)
    if not regular_patient:
        raise HTTPException(400,"Phone number already registered")
    return patient 

@app.get("/patients/",response_model=List[schemas.PatientResponse])
def get_patients(db:Session= Depends(get_db)):
    return crud.get_patients(db)

@app.get("/patients/doctor{doctor_name}",response_model=List[schemas.PatientResponse])
def get_doctor( doctor_name: str, db:Session = Depends(get_db)):
    doctor =  crud.get_doctor(db,doctor_name)
    if not doctor:
        raise HTTPException(404,"Doctor not found")
    return doctor 

@app.get("/patients/{patient_id}",response_model=schemas.PatientResponse)
def get_patient( patient_id:int, db:Session = Depends(get_db)):
    patient = crud.get_patient(db,patient_id)
    if not patient:
        raise HTTPException(404,"Patient not found")
    return patient 


@app.put("/patients/{patient_id}",response_model=schemas.PatientResponse)
def update_patient(patient_id:int,data:schemas.PatientUpdate,db:Session = Depends(get_db)):
    patient_updated = crud.update_patient(db,patient_id,data)
    if not patient_updated:
        raise HTTPException(404,"Patient not found")
    return patient_updated

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int,db:Session = Depends(get_db)):
    patient = crud.delete_patient(db,patient_id)
    if not patient:
        raise HTTPException(404,"Patient not found")
    return {"message":"Patient deleted successfully"}

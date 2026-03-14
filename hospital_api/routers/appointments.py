from fastapi import APIRouter , HTTPException
from hospital_api.model import Appointment
from fastapi.responses import JSONResponse
from pathlib import Path
import json
router=APIRouter()

BASE_URL=Path(__file__).resolve().parent.parent
DATA_FILE=BASE_URL/'data'/'appiontment.json'
PATIENT_FILE=BASE_URL/'data'/'patient.json'
DOCTOR_FILE=BASE_URL/'data'/'doctor.json'

def load_data(file_path):
    try:
        with open(file_path,'r')as f:
            data=json.load(f)
            return data
    except:
        return {}
    
def save_data(file_path,data):
    with open(file_path,'w') as f:
        json.dump(data,f)

@router.post('/create')
def create_appointment(appointment:Appointment):

    appointment_data=load_data(DATA_FILE)
    patient=load_data(PATIENT_FILE)
    doctor=load_data(DOCTOR_FILE)
    if appointment.patient_id not in patient:
        raise HTTPException(status_code=404,detail="Invalid paitient_id ,patient does not exict")
    if appointment.doctor_id not in doctor:
        raise HTTPException(status_code=404,detail="Invalid doctor id , doctor doesn't exist" )
    if appointment.id in appointment_data:
        raise HTTPException(status_code=404,detail="Appointment alread exist")
    appointment_data[appointment.id]=appointment.model_dump(exclude=['id'],mode="json")


    save_data(DATA_FILE,appointment_data)

    return JSONResponse(status_code=200,content={'message':'appointment created successfully'})

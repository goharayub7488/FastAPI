from fastapi import APIRouter , HTTPException , Query
from fastapi import Path as APIPath
from hospital_api.model import Appointment , UpdateAppointment
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

@router.put('/edit/{appoint_id}')
def update_appoint(appoint_id:str,appointUpdate:UpdateAppointment):
    data=load_data(DATA_FILE)
    if appoint_id not in data:
        raise HTTPException(status_code=404,detail="Invalid Appointment id")
    existing_appoint_info=data[appoint_id]
    update_appoint_info=appointUpdate.model_dump(exclude_unset=True,mode='json')

    for key,value in update_appoint_info.items():
        existing_appoint_info[key]=value
    data[appoint_id]=existing_appoint_info
    save_data(DATA_FILE,data)

    return JSONResponse(status_code=200,content={'message':'Appointment updated successfully'})

@router.get('/view')
def view_appointment():
    data=load_data(DATA_FILE)
    return data

@router.get('/view/{appoint_id}')
def view_single_appoint(appoint_id:str = APIPath(...,description="Enter the appointment id to get particular appointment",examples=['App-1'])):
    data =load_data(DATA_FILE)
    if appoint_id not in data:
        raise HTTPException(status_code=404,detail="Appointment does not exist")
    return data[appoint_id]

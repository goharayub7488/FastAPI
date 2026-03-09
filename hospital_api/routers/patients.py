from fastapi import HTTPException , APIRouter ,Query
from fastapi import Path as FastAPIPath

from hospital_api.model import Patient,Update_patient
from fastapi.responses import JSONResponse 
from pathlib import Path
import json

BASE_DIR= Path(__file__).resolve().parent.parent
DATA_FILE=BASE_DIR/'data'/'patient.json'

def load_patient():
    with open(DATA_FILE,'r') as f:
        data=json.load(f)
        return data
    
def save_data(data):
    with open(DATA_FILE,'w') as file:
        json.dump(data,file)



router=APIRouter()


@router.post('/create')
def create_patient(patient:Patient):
    data=load_patient()

    if patient.id in data:
        raise HTTPException(status_code=404,detail="patient alread exist")
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=200,content="patient successfully created")

@router.get('/view')
def view():
    data=load_patient()
    return data

@router.get('/view/{patient_id}')
def get_patient(patient_id: str=FastAPIPath(...,description='Enter patient_id to extract respective data')):
    data=load_patient()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient does no exist")
    
    return data[patient_id]

@router.get('/sort')
def sort_patients(sort_by:str = Query(...,description="sort patient order by weight ,height , bmi"),
                  order:str=Query(...,description="Sort patients in asc and desc order")):
    data=load_data()
    valid_field=['weight','height','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=404,detail="Invalid field")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404,detail="Ivalide order choose asc or desc")

    sort_order = True if 'desc' else False
    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data

@router.put('/edit/{patient_id}')
def update_patient(patient_id:str,PatientUpdate:Update_patient):
    data = load_patient()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient does not exist")
    
    existing_patient_info=data[patient_id]
    updated_patient_info=PatientUpdate.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info['id']=patient_id

    patient_pydantic_object=Patient(**existing_patient_info)

    existing_patient_info=patient_pydantic_object.model_dump(exclude='id')

    data[patient_id]=existing_patient_info
    save_data(data)

    return JSONResponse(status_code=202,content="patient updated successfully ")


@router.delete('/delete/{patient_id}')
def delete_patient(patient_id:str=FastAPIPath(...,description="Enter the patient id which you want to delete ")):
    data=load_patient()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Invalid patient id, This pathient doesn't exist")
    del (data[patient_id])
    save_data(data)
    return JSONResponse(status_code=200,content="Patient deleted successfully")
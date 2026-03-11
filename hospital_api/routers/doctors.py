from fastapi import APIRouter,HTTPException,Query
from fastapi import Path as APIPath
from fastapi.responses import JSONResponse

from hospital_api.model import Doctor ,Update_doctor
from pathlib import Path
import json

router=APIRouter()

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_FILE=BASE_DIR/'data'/'doctor.json'

def load_data():
    try:
        with open(DATA_FILE,'r') as f:
            data=json.load(f)
            return data
    except(FileNotFoundError,json.JSONDecodeError):
        return {}
def save_data(data):
    with open(DATA_FILE,'w') as f:
        json.dump(data,f)

@router.post('/create')
def create_doc(doctor:Doctor):
    data=load_data()

    if doctor.id in data:
        raise HTTPException(status_code=404,detail="Doctor id is already exist")
    data[doctor.id]=doctor.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=200,content={'message':"Doctor created successfully"})

@router.put('/edit/{doctor_id}')
def update_doctor(doctor_id:str,UpdatedDoctor:Update_doctor):
    data=load_data()

    if doctor_id not in data:
        raise HTTPException(status_code=404,detail="Doctor with that id does not exist")

    existing_doctor_info=data[doctor_id]
    updated_doctor_info=UpdatedDoctor.model_dump(exclude_unset=True)

    for key,value in updated_doctor_info.items():
        existing_doctor_info[key]=value

    data[doctor_id]=existing_doctor_info

    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Doctor updated successfully'})

@router.get('/view')
def view():
    data = load_data()
    return data

@router.get('/view/{doctor_id}')
def view_doc(doctor_id:str=APIPath(...,description="Enter the doctor id to get particular doctor")):
    data=load_data()

    if doctor_id not in data:
        raise HTTPException(status_code=404,detail="Invalid doctor id")
    return data[doctor_id]

@router.get('/sort')
def get_doc(sort_by:str=Query(...,description="you can sort doctors by speclization & experience"),
            order:str=Query(...,description="you can preform sorting in asc & desc")):
    data=load_data()
    valid_field=['speclization','years_of_experience']
    if sort_by not in valid_field:
        raise HTTPException(status_code=404,detail="Invalid field ")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404,detail="Invalid order")
    

    sort_order=True if order == 'desc' else False
    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data

@router.delete('/delete{doctor_id}')
def delete_doc(doctor_id:str=APIPath(...,description="Enter doctor id to delete",example=['doc-1'])):
    data=load_data()
    if doctor_id not in data:
        raise HTTPException(status_code=404,detail="Doctor does not exist")
    del(data[doctor_id])
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Doctor deleted successfully'})

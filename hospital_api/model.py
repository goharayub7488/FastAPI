from pydantic import BaseModel , Field ,computed_field
from typing import Annotated , Literal ,Optional
class Patient(BaseModel):

    id: Annotated[str,Field(...,description="Enter the patient id",examples=["p1"])]
    name:Annotated[str,Field(...,description='Enter patient name')]
    age: Annotated[int,Field(...,gt=0,lt=100,description="How old patient is")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Select patient gender")]
    phone:Annotated[str,Field(...,pattern="^[0-9]{11}$",description="Enter patient contact number",examples=['03001234567'])]
    weight:Annotated[float,Field(...,gt=0,description="Enter patient weight in kg")]
    height:Annotated[float,Field(...,gt=0,description="Enter patient height in meter")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

class Update_patient(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Literal['male','female','other'],Field(default=None)]
    phone:Annotated[Optional[str],Field(pattern="^[0-9]{11}$",description="Enter patient contact number",examples=['03001234567'])]
    weight:Annotated[Optional[float],Field(gt=0,description="Enter patient weight in kg",default=None)]
    height:Annotated[Optional[float],Field(gt=0,description="Enter patient height in meter",default=None)]


class Doctor(BaseModel):

    id:Annotated[str,Field(...,description="Enter doctor id ",examples=['doc-1'])]
    name:Annotated[str,Field(...,description="Enter Doctor name")]
    speclization:Annotated[str,Field(...,description="Enter the doctor specliety")]
    years_of_experience:Annotated[float,Field(...,description="Practicing experience")]

class Update_doctor(BaseModel):

    name:Annotated[Optional[str],Field(default=None)]
    speclization:Annotated[Optional[str],Field(default=None)]
    years_of_experience:Annotated[Optional[float],Field(default=None)]
from fastapi import FastAPI
from hospital_api.routers import patients,doctors,appointments

app = FastAPI(title="Hospital API")

# including route
app.include_router(patients.router,prefix="/patients",tags=["Patients"])
app.include_router(doctors.router,prefix="/doctors",tags=['Doctors'])
app.include_router(appointments.router,prefix='/appointment',tags=['Appointments'])
    

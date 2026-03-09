from fastapi import FastAPI
from hospital_api.routers import patients,doctors

app = FastAPI(title="Hospital API")

# including route
app.include_router(patients.router,prefix="/patients",tags=["Patients"])
app.include_router(doctors.router,prefix="/doctors",tags=['Doctors'])

    

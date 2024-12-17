from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise Exception("Supabase URL and Key are required")

supabase = create_client(supabase_url, supabase_key)

# Pydantic model for inspection data
class InspectionData(BaseModel):
    timestamp: str
    email: str
    plate_number: str
    driver_name: str
    mileage: int
    engine_start: bool
    engine_noise: bool
    transmission_smooth: bool
    brakes_effective: bool
    brake_noise: bool
    steering_normal: bool
    steering_noise: bool
    tires_inflated: bool
    tire_wear: bool
    wheel_nuts_secure: bool
    lights_working: bool
    interior_components: bool
    battery_charged: bool
    oil_level: bool
    ride_smooth: bool
    body_damage: bool
    additional_comments: str = None

@app.options("/submit-inspection/")
async def options_submit_inspection():
    return {"Allow": "POST, OPTIONS"}

@app.post("/submit-inspection/")
async def submit_inspection(inspection_data: InspectionData):
    try:
        # Insert inspection data into Supabase
        response = supabase.table("van_inspections").insert([inspection_data.dict()]).execute()
        if response.data:
            return {"message": "Inspection submitted successfully", "data": response.data}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit inspection")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "OK"}

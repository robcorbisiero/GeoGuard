from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.geocoding import get_coordinates
from services.climate import get_elevation, get_historical_climate
from services.ai_engine import generate_recommendation

app = FastAPI(title="GeoGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RiskRequest(BaseModel):
    address: str
    land_cover: str = "Urban"

class RiskResponse(BaseModel):
    lat: float
    lon: float
    elevation: float
    historical_rainfall_mm: float
    historical_max_temp_c: float
    recommendation: str

@app.post("/api/assess-risk", response_model=RiskResponse)
def assess_risk(req: RiskRequest):
    coords = get_coordinates(req.address)
    if not coords:
        raise HTTPException(status_code=400, detail="Address not found")
    lat, lon = coords

    elevation = get_elevation(lat, lon)
    if elevation is None:
        raise HTTPException(status_code=500, detail="Failed to fetch elevation")

    climate_data = get_historical_climate(lat, lon)
    if not climate_data:
        raise HTTPException(status_code=500, detail="Failed to fetch climate data")

    recommendation = generate_recommendation(
        elevation=elevation,
        climate_data=climate_data,
        land_cover=req.land_cover
    )

    return RiskResponse(
        lat=lat,
        lon=lon,
        elevation=elevation,
        historical_rainfall_mm=climate_data.get('avg_yearly_rainfall', 0.0),
        historical_max_temp_c=climate_data.get('max_temp', 0.0),
        recommendation=recommendation
    )

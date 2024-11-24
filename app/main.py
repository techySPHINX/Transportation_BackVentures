from fastapi import FastAPI
from app.routes.geofencing import router as geofencing_router

app = FastAPI()

# Register the geofencing router
app.include_router(geofencing_router, prefix="/api", tags=["Geofencing"])

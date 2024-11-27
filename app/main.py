from fastapi import FastAPI
from routes.geofencing import router as geofencing_router
from routes.stop import router as stops_router
from routes.space import router as space_utilization_router
from routes.Capacity_Sharing import router as capacity_sharing_router
from routes.thirdparty import router as third_party_partners_router
from app.routes.Dynamic_routing import router as dynamic_routing_router
from app.routes.packages import router as package_router
from db import Base, engine
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Logistics Management API",
    description="API for managing geofencing, truck stops, space utilization, capacity sharing, and third-party partners.",
    version="1.0.0",
)

app.include_router(geofencing_router,
                   prefix="/api/geofencing", tags=["Geofencing"])
app.include_router(stops_router, prefix="/api/stops", tags=["Stops"])
app.include_router(space_utilization_router,
                   prefix="/api/space_utilization", tags=["Space Utilization"])
app.include_router(capacity_sharing_router,
                   prefix="/api/capacity_sharing", tags=["Capacity Sharing"])
app.include_router(third_party_partners_router,
                   prefix="/api/third_party_partners", tags=["Third Party Partners"])
app.include_router(dynamic_routing_router, prefix="/api/dynamic_routing",
                   tags=["Dynamic Routing"])
app.include_router(package_router, prefix="/api/packages", tags=["Packages"])


@app.get("/")
async def root():
 return {"message": "Welcome to the Transport_BackVentures Management API"}

if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)

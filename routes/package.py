# routes/packages.py
from fastapi import APIRouter, HTTPException
from models import Package
from db import get_package, update_package

router = APIRouter()

@router.get("/packages/")
async def read_packages():
    return get_package()

@router.get("/packages/{package_id}")
async def read_package(package_id: int):
    package = get_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.put("/packages/{package_id}")
async def update_package(package_id: int, package: Package):
    update_package(package_id, package)
    return {"message": "Package updated successfully"}
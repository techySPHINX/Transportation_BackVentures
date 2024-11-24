# routes/third_party_partners.py
from fastapi import APIRouter, HTTPException
from models import ThirdPartyPartner
from app.db import get_third_party_partner, update_third_party_partner

router = APIRouter()

@router.get("/third_party_partners/")
async def read_third_party_partners():
    return get_third_party_partner()

@router.get("/third_party_partners/{third_party_partner_id}")
async def read_third_party_partner(third_party_partner_id: int):
    third_party_partner = get_third_party_partner(third_party_partner_id)
    if not third_party_partner:
        raise HTTPException(status_code=404, detail="Third Party Partner not found")
    return third_party_partner

@router.put("/third_party_partners/{third_party_partner_id}")
async def update_third_party_partner(third_party_partner_id: int, third_party_partner: ThirdPartyPartner):
    update_third_party_partner(third_party_partner_id, third_party_partner)
    return {"message": "Third Party Partner updated successfully"}

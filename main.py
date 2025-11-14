import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Vehicle, Lead

app = FastAPI(title="Automobile Company API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Automobile API running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Helper to convert Mongo _id to string
class VehicleOut(Vehicle):
    id: str

class LeadOut(Lead):
    id: str


@app.post("/api/vehicles", response_model=dict)
def create_vehicle(vehicle: Vehicle):
    try:
        inserted_id = create_document("vehicle", vehicle)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vehicles", response_model=List[VehicleOut])
def list_vehicles():
    try:
        docs = get_documents("vehicle")
        output = []
        for d in docs:
            d["id"] = str(d.pop("_id"))
            output.append(VehicleOut(**d))
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vehicles/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: str):
    try:
        if db is None:
            raise Exception("Database not available")
        doc = db["vehicle"].find_one({"_id": ObjectId(vehicle_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        doc["id"] = str(doc.pop("_id"))
        return VehicleOut(**doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/leads", response_model=dict)
def create_lead(lead: Lead):
    try:
        inserted_id = create_document("lead", lead)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/leads", response_model=List[LeadOut])
def list_leads():
    try:
        docs = get_documents("lead")
        output = []
        for d in docs:
            d["id"] = str(d.pop("_id"))
            output.append(LeadOut(**d))
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

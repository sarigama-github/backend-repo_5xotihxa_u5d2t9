"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Automobile website schemas

class Vehicle(BaseModel):
    """
    Vehicles collection schema
    Collection name: "vehicle"
    """
    make: str = Field(..., description="Manufacturer, e.g., Toyota")
    model: str = Field(..., description="Model name, e.g., Camry")
    year: int = Field(..., ge=1950, le=2100, description="Year of manufacture")
    price: float = Field(..., ge=0, description="Price in USD")
    mileage: Optional[int] = Field(None, ge=0, description="Mileage in miles")
    body_type: Optional[str] = Field(None, description="Sedan, SUV, Truck, etc.")
    fuel_type: Optional[str] = Field(None, description="Petrol, Diesel, Electric, Hybrid")
    transmission: Optional[str] = Field(None, description="Automatic, Manual")
    color: Optional[str] = Field(None, description="Exterior color")
    vin: Optional[str] = Field(None, description="Vehicle Identification Number")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    features: List[str] = Field(default_factory=list, description="Feature list")
    description: Optional[str] = Field(None, description="Short description")
    in_stock: bool = Field(True, description="Whether vehicle is available")

class Lead(BaseModel):
    """
    Leads collection schema
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name of the lead")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    vehicle_id: Optional[str] = Field(None, description="Interested vehicle ID")
    message: Optional[str] = Field(None, description="Additional message or request")
    type: str = Field("test_drive", description="lead type: test_drive | inquiry | service")

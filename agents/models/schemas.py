from pydantic import BaseModel
from typing import Optional
 main
from enum import Enum


class Intent(str, Enum):
    ORDER = "order"
    AVAILABILITY = "availability_check"
    REFILL = "refill"
    GENERAL = "general_query"


class MedicineOrder(BaseModel):
    intent: Intent
    medicine_name: str
    dosage: Optional[str] = None
    quantity: int



class MedicineOrder(BaseModel):
    intent: str
    medicine_name: Optional[str] = None
    quantity: Optional[int] = None
    stock: Optional[int] = None
    customer_id: Optional[str] = None
 main

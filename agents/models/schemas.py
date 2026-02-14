from pydantic import BaseModel
from typing import Optional
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

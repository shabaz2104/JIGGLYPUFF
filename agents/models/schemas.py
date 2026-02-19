from pydantic import BaseModel
from typing import Optional


class MedicineOrder(BaseModel):
    intent: str
    medicine_name: Optional[str] = None
    quantity: Optional[int] = None
    stock: Optional[int] = None
    customer_id: Optional[str] = None

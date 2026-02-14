from agents.core.controller import process_order
from agents.models.schemas import MedicineOrder, Intent


test_order = MedicineOrder(
    intent=Intent.ORDER,
    medicine_name="Crocin",
    dosage="650mg",
    quantity=2
)

response = process_order(test_order)

print(response)

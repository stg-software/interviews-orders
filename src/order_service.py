# src/order_service.py
from typing import Dict, List, Any, TypedDict

class RawOrder(TypedDict):
    id: int
    amount: float
    priority: bool

class ProcessedOrder(TypedDict):
    id: int | None
    status: str
    priority: bool

def is_valid_order(order: Dict[str, Any]) -> bool:
    if "amount" not in order:
        return False

    if order["amount"] is None:
        return False

    return order["amount"] > 0

def transform_order(order: Dict[str, Any]) -> ProcessedOrder:
    order_id = order.get("id")
    if is_valid_order(order):
        return {
            "id": order_id, 
            "status": "ok", 
            "priority": order.get("priority", False)
        }
    else:
        return {
            "id": order_id, 
            "status": "error",
            "priority": order.get("priority", False)
        }

def sort_by_priority(orders: List[ProcessedOrder]) -> List[ProcessedOrder]:
    return sorted(orders, key=lambda order: order.get("priority", False), reverse=True)

def process_orders(orders: List[Dict[str, Any]]) -> List[ProcessedOrder]:
    processed_orders = [transform_order(order) for order in orders]
    return sort_by_priority(processed_orders)

def process_data(data: List[Dict[str, Any]]) -> List[ProcessedOrder]:
    return process_orders(data)

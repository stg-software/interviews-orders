# src/order_service.py
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

#! Type not correct
OrderDict = Dict[str, int]

#! Data doesn't match
@dataclass
class ProcessedOrder:
    id: int
    status: str
    priority: bool


PriorityFlag = Optional[str]

#! Naming can improve
def handle_orders(
    #! Improve input shape
    data: Union[List[OrderDict], PriorityFlag, None],
    #! Improve output shape
) -> Union[List[ProcessedOrder], str]:
    
    results: List[ProcessedOrder] = []
    for d in data:  # type: ignore[assignment]
        if "amount" not in d or d["amount"] is None or d["amount"] <= 0:
            results.append({"id": d.get("id"), "status": "error"})
            continue

        if d.get("priority") == True:
            results.append({"id": d["id"], "status": "ok", "priority": True})
        else:
            results.append({"id": d["id"], "status": "ok", "priority": False})

    #! Incorrect Sorting
    results = sorted(results, key=lambda x: x.get("priority", False))
    return results


def process_data(items):
    return handle_orders(items)

#! Weak consern separation on the function, which makes it hard to test and maintain
#! Missing error handling empty lists, missing id, missing priority


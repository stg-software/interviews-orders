# tests/test_order_service.py
import pytest
from typing import cast
from src.order_service import (
    is_valid_order,
    transform_order,
    sort_by_priority,
    process_orders,
    process_data,
    ProcessedOrder,
)

class TestValidation:

    @pytest.mark.parametrize(
        "order, expected",
        [
            ({"id": 1, "amount": 100, "priority": True}, True),
            ({"id": 1, "amount": 10.5, "priority": True}, True),
            ({"id": 1, "amount": 0.01, "priority": True}, True),
        ],
    )
    def test_valid_order(self, order, expected):
        assert is_valid_order(order) == expected

    @pytest.mark.parametrize(
        "order, expected",
        [
            ({"id": 1, "amount": None, "priority": True}, False),
            ({"id": 1, "amount": -1, "priority": True}, False),
            ({"id": 1, "priority": True}, False),
        ],
    )
    def test_invalid_order(self, order, expected):
        assert is_valid_order(order) == expected

class TestTransformation:

    @pytest.mark.parametrize(
        "order, expected",
        [
            (
                {"id": 1, "amount": 100 }, 
                {"id": 1, "status": "ok", "priority": False},
            ),
            (
                {"id": 2, "amount": 10.5, "priority": True}, 
                {"id": 2, "status": "ok", "priority": True},
            ),
            (
                {"id": 3, "amount": 0.01, "priority": True}, 
                {"id": 3, "status": "ok", "priority": True},
            ),
        ],
    )
    def test_transform_valid_order(self, order, expected):
        assert transform_order(order) == expected

    @pytest.mark.parametrize(
        "order, expected",
        [
            ({"id": 1, "amount": None, "priority": True}, 1),
            ({"id": 2, "amount": -1, "priority": True}, 2),
            ({"id": 3, "priority": True}, 3),
            ({"amount": 0}, None),
        ],
    )
    def test_transform_invalid_order(self, order, expected_id):
        result = transform_order(order)
        assert result["id"] == expected_id
        assert result["status"] == "error"


class TestSorting:
    def test_sort_by_priority(self):
        orders = [
            {"id": 1, "amount": 100, "priority": False},
            {"id": 2, "amount": 10.5, "priority": True},
            {"id": 3, "amount": 0.01, "priority": False},
        ]
        sorted_orders = sort_by_priority(orders)
        assert sorted_orders[0]["id"] == 2
        assert sorted_orders[0]["priority"] == True


class TestEndToEnd:
    
    def test_process_mixed_valid_invalid_orders(self):
        orders = [
            {"id": 1, "amount": 100, "priority": False},
            {"id": 2, "amount": 0},
            {"id": 3, "amount": 0.01, "priority": True},
        ]
        processed_orders = process_orders(orders)


        assert processed_orders[0]["id"] == 3
        assert processed_orders[0]["priority"] == True
        assert processed_orders[0]["status"] == "ok"

        assert processed_orders[1]["id"] == 1
        assert processed_orders[1]["priority"] == False
        assert processed_orders[1]["status"] == "ok"

        assert processed_orders[2]["id"] == 2
        assert processed_orders[2]["priority"] == False
        assert processed_orders[2]["status"] == "error"


class TestCompatibility:
    def test_process_data(self):
        orders = [
            {"id": 1, "amount": 100, "priority": False},
            {"id": 2, "amount": 0},
            {"id": 3, "amount": 0.01, "priority": True},
        ]
        processed_orders = process_data(orders)

        assert processed_orders[0]["id"] == 3
        assert processed_orders[0]["priority"] == True
        assert processed_orders[0]["status"] == "ok"

        assert processed_orders[1]["id"] == 1
        assert processed_orders[1]["priority"] == False
        assert processed_orders[1]["status"] == "ok"

        assert processed_orders[2]["id"] == 2
        assert processed_orders[2]["priority"] == False
        assert processed_orders[2]["status"] == "error"

        
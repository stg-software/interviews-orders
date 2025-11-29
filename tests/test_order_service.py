# tests/test_order_service.py
from src.order_service import process_data


def test_ok_basic():
    data = [{"id": 1, "amount": 100}]
    out = process_data(data)
    assert out[0]["status"] == "ok"


def test_error_amount_zero():
    data = [{"id": 2, "amount": 0}]
    out = process_data(data)
    assert out[0]["status"] == "error"

#! more test cases needed
from models.inventory_optimization import economic_order_quantity, safety_stock


def test_eoq_positive():
    assert economic_order_quantity(1000, 50, 2) > 0


def test_safety_stock_not_negative():
    assert safety_stock(10, 8, 6, 4) >= 0

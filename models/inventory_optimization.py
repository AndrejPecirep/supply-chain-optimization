from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dataclasses import dataclass
import math
import pandas as pd

@dataclass
class InventoryPolicy:
    sku: str
    eoq: int
    safety_stock: int
    reorder_point: int
    average_daily_demand: float


def economic_order_quantity(annual_demand: float, ordering_cost: float, holding_cost_per_unit: float) -> int:
    if annual_demand <= 0 or ordering_cost <= 0 or holding_cost_per_unit <= 0:
        raise ValueError('All EOQ inputs must be positive')
    return math.ceil(math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit))


def safety_stock(max_daily_demand: float, avg_daily_demand: float, max_lead_time: float, avg_lead_time: float) -> int:
    return max(0, math.ceil((max_daily_demand * max_lead_time) - (avg_daily_demand * avg_lead_time)))


def build_inventory_policies(demand: pd.DataFrame, suppliers: pd.DataFrame) -> pd.DataFrame:
    demand = demand.copy()
    demand['order_date'] = pd.to_datetime(demand['order_date'])
    daily = demand.groupby(['sku','order_date'], as_index=False)['quantity'].sum()
    stats = daily.groupby('sku')['quantity'].agg(['mean','max','sum']).reset_index()
    avg_lead = suppliers['lead_time_days'].mean()
    max_lead = suppliers['lead_time_days'].max()
    policies = []
    for row in stats.itertuples(index=False):
        eoq = economic_order_quantity(row.sum, ordering_cost=75, holding_cost_per_unit=2.5)
        ss = safety_stock(row.max, row.mean, max_lead, avg_lead)
        policies.append(InventoryPolicy(row.sku, eoq, ss, int(ss + row.mean * avg_lead), float(row.mean)).__dict__)
    return pd.DataFrame(policies)

if __name__ == '__main__':
    from utils.io import RAW, OUTPUT
    demand = pd.read_csv(RAW/'customer_orders_demand.csv')
    suppliers = pd.read_csv(RAW/'suppliers_master_data.csv')
    result = build_inventory_policies(demand, suppliers)
    result.to_csv(OUTPUT/'inventory_policy_recommendations.csv', index=False)
    print(result)

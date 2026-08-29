from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from utils.io import RAW, OUTPUT, write_json
from models.inventory_optimization import build_inventory_policies
from models.ai_demand_forecasting import create_future_forecast
from models.ai_supplier_risk_agent import score_suppliers
from models.ai_document_parser import parse_all_manifests


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    suppliers = pd.read_csv(RAW/'suppliers_master_data.csv')
    demand = pd.read_csv(RAW/'customer_orders_demand.csv')
    inventory = pd.read_csv(RAW/'inventory_levels_historical.csv')

    policies = build_inventory_policies(demand, suppliers)
    policies.to_csv(OUTPUT/'inventory_policy_recommendations.csv', index=False)

    forecast = create_future_forecast(90)
    forecast.to_csv(OUTPUT/'demand_forecast_90_days.csv', index=False)

    risk = score_suppliers()
    risk.to_csv(OUTPUT/'supplier_risk_scores.csv', index=False)
    write_json(OUTPUT/'supplier_risk_scores.json', risk.to_dict(orient='records'))

    manifests = parse_all_manifests()
    write_json(OUTPUT/'parsed_shipping_manifests.json', manifests)

    try:
        inventory.to_parquet(OUTPUT/'cleaned_inventory_data.parquet', index=False)
    except ImportError:
        inventory.to_csv(OUTPUT/'cleaned_inventory_data.csv', index=False)
    print('Pipeline completed. Outputs are available in data/output/.')

if __name__ == '__main__':
    main()

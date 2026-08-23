from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from utils.io import RAW

REQUIRED_FILES = ["suppliers_master_data.csv", "inventory_levels_historical.csv", "customer_orders_demand.csv"]


def validate_required_files() -> list[str]:
    errors = []
    for name in REQUIRED_FILES:
        if not (RAW / name).exists():
            errors.append(f"Missing required file: {name}")
    return errors


def validate_supplier_data() -> list[str]:
    df = pd.read_csv(RAW / "suppliers_master_data.csv")
    required = {"supplier_id", "supplier_name", "lead_time_days", "on_time_delivery_rate", "quality_defect_rate"}
    missing = required - set(df.columns)
    errors = [f"Missing supplier columns: {missing}"] if missing else []
    if not df["on_time_delivery_rate"].between(0, 1).all():
        errors.append("on_time_delivery_rate must be between 0 and 1")
    if not df["quality_defect_rate"].between(0, 1).all():
        errors.append("quality_defect_rate must be between 0 and 1")
    return errors


def run_validation() -> None:
    errors = validate_required_files() + validate_supplier_data()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Data validation passed.")


if __name__ == "__main__":
    run_validation()

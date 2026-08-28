from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
import re
import pandas as pd
from utils.io import RAW, OUTPUT, write_json

RISK_TERMS = {
    "penalty": 18,
    "expedited freight": 18,
    "single-source": 20,
    "exclusivity": 16,
    "cure period": 10,
    "below 90%": 12,
    "termination": 8,
}


def load_contract_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        except Exception:
            return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_contract_terms(text: str) -> dict:
    supplier = re.search(r"Supplier:\s*(.+)", text)
    sla = re.search(r"SLA:\s*(.+)", text)
    penalty = re.search(r"Penalty:\s*(.+)", text)
    risks = []
    score = 0
    lower = text.lower()
    for term, value in RISK_TERMS.items():
        if term in lower:
            risks.append(term)
            score += value
    return {
        "supplier_name": supplier.group(1).strip() if supplier else "Unknown Supplier",
        "sla_summary": sla.group(1).strip() if sla else "Not found",
        "penalty_clause": penalty.group(1).strip() if penalty else "Not found",
        "detected_risk_terms": risks,
        "contract_risk_score": min(score, 100),
    }


def score_suppliers() -> pd.DataFrame:
    suppliers = pd.read_csv(RAW / "suppliers_master_data.csv")
    contract_rows = []
    for path in (RAW / "supplier_contracts_pdf").glob("*"):
        terms = extract_contract_terms(load_contract_text(path))
        contract_rows.append(terms)
    contracts = pd.DataFrame(contract_rows)
    if contracts.empty:
        contracts = pd.DataFrame(columns=["supplier_name", "contract_risk_score", "sla_summary", "penalty_clause"])
    merged = suppliers.merge(contracts, left_on="supplier_name", right_on="supplier_name", how="left")
    merged["contract_risk_score"] = merged["contract_risk_score"].fillna(15)
    merged["operational_risk_score"] = (
        (1 - merged["on_time_delivery_rate"]) * 35
        + merged["quality_defect_rate"] * 300
        + (100 - merged["financial_health_score"]) * 0.35
        + merged["is_single_source"].astype(bool).astype(int) * 15
        + merged["contract_risk_score"] * 0.35
    ).round(2).clip(0, 100)
    merged["risk_level"] = pd.cut(
        merged["operational_risk_score"], bins=[-1, 45, 75, 101], labels=["LOW", "MEDIUM", "HIGH"]
    )
    merged["recommended_action"] = merged["risk_level"].map({
        "LOW": "Continue standard monitoring.",
        "MEDIUM": "Create mitigation plan and review alternate suppliers.",
        "HIGH": "Escalate to procurement leadership and legal review.",
    })
    return merged


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = score_suppliers()
    result.to_csv(OUTPUT / "supplier_risk_scores.csv", index=False)
    write_json(OUTPUT / "supplier_risk_scores.json", result.to_dict(orient="records"))
    print(result[["supplier_name", "operational_risk_score", "risk_level", "recommended_action"]])

from models.ai_supplier_risk_agent import extract_contract_terms
from models.ai_document_parser import parse_manifest_text


def test_contract_extraction_detects_penalty():
    text = "Supplier: TestCo\nSLA: Delivery within 7 days.\nPenalty: 2% credit below 90%.\nTermination: allowed."
    result = extract_contract_terms(text)
    assert result["supplier_name"] == "TestCo"
    assert result["contract_risk_score"] > 0


def test_manifest_parser_extracts_items():
    text = "Manifest ID: M1\nSupplier: TestCo\nDelivery Date: 2026-01-01\nSKU: SKU-A100 Quantity: 12"
    parsed = parse_manifest_text(text)
    assert parsed["total_quantity"] == 12
    assert parsed["items"][0]["sku"] == "SKU-A100"

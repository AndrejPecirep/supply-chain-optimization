from scripts.validate_data import validate_required_files, validate_supplier_data


def test_required_files_exist():
    assert validate_required_files() == []


def test_supplier_data_valid():
    assert validate_supplier_data() == []

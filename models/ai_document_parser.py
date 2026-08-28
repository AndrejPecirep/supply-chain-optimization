from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
import re
from utils.io import RAW, OUTPUT, write_json


def parse_manifest_text(text: str) -> dict:
    manifest = re.search(r'Manifest ID:\s*(.+)', text)
    supplier = re.search(r'Supplier:\s*(.+)', text)
    date = re.search(r'Delivery Date:\s*(.+)', text)
    vehicle = re.search(r'Vehicle:\s*(.+)', text)
    items = []
    for sku, qty in re.findall(r'SKU:\s*([A-Z0-9-]+)\s+Quantity:\s*(\d+)', text):
        items.append({'sku': sku, 'quantity': int(qty)})
    return {
        'manifest_id': manifest.group(1).strip() if manifest else None,
        'supplier': supplier.group(1).strip() if supplier else None,
        'delivery_date': date.group(1).strip() if date else None,
        'vehicle': vehicle.group(1).strip() if vehicle else None,
        'items': items,
        'total_quantity': sum(item['quantity'] for item in items),
    }


def parse_manifest_file(path: Path) -> dict:
    if path.suffix.lower() in ['.png','.jpg','.jpeg','.tif','.tiff']:
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(path))
    else:
        text = path.read_text(encoding='utf-8', errors='ignore')
    return parse_manifest_text(text)


def parse_all_manifests() -> list[dict]:
    payload = []
    for path in (RAW/'shipping_manifests_scans').glob('*'):
        if path.is_file():
            item = parse_manifest_file(path)
            item['source_file'] = path.name
            payload.append(item)
    return payload

if __name__ == '__main__':
    result = parse_all_manifests()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT/'parsed_shipping_manifests.json', result)
    print(result)

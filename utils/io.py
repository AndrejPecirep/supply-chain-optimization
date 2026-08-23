from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
OUTPUT = ROOT / 'data' / 'output'

for directory in [RAW, PROCESSED, OUTPUT]:
    directory.mkdir(parents=True, exist_ok=True)

def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name)

def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding='utf-8')

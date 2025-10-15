import csv
from typing import List, Dict, Any

NUMERIC_COLS = {"Sales", "Profit", "Discount"}
KEEP_COLS = {"Sales", "Profit", "Category", "Region", "Discount"}

def _to_float_safe(x: str) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0

def _clean_row(raw: Dict[str, str]) -> Dict[str, Any]:
    row = {}
    for k, v in raw.items():
        if k in KEEP_COLS:
            if k in NUMERIC_COLS:
                row[k] = _to_float_safe(v)
            else:
                row[k] = (v or "").strip()
    return row

def read_superstore_csv(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            rows.append(_clean_row(raw))
    return rows

def write_csv(path: str, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def write_txt(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
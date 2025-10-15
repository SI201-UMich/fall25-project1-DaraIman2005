from typing import Dict, List, Tuple, Any
from collections import defaultdict
import math

DEFAULT_DISCOUNT_BINS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

def _bucket_label(lo: float, hi: float | None) -> str:
    if hi is None:
        return f"{lo:.1f}+"
    return f"{lo:.1f}–{hi:.1f}"

def _discount_bucket(discount: float, bins: List[float]) -> str:

    d = max(0.0, discount)
    last = None
    for b in bins:
        if d < b:
            return _bucket_label(last, b) 
        last = b
    return _bucket_label(bins[-1], None)

def avg_profit_by_region(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    sums: Dict[str, float] = defaultdict(float)
    counts: Dict[str, int] = defaultdict(int)
    for r in rows:
        region = r.get("Region", "")
        profit = float(r.get("Profit", 0.0))
        if not region:
            continue
        sums[region] += profit
        counts[region] += 1
    return {reg: (sums[reg] / counts[reg]) for reg in sums if counts[reg] > 0}

def best_region_by_profit(avg_map: Dict[str, float]) -> Tuple[str, float]:
    if not avg_map:
        return ("", 0.0)
    best_reg = max(avg_map, key=lambda k: avg_map[k])
    return (best_reg, avg_map[best_reg])

def avg_sales_by_category_and_discount(
    rows: List[Dict[str, Any]],
    bins: List[float] = DEFAULT_DISCOUNT_BINS
) -> List[Dict[str, Any]]:
    sums: Dict[Tuple[str, str], float] = defaultdict(float)
    counts: Dict[Tuple[str, str], int] = defaultdict(int)

    for r in rows:
        category = r.get("Category", "")
        sales = float(r.get("Sales", 0.0))
        discount = float(r.get("Discount", 0.0))
        if not category:
            continue
        bucket = _discount_bucket(discount, bins)
        key = (category, bucket)
        sums[key] += sales
        counts[key] += 1

    out: List[Dict[str, Any]] = []
    def bucket_key(lbl: str) -> float:
        # "0.1–0.2" -> 0.1 ; "0.8+" -> 0.8
        if "+" in lbl:
            return float(lbl.replace("+", ""))
        lo = lbl.split("–")[0]
        return float(lo)

    cats = sorted({k[0] for k in sums.keys()})
    for cat in cats:
        cat_keys = [(c, b) for (c, b) in sums.keys() if c == cat]
        cat_keys.sort(key=lambda t: bucket_key(t[1]))
        for key in cat_keys:
            total = sums[key]
            n = counts[key]
            avg = total / n if n else 0.0
            out.append({
                "Category": key[0],
                "DiscountRange": key[1],
                "AverageSales": f"{avg:.2f}",
                "Count": n
            })
    return out

def corr_discount_profit(rows: List[Dict[str, Any]]) -> Tuple[float, int]:
    xs: List[float] = []
    ys: List[float] = []
    for r in rows:
        xs.append(float(r.get("Discount", 0.0)))
        ys.append(float(r.get("Profit", 0.0)))
    n = min(len(xs), len(ys))
    if n == 0:
        return (0.0, 0)

    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return (0.0, n)
    return (num / (den_x * den_y), n)

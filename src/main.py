"""
SI 201 – Project 1: Data Analysis
Student: YOUR NAME (daraiman@umich.edu) | ID: XXXXXXXXX
Collaborators: (None)
GenAI usage: help with filetree, having code function accross files, and help with io_utils
Authorship:

Dataset: Sample Superstore Dataset (Kaggle, uploaded by Aman Sharma)
Columns used: Sales, Profit, Category, Region, Discount

Outputs:
- outputs/regional_profit.csv
- outputs/category_sales_by_discount.csv
- outputs/correlation.txt
"""

from io_utils import read_superstore_csv, write_csv, write_txt
from calcs import (
    avg_profit_by_region,
    best_region_by_profit,
    avg_sales_by_category_and_discount,
    corr_discount_profit,
    DEFAULT_DISCOUNT_BINS,
)

def main():
    rows = read_superstore_csv("data/sample_superstore.csv")

    region_to_avg_profit = avg_profit_by_region(rows)
    best_region, best_avg = best_region_by_profit(region_to_avg_profit)

    reg_rows = [{"Region": r, "AverageProfit": f"{avg:.2f}"} for r, avg in sorted(region_to_avg_profit.items())]
    write_csv("outputs/regional_profit.csv", reg_rows, fieldnames=["Region", "AverageProfit"])

    cat_disc_rows = avg_sales_by_category_and_discount(rows, bins=DEFAULT_DISCOUNT_BINS)
    write_csv(
        "outputs/category_sales_by_discount.csv",
        cat_disc_rows,
        fieldnames=["Category", "DiscountRange", "AverageSales", "Count"]
    )

    r_val, n = corr_discount_profit(rows)
    direction = "negative" if r_val < 0 else ("positive" if r_val > 0 else "no linear")
    corr_text = []
    corr_text.append(f"Pearson correlation between Discount and Profit: r = {r_val:.4f} (n = {n})")
    corr_text.append(f"Interpretation: {direction} relationship (magnitude ≈ {abs(r_val):.4f}).")
    corr_text.append(f"Best region by average profit: {best_region} (avg = {best_avg:.2f})")
    write_txt("outputs/correlation.txt", "\n".join(corr_text))

    print("=== Analysis complete ===")
    print(f"- Wrote outputs/regional_profit.csv")
    print(f"- Wrote outputs/category_sales_by_discount.csv")
    print(f"- Wrote outputs/correlation.txt")
    print(f"- Best region by average profit: {best_region} (avg = {best_avg:.2f})")
    print(f"- Corr(Discount, Profit) = {r_val:.4f} (n={n})")

if __name__ == "__main__":
    main()
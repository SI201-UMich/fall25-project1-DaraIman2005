import unittest
from src.calcs import avg_profit_by_region, best_region_by_profit, avg_sales_by_category_and_discount, DEFAULT_DISCOUNT_BINS

class TestAvgProfitByRegion(unittest.TestCase):
    def test_usual_two_regions(self):
        rows = [
            {"Region": "West", "Profit": 10.0},
            {"Region": "West", "Profit": 30.0},
            {"Region": "East", "Profit": 20.0},
        ]
        res = avg_profit_by_region(rows)
        self.assertAlmostEqual(res["West"], 20.0, places=5)
        self.assertAlmostEqual(res["East"], 20.0, places=5)

    def test_edge_missing_region(self):
        rows = [{"Region": "", "Profit": 99.0}]
        res = avg_profit_by_region(rows)
        self.assertEqual(res, {})

    def test_edge_zero_counts(self):
        res = avg_profit_by_region([])
        self.assertEqual(res, {})

    def test_best_region(self):
        avg_map = {"West": 5.0, "East": 10.0, "South": -2.0}
        reg, val = best_region_by_profit(avg_map)
        self.assertEqual(reg, "East")
        self.assertEqual(val, 10.0)

class TestAvgSalesByCategoryAndDiscount(unittest.TestCase):
    def test_usual_two_buckets(self):
        rows = [
            {"Category": "Furniture", "Sales": 100.0, "Discount": 0.05},
            {"Category": "Furniture", "Sales": 200.0, "Discount": 0.05},
            {"Category": "Furniture", "Sales": 300.0, "Discount": 0.25},
        ]
        out = avg_sales_by_category_and_discount(rows, bins=DEFAULT_DISCOUNT_BINS)
        f_0_0_1 = next(r for r in out if r["Category"] == "Furniture" and r["DiscountRange"] == "0.0–0.1")
        f_0_2_0_3 = next(r for r in out if r["Category"] == "Furniture" and r["DiscountRange"] == "0.2–0.3")
        self.assertEqual(f_0_0_1["Count"], 2)
        self.assertEqual(f_0_2_0_3["Count"], 1)
        self.assertEqual(f_0_0_1["AverageSales"], "150.00")
        self.assertEqual(f_0_2_0_3["AverageSales"], "300.00")

    def test_edge_missing_category(self):
        rows = [
            {"Category": "", "Sales": 50.0, "Discount": 0.0},
            {"Category": "Technology", "Sales": 100.0, "Discount": 0.85},
        ]
        out = avg_sales_by_category_and_discount(rows)
        self.assertTrue(any(r["Category"] == "Technology" for r in out))
        self.assertFalse(any(r["Category"] == "" for r in out))

    def test_edge_negative_discount_bucketed_to_zero(self):
        rows = [
            {"Category": "Office Supplies", "Sales": 120.0, "Discount": -0.2},
        ]
        out = avg_sales_by_category_and_discount(rows)
        row = next(r for r in out if r["Category"] == "Office Supplies")
        self.assertEqual(row["DiscountRange"], "0.0–0.1") 

    def test_edge_high_discount_goes_to_plus_bucket(self):
        rows = [
            {"Category": "Technology", "Sales": 400.0, "Discount": 0.95},
        ]
        out = avg_sales_by_category_and_discount(rows)
        row = next(r for r in out if r["Category"] == "Technology")
        self.assertEqual(row["DiscountRange"], "0.8+")
        self.assertEqual(row["AverageSales"], "400.00")

if __name__ == "__main__":
    unittest.main()

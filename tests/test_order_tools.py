import unittest
from src.order_tools import normalize_sku, apply_discount, parse_tags, shipping_label, retry_delay

class OrderToolsTests(unittest.TestCase):
    def test_normalize_sku_trims_and_uppercases(self):
        self.assertEqual(normalize_sku("  rb100  "), "RB100")

    def test_normalize_sku_preserves_hyphen(self):
        self.assertEqual(normalize_sku(" ab-12 "), "AB-12")

    def test_discount_applies_at_minimum_subtotal(self):
        self.assertEqual(apply_discount(100.0, 10.0), 90.0)

    def test_parse_tags_basic(self):
        self.assertEqual(parse_tags("Red, Blue"), ["red", "blue"])

    def test_shipping_label_ascii_name(self):
        self.assertEqual(shipping_label("John Smith", "AR-42"), "John Smith | AR-42")

    def test_retry_delay_is_capped(self):
        self.assertEqual(retry_delay(10), 60)

if __name__ == "__main__":
    unittest.main()

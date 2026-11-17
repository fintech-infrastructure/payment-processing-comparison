"""Schema and data integrity tests for data/providers.json and data/pricing.json."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.calculator.engine import load_data


ROOT_DIR = Path(__file__).resolve().parents[1]


class TestDataSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.providers_data, self.pricing_data = load_data(ROOT_DIR / "data")

    def test_provider_and_pricing_ids_match(self) -> None:
        provider_ids = {p["id"] for p in self.providers_data["providers"]}
        pricing_ids = {p["provider_id"] for p in self.pricing_data["pricing"]}
        self.assertEqual(provider_ids, pricing_ids)
        self.assertGreaterEqual(len(provider_ids), 24)

    def test_required_provider_fields_and_country_separation(self) -> None:
        for provider in self.providers_data["providers"]:
            self.assertIn("merchant_countries", provider)
            self.assertIn("customer_countries", provider)
            self.assertIsInstance(provider["merchant_countries"], list)
            self.assertIsInstance(provider["customer_countries"], dict)
            self.assertTrue(provider["pricing_url"].startswith("https://"))
            self.assertTrue(provider["docs_url"].startswith("https://"))
            self.assertIn("verification_date", provider)

    def test_required_pricing_sources(self) -> None:
        for entry in self.pricing_data["pricing"]:
            self.assertTrue(entry["source_url"].startswith("https://"))
            self.assertIn("verification_date", entry)
            self.assertIn(
                entry["pricing_model"],
                {"flat_rate", "interchange_plus", "subscription_interchange_plus", "custom"},
            )


if __name__ == "__main__":
    unittest.main()

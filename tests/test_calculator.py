"""Unit tests for the payment processor comparison calculator."""

from __future__ import annotations

import unittest

from src.calculator.engine import CalculatorInput, compare_processors


class TestCalculatorEngine(unittest.TestCase):
    def test_mvp_example_rates(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=20000,
                avg_ticket_usd=50,
                channel="online",
                payment_type="cards",
                platform="custom_website",
            )
        )
        self.assertEqual(report.estimated_transactions, 400.0)
        by_id = {r.provider_id: r for r in report.compatible}

        self.assertEqual(by_id["paypal"].monthly_cost_usd, 694.00)
        self.assertEqual(by_id["stripe"].monthly_cost_usd, 700.00)
        self.assertEqual(by_id["square"].monthly_cost_usd, 780.00)
        self.assertAlmostEqual(
            by_id["square"].monthly_cost_usd - by_id["paypal"].monthly_cost_usd,
            86.00,
            places=2,
        )

    def test_compatibility_first_excludes_shopify_on_woocommerce(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=20000,
                avg_ticket_usd=50,
                platform="woocommerce",
                payment_type="cards",
            )
        )
        excluded_ids = {r.provider_id: r.exclusion_reasons for r in report.incompatible}
        self.assertIn("shopify-payments", excluded_ids)
        self.assertIn("gocardless", excluded_ids)

    def test_ach_compatibility(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=50000,
                avg_ticket_usd=500,
                payment_type="ach",
                platform="saas_billing",
            )
        )
        compatible_ids = {r.provider_id for r in report.compatible}
        self.assertIn("gocardless", compatible_ids)
        self.assertIn("stripe", compatible_ids)
        self.assertNotIn("paypal", compatible_ids)

    def test_merchant_of_record_filter(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=10000,
                avg_ticket_usd=40,
                platform="saas_billing",
                billing_model="subscriptions",
                require_mor=True,
            )
        )
        compatible_ids = {r.provider_id for r in report.compatible}
        self.assertEqual(compatible_ids, {"paddle", "lemon-squeezy", "2checkout", "fastspring"})

    def test_switching_calculator_from_stripe(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=20000,
                avg_ticket_usd=50,
                platform="custom_website",
                current_provider_id="stripe",
            )
        )
        self.assertEqual(report.current_provider_cost_usd, 700.00)
        by_id = {r.provider_id: r for r in report.compatible}
        self.assertEqual(by_id["paypal"].monthly_savings_usd, 6.00)
        self.assertEqual(by_id["paypal"].annual_savings_usd, 72.00)
        self.assertIsNone(by_id["stripe"].monthly_savings_usd)

    def test_custom_pricing_never_fabricated(self) -> None:
        report = compare_processors(
            CalculatorInput(
                monthly_volume_usd=20000,
                avg_ticket_usd=50,
                platform="custom_website",
            )
        )
        by_id = {r.provider_id: r for r in report.compatible}
        self.assertIsNone(by_id["adyen"].monthly_cost_usd)
        self.assertIn("Custom pricing / Enterprise quote required", by_id["adyen"].reasons)


if __name__ == "__main__":
    unittest.main()

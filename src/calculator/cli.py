"""Command-line interface for the payment processor comparison calculator."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .engine import CalculatorInput, compare_processors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare compatible payment processors and monthly fees."
    )
    parser.add_argument("--volume", type=float, required=True, help="Monthly sales volume in USD")
    parser.add_argument("--ticket", type=float, required=True, help="Average transaction amount in USD")
    parser.add_argument("--channel", choices=["online", "in_person"], default="online")
    parser.add_argument("--payment-type", choices=["cards", "ach"], default="cards")
    parser.add_argument(
        "--platform",
        choices=["any", "custom_website", "shopify", "woocommerce", "mobile_app", "saas_billing", "pos_in_person"],
        default="any",
    )
    parser.add_argument(
        "--billing",
        choices=["any", "one_time", "subscriptions", "metered_billing", "invoicing"],
        default="any",
    )
    parser.add_argument("--country", default="US", help="Merchant country code (default: US)")
    parser.add_argument("--intl-share", type=float, default=0.0, help="International volume share (0.0-1.0)")
    parser.add_argument("--mor", action="store_true", help="Require Merchant of Record (tax handled)")
    parser.add_argument("--current", default=None, help="Current provider ID for switching savings")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    report = compare_processors(
        CalculatorInput(
            monthly_volume_usd=args.volume,
            avg_ticket_usd=args.ticket,
            channel=args.channel,
            payment_type=args.payment_type,
            platform=args.platform,
            billing_model=args.billing,
            merchant_country=args.country,
            international_share=args.intl_share,
            require_mor=args.mor,
            current_provider_id=args.current,
        )
    )

    if args.json:
        print(json.dumps(asdict(report), indent=2))
        return

    print(
        f"Volume: ${report.monthly_volume_usd:,.2f}/mo | "
        f"Avg ticket: ${report.avg_ticket_usd:,.2f} | "
        f"Est. transactions: {report.estimated_transactions:,.0f}"
    )
    print("\nCompatible Providers:")
    for item in report.compatible:
        cost_str = f"${item.monthly_cost_usd:,.2f}/mo ({item.effective_rate_percent:.2f}%)" if item.monthly_cost_usd is not None else "Custom pricing"
        savings_str = ""
        if item.monthly_savings_usd is not None:
            sign = "+" if item.monthly_savings_usd < 0 else ""
            savings_str = f" | Switching savings: ${item.monthly_savings_usd:,.2f}/mo (${item.annual_savings_usd:,.2f}/yr)" if item.monthly_savings_usd >= 0 else f" | {sign}${-item.monthly_savings_usd:,.2f}/mo more"
        reasons_str = f" [{'; '.join(item.reasons)}]" if item.reasons else ""
        print(f"  - {item.name:18s} {item.rate_display:34s} -> {cost_str}{savings_str}{reasons_str}")

    if report.incompatible:
        print("\nExcluded (Incompatible):")
        for ex in report.incompatible:
            print(f"  x {ex.name:18s} -> {'; '.join(ex.exclusion_reasons)}")


if __name__ == "__main__":
    main()

"""Core calculation and compatibility-first filtering engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@dataclass(frozen=True)
class CalculatorInput:
    """User business parameters for payment processor comparison."""

    monthly_volume_usd: float
    avg_ticket_usd: float
    channel: str = "online"  # "online" | "in_person"
    payment_type: str = "cards"  # "cards" | "ach"
    platform: str = "any"  # "any" | "custom_website" | "shopify" | "woocommerce" | "mobile_app" | "saas_billing" | "pos_in_person"
    billing_model: str = "any"  # "any" | "one_time" | "subscriptions" | "metered_billing" | "invoicing"
    merchant_country: str = "US"
    international_share: float = 0.0  # 0.0 to 1.0
    require_mor: bool = False
    current_provider_id: Optional[str] = None


@dataclass
class ProviderResult:
    """Calculated fee and compatibility explanation for a compatible provider."""

    provider_id: str
    name: str
    category: str
    pricing_model: str
    rate_display: str
    monthly_cost_usd: Optional[float]
    effective_rate_percent: Optional[float]
    is_estimated: bool
    reasons: list[str] = field(default_factory=list)
    monthly_savings_usd: Optional[float] = None
    annual_savings_usd: Optional[float] = None
    migration_effort: Optional[str] = None
    migration_notes: Optional[str] = None
    source_url: str = ""


@dataclass
class IncompatibleProvider:
    """Provider excluded during Compatibility First filtering, with reasons."""

    provider_id: str
    name: str
    exclusion_reasons: list[str]


@dataclass
class CalculationReport:
    """Complete comparison output including compatible and excluded providers."""

    monthly_volume_usd: float
    avg_ticket_usd: float
    estimated_transactions: float
    compatible: list[ProviderResult]
    incompatible: list[IncompatibleProvider]
    current_provider_cost_usd: Optional[float] = None
    lowest_monthly_cost_usd: Optional[float] = None
    highest_monthly_cost_usd: Optional[float] = None
    spread_usd: Optional[float] = None


def load_data(data_dir: Path = DEFAULT_DATA_DIR) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load providers.json and pricing.json from the data directory."""
    providers_path = data_dir / "providers.json"
    pricing_path = data_dir / "pricing.json"
    with providers_path.open("r", encoding="utf-8") as f:
        providers_data = json.load(f)
    with pricing_path.open("r", encoding="utf-8") as f:
        pricing_data = json.load(f)
    return providers_data, pricing_data


def _supports_country(provider: dict[str, Any], country: str) -> bool:
    countries = provider.get("merchant_countries", [])
    upper_country = country.upper()
    for entry in countries:
        if upper_country == entry.upper() or "GLOBAL" in entry.upper():
            return True
    return False


def _check_compatibility(
    provider: dict[str, Any],
    pricing: dict[str, Any],
    params: CalculatorInput,
) -> tuple[bool, list[str], list[str]]:
    """Return (is_compatible, positive_reasons, exclusion_reasons)."""
    exclusions: list[str] = []
    reasons: list[str] = []

    if not _supports_country(provider, params.merchant_country):
        exclusions.append(f"Merchant country {params.merchant_country} is not in supported list")

    if params.platform != "any":
        if params.platform not in provider.get("platforms", []):
            exclusions.append(f"Does not natively support platform '{params.platform}'")
        else:
            reasons.append(f"Compatible with {params.platform.replace('_', ' ')}")

    if params.payment_type not in provider.get("payment_types", []):
        exclusions.append(f"Does not support payment type '{params.payment_type}'")
    elif params.payment_type == "ach":
        reasons.append("Supports ACH")

    if params.billing_model != "any":
        if params.billing_model not in provider.get("billing_models", []):
            exclusions.append(f"Does not support '{params.billing_model}' billing")
        else:
            reasons.append(f"Supports {params.billing_model.replace('_', ' ')}")

    if params.require_mor and provider.get("tax_responsibility") != "merchant_of_record":
        exclusions.append("Not a Merchant of Record (merchant handles sales tax)")
    elif provider.get("tax_responsibility") == "merchant_of_record":
        reasons.append("Merchant of Record (handles global sales tax/VAT)")

    # Channel / pricing availability check
    if params.payment_type == "ach":
        if pricing.get("ach") is None:
            exclusions.append("No published ACH rate for this configuration")
    else:
        rate_key = "in_person_card" if params.channel == "in_person" else "online_card"
        if pricing.get(rate_key) is None:
            exclusions.append(f"Does not support {params.channel.replace('_', '-')} card processing")

    if pricing.get("pricing_model") == "custom":
        reasons.append("Custom pricing / Enterprise quote required")
    elif pricing.get("is_estimated"):
        reasons.append("Estimated rate only (Interchange + markup)")

    if params.platform == "shopify" and provider["id"] != "shopify-payments":
        reasons.append("Note: Shopify adds a 0.6%-2.0% third-party gateway fee")

    return len(exclusions) == 0, reasons, exclusions


def _calculate_monthly_cost(
    pricing: dict[str, Any],
    benchmark: dict[str, Any],
    params: CalculatorInput,
    tx_count: float,
) -> tuple[Optional[float], str]:
    """Calculate estimated monthly cost in USD and rate display string."""
    model = pricing.get("pricing_model", "flat_rate")
    monthly_fee = float(pricing.get("monthly_fee_usd", 0.0))

    if params.payment_type == "ach":
        ach = pricing["ach"]
        pct = float(ach.get("percent", 0.0))
        fixed = float(ach.get("fixed_usd", 0.0))
        cap = ach.get("cap_usd")
        min_fee = float(ach.get("min_usd", 0.0))
        per_tx = params.avg_ticket_usd * pct + fixed
        if cap is not None:
            per_tx = min(per_tx, float(cap))
        per_tx = max(per_tx, min_fee)
        total = monthly_fee + tx_count * per_tx
        return round(total, 2), ach.get("display", "ACH")

    rate_key = "in_person_card" if params.channel == "in_person" else "online_card"
    card_rate = pricing[rate_key]

    if model == "custom" or card_rate.get("percent") is None and card_rate.get("markup_percent") is None:
        return None, card_rate.get("display", "Custom pricing")

    intl_surcharge = float(pricing.get("international_card_surcharge_percent", 0.0)) * params.international_share

    if model in ("interchange_plus", "subscription_interchange_plus"):
        base_pct = float(benchmark["cp_percent"] if params.channel == "in_person" else benchmark["cnp_percent"])
        base_fixed = float(benchmark["cp_fixed_usd"] if params.channel == "in_person" else benchmark["cnp_fixed_usd"])
        markup_pct = float(card_rate.get("markup_percent", 0.0))
        markup_fixed = float(card_rate.get("markup_fixed_usd", 0.0))
        total = (
            monthly_fee
            + params.monthly_volume_usd * (base_pct + markup_pct + intl_surcharge)
            + tx_count * (base_fixed + markup_fixed)
        )
        return round(total, 2), card_rate.get("display", "Interchange-plus")

    # flat_rate
    pct = float(card_rate["percent"])
    fixed = float(card_rate["fixed_usd"])
    total = monthly_fee + params.monthly_volume_usd * (pct + intl_surcharge) + tx_count * fixed
    return round(total, 2), card_rate.get("display", f"{pct*100:.2f}% + ${fixed:.2f}")


def compare_processors(
    params: CalculatorInput,
    data_dir: Path = DEFAULT_DATA_DIR,
) -> CalculationReport:
    """Run Compatibility First filtering, fee calculation, and switching savings."""
    if params.monthly_volume_usd <= 0:
        raise ValueError("monthly_volume_usd must be positive")
    if params.avg_ticket_usd <= 0:
        raise ValueError("avg_ticket_usd must be positive")
    if not (0.0 <= params.international_share <= 1.0):
        raise ValueError("international_share must be between 0.0 and 1.0")

    providers_data, pricing_data = load_data(data_dir)
    pricing_by_id = {item["provider_id"]: item for item in pricing_data["pricing"]}
    benchmark = pricing_data["interchange_benchmark"]
    tx_count = params.monthly_volume_usd / params.avg_ticket_usd

    compatible: list[ProviderResult] = []
    incompatible: list[IncompatibleProvider] = []
    current_cost: Optional[float] = None

    # Compute current provider baseline cost if requested
    if params.current_provider_id and params.current_provider_id in pricing_by_id:
        curr_pricing = pricing_by_id[params.current_provider_id]
        curr_provider = next(
            (p for p in providers_data["providers"] if p["id"] == params.current_provider_id),
            None,
        )
        if curr_provider is not None:
            ok, _, _ = _check_compatibility(curr_provider, curr_pricing, params)
            if ok:
                current_cost, _ = _calculate_monthly_cost(curr_pricing, benchmark, params, tx_count)

    for provider in providers_data["providers"]:
        pid = provider["id"]
        pricing = pricing_by_id.get(pid)
        if pricing is None:
            continue

        is_ok, reasons, exclusions = _check_compatibility(provider, pricing, params)
        if not is_ok:
            incompatible.append(
                IncompatibleProvider(
                    provider_id=pid,
                    name=provider["name"],
                    exclusion_reasons=exclusions,
                )
            )
            continue

        cost, rate_display = _calculate_monthly_cost(pricing, benchmark, params, tx_count)
        effective_rate = (
            round((cost / params.monthly_volume_usd) * 100, 2) if cost is not None else None
        )

        savings_mo: Optional[float] = None
        savings_yr: Optional[float] = None
        if current_cost is not None and cost is not None and pid != params.current_provider_id:
            savings_mo = round(current_cost - cost, 2)
            savings_yr = round(savings_mo * 12, 2)

        migration = provider.get("migration", {})
        compatible.append(
            ProviderResult(
                provider_id=pid,
                name=provider["name"],
                category=provider["category"],
                pricing_model=pricing["pricing_model"],
                rate_display=rate_display,
                monthly_cost_usd=cost,
                effective_rate_percent=effective_rate,
                is_estimated=bool(pricing.get("is_estimated", False)),
                reasons=reasons,
                monthly_savings_usd=savings_mo,
                annual_savings_usd=savings_yr,
                migration_effort=migration.get("effort"),
                migration_notes=migration.get("notes"),
                source_url=pricing.get("source_url", ""),
            )
        )

    compatible.sort(
        key=lambda r: (r.monthly_cost_usd is None, r.monthly_cost_usd if r.monthly_cost_usd is not None else 0.0)
    )

    numeric_costs = [r.monthly_cost_usd for r in compatible if r.monthly_cost_usd is not None]
    lowest = min(numeric_costs) if numeric_costs else None
    highest = max(numeric_costs) if numeric_costs else None
    spread = round(highest - lowest, 2) if (lowest is not None and highest is not None) else None

    return CalculationReport(
        monthly_volume_usd=params.monthly_volume_usd,
        avg_ticket_usd=params.avg_ticket_usd,
        estimated_transactions=round(tx_count, 2),
        compatible=compatible,
        incompatible=incompatible,
        current_provider_cost_usd=current_cost,
        lowest_monthly_cost_usd=lowest,
        highest_monthly_cost_usd=highest,
        spread_usd=spread,
    )

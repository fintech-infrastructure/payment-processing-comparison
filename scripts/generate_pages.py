"""Generate comparison, alternatives, and category HTML + Markdown pages from data/."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.calculator.engine import CalculatorInput, compare_processors, load_data


BASE_URL = "https://fintech-infrastructure.github.io/payment-processing-comparison"
VERIFIED_DATE = "2026-11-17"

VS_PAIRS: list[tuple[str, str, str]] = [
    ("stripe", "square", "Stripe vs Square"),
    ("stripe", "paypal", "Stripe vs PayPal"),
    ("square", "paypal", "Square vs PayPal"),
    ("stripe", "helcim", "Stripe vs Helcim"),
    ("stripe", "paddle", "Stripe vs Paddle"),
    ("stripe", "braintree", "Stripe vs Braintree"),
    ("stripe", "adyen", "Stripe vs Adyen"),
    ("stripe", "dharma-merchant-services", "Stripe vs Dharma Merchant Services"),
    ("stripe", "stax", "Stripe vs Stax"),
    ("stripe", "authorize-net", "Stripe vs Authorize.net"),
    ("stripe", "lemon-squeezy", "Stripe vs Lemon Squeezy"),
    ("stripe", "2checkout", "Stripe vs 2Checkout"),
    ("square", "clover", "Square vs Clover"),
    ("square", "toast", "Square vs Toast"),
    ("square", "sumup", "Square vs SumUp"),
    ("square", "helcim", "Square vs Helcim"),
    ("helcim", "stax", "Helcim vs Stax"),
    ("helcim", "dharma-merchant-services", "Helcim vs Dharma Merchant Services"),
    ("helcim", "payment-depot", "Helcim vs Payment Depot"),
    ("paddle", "lemon-squeezy", "Paddle vs Lemon Squeezy"),
    ("gocardless", "dwolla", "GoCardless vs Dwolla"),
    ("authorize-net", "nmi", "Authorize.net vs NMI"),
]

ALTERNATIVES_PAGES: list[tuple[str, str, str, list[str]]] = [
    (
        "stripe-alternatives",
        "Best Stripe Alternatives",
        "Compare interchange-plus rates, Merchant of Record tax handling, and B2B ACH.",
        ["helcim", "dharma-merchant-services", "stax", "braintree", "paddle", "lemon-squeezy", "gocardless", "adyen"],
    ),
    (
        "square-alternatives",
        "Best Square Alternatives",
        "Compare lower online card rates, POS systems, and zero-fee micro-merchant tools.",
        ["stripe", "helcim", "sumup", "clover", "toast", "chase-payment-solutions", "paypal"],
    ),
    (
        "paypal-alternatives",
        "Best PayPal Alternatives",
        "Compare developer APIs, native ACH support, and lower card processing fees.",
        ["stripe", "braintree", "helcim", "chase-payment-solutions", "authorize-net", "2checkout"],
    ),
    (
        "shopify-payments-alternatives",
        "Best Shopify Payments Alternatives",
        "Compare third-party gateways for Shopify stores and cross-border checkout.",
        ["stripe", "paypal", "authorize-net", "adyen", "2checkout"],
    ),
    (
        "braintree-alternatives",
        "Best Braintree Alternatives",
        "Compare developer-first gateways, interchange-plus pricing, and wallet support.",
        ["stripe", "adyen", "helcim", "authorize-net", "nmi", "paypal"],
    ),
    (
        "authorize-net-alternatives",
        "Best Authorize.net Alternatives",
        "Compare modern payment APIs, gateway-only options, and no-monthly-fee processors.",
        ["nmi", "stripe", "helcim", "dharma-merchant-services", "payline-data", "braintree"],
    ),
    (
        "paddle-alternatives",
        "Best Paddle Alternatives (MoR)",
        "Compare SaaS Merchant of Record platforms and global tax-handling options.",
        ["lemon-squeezy", "2checkout", "fastspring", "stripe"],
    ),
    (
        "clover-alternatives",
        "Best Clover Alternatives",
        "Compare transparent POS and online card processors without long reseller contracts.",
        ["square", "toast", "helcim", "sumup", "stripe", "chase-payment-solutions"],
    ),
    (
        "high-risk-payment-processors",
        "High-Risk Payment Processors",
        "Compare gateways and underwritten accounts for industries declined by aggregators.",
        ["durango-merchant-services", "nmi", "payline-data", "authorize-net", "adyen"],
    ),
]


def _clean_copy(text: str) -> str:
    return (
        text.replace("—", ", ")
        .replace("–", " to ")
        .replace("'", "’")
    )


def _html_shell(title: str, description: str, canonical: str, h1: str, lead: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{html.escape(canonical)}">
  <link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="./">Payment Processor Comparison</a>
      <nav class="top-nav">
        <a href="./">Fee Calculator</a>
        <a href="stripe-vs-square.html">Stripe vs Square</a>
        <a href="stripe-alternatives.html">Stripe Alternatives</a>
        <a href="cheapest-payment-processors.html">Cheapest Processors</a>
        <a href="payment-gateway-api-comparison.html">API Comparison</a>
        <a class="gh-star-btn" data-gh-stars href="https://github.com/fintech-infrastructure/payment-processing-comparison" target="_blank" rel="noopener">Star on GitHub</a>
      </nav>
    </div>
  </header>
  <main class="container">
    <section class="hero">
      <h1>{html.escape(_clean_copy(h1))}</h1>
      <p class="lead">{html.escape(_clean_copy(lead))}</p>
    </section>
    {body_html}
  </main>
  <footer class="site-footer"><div class="container">Verified {VERIFIED_DATE}. <a href="./">Back to Calculator</a></div></footer>
  <script src="assets/star-count.js"></script>
</body>
</html>
"""


def _rate_str(pricing: dict) -> str:
    if pricing.get("online_card"):
        return pricing["online_card"]["display"]
    if pricing.get("ach"):
        return pricing["ach"]["display"]
    return "Custom pricing"


def _cost_str(provider_id: str, volume: float, ticket: float, payment_type: str = "cards") -> str:
    report = compare_processors(
        CalculatorInput(
            monthly_volume_usd=volume,
            avg_ticket_usd=ticket,
            payment_type=payment_type,
        )
    )
    for item in report.compatible:
        if item.provider_id == provider_id:
            if item.monthly_cost_usd is None:
                return "Custom pricing"
            est = " (est.)" if item.is_estimated else ""
            return f"${item.monthly_cost_usd:,.2f}/mo ({item.effective_rate_percent:.2f}%){est}"
    return "Not supported"


def generate_vs_pages(providers_by_id: dict, pricing_by_id: dict) -> list[tuple[str, str, str]]:
    generated = []
    for id_a, id_b, title_label in VS_PAIRS:
        slug = f"{id_a}-vs-{id_b}"
        pa, pb = providers_by_id[id_a], providers_by_id[id_b]
        pra, prb = pricing_by_id[id_a], pricing_by_id[id_b]

        ptype = "ach" if (pa["payment_types"] == ["ach"] and pb["payment_types"] == ["ach"]) else "cards"
        cost20_a = _cost_str(id_a, 20000, 50, ptype)
        cost20_b = _cost_str(id_b, 20000, 50, ptype)
        cost100_a = _cost_str(id_a, 100000, 100, ptype)
        cost100_b = _cost_str(id_b, 100000, 100, ptype)

        rate_a = _rate_str(pra)
        rate_b = _rate_str(prb)
        ach_a = pra["ach"]["display"] if pra.get("ach") else "Not available"
        ach_b = prb["ach"]["display"] if prb.get("ach") else "Not available"
        tax_a = "Merchant of Record" if pa["tax_responsibility"] == "merchant_of_record" else "Merchant handles tax"
        tax_b = "Merchant of Record" if pb["tax_responsibility"] == "merchant_of_record" else "Merchant handles tax"

        short_h1 = title_label if len(title_label) <= 44 else f"{pa['name']} vs {pb['name']}"
        lead = f"Compare {_clean_copy(rate_a)} on {pa['name']} against {_clean_copy(rate_b)} on {pb['name']}."
        if len(lead.split()) > 12:
            lead = f"Compare real monthly fees, ACH, countries, and integrations for {pa['name']} and {pb['name']}."
            if len(lead.split()) > 12:
                lead = f"Compare real monthly fees and compatibility for {pa['name']} and {pb['name']}."

        body = f"""<section class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Criteria</th><th>{html.escape(pa['name'])}</th><th>{html.escape(pb['name'])}</th></tr></thead>
          <tbody>
            <tr><td>Pricing model</td><td>{html.escape(pra['pricing_model'].replace('_', ' '))}</td><td>{html.escape(prb['pricing_model'].replace('_', ' '))}</td></tr>
            <tr><td>Published rate</td><td class="mono">{html.escape(_clean_copy(rate_a))}</td><td class="mono">{html.escape(_clean_copy(rate_b))}</td></tr>
            <tr><td>$20k/mo ($50 avg ticket)</td><td class="mono">{html.escape(cost20_a)}</td><td class="mono">{html.escape(cost20_b)}</td></tr>
            <tr><td>$100k/mo ($100 avg ticket)</td><td class="mono">{html.escape(cost100_a)}</td><td class="mono">{html.escape(cost100_b)}</td></tr>
            <tr><td>ACH bank debit</td><td class="mono">{html.escape(_clean_copy(ach_a))}</td><td class="mono">{html.escape(_clean_copy(ach_b))}</td></tr>
            <tr><td>Merchant countries</td><td>{pa['merchant_country_count']} countries</td><td>{pb['merchant_country_count']} countries</td></tr>
            <tr><td>Tax responsibility</td><td>{tax_a}</td><td>{tax_b}</td></tr>
            <tr><td>Summary</td><td>{html.escape(_clean_copy(pa['summary']))}</td><td>{html.escape(_clean_copy(pb['summary']))}</td></tr>
          </tbody>
        </table>
      </div>
      <a class="cta-link" href="./">Compare with your volume</a>
    </section>"""

        html_out = _html_shell(
            f"{title_label} (2026): Fees, Compatibility & Cost Comparison",
            f"Compare {pa['name']} ({rate_a}) vs {pb['name']} ({rate_b}) for US businesses.",
            f"{BASE_URL}/{slug}.html",
            short_h1,
            lead,
            body,
        )
        (ROOT_DIR / "docs" / f"{slug}.html").write_text(html_out, encoding="utf-8")

        md_out = f"""# {title_label} (US Businesses, 2026)

| Criteria | {pa['name']} | {pb['name']} |
| --- | --- | --- |
| **Pricing model** | {pra['pricing_model']} | {prb['pricing_model']} |
| **Published rate** | {rate_a} | {rate_b} |
| **$20k/mo ($50 avg ticket)** | {cost20_a} | {cost20_b} |
| **$100k/mo ($100 avg ticket)** | {cost100_a} | {cost100_b} |
| **ACH bank debit** | {ach_a} | {ach_b} |
| **Merchant countries** | {pa['merchant_country_count']} | {pb['merchant_country_count']} |
| **Tax responsibility** | {tax_a} | {tax_b} |

- **{pa['name']}:** {pa['summary']} ([Official pricing]({pra['source_url']}))
- **{pb['name']}:** {pb['summary']} ([Official pricing]({prb['source_url']}))
"""
        (ROOT_DIR / "docs" / "comparisons" / f"{slug}.md").write_text(md_out, encoding="utf-8")
        generated.append((f"{slug}.html", title_label, f"{rate_a} vs {rate_b}"))
    return generated


def generate_alternatives_pages(providers_by_id: dict, pricing_by_id: dict) -> list[tuple[str, str, str]]:
    generated = []
    for slug, title_label, lead_copy, alt_ids in ALTERNATIVES_PAGES:
        rows_html = []
        rows_md = []
        for pid in alt_ids:
            p = providers_by_id[pid]
            pr = pricing_by_id[pid]
            rate = _rate_str(pr)
            cost20 = _cost_str(pid, 20000, 50, "ach" if p["payment_types"] == ["ach"] else "cards")
            rows_html.append(
                f"<tr><td><strong>{html.escape(p['name'])}</strong></td>"
                f"<td class=\"mono\">{html.escape(_clean_copy(rate))}</td>"
                f"<td class=\"mono\">{html.escape(cost20)}</td>"
                f"<td>{html.escape(_clean_copy(p['summary']))}</td>"
                f"<td>{html.escape(p['migration']['effort'].title())}</td></tr>"
            )
            rows_md.append(
                f"| **{p['name']}** | {rate} | {cost20} | {p['summary']} | {p['migration']['effort'].title()} |"
            )

        body = f"""<section class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Provider</th><th>Published Rate</th><th>$20k/mo Est.</th><th>Best Fit</th><th>Migration Effort</th></tr></thead>
          <tbody>
            {''.join(rows_html)}
          </tbody>
        </table>
      </div>
      <a class="cta-link" href="./">Calculate switching savings</a>
    </section>"""

        html_out = _html_shell(
            f"{title_label} (2026): Fees & Switching Comparison",
            lead_copy,
            f"{BASE_URL}/{slug}.html",
            title_label,
            lead_copy,
            body,
        )
        (ROOT_DIR / "docs" / f"{slug}.html").write_text(html_out, encoding="utf-8")

        md_out = f"""# {title_label} (2026)

{lead_copy}

| Provider | Published Rate | $20k/mo Est. | Best Fit | Migration Effort |
| --- | --- | --- | --- | --- |
{chr(10).join(rows_md)}
"""
        (ROOT_DIR / "docs" / "alternatives" / f"{slug}.md").write_text(md_out, encoding="utf-8")
        generated.append((f"{slug}.html", title_label, lead_copy))
    return generated


def generate_category_pages(providers_data: dict, pricing_by_id: dict) -> list[tuple[str, str, str]]:
    providers = providers_data["providers"]
    generated = []

    # 1. Payment Gateway API Comparison
    api_rows = []
    for p in providers:
        api = p["api_features"]
        if not api["rest_api"]:
            continue
        sdks = ", ".join(api["sdks"][:5]) + ("…" if len(api["sdks"]) > 5 else "")
        billing = ", ".join(b.replace("_", " ") for b in p["billing_models"])
        api_rows.append(
            f"<tr><td><strong>{html.escape(p['name'])}</strong></td>"
            f"<td>{'Yes' if api['webhooks'] else 'No'} / {'Yes' if api['sandbox'] else 'No'}</td>"
            f"<td>{html.escape(sdks)}</td>"
            f"<td>{html.escape(billing)}</td></tr>"
        )
    api_body = f"""<section class="card"><div class="table-wrap"><table>
      <thead><tr><th>Provider</th><th>Webhooks / Sandbox</th><th>SDKs</th><th>Billing Models</th></tr></thead>
      <tbody>{''.join(api_rows)}</tbody></table></div>
      <a class="cta-link" href="./">Check fees in calculator</a></section>"""
    (ROOT_DIR / "docs" / "payment-gateway-api-comparison.html").write_text(
        _html_shell(
            "Payment Gateway API Comparison (2026): SDKs, Webhooks & Billing",
            "Compare REST APIs, webhooks, sandboxes, and SDKs across 20+ payment providers.",
            f"{BASE_URL}/payment-gateway-api-comparison.html",
            "Payment Gateway API Comparison",
            "Compare REST APIs, webhooks, test sandboxes, SDKs, and billing models.",
            api_body,
        ),
        encoding="utf-8",
    )
    generated.append(("payment-gateway-api-comparison.html", "Payment Gateway API Comparison", "SDKs, webhooks, sandboxes, and metered billing."))

    # 2. ACH Payment Processors
    ach_report = compare_processors(CalculatorInput(monthly_volume_usd=50000, avg_ticket_usd=500, payment_type="ach"))
    ach_rows = []
    for r in ach_report.compatible:
        cost = f"${r.monthly_cost_usd:,.2f}/mo" if r.monthly_cost_usd is not None else "Custom pricing"
        ach_rows.append(
            f"<tr><td><strong>{html.escape(r.name)}</strong></td>"
            f"<td class=\"mono\">{html.escape(_clean_copy(r.rate_display))}</td>"
            f"<td class=\"mono\">{html.escape(cost)}</td></tr>"
        )
    ach_body = f"""<section class="card"><div class="table-wrap"><table>
      <thead><tr><th>Provider</th><th>Published ACH Rate</th><th>$50k/mo ($500 avg)</th></tr></thead>
      <tbody>{''.join(ach_rows)}</tbody></table></div>
      <a class="cta-link" href="./">Model ACH volume in calculator</a></section>"""
    (ROOT_DIR / "docs" / "ach-payment-processors.html").write_text(
        _html_shell(
            "ACH Payment Processors & Bank Debit Comparison (2026)",
            "Compare US ACH fees across Stripe, GoCardless, Dwolla, Helcim, Braintree, and Dharma.",
            f"{BASE_URL}/ach-payment-processors.html",
            "ACH Payment Processors Compared",
            "Compare US ACH and bank debit fees for B2B invoices and subscriptions.",
            ach_body,
        ),
        encoding="utf-8",
    )
    generated.append(("ach-payment-processors.html", "ACH Payment Processors", "Bank-to-bank ACH fees vs card processing."))

    # 3. Cheapest Payment Processors
    cheap_report = compare_processors(CalculatorInput(monthly_volume_usd=20000, avg_ticket_usd=50, payment_type="cards"))
    cheap_rows = []
    for r in cheap_report.compatible:
        if r.monthly_cost_usd is None:
            continue
        est = " (est.)" if r.is_estimated else ""
        cheap_rows.append(
            f"<tr><td><strong>{html.escape(r.name)}</strong></td>"
            f"<td>{html.escape(r.pricing_model.replace('_', ' '))}</td>"
            f"<td class=\"mono\">{html.escape(_clean_copy(r.rate_display))}</td>"
            f"<td class=\"mono\">${r.monthly_cost_usd:,.2f}/mo ({r.effective_rate_percent:.2f}%){est}</td></tr>"
        )
    cheap_body = f"""<section class="card"><div class="table-wrap"><table>
      <thead><tr><th>Provider</th><th>Model</th><th>Published Rate</th><th>$20k/mo ($50 avg)</th></tr></thead>
      <tbody>{''.join(cheap_rows)}</tbody></table></div>
      <a class="cta-link" href="./">Test your own ticket size</a></section>"""
    (ROOT_DIR / "docs" / "cheapest-payment-processors.html").write_text(
        _html_shell(
            "Cheapest Payment Processors for US Businesses (2026)",
            "Ranked comparison of US card processing fees at $20,000/mo across flat-rate and interchange-plus providers.",
            f"{BASE_URL}/cheapest-payment-processors.html",
            "Cheapest Payment Processors (US)",
            "Ranked by estimated monthly fees at $20,000/mo and $50 average ticket.",
            cheap_body,
        ),
        encoding="utf-8",
    )
    generated.append(("cheapest-payment-processors.html", "Cheapest Payment Processors", "Ranked by real monthly cost at $20k/mo."))

    # 4. Merchant of Record Comparison
    mor_report = compare_processors(CalculatorInput(monthly_volume_usd=20000, avg_ticket_usd=50, require_mor=True))
    mor_rows = []
    for r in mor_report.compatible:
        cost = f"${r.monthly_cost_usd:,.2f}/mo" if r.monthly_cost_usd is not None else "Custom pricing"
        mor_rows.append(
            f"<tr><td><strong>{html.escape(r.name)}</strong></td>"
            f"<td class=\"mono\">{html.escape(_clean_copy(r.rate_display))}</td>"
            f"<td class=\"mono\">{html.escape(cost)}</td></tr>"
        )
    mor_body = f"""<section class="card"><div class="table-wrap"><table>
      <thead><tr><th>Merchant of Record</th><th>Published Rate</th><th>$20k/mo ($50 avg)</th></tr></thead>
      <tbody>{''.join(mor_rows)}</tbody></table></div>
      <a class="cta-link" href="./">Filter by Merchant of Record</a></section>"""
    (ROOT_DIR / "docs" / "merchant-of-record-comparison.html").write_text(
        _html_shell(
            "Merchant of Record Comparison (2026): Paddle, Lemon Squeezy, 2Checkout, FastSpring",
            "Compare Merchant of Record platforms that handle global SaaS sales tax and VAT compliance.",
            f"{BASE_URL}/merchant-of-record-comparison.html",
            "Merchant of Record Comparison",
            "Compare SaaS Merchant of Record platforms handling global sales tax and VAT.",
            mor_body,
        ),
        encoding="utf-8",
    )
    generated.append(("merchant-of-record-comparison.html", "Merchant of Record Comparison", "Paddle, Lemon Squeezy, 2Checkout, FastSpring."))

    return generated


def update_sitemap_and_llms(all_pages: list[tuple[str, str, str]]) -> None:
    urls = [f"  <url>\n    <loc>{BASE_URL}/</loc>\n    <lastmod>{VERIFIED_DATE}</lastmod>\n  </url>"]
    llms_lines = [
        "# Payment Processor Comparison",
        "",
        "Open-source comparison of 24 payment processors for US businesses: real transaction fees, compatibility-first filtering, switching savings, and API support.",
        "",
        f"- Interactive Calculator: {BASE_URL}/",
    ]
    for filename, label, _ in all_pages:
        urls.append(f"  <url>\n    <loc>{BASE_URL}/{filename}</loc>\n    <lastmod>{VERIFIED_DATE}</lastmod>\n  </url>")
        llms_lines.append(f"- {label}: {BASE_URL}/{filename}")
    llms_lines.append("- Raw JSON Data: data/providers.json, data/pricing.json")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    (ROOT_DIR / "docs" / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT_DIR / "docs" / "llms.txt").write_text("\n".join(llms_lines) + "\n", encoding="utf-8")


def update_index_guides(
    vs_pages: list[tuple[str, str, str]],
    alt_pages: list[tuple[str, str, str]],
    cat_pages: list[tuple[str, str, str]],
    providers: list[dict],
) -> None:
    index_path = ROOT_DIR / "docs" / "index.html"
    content = index_path.read_text(encoding="utf-8")

    # Update currentProvider dropdown to include all key processors
    options = ['<option value="">None (New setup)</option>']
    for p in providers:
        selected = ' selected' if p["id"] == "stripe" else ""
        options.append(f'            <option value="{p["id"]}"{selected}>{html.escape(p["name"])}</option>')

    start_sel = content.index('<select id="currentProvider">')
    end_sel = content.index('</select>', start_sel) + len('</select>')
    new_sel = f'<select id="currentProvider">\n            {chr(10).join(options)}\n          </select>'
    content = content[:start_sel] + new_sel + content[end_sel:]

    def cards(items: list[tuple[str, str, str]]) -> str:
        return "\n        ".join(
            f'<a class="guide-card" href="{fn}"><h3>{html.escape(_clean_copy(lbl))}</h3><p>{html.escape(_clean_copy(desc))}</p></a>'
            for fn, lbl, desc in items
        )

    guides_block = f"""<section class="guides-section">
      <h2>Category &amp; API Guides</h2>
      <div class="guides-grid">
        {cards(cat_pages)}
      </div>
    </section>

    <section class="guides-section">
      <h2>Processor Alternatives</h2>
      <div class="guides-grid">
        {cards(alt_pages)}
      </div>
    </section>

    <section class="guides-section">
      <h2>Head-to-Head Comparisons</h2>
      <div class="guides-grid">
        {cards(vs_pages)}
      </div>
    </section>"""

    start_guides = content.index('<section class="guides-section">')
    end_guides = content.index('</main>', start_guides)
    content = content[:start_guides] + guides_block + "\n  " + content[end_guides:]
    index_path.write_text(content, encoding="utf-8")


def main() -> None:
    providers_data, pricing_data = load_data(ROOT_DIR / "data")
    providers_by_id = {p["id"]: p for p in providers_data["providers"]}
    pricing_by_id = {p["provider_id"]: p for p in pricing_data["pricing"]}

    vs_pages = generate_vs_pages(providers_by_id, pricing_by_id)
    alt_pages = generate_alternatives_pages(providers_by_id, pricing_by_id)
    cat_pages = generate_category_pages(providers_data, pricing_by_id)

    all_pages = cat_pages + alt_pages + vs_pages
    update_sitemap_and_llms(all_pages)
    update_index_guides(vs_pages, alt_pages, cat_pages, providers_data["providers"])
    import json as _json
    embedded_js = (
        "window.PPC_DATA = "
        + _json.dumps({"providers": providers_data, "pricing": pricing_data}, separators=(",", ":"))
        + ";\n"
    )
    (ROOT_DIR / "docs" / "data" / "embedded-data.js").write_text(embedded_js, encoding="utf-8")
    print(f"Generated {len(all_pages)} HTML subpages (+1 index.html = {len(all_pages)+1} total HTML pages).")


if __name__ == "__main__":
    main()

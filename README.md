# Payment Processor Comparison

**Compare fees. Check compatibility. Find a better fit.**

Open-source dataset, compatibility-first comparison engine, and fee calculator for US businesses choosing or replacing a payment processor.

- **Interactive Calculator & Guides:** [fintech-infrastructure.github.io/payment-processing-comparison](https://fintech-infrastructure.github.io/payment-processing-comparison/)
- **Last Verified:** `2026-11-17` (all rates sourced from official provider pricing pages in [`data/pricing.json`](data/pricing.json))

---

## Why This Exists

Most payment processor lists just rank brands. When choosing or switching a processor, you actually need three answers:

1. **Compatibility First:** Can my US/global business legally onboard, and does it support my platform (Shopify, WooCommerce, custom API), payment methods (cards, ACH), and tax model?
2. **Real Monthly Cost:** At my monthly sales volume and average ticket size, what will I actually pay?
3. **Switching Savings:** If I'm currently on Stripe, Square, or PayPal, how much would I save per month—and what is the migration effort?

---

## Provider Comparison Table (US Businesses)

| Provider | Pricing Model | US Online Card Rate | ACH Rate | Monthly Fee | Tax / MoR | Best For |
| --- | --- | --- | --- | --- | --- | --- |
| **Stripe** | Flat-rate | `2.9% + $0.30` | `0.8%` (cap `$5.00`) | `$0` | Merchant | SaaS, marketplaces, custom APIs |
| **Square** | Flat-rate | `3.3% + $0.30` (Free) | `1.0%` (`$1.00` min) | `$0` | Merchant | Retail, restaurants, omnichannel POS |
| **PayPal** | Flat-rate | `2.89% + $0.29` (Expanded) | — | `$0` | Merchant | Checkout conversion (PayPal/Venmo) |
| **Braintree** | Flat-rate | `2.59% + $0.49` | `0.75%` (cap `$5.00`) | `$0` | Merchant | High-ticket cards + PayPal/Venmo |
| **Helcim** | Interchange-plus | `IC + 0.50% + $0.25` | `0.5% + $0.25` (cap `$6.00`) | `$0` | Merchant | US/CA SMBs lowering card fees |
| **Authorize.net** | Flat-rate / Gateway | `2.9% + $0.30` | `0.75%` (eCheck) | `$25` | Merchant | Bring-your-own-acquirer flexibility |
| **Stax** | Subscription + IC | `IC + 0% + $0.15` | Custom / Included | `$99+` | Merchant | High-volume US merchants (`>$10k/mo`) |
| **Shopify Payments** | Flat-rate | `2.9% + $0.30` (Basic) | — | `$0` (+Shopify) | Merchant | Shopify stores (avoids 3rd-party fee) |
| **Adyen** | Custom (Interchange++) | Custom pricing | Custom | Custom | Merchant | Enterprise global acquiring |
| **GoCardless** | Flat-rate (Bank Debit) | — (No cards) | `1.0% + $0.25` (cap `$4.00`) | `$0` | Merchant | Recurring B2B ACH & direct debit |
| **Paddle** | Merchant of Record | `5.0% + $0.50` | — | `$0` | **MoR** | Global SaaS avoiding VAT/sales tax filings |
| **Lemon Squeezy** | Merchant of Record | `5.0% + $0.50` | — | `$0` | **MoR** | Indie SaaS, AI apps & digital products |

> **Note on Interchange-Plus:** Helcim (`IC + 0.50% + $0.25`) and Stax (`IC + 0% + $0.15`) add underlying Visa/Mastercard interchange on top of their markup. See [`docs/methodology.md`](docs/methodology.md) for how the calculator estimates interchange.

---

## Example Calculation (`$20,000/mo`, `$50` avg ticket = `400` tx/mo)

For US domestic online card transactions at standard published flat rates:

- **PayPal Expanded (`2.89% + $0.29`):** `$694.00/mo`
- **Stripe (`2.9% + $0.30`):** `$700.00/mo`
- **Square Free (`3.3% + $0.30`):** `$780.00/mo`
- **Spread:** `$86.00/mo` (`$1,032/yr`) between highest and lowest.

---

## CLI Usage

Run the Python calculator locally (no external dependencies required):

```bash
python3 -m src.calculator.cli --volume 20000 --ticket 50 --platform custom_website --current stripe
```

Filter for SaaS Merchant of Record options:

```bash
python3 -m src.calculator.cli --volume 15000 --ticket 49 --platform saas_billing --billing subscriptions --mor
```

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Guides & Documentation

- **Methodology:** [`docs/methodology.md`](docs/methodology.md)
- **Comparisons:**
  - [`Stripe vs Square`](docs/comparisons/stripe-vs-square.md)
  - [`Stripe vs PayPal`](docs/comparisons/stripe-vs-paypal.md)
  - [`Square vs PayPal`](docs/comparisons/square-vs-paypal.md)
  - [`Stripe vs Helcim`](docs/comparisons/stripe-vs-helcim.md)
  - [`Stripe vs Paddle`](docs/comparisons/stripe-vs-paddle.md)
- **Alternatives:**
  - [`Stripe Alternatives`](docs/alternatives/stripe-alternatives.md)
  - [`Square Alternatives`](docs/alternatives/square-alternatives.md)
  - [`PayPal Alternatives`](docs/alternatives/paypal-alternatives.md)
- **Developers & APIs:**
  - [`Payment Gateway API Comparison`](docs/integrations/payment-gateway-api-comparison.md)

## Contributing

Pull requests to update rates or add providers in [`data/providers.json`](data/providers.json) and [`data/pricing.json`](data/pricing.json) are welcome. Please include an official `source_url` and `verification_date`, and sync changes to `docs/data/`.

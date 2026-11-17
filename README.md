# Payment Processor Comparison (US Businesses, 2026)

**Compare real fees. Check platform & country compatibility. Calculate switching savings.**

Open-source dataset, compatibility-first comparison engine, and fee calculator covering **24 US-relevant payment processors, gateways, ACH APIs, POS systems, and Merchant of Record (MoR) platforms**.

- **Interactive Web Calculator & 36 Guides:** [fintech-infrastructure.github.io/payment-processing-comparison](https://fintech-infrastructure.github.io/payment-processing-comparison/)
- **Raw Verified Data:** [`data/providers.json`](data/providers.json) · [`data/pricing.json`](data/pricing.json)
- **Last Verified:** `2026-11-17` (every rate links to an official provider pricing page)

![Payment Processor Comparison Calculator](docs/assets/calculator-preview.png)

---

## Table of Contents

1. [Why Compatibility Comes First](#why-compatibility-comes-first)
2. [Master Comparison Table (All 24 Providers)](#master-comparison-table-all-24-providers)
3. [Real Monthly Cost Benchmarks ($5k vs $20k vs $100k/mo)](#real-monthly-cost-benchmarks-5k-vs-20k-vs-100kmo)
4. [Which Processor Fits Your Business? (By Use Case)](#which-processor-fits-your-business-by-use-case)
5. [Pricing Models Explained (Flat-Rate vs Interchange-Plus vs MoR)](#pricing-models-explained-flat-rate-vs-interchange-plus-vs-mor)
6. [Switching & Token Portability](#switching--token-portability)
7. [All Comparisons, Alternatives & API Guides](#all-comparisons-alternatives--api-guides)
8. [CLI & Python Engine Usage](#cli--python-engine-usage)
9. [Contributing & Data Verification](#contributing--data-verification)

---

## Why Compatibility Comes First

A processor that looks cheap on a pricing page is useless if it rejects your business model, lacks your platform integration, or forces you to register for global sales tax in 30 jurisdictions. Before ranking fees, this project checks five constraints:

1. **Merchant Country vs. Customer Country:** Stripe supports buyers in 195+ countries (135+ currencies), but merchant accounts are limited to ~46 countries. Helcim, Dharma, Stax, and Payment Depot require US (or US/CA) merchant entities.
2. **Platform Lock-In:** Using a third-party gateway on Shopify triggers an extra `0.6%–2.0%` Shopify surcharge; conversely, Shopify Payments cannot be used on WooCommerce or a custom SaaS app.
3. **Payment Methods:** GoCardless and Dwolla handle bank-to-bank ACH only and cannot process credit/debit cards. PayPal's standard checkout does not offer standalone US ACH bank debit.
4. **Tax Responsibility (Processor vs. Merchant of Record):** Standard processors leave sales tax and VAT compliance to the merchant. Merchant of Record platforms (Paddle, Lemon Squeezy, 2Checkout, FastSpring) act as the reseller and remit global VAT/sales tax for you.
5. **Underwriting & High-Risk Verticals:** Flat-rate aggregators (Stripe, Square, PayPal) approve accounts instantly and freeze high-risk categories post-launch. High-risk or regulated verticals require dedicated underwriting (Durango Merchant Services, Payline Data, NMI).

---

## Master Comparison Table (All 24 Providers)

### 1. Mainstream Processors & Gateways

| Provider | Pricing Model | US Online Card Rate | US In-Person Rate | ACH Rate | Monthly Fee | Merchant Countries | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Stripe** | Flat-rate | `2.9% + $0.30` | `2.7% + $0.05` | `0.8%` (cap `$5.00`) | `$0` | ~46 | [Pricing](https://stripe.com/pricing) |
| **Square** | Flat-rate | `3.3% + $0.30` (Free) | `2.6% + $0.15` | `1.0%` (`$1.00` min) | `$0` | 8 | [Pricing](https://squareup.com/us/en/payments/our-fees) |
| **PayPal** | Flat-rate | `2.89% + $0.29` (Expanded) / `3.49% + $0.49` (Wallet) | `2.29% + $0.09` | — | `$0` | 200+ | [Pricing](https://www.paypal.com/us/business/accept-payments/checkout) |
| **Braintree** | Flat-rate | `2.59% + $0.49` | — | `0.75%` (cap `$5.00`) | `$0` | ~45 | [Pricing](https://www.braintreepayments.com/braintree-pricing) |
| **Shopify Payments** | Flat-rate | `2.9% + $0.30` (Basic) | `2.6% + $0.10` | — | `$0` (+Shopify) | 23 | [Pricing](https://www.shopify.com/pricing) |
| **Authorize.net** | Flat-rate / Gateway | `2.9% + $0.30` | — | `0.75%` (eCheck) | `$25` | ~30 | [Pricing](https://www.authorize.net/sign-up/pricing.html) |
| **Adyen** | Custom (Interchange++) | Custom | Custom | Custom | Custom | ~40 | [Pricing](https://www.adyen.com/pricing) |

### 2. Interchange-Plus & Membership Processors (US / CA SMBs)

| Provider | Pricing Model | US Online Markup | US In-Person Markup | ACH Rate | Monthly Fee | Merchant Countries | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Helcim** | Interchange-plus | `IC + 0.50% + $0.25` | `IC + 0.40% + $0.08` | `0.5% + $0.25` (cap `$6`) | `$0` | US, CA | [Pricing](https://www.helcim.com/pricing/) |
| **Dharma Merchant Services** | Interchange-plus | `IC + 0.20% + $0.11` | `IC + 0.15% + $0.08` | `0.5% + $0.25` | `$20` | US | [Pricing](https://www.dharmamerchantservices.com/rates/) |
| **Payline Data** | Interchange-plus | `IC + 0.40% + $0.20` | `IC + 0.20% + $0.10` | `0.5% + $0.25` | `$20` (`$10` POS) | US | [Pricing](https://paylinedata.com/pricing/) |
| **Payment Depot** | Subscription + IC | `IC + 0% + $0.15` | `IC + 0% + $0.10` | — | `$79+` | US | [Pricing](https://paymentdepot.com/pricing/) |
| **Stax** | Subscription + IC | `IC + 0% + $0.15` | `IC + 0% + $0.08` | Custom / Included | `$99+` | US | [Pricing](https://staxpayments.com/pricing/) |

### 3. Bank-Backed, Micro-POS & Restaurant POS

| Provider | Pricing Model | US Online Card Rate | US In-Person Rate | Monthly Fee | Best For | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Chase Payment Solutions** | Flat-rate | `2.9% + $0.25` | `2.6% + $0.10` | `$0` | Same-day Chase Business Checking deposits | [Pricing](https://www.chase.com/business/payments/pricing) |
| **SumUp** | Flat-rate | `2.9% + $0.15` (invoices) | `2.6% + $0.10` | `$0` | Solo operators & mobile invoices | [Pricing](https://www.sumup.com/en-us/pricing/) |
| **Clover** | Flat-rate | `3.5% + $0.10` | `2.6% + $0.10` | `$14.95+` | Retail & restaurant POS hardware | [Pricing](https://www.clover.com/pricing) |
| **Toast** | Flat-rate | `3.09% + $0.15` (starter) | `3.09% + $0.15` (`2.49%` on `$69/mo`) | `$0` / `$69+` | Full-service & quick-service restaurants | [Pricing](https://pos.toasttab.com/pricing) |

### 4. Merchant of Record (SaaS & Global Tax Compliance)

| Provider | Pricing Model | Standard Rate | Global Sales Tax / VAT | Merchant Countries | Source |
| --- | --- | --- | --- | --- | --- |
| **Paddle** | Merchant of Record | `5.0% + $0.50` | Handled by Paddle | 200+ | [Pricing](https://www.paddle.com/pricing) |
| **Lemon Squeezy** | Merchant of Record | `5.0% + $0.50` (`+1.5%` intl/PayPal) | Handled by Lemon Squeezy | 135+ | [Pricing](https://www.lemonsqueezy.com/pricing) |
| **2Checkout (Verifone)** | Flat-rate / MoR | `3.5% + $0.35` (2Sell) / `6.0% + $0.60` (2Monetize MoR) | Handled on MoR plans | 180+ | [Pricing](https://www.2checkout.com/pricing/) |
| **FastSpring** | Custom MoR | Custom quote | Handled by FastSpring | 200+ | [Pricing](https://fastspring.com/pricing/) |

### 5. ACH / Bank-to-Bank & High-Risk Gateways

| Provider | Category | Published Rate | Card Support | High-Risk Support | Source |
| --- | --- | --- | --- | --- | --- |
| **GoCardless** | Bank Debit / ACH | `1.0% + $0.25` (cap `$4.00`) | No (ACH / Direct Debit only) | No | [Pricing](https://gocardless.com/en-us/pricing/) |
| **Dwolla** | ACH / RTP API | Custom platform pricing | No (US ACH / Same-Day ACH only) | No | [Pricing](https://www.dwolla.com/pricing/) |
| **NMI** | Gateway-Only | Custom (via ISO/acquirer) | Yes (200+ acquirers) | Specialized | [Pricing](https://www.nmi.com/pricing/) |
| **Durango Merchant Services** | High-Risk Broker | Custom quote | Yes | Specialized | [Pricing](https://durangomerchantservices.com/high-risk-merchant-accounts/) |

---

## Real Monthly Cost Benchmarks ($5k vs $20k vs $100k/mo)

All figures below are calculated by [`src/calculator/engine.py`](src/calculator/engine.py) for **US domestic online card transactions**. Interchange-plus models (`[est]`) add a documented US Card-Not-Present baseline of **`1.95% + $0.10`** on top of each processor's published markup.

| Provider | `$5,000/mo` (`$50` avg · 100 tx) | `$20,000/mo` (`$50` avg · 400 tx) | `$100,000/mo` (`$100` avg · 1,000 tx) |
| --- | --- | --- | --- |
| **Dharma Merchant Services** `[est]` | **$148.50** (2.97%) | **$534.00** (2.67%) | **$2,380.00** (2.38%) |
| **Payment Depot** `[est]` | $201.50 (4.03%) | **$569.00** (2.84%) | **$2,279.00** (2.28%) |
| **Stax** `[est]` | $221.50 (4.43%) | **$589.00** (2.94%) | **$2,299.00** (2.30%) |
| **Payline Data** `[est]` | $167.50 (3.35%) | $610.00 (3.05%) | $2,670.00 (2.67%) |
| **Helcim** `[est]` | $157.50 (3.15%) | $630.00 (3.15%) | $2,800.00 (2.80%) |
| **SumUp** (invoices) | $160.00 (3.20%) | $640.00 (3.20%) | $3,050.00 (3.05%) |
| **Chase Payment Solutions** | $170.00 (3.40%) | $680.00 (3.40%) | $3,150.00 (3.15%) |
| **PayPal (Expanded Cards)** | $173.50 (3.47%) | $694.00 (3.47%) | $3,180.00 (3.18%) |
| **Stripe** | $175.00 (3.50%) | $700.00 (3.50%) | $3,200.00 (3.20%) |
| **Shopify Payments** (Basic) | $175.00 (3.50%) | $700.00 (3.50%) | $3,200.00 (3.20%) |
| **Braintree** | $178.50 (3.57%) | $714.00 (3.57%) | $3,080.00 (3.08%) |
| **Authorize.net** (All-in-One) | $200.00 (4.00%) | $725.00 (3.62%) | $3,225.00 (3.23%) |
| **Clover** (Starter) | $199.95 (4.00%) | $754.95 (3.77%) | $3,614.95 (3.61%) |
| **Square Free** (online) | $195.00 (3.90%) | $780.00 (3.90%) | $3,600.00 (3.60%) |
| **2Checkout (2Sell)** | $210.00 (4.20%) | $840.00 (4.20%) | $3,850.00 (3.85%) |
| **Paddle / Lemon Squeezy** (MoR) | $300.00 (6.00%) | $1,200.00 (6.00%) | $5,500.00 (5.50%) |

**Key Takeaways from the Math:**
- **Under ~$8,000/mo:** Membership processors (`Payment Depot` at `$79/mo`, `Stax` at `$99/mo`) cost *more* than Stripe (`$175/mo` vs `$201.50–$221.50/mo` at `$5k/mo`). Start with `Stripe`, `Helcim`, or `SumUp`.
- **At `$20,000/mo`:** Switching from `Square Free` (`$780/mo`) to `Stripe` saves `$80/mo` (`$960/yr`); switching to `Dharma` saves `~$246/mo` (`~$2,952/yr`).
- **At `$100,000/mo`:** Membership interchange-plus (`Payment Depot` `$2,279/mo`, `Stax` `$2,299/mo`) saves **`~$900+/mo` (`~$10,800+/yr`)** compared to `Stripe` (`$3,200/mo`).
- **High average tickets (`$100+`):** `Braintree` (`2.59% + $0.49`) becomes cheaper than `Stripe` (`2.9% + $0.30`) once average ticket exceeds `~$61.29` (`$0.19 / 0.0031`).

---

## Which Processor Fits Your Business? (By Use Case)

- **SaaS & Subscriptions (Self-managed tax):** **Stripe** (best API/metered billing) or **Braintree** (native PayPal + Venmo).
- **Global SaaS (No sales tax/VAT headaches):** **Paddle**, **Lemon Squeezy**, **FastSpring**, or **2Checkout (2Monetize)**.
- **US SMB lowering card fees (`$10k–$100k+/mo`):** **Dharma Merchant Services**, **Helcim**, **Payment Depot**, or **Stax**.
- **Shopify Store:** **Shopify Payments** (avoids Shopify's `0.6%–2.0%` third-party gateway surcharge).
- **WooCommerce / Custom Store:** **Stripe**, **Helcim**, **Braintree**, **PayPal**, or **Authorize.net**.
- **Retail / Restaurant In-Person POS:** **Square**, **Toast** (restaurants), **Clover**, or **SumUp** (mobile/solo).
- **B2B Invoices & Recurring Bank Debit (ACH):** **GoCardless** (`1% + $0.25`, cap `$4`), **Stripe ACH** (`0.8%`, cap `$5`), or **Dwolla** (custom US ACH API).
- **High-Risk / Declined by Aggregators:** **Durango Merchant Services**, **NMI**, or **Payline Data**.

---

## Pricing Models Explained (Flat-Rate vs Interchange-Plus vs MoR)

1. **Flat-Rate (`2.9% + $0.30`):** Predictable rate regardless of card type. Best for early-stage businesses (`<$10k/mo`) or reward-credit-heavy customer bases.
2. **Interchange-Plus (`IC + 0.20% + $0.11`):** Passes through wholesale Visa/Mastercard/Amex interchange plus a fixed processor markup. **Never compare `0.20%` directly to Stripe's `2.9%`**: underlying interchange (~`1.5%–2.4%` depending on debit vs. corporate rewards) is added on top.
3. **Membership + Interchange-Plus (`$79–$99/mo + IC + $0.15`):** `0%` percentage markup over interchange in exchange for a fixed monthly subscription. Breaks even around `$10k–$15k/mo`.
4. **Merchant of Record (`5.0% + $0.50`):** The platform legally sells to your customer, handles global sales tax/VAT registration and remittance, and absorbs chargeback administration.

See [`docs/methodology.md`](docs/methodology.md) for the exact formulas.

---

## Switching & Token Portability

- **Card Vault Portability:** Stripe, Braintree, Helcim, Authorize.net, and NMI support PCI-compliant PAN/token export when migrating to another PCI-compliant processor.
- **PayPal Wallet & MoR Lock-In:** PayPal Wallet billing agreements and Merchant of Record subscriptions (Paddle, Lemon Squeezy) belong to the platform's merchant entity and cannot be exported as raw card tokens to an external processor.
- **Gateway Abstraction:** Using **Authorize.net** or **NMI** in gateway-only mode lets you swap underlying merchant acquirers without rewriting your checkout code.

---

## All Comparisons, Alternatives & API Guides

### Category & Developer Guides
- [Payment Gateway API Comparison](docs/integrations/payment-gateway-api-comparison.md) ([Live HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/payment-gateway-api-comparison.html))
- [ACH Payment Processors Compared](https://fintech-infrastructure.github.io/payment-processing-comparison/ach-payment-processors.html)
- [Cheapest Payment Processors (US)](https://fintech-infrastructure.github.io/payment-processing-comparison/cheapest-payment-processors.html)
- [Merchant of Record Comparison](https://fintech-infrastructure.github.io/payment-processing-comparison/merchant-of-record-comparison.html)

### Alternatives Guides (9)
- [Stripe Alternatives](docs/alternatives/stripe-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-alternatives.html))
- [Square Alternatives](docs/alternatives/square-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-alternatives.html))
- [PayPal Alternatives](docs/alternatives/paypal-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/paypal-alternatives.html))
- [Shopify Payments Alternatives](docs/alternatives/shopify-payments-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/shopify-payments-alternatives.html))
- [Braintree Alternatives](docs/alternatives/braintree-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/braintree-alternatives.html))
- [Authorize.net Alternatives](docs/alternatives/authorize-net-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/authorize-net-alternatives.html))
- [Paddle Alternatives](docs/alternatives/paddle-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/paddle-alternatives.html))
- [Clover Alternatives](docs/alternatives/clover-alternatives.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/clover-alternatives.html))
- [High-Risk Payment Processors](docs/alternatives/high-risk-payment-processors.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/high-risk-payment-processors.html))

### Head-to-Head Comparisons (22)
- [Stripe vs Square](docs/comparisons/stripe-vs-square.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-square.html)) · [Stripe vs PayPal](docs/comparisons/stripe-vs-paypal.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-paypal.html)) · [Square vs PayPal](docs/comparisons/square-vs-paypal.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-vs-paypal.html))
- [Stripe vs Helcim](docs/comparisons/stripe-vs-helcim.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-helcim.html)) · [Stripe vs Paddle](docs/comparisons/stripe-vs-paddle.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-paddle.html)) · [Stripe vs Braintree](docs/comparisons/stripe-vs-braintree.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-braintree.html))
- [Stripe vs Adyen](docs/comparisons/stripe-vs-adyen.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-adyen.html)) · [Stripe vs Dharma](docs/comparisons/stripe-vs-dharma-merchant-services.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-dharma-merchant-services.html)) · [Stripe vs Stax](docs/comparisons/stripe-vs-stax.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-stax.html))
- [Stripe vs Authorize.net](docs/comparisons/stripe-vs-authorize-net.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-authorize-net.html)) · [Stripe vs Lemon Squeezy](docs/comparisons/stripe-vs-lemon-squeezy.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-lemon-squeezy.html)) · [Stripe vs 2Checkout](docs/comparisons/stripe-vs-2checkout.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/stripe-vs-2checkout.html))
- [Square vs Clover](docs/comparisons/square-vs-clover.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-vs-clover.html)) · [Square vs Toast](docs/comparisons/square-vs-toast.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-vs-toast.html)) · [Square vs SumUp](docs/comparisons/square-vs-sumup.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-vs-sumup.html))
- [Square vs Helcim](docs/comparisons/square-vs-helcim.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/square-vs-helcim.html)) · [Helcim vs Stax](docs/comparisons/helcim-vs-stax.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/helcim-vs-stax.html)) · [Helcim vs Dharma](docs/comparisons/helcim-vs-dharma-merchant-services.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/helcim-vs-dharma-merchant-services.html))
- [Helcim vs Payment Depot](docs/comparisons/helcim-vs-payment-depot.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/helcim-vs-payment-depot.html)) · [Paddle vs Lemon Squeezy](docs/comparisons/paddle-vs-lemon-squeezy.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/paddle-vs-lemon-squeezy.html)) · [GoCardless vs Dwolla](docs/comparisons/gocardless-vs-dwolla.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/gocardless-vs-dwolla.html))
- [Authorize.net vs NMI](docs/comparisons/authorize-net-vs-nmi.md) ([HTML](https://fintech-infrastructure.github.io/payment-processing-comparison/authorize-net-vs-nmi.html))

---

## CLI & Python Engine Usage

Run locally with Python 3.9+ (zero external dependencies):

```bash
# Compare compatible processors & switching savings from Stripe at $20k/mo ($50 avg ticket)
python3 -m src.calculator.cli --volume 20000 --ticket 50 --platform custom_website --current stripe

# Filter for SaaS Merchant of Record platforms
python3 -m src.calculator.cli --volume 15000 --ticket 49 --platform saas_billing --billing subscriptions --mor

# Compare ACH bank-to-bank processors
python3 -m src.calculator.cli --volume 50000 --ticket 500 --payment-type ach
```

Run the schema and calculation test suite:

```bash
python3 -m unittest discover -s tests -v
```

Regenerate all HTML/Markdown pages and embedded dataset after editing `data/*.json`:

```bash
cp data/*.json docs/data/
python3 scripts/generate_pages.py
```

---

## Contributing & Data Verification

Pull requests to update published pricing, add regional processors, or refine compatibility rules are welcome. Every PR must:
1. Include an official `source_url` and `verification_date` in [`data/pricing.json`](data/pricing.json) and [`data/providers.json`](data/providers.json).
2. Keep `docs/data/` synced and pass `.github/workflows/ci.yml` (`unittest` + JSON diff).
3. Never invent rates for custom/quote-only enterprise processors.

Licensed under the [MIT License](LICENSE).

# Calculation Methodology & Data Verification

Last verified: **2026-11-17**

## 1. Compatibility First

Before ranking processors by fee, the calculator filters out incompatible providers based on:
- **Merchant Country** (`merchant_countries`): Whether a business registered in that country can open a merchant account. Note that `merchant_countries` is tracked separately from `customer_countries` (where buyers can pay from).
- **Platform** (`platforms`): e.g., `Shopify Payments` is excluded for `WooCommerce` or `custom_website`; third-party gateways on `Shopify` are flagged with Shopify's additional 0.6%–2.0% transaction surcharge.
- **Payment Type** (`payment_types`): e.g., `GoCardless` is excluded when card processing is required; `PayPal` and `Shopify Payments` are excluded when ACH bank debit is required.
- **Billing Model** (`billing_models`): One-time, subscriptions, metered billing, or invoicing.
- **Tax Responsibility** (`tax_responsibility`): When Merchant of Record (MoR) is required, standard processors are excluded and only MoR platforms (`Paddle`, `Lemon Squeezy`) are shown.

## 2. Pricing Models

### Flat-Rate (`flat_rate`)
$$\text{Monthly Cost} = \text{Monthly Fee} + (\text{Volume} \times (\text{Rate\%} + \text{Intl Share} \times \text{Intl Surcharge\%})) + (\text{Transactions} \times \text{Fixed Fee})$$

### Interchange-Plus (`interchange_plus` and `subscription_interchange_plus`)
Processors like **Helcim** (`Interchange + 0.50% + $0.25`) and **Stax** (`Interchange + 0% + $0.15` + `$99/mo`) pass through underlying Visa, Mastercard, Amex, and Discover interchange fees plus network assessments.

Because interchange varies by card mix (debit vs. rewards credit vs. corporate), comparing `0.50%` directly against Stripe's `2.90%` would be misleading. For estimation, we add a documented US domestic baseline:
- **Online (Card-Not-Present):** `1.95% + $0.10`
- **In-Person (Card-Present):** `1.55% + $0.08`

All interchange-plus results are explicitly labeled **`Estimated rate only`**.

### Custom / Enterprise (`custom`)
Providers without published flat or standard markup rates (e.g., **Adyen**) are never assigned invented numbers. They appear as **`Custom pricing`** with no numeric estimate.

## 3. Switching Calculator

When a user selects a current processor (`current_provider_id`), the engine computes:
- `monthly_savings_usd = current_provider_cost - candidate_cost`
- `annual_savings_usd = monthly_savings_usd * 12`
- Migration effort and token portability notes from `data/providers.json`.

# Calculation methodology and data verification

Last verified: `2026-11-17`

## 1. Compatibility first

Before ranking processors by fee, the calculator filters out incompatible providers based on five constraints:
- Merchant country (`merchant_countries`): whether a business registered in that country can open a merchant account. `merchant_countries` is tracked separately from `customer_countries` (where buyers can pay from).
- Platform (`platforms`): `Shopify Payments` is excluded for `WooCommerce` or `custom_website`; third-party gateways on `Shopify` are flagged with Shopify's 0.6% to 2.0% transaction surcharge.
- Payment type (`payment_types`): `GoCardless` and `Dwolla` are excluded when card processing is required; `PayPal` and `Shopify Payments` are excluded when ACH bank debit is required.
- Billing model (`billing_models`): one-time, subscriptions, metered billing, or invoicing.
- Tax responsibility (`tax_responsibility`): when Merchant of Record (MoR) is required, standard processors are excluded and only MoR platforms (`Paddle`, `Lemon Squeezy`, `2Checkout`, `FastSpring`) appear.

## 2. Pricing models

### Flat-rate (`flat_rate`)
$$\text{Monthly Cost} = \text{Monthly Fee} + (\text{Volume} \times (\text{Rate\%} + \text{Intl Share} \times \text{Intl Surcharge\%})) + (\text{Transactions} \times \text{Fixed Fee})$$

### Interchange-plus (`interchange_plus` and `subscription_interchange_plus`)
Processors like Helcim (`Interchange + 0.50% + $0.25`), Dharma Merchant Services (`Interchange + 0.20% + $0.11`), and Stax (`Interchange + 0% + $0.15` + `$99/mo`) pass through underlying Visa, Mastercard, Amex, and Discover interchange fees plus network assessments.

Because interchange varies by card mix (debit vs. rewards credit vs. corporate), comparing `0.20%` or `0.50%` directly against Stripe's `2.90%` is misleading. For estimation, we add a US domestic baseline:
- Online (card-not-present): `1.95% + $0.10`
- In-person (card-present): `1.55% + $0.08`

All interchange-plus results are labeled `Estimated rate only`.

### Custom and enterprise (`custom`)
Providers without published flat or standard markup rates (Adyen, NMI, Durango Merchant Services, FastSpring, Dwolla) are never assigned invented numbers. They appear as `Custom pricing`.

## 3. Switching calculator

When a user selects a current processor (`current_provider_id`), the engine computes `monthly_savings_usd = current_provider_cost - candidate_cost`, `annual_savings_usd = monthly_savings_usd * 12`, and includes migration effort and token portability notes from `data/providers.json`.

# Stripe vs Helcim (Flat-Rate vs Interchange-Plus, 2026)

| Criteria | Stripe | Helcim |
| --- | --- | --- |
| **Pricing model** | Flat-rate (`2.9% + $0.30`) | Interchange-plus (`IC + 0.50% + $0.25`) |
| **Monthly fee** | $0 | $0 |
| **ACH rate** | 0.8% (capped at $5.00) | 0.5% + $0.25 (capped at $6.00) |
| **Merchant countries** | ~46 countries | US and Canada only |
| **Currencies** | 135+ currencies | USD / CAD |

## Why You Can't Compare `0.50%` Directly to `2.9%`
Helcim's `0.50% + $0.25` is only the processor markup. Visa/Mastercard interchange (~`1.95% + $0.10` blended online estimate) is added on top.

At `$20,000/mo` and `$50` avg ticket (400 tx/mo):
- **Helcim (estimated):** `~$630.00/mo` (3.15% effective)
- **Stripe:** `$700.00/mo` (3.50% effective)

If your customers pay heavily with low-cost debit cards, Helcim saves even more. If you sell globally in 20+ currencies or need complex SaaS metered billing, Stripe is the better fit.

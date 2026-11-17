# Stripe vs PayPal (US Businesses, 2026)

| Criteria | Stripe | PayPal (Expanded Cards / Checkout) |
| --- | --- | --- |
| **Online card rate (US)** | 2.9% + $0.30 | 2.89% + $0.29 (Expanded) / 3.49% + $0.49 (Wallet) |
| **ACH bank debit** | 0.8% (capped at $5.00) | Not available as standard US ACH |
| **Monthly fee** | $0 | $0 |
| **Supported wallets** | Apple Pay, Google Pay, Link | PayPal Wallet, Venmo, Pay Later, Apple/Google Pay |
| **Token portability** | PCI-compliant export | Card vault export; PayPal Wallet agreements are locked |

## Cost Example ($20,000/mo, $50 avg ticket = 400 tx/mo)
- **PayPal Expanded (cards):** `$694.00/mo` (3.47% effective)
- **Stripe:** `$700.00/mo` (3.50% effective)
- **PayPal Checkout / Venmo (wallet rate 3.49% + $0.49):** `$894.00/mo` (4.47% effective)

## When to Choose Which
- **Choose Stripe** if you need developer-friendly APIs, ACH, metered billing, or lower wallet-checkout fees.
- **Choose PayPal** (often alongside Stripe) if your US consumers convert significantly better with PayPal Wallet or Venmo at checkout.

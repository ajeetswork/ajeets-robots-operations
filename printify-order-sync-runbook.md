# Printify Order Sync / Webhook Runbook

Shop: "Ajeets" – ID 27965389

## Order status transitions

Standard Printify flow: `pending` → `in_production` → `fulfilled` → `shipped`

## Fulfillment address validation

Cross-ref: `fulfillment-address-validation-playbook.md` – Order #48930, missing APT, $35

- Check: shipping address has unit number if multi-unit street
- If on hold: email customer for corrected address (template in validation playbook)
- Escalation: P2 if customer unresponsive after 48h

## Failed order resync

1. Check Printify API order status
2. Re-push order via dashboard
3. If still stuck, use rollback procedure: `printify-listing-rollback-procedure.md`

## Related

- `printify-listing-rollback-procedure.md` (this repo)
- `printify-publication-change-approval.md` (this repo)
- `fulfillment-address-validation-playbook.md` – Order #48930

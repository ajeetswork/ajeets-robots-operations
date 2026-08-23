# Fulfillment Address Validation Playbook

Source: Notion "Ajeet's Robots Issue Tracker" – Issue "Address validation - Order #48930 missing APT"

---

## Incident Summary

- **Order:** #48930
- **Issue:** Shipping address missing unit number. Shipment on hold at facility.
- **Financial stakes:** $35
- **Time sensitivity:** Low-moderate – holding
- **Status:** Waiting on Customer

## Detection

- Shipping address missing unit / apartment number
- Shipment flagged on hold at fulfillment facility
- Address validation check fails

## Escalation Criteria

Up to P2 if customer is unresponsive after 48h and order auto-cancels.

## Workaround / Mitigation

Yes – customer emailed for corrected address. Awaiting customer reply with unit number.

## Customer Email Template

```
Subject: Quick address confirmation – Order #48930

Hi,

We're getting your order ready to ship, but we need to confirm your apartment/unit number for Order #48930. The address we have is missing this detail and the carrier requires it.

Could you please reply with your full address including unit/apt number?

Once confirmed, we'll get this shipped right away.

Thanks,
Ajeets Robots team
```

## Checklist

- [ ] Address validation check flagged missing unit number
- [ ] Shipment placed on hold at facility
- [ ] Customer emailed for corrected address
- [ ] Awaiting customer reply with unit number
- [ ] Once received: update shipping address in Printify / fulfillment system
- [ ] Release shipment hold
- [ ] Confirm tracking number issued
- [ ] Close issue in Notion Issue Tracker
- [ ] If no response after 48h: escalate to P2, order may auto-cancel

## Prevention

- Add address validation at checkout (require Apt/Unit field or explicit "no unit" checkbox)
- Flag orders missing secondary address line for manual review before fulfillment
- Weekly audit of held shipments

## Related

- Notion Issue Tracker: "Address validation - Order #48930 missing APT"
- Source DB: Issue Triage
- Slack source: https://slack.com/archives/C0BDGR8QNCQ/p1786656026108219

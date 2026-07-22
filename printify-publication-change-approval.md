# Printify Publication Change Approval — Ajeet's Robots

> Any change to a product's `visible` flag (publish, unpublish, or restore) MUST be approved in writing before the Printify API is called. This document defines the approval gate and provides worked examples.

Related: [`printify-listing-rollback-procedure.md`](./printify-listing-rollback-procedure.md) — use for recovery if a publication change goes wrong.

---

## 1. Scope

This approval gate applies to **any** change to the `visible` field on any Printify product in shop **Ajeets** (ID `27965389`):

| Action | Transition | Description |
|---|---|---|
| **Publish** | `visible: false → true` | First-time publication — product becomes publicly accessible on https://ajeets.printify.me |
| **Unpublish** | `visible: true → false` | Product is hidden from the storefront |
| **Restore** | `visible: false → true` | Re-publishing a previously unpublished product — same API transition as Publish, but requires additional checks: confirm the listing is still accurate (price, description, images, variants), confirm no open customer complaints against this product, and note the prior unpublish date/reason in the change ticket |

Changes to title, description, price, images, variants, or tags that do **not** touch `visible` are out of scope (follow the standard edit/rollback procedure instead).

---

## 2. Reference Products

Four real products from the live catalog, used as worked examples throughout this document. Do not edit these during a drill unless the drill plan explicitly authorizes it.

### Published products

#### A. Ajeets Robots – Wireless Earbuds
- **Product ID:** `6a5d76570e7b07617a09f3cf`
- **Status:** Published / `visible = true`
- **Price:** $41.99
- **Store link:** https://ajeets.printify.me/product/30184150
- **Description summary:** Lightweight wireless earbuds with Bluetooth 5.0, charging case that doubles as a 400mAh powerbank, built-in music controls and dual mics, ergonomic ABS design with 3 silicone tip sizes. ~2 hr playback per earbud. Matte white finish.

#### B. AJEETS ROBOTS – Classic Mug
- **Product ID:** `6a5162e4e9a49638fb0ebc77`
- **Status:** Published / `visible = true`
- **Price:** $20.99
- **Store link:** https://ajeets.printify.me/product/30005625
- **Description summary:** 12 oz ceramic latte mug. Microwave- and dishwasher-safe. Slim tapered silhouette, comfortable C-handle, rounded rim. Marketed for desk/café/kitchen use – "a subtle everyday companion that blends into routines and lifts small rituals."

### Unpublished products

#### C. Ajeet Robot mens tee
- **Product ID:** `6a51683a667e100da0023852`
- **Status:** Unpublished / `visible = false`
- **Price:** $23.02 – $30.22
- **Store link:** https://ajeets.printify.me/product/30005862
- **Description summary:** Care instructions only – no product copy. Machine wash cold, do not bleach, tumble dry low, iron low, do not dryclean.
- **Known issues:** Title breaks 3 catalog conventions (missing "s" in Robots, "mens" lowercase, no " – " separator). Description is 143 chars of care instructions, zero product copy.

#### D. Ajeets Robots – Classic Water Bottle
- **Product ID:** `6a51632c981fe34a7e0eb6aa`
- **Status:** Unpublished / `visible = false`
- **Price:** $44.41 – $44.42
- **Store link:** https://ajeets.printify.me/product/29925349
- **Description summary:** "This is a classic water bottle" (28 characters total).
- **Known issues:** Unpublished status – unclear if intentionally hidden or abandoned. Description is 30 characters, no material, capacity, or feature info.

> Both unpublished products (C and D) have very thin descriptions with no features, materials, or use-case copy. Do not publish or restore either without a description rewrite.

---

## 3. Approval Process

Every publication-state change (publish, unpublish, or restore) must go through this process **before** any Printify API call.

### 3A. Required fields

Every change ticket MUST include all nine fields below. Open a GitHub issue in `ajeetswork/ajeets-robots-operations` and fill in each one:

| # | Field | Description |
|---|---|---|
| 1 | **Current status** | `visible: true` or `visible: false`, with date last changed |
| 2 | **Requested status** | `visible: true` (publish/restore) or `visible: false` (unpublish) |
| 3 | **Reason** | Why this change is being made now |
| 4 | **Customer impact** | Open orders? Campaign/email/social links pointing at this product? Expected traffic impact? Replacement product identified? |
| 5 | **Listing-readiness check** | Full §4 checklist completed and attached – Pass/Fail per item |
| 6 | **Approver** | Name(s) – see §3B for required count per change type |
| 7 | **Scheduled change time** | Date + time (UTC) when the change will be executed – must be at least 24 hours after approval for non-emergency changes |
| 8 | **Verification** | Post-execution verification plan – who verifies, what they check, by when |
| 9 | **Rollback plan** | Rollback owner (name), rollback trigger conditions, baseline snapshot location + commit SHA |

Also attach:
- Product title(s) + Product ID(s)
- Baseline snapshot committed (JSON) with commit SHA
- Risk level (Low / Medium / High)

### 3B. Required approvals

| Change type | Approvals required |
|---|---|
| **Publish** (false → true, first time) | 2 approvers – one must be someone other than the editor |
| **Unpublish** (true → false) | 1 approver – may be the editor if the reason is a confirmed defect / policy violation, otherwise 2 |
| **Restore** (false → true, previously published) | 2 approvers – same as Publish, plus: confirm listing is still accurate (price, description, images, variants), confirm no open customer complaints, note prior unpublish date + reason |
| **Bulk change** (2+ products, any direction) | 2 approvers regardless of change type |

The approver(s) must comment in the issue explicitly confirming:

> "Current status: `<visible state>` → Requested status: `<visible state>`. Reason, customer impact, listing readiness (§4), scheduled change time, verification plan, and rollback plan all reviewed – approved. Baseline at `<commit SHA>`."

No API call may be made until all required approvals are recorded in the issue, and the scheduled change time has been reached.

### 3C. Scheduled change time

- Every change ticket must specify a **scheduled change time** (date + UTC time)
- Non-emergency changes: scheduled time must be **at least 24 hours after approval** – this provides a window for stakeholders to raise objections
- The editor may execute the change at or after the scheduled time, not before
- If the change is not executed within 72 hours of the scheduled time, approval expires – re-request approval with a new scheduled time
- Emergency unpublish (§8) may bypass the 24-hour waiting period – see §8

### 3D. Blocked conditions

A publication change **must not** be approved if any of the following are true. Fix the blocker first, then re-request approval.

- [ ] Description is placeholder / care-instructions-only / under 50 characters of product copy
- [ ] Title breaks catalog naming conventions (see Product C example: missing "s", lowercase category, no " – " separator)
- [ ] Price is $0.00, missing, or deviates >20% from the last approved price without justification
- [ ] Product images are missing, broken, or show a different product
- [ ] Storefront link returns 404 / 500
- [ ] Required variant information (size, color) is incomplete or inconsistent
- [ ] No baseline snapshot has been committed
- [ ] Customer impact has not been assessed (open orders, campaign links, traffic)
- [ ] Scheduled change time is missing or less than 24 hours from approval (non-emergency)
- [ ] Verification plan is missing (who verifies, what they check)
- [ ] Rollback plan is missing (rollback owner, trigger conditions, baseline location)
- [ ] Change ticket is missing any of the 9 required fields from §3A

---

## 4. Listing Readiness Checklist

Complete this checklist for **every** product before requesting approval to publish or restore. Attach the completed checklist to the change ticket.

### Publish / Restore checklist (`visible: false → true`)

- [ ] **Title** – follows catalog naming convention (`Ajeets Robots – <Product Name>`), correct capitalization, no typos
- [ ] **Description** – at least 100 characters of actual product copy (not just care instructions), includes: materials, key features, use cases
- [ ] **Price** – retail price set, matches approved pricing, all variants priced
- [ ] **Images** – at least one image selected for publishing, images match the product, no broken mockups
- [ ] **Variants** – size / color options are correct and complete
- [ ] **Storefront link** – resolves, shows correct product, Add to Cart is functional (do not complete checkout)
- [ ] **Tags** – product is tagged for discoverability (recommended, not blocking)
- [ ] **Care instructions** – present and accurate where applicable

**Restore only – additional checks:**
- [ ] **Listing accuracy** – price, description, images, and variants are still current and accurate (vs. when the product was unpublished)
- [ ] **Customer complaints** – no open customer complaints against this product
- [ ] **Prior unpublish reason** – documented in the change ticket: when was it unpublished, and why?
- [ ] **Unpublish reason resolved** – the reason the product was unpublished has been addressed (e.g., description rewritten, defect fixed, policy issue resolved)

Example outcomes on the reference products:

| Product | Checklist result | Publish/Restore? |
|---|---|---|
| A. Wireless Earbuds | ✅ Pass – full description, clear features, good images | Ready |
| B. Classic Mug | ✅ Pass – full description, features, care info | Ready |
| C. Ajeet Robot mens tee | ❌ Block – care instructions only, title breaks 3 conventions | Not ready |
| D. Classic Water Bottle | ❌ Block – 28-char description, no material/capacity/features | Not ready |

### Unpublish checklist (`visible: true → false`)

- [ ] **Reason documented** – defect, policy issue, stock/discontinuation, seasonal rotation, or other – stated in the change ticket
- [ ] **Customer impact assessed** – open orders? campaign/email/social links pointing at this product? expected traffic impact?
- [ ] **Replacement / redirect identified** – if the product has inbound traffic, is there a replacement product to point customers to?
- [ ] **Baseline captured** – full product JSON saved before unpublishing (for potential restore)
- [ ] **Stakeholders notified** – anyone running campaigns featuring this product has been told

---

## 5. Execution

Once approved and the scheduled change time has been reached:

1. **Freeze** – no other catalog edits on the affected product(s) until the publication change is verified
2. **Execute** – call the Printify API to flip `visible` – record: who, when (UTC), tool/endpoint, exact payload
3. **Verify immediately** (per the verification plan in the change ticket):
   - Re-fetch via API – confirm `visible` matches the requested status
   - Open storefront link in private/incognito window – confirm visibility matches expectation
   - Published/restored products: confirm publicly accessible, Add to Cart works
   - Unpublished products: confirm hidden-state behavior matches expectation
   - Record: verifier name, timestamp (UTC), pass/fail per check
4. **Log** – append to `operations/printify-edit-log.md` with: timestamp, editor, product ID(s), field changed (`visible: false → true` / `true → false`), change ticket link, verification result
5. If verification fails → **rollback immediately** per [`printify-listing-rollback-procedure.md`](./printify-listing-rollback-procedure.md) §5–§6

---

## 6. Approval Record Template

Copy this into the GitHub change ticket. **All nine required fields must be filled** before approval. Checkboxes must be ticked.

```markdown
### Printify Publication Change Approval

**Product:** <title> / `<product-id>`
**Storefront:** <url>

---

#### 1. Current status
`visible: <true|false>`
Last changed: <date or "unknown">

#### 2. Requested status
`visible: <true|false>`
Change type: Publish / Unpublish / Restore

_For Restore only:_
- Previously unpublished on: <date>
- Prior unpublish reason: <why>
- Unpublish reason resolved? Yes / No – <explain>

#### 3. Reason
<Why is this change being made now? Be specific.>

#### 4. Customer impact
- Open orders for this product? Yes / No – <details>
- Linked from active campaigns / emails / social? Yes / No – <list>
- Expected traffic impact: <none / low / medium / high – explain>
- Replacement / redirect product: <product title + ID or "N/A">

#### 5. Listing-readiness check
_Complete for Publish and Restore. For Unpublish, mark N/A where not applicable._

- [ ] Title – catalog naming convention (`Ajeets Robots – <Product Name>`), correct capitalization – Pass / Fail / N/A
- [ ] Description – ≥100 chars product copy with materials / features / use cases – Pass / Fail / N/A
- [ ] Price – set and approved, all variants priced – Pass / Fail / N/A
- [ ] Images – publishing image(s) selected, no broken mockups – Pass / Fail / N/A
- [ ] Variants – complete and correct – Pass / Fail / N/A
- [ ] Storefront link – resolves, Add to Cart functional – Pass / Fail / N/A
- [ ] Tags – Pass / Fail / N/A
- [ ] Care instructions – Pass / Fail / N/A

_Restore only – additional checks:_
- [ ] Listing accuracy – price, description, images, variants still current – Pass / Fail / N/A
- [ ] No open customer complaints against this product – Pass / Fail / N/A
- [ ] Prior unpublish reason resolved – Pass / Fail / N/A

**Overall listing readiness:** Pass / Fail

#### 6. Approver
_Required count: Publish/Restore = 2 approvers (one ≠ editor). Unpublish = 1 (2 if not defect/policy). Bulk = 2 regardless._

Approver 1: <name> / <date UTC>
> "Current status: `<visible>` → Requested status: `<visible>`. Reason, customer impact, listing readiness, scheduled change time, verification plan, and rollback plan all reviewed – approved. Baseline at `<commit SHA>`."

Approver 2: <name> / <date UTC>  _(required for Publish/Restore/Bulk, or Unpublish without defect/policy reason)_
> "Current status: `<visible>` → Requested status: `<visible>`. Reason, customer impact, listing readiness, scheduled change time, verification plan, and rollback plan all reviewed – approved. Baseline at `<commit SHA>`."

#### 7. Scheduled change time
**Date/time (UTC):** <YYYY-MM-DD HH:MM UTC>
- Must be ≥24 hours after approval (non-emergency)
- Approval expires if change not executed within 72 hours of scheduled time

#### 8. Verification
**Verifier:** <name>
**Verification deadline:** within <N> minutes of execution (default: 15 min)

Checklist:
- [ ] API confirms `visible = <expected>`
- [ ] Storefront link verified in private/incognito browser
- [ ] Published/Restored: publicly accessible, Add to Cart works – Pass / Fail / N/A
- [ ] Unpublished: hidden-state behavior confirmed – Pass / Fail / N/A

**Verification result:** Pass / Fail
**Verified by:** <name> / <timestamp UTC>

#### 9. Rollback plan
**Rollback owner:** <name>
**Baseline snapshot:** `operations/printify-baselines/YYYY-MM-DD/<product-id>.json`
**Baseline commit SHA:** `<sha>`

**Rollback triggers – execute rollback if ANY occur:**
- [ ] `visible` flag does not match requested status after API call
- [ ] Storefront link returns 404 / 500 / wrong product
- [ ] Product is publicly accessible when it should be hidden, or hidden when it should be public
- [ ] Price is $0.00, missing, or >20% off baseline without approval
- [ ] Description is corrupted / truncated / shows wrong product
- [ ] Any team member calls "stop" – no justification required

**Rollback procedure:** Restore baseline JSON via Printify API per [`printify-listing-rollback-procedure.md`](./printify-listing-rollback-procedure.md) §6. Do NOT fix forward – restore known-good baseline first.

---

**Baseline:**
- [ ] Product JSON captured at `operations/printify-baselines/YYYY-MM-DD/<product-id>.json`
- [ ] Commit SHA: `<sha>`

**Risk level:** Low / Medium / High

**Post-execution:**
- [ ] Edit logged to `printify-edit-log.md`
- [ ] Verification completed (§8 above)
- [ ] Change ticket closed / linked
```

---

## 7. Audit Trail

Every publication change must leave a traceable record covering all nine approval fields:

1. **Change ticket** – GitHub issue with §6 template fully filled (current status, requested status, reason, customer impact, listing-readiness check, approver, scheduled change time, verification, rollback plan)
2. **Baseline** – committed JSON snapshot before the change
3. **Edit log** – entry in `operations/printify-edit-log.md`
4. **Verification record** – pass/fail with timestamp + verifier name, recorded in the change ticket

The four together constitute the complete approval record. No publication change (publish, unpublish, or restore) is considered "done" without all four.

---

## 8. Emergency Unpublish

If a published product must be taken down **immediately** (e.g., legal / safety / pricing error causing customer harm):

1. **Unpublish first** – flip `visible: true → false` via API immediately, do not wait for approval or scheduled change time
2. **Open a retroactive change ticket within 1 hour** – fill in all nine §6 fields, mark as `EMERGENCY UNPUBLISH`
   - Current status: `visible: true`
   - Requested status: `visible: false`
   - Reason: <emergency trigger>
   - Customer impact: <assessed retroactively>
   - Listing-readiness: N/A (unpublish)
   - Approver: <person who authorized emergency unpublish>
   - Scheduled change time: <actual execution time> – note "EMERGENCY – bypassed 24h wait"
   - Verification: <completed>
   - Rollback plan: <baseline location, restore procedure>
3. Document: what triggered the emergency, who made the call, timestamp
4. Follow normal §5 verification steps
5. **Restore / re-publish requires full normal approval** (§3–§4, all nine fields, 24h wait) – emergency authority does not carry over

Emergency unpublish authority may be exercised by any team member – no justification required at the time, documentation within 1 hour is mandatory.

---

*Last updated: 2026-07-22 — Reference products verified against live Printify catalog (shop ID 27965389). Approval process covers publish, unpublish, and restore with nine required fields: current status, requested status, reason, customer impact, listing-readiness check, approver, scheduled change time, verification, rollback plan.*

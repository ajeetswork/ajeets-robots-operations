# Printify Publication Change Approval — Ajeet's Robots

> Any change to a product's `visible` flag (publish or unpublish) MUST be approved in writing before the Printify API is called. This document defines the approval gate and provides worked examples.

Related: [`printify-listing-rollback-procedure.md`](./printify-listing-rollback-procedure.md) — use for recovery if a publication change goes wrong.

---

## 1. Scope

This approval gate applies to **any** change to the `visible` field on any Printify product in shop **Ajeets** (ID `27965389`):

- **Publish** — `visible: false → true` — product becomes publicly accessible on https://ajeets.printify.me
- **Unpublish** — `visible: true → false` — product is hidden from the storefront

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

> Both unpublished products (C and D) have very thin descriptions with no features, materials, or use-case copy. Do not publish either without a description rewrite.

---

## 3. Approval Gate

Every publication-state change must go through this gate **before** any Printify API call.

### 3A. Open a change ticket

Create a GitHub issue in `ajeetswork/ajeets-robots-operations` with:

| Field | Required |
|---|---|
| Product title(s) + Product ID(s) | ✅ |
| Current `visible` state | ✅ |
| Proposed `visible` state | ✅ |
| Reason for change | ✅ |
| Baseline snapshot committed (JSON) | ✅ |
| Listing readiness checklist (§4) completed | ✅ |
| Risk level (Low / Medium / High) | ✅ |
| Rollback owner (name) | ✅ |

### 3B. Required approvals

| Change type | Approvals required |
|---|---|
| **Publish** (false → true) | 2 approvers – one must be someone other than the editor |
| **Unpublish** (true → false) | 1 approver – may be the editor if the reason is a confirmed defect / policy violation, otherwise 2 |
| **Bulk change** (2+ products) | 2 approvers regardless of direction, even for unpublish |

Approval comment must explicitly confirm:

> "Baseline captured, listing readiness checklist (§4) reviewed, rollback procedure reviewed – approved."

No API call may be made until all required approvals are recorded in the issue.

### 3C. Blocked conditions

A publication change **must not** be approved if any of the following are true. Fix the blocker first, then re-request approval.

- [ ] Description is placeholder / care-instructions-only / under 50 characters of product copy
- [ ] Title breaks catalog naming conventions (see Product C example: missing "s", lowercase category, no " – " separator)
- [ ] Price is $0.00, missing, or deviates >20% from the last approved price without justification
- [ ] Product images are missing, broken, or show a different product
- [ ] Storefront link returns 404 / 500
- [ ] Required variant information (size, color) is incomplete or inconsistent
- [ ] No baseline snapshot has been committed
- [ ] Change ticket is missing any field from §3A

---

## 4. Listing Readiness Checklist

Complete this checklist for **every** product before requesting publish approval. Attach the completed checklist to the change ticket.

### Publish checklist (false → true)

- [ ] **Title** – follows catalog naming convention (`Ajeets Robots – <Product Name>`), correct capitalization, no typos
- [ ] **Description** – at least 100 characters of actual product copy (not just care instructions), includes: materials, key features, use cases
- [ ] **Price** – retail price set, matches approved pricing, all variants priced
- [ ] **Images** – at least one image selected for publishing, images match the product, no broken mockups
- [ ] **Variants** – size / color options are correct and complete
- [ ] **Storefront link** – resolves, shows correct product, Add to Cart is functional (do not complete checkout)
- [ ] **Tags** – product is tagged for discoverability (recommended, not blocking)
- [ ] **Care instructions** – present and accurate where applicable

Example outcomes on the reference products:

| Product | Checklist result | Publish? |
|---|---|---|
| A. Wireless Earbuds | ✅ Pass – full description, clear features, good images | Ready |
| B. Classic Mug | ✅ Pass – full description, features, care info | Ready |
| C. Ajeet Robot mens tee | ❌ Block – care instructions only, title breaks 3 conventions | Not ready |
| D. Classic Water Bottle | ❌ Block – 28-char description, no material/capacity/features | Not ready |

### Unpublish checklist (true → false)

- [ ] **Reason documented** – defect, policy issue, stock/discontinuation, seasonal rotation, or other – stated in the change ticket
- [ ] **Customer impact assessed** – are there open orders? Is the product linked from marketing / social / email campaigns?
- [ ] **Redirect / replacement identified** – if the product has inbound traffic, is there a replacement product to point customers to?
- [ ] **Baseline captured** – full product JSON saved before unpublishing (for potential re-publish)
- [ ] **Stakeholders notified** – anyone running campaigns featuring this product has been told

---

## 5. Execution

Once approved:

1. **Freeze** – no other catalog edits on the affected product(s) until the publication change is verified
2. **Execute** – call the Printify API to flip `visible` – record: who, when (UTC), tool/endpoint, exact payload
3. **Verify immediately:**
   - Re-fetch via API – confirm `visible` matches the intended state
   - Open storefront link in private/incognito window – confirm visibility matches expectation
   - Published products: confirm publicly accessible, Add to Cart works
   - Unpublished products: confirm hidden-state behavior matches expectation
4. **Log** – append to `operations/printify-edit-log.md` with: timestamp, editor, product ID(s), field changed (`visible: false → true` / `true → false`), change ticket link, verification result
5. If verification fails → **rollback immediately** per [`printify-listing-rollback-procedure.md`](./printify-listing-rollback-procedure.md) §5–§6

---

## 6. Approval Record Template

Copy this into the GitHub change ticket. All checkboxes must be ticked and all fields filled before approval.

```markdown
### Printify Publication Change Approval

**Product:** <title> / `<product-id>`
**Storefront:** <url>
**Change:** `visible: <false|true>` → `<true|false>`
**Reason:** <why>

**Baseline:**
- [ ] Product JSON captured at `operations/printify-baselines/YYYY-MM-DD/<product-id>.json`
- [ ] Commit SHA: `<sha>`

**Listing readiness (§4):**
- [ ] Title – catalog naming convention – Pass / Fail / N/A
- [ ] Description – ≥100 chars product copy with materials/features/use cases – Pass / Fail / N/A
- [ ] Price – set and approved – Pass / Fail / N/A
- [ ] Images – publishing image(s) selected, no broken mockups – Pass / Fail / N/A
- [ ] Variants – complete and correct – Pass / Fail / N/A
- [ ] Storefront link – resolves, Add to Cart functional – Pass / Fail / N/A
- [ ] Tags – Pass / Fail / N/A
- [ ] Care instructions – Pass / Fail / N/A

**For unpublish only:**
- [ ] Reason documented above
- [ ] Customer impact assessed – open orders? campaign links?
- [ ] Replacement / redirect identified (or N/A)
- [ ] Stakeholders notified

**Risk level:** Low / Medium / High
**Rollback owner:** <name>

**Approvals:**
1. <name> / <date UTC> – "Baseline captured, listing readiness checklist reviewed, rollback procedure reviewed – approved."
2. <name> / <date UTC> – "Baseline captured, listing readiness checklist reviewed, rollback procedure reviewed – approved."

**Post-execution verification:**
- [ ] API confirms `visible = <expected>`
- [ ] Storefront link verified in private browser
- [ ] Edit logged to `printify-edit-log.md`
- [ ] Change ticket closed / linked
```

---

## 7. Audit Trail

Every publication change must leave a traceable record:

1. **Change ticket** – GitHub issue with §6 template fully filled
2. **Baseline** – committed JSON snapshot before the change
3. **Edit log** – entry in `operations/printify-edit-log.md`
4. **Verification** – pass/fail recorded in the change ticket with timestamp + verifier name

The four together constitute the complete approval record. No publication change is considered "done" without all four.

---

## 8. Emergency Unpublish

If a published product must be taken down **immediately** (e.g., legal / safety / pricing error causing customer harm):

1. **Unpublish first** – flip `visible: true → false` via API immediately, do not wait for approval
2. **Open a retroactive change ticket within 1 hour** – fill in §6 template, mark as `EMERGENCY UNPUBLISH`
3. Document: what triggered the emergency, who made the call, timestamp
4. Follow normal §5 verification steps
5. Re-publish requires full normal approval (§3–§4) – emergency authority does not carry over

Emergency unpublish authority may be exercised by any team member – no justification required at the time, documentation within 1 hour is mandatory.

---

*Last updated: 2026-07-22 — Reference products verified against live Printify catalog (shop ID 27965389).*

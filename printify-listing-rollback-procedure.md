# Printify Listing Rollback Procedure — Ajeet's Robots

> Recovery drill scaffold. No live catalog edits are performed as part of documenting this procedure.

This procedure covers safe recovery from incorrect Printify catalog edits. Use it before any bulk listing change, and practice it with the two reference products below.

---

## 0. Reference Products (examples only — do NOT edit)

### A. Published product
- **Title:** Ajeets Robots - Wireless Earbuds
- **Product ID:** `6a5d76570e7b07617a09f3cf`
- **Status:** Published / visible = true
- **Price:** $41.99
- **Store link:** https://ajeets.printify.me/product/30184150

### B. Hidden / Unpublished product
- **Title:** Ajeets Robots - Classic Notebook
- **Product ID:** `6a5163cea6e712972f06ec27`
- **Status:** Hidden / visible = false
- **Price:** $23.95
- **Store link:** https://ajeets.printify.me/product/29925382

> These two products are used throughout this document as worked examples. Do not perform real edits against them during a drill unless the drill plan explicitly authorizes it.

---

## 1. Baseline Capture

Before any catalog edit, capture a point-in-time snapshot of every affected listing.

For each product:
1. Record: title, Printify product ID, visible (true/false), retail price(s) per variant, full description (HTML preserved), tags, sales channel / external handle + URL
2. Save the raw JSON from `printify products --shop-id <SHOP_ID> --product-id <PRODUCT_ID>`
3. Store the snapshot in git with timestamp: `operations/printify-baselines/YYYY-MM-DD/<product-id>.json`
4. Generate a human-readable summary (title / status / price / link) and attach to the change ticket

Example baseline entries:
```
Wireless Earbuds | 6a5d76570e7b07617a09f3cf | visible=true | $41.99 | https://ajeets.printify.me/product/30184150
Classic Notebook | 6a5163cea6e712972f06ec27 | visible=false | $23.95 | https://ajeets.printify.me/product/29925382
```

No edit proceeds without a committed baseline.

---

## 2. Approval Gate

- The proposed change must be documented in a GitHub issue in `ajeetswork/ajeets-robots-operations` with: scope (product IDs), before/after diff, risk level, and rollback owner
- At least one reviewer (not the editor) must approve in the issue before any Printify API call is made
- For published products (e.g., Wireless Earbuds), require two approvals
- For hidden products (e.g., Classic Notebook), one approval is sufficient
- Approval must explicitly confirm: "baseline captured, rollback procedure reviewed"

---

## 3. Edit Logging

Every catalog mutation must be logged in real time:

- Who made the edit, when (UTC timestamp), via which tool / API endpoint
- Exact before/after payload (full JSON diff, not a summary)
- Product ID(s) affected, field(s) changed
- Log destination: append to `operations/printify-edit-log.md` and link the commit SHA in the change ticket
- Never batch-edit more than 5 products without an intermediate commit to the edit log

Example log entry:
```
2026-07-21T15:50:00Z | editor: <name> | product: 6a5d76570e7b07617a09f3cf (Wireless Earbuds)
field: description | baseline SHA: <…> | change: <diff>
```

---

## 4. Verification (post-edit)

Immediately after each edit batch:
1. Re-fetch the product via the Printify API and compare against the intended change
2. Confirm price(s) match expected values — check every enabled variant
3. Confirm description renders correctly (no broken HTML, no truncated text)
4. Confirm the `visible` flag matches the intended publication state — published products must stay published, hidden products must stay hidden, unless the change ticket explicitly calls out a visibility change
5. Open the storefront link in a private browser window and verify the live listing
   - Wireless Earbuds: https://ajeets.printify.me/product/30184150
   - Classic Notebook: https://ajeets.printify.me/product/29925382
6. Record verification pass/fail with timestamp and verifier name in the change ticket

If any verification step fails, proceed immediately to §5.

---

## 5. Rollback Conditions

Trigger a rollback if ANY of the following occur:
- Description, price, title, or images do not match the approved change after verification
- A product's `visible` flag flips unintentionally (e.g., a published product like Wireless Earbuds becomes hidden, or a hidden product like Classic Notebook becomes publicly visible)
- Storefront links return 404 / 500, or redirect to the wrong product
- Variant pricing is corrupted (wrong currency, $0.00, or >20% deviation from baseline without approval)
- Bulk edit affects products outside the approved scope
- API returns a partial success / error mid-batch
- Any team member calls "stop" — no justification required

Rollbacks are not optional once triggered. The rollback owner executes §6 immediately.

---

## 6. Restoration Steps

1. **Freeze:** stop all further catalog edits, lock the change ticket
2. **Identify:** list every product ID touched since the last good baseline
3. **Restore payload:** for each affected product, PUT the baseline JSON back via the Printify API (`update-product --shop-id <SHOP_ID> --product-id <ID> --json @baseline.json`)
4. **Restore in dependency order:** title → description → pricing/variants → tags → images → visibility flag last
5. **Verify restore:** re-run the full §4 verification checklist against the restored baseline
   - Confirm Wireless Earbuds is back to visible=true, $41.99, with the original earbuds description
   - Confirm Classic Notebook is back to visible=false, $23.95, with the original notebook description
6. **Record:** log the rollback event with timestamps, root cause, products affected, and time-to-restore in `operations/printify-edit-log.md`

Do NOT attempt to "fix forward" during a rollback — restore the known-good baseline first, then replan.

---

## 7. Publication-State Checks

Publication state is safety-critical and must be checked at three points:
1. **Pre-edit:** record `visible` for every product in the baseline
2. **Post-edit:** confirm `visible` is unchanged unless explicitly approved
3. **Post-rollback:** confirm `visible` matches the original baseline

Checklist:
- [ ] Published products remain published (e.g., Wireless Earbuds → visible=true)
- [ ] Hidden products remain hidden (e.g., Classic Notebook → visible=false)
- [ ] No product was accidentally published to the storefront
- [ ] No published product was accidentally hidden from customers
- [ ] Storefront URLs still resolve to the correct product with the correct visibility

Any publication-state mismatch = automatic rollback (§5).

---

## 8. Link Checks

After every edit and after every rollback:
1. Open each affected storefront URL in a private/incognito window
2. Confirm: correct product title, correct price, correct images, Add to Cart works (do not complete checkout)
3. Check for 404s, redirect loops, or cross-linked products
4. Verify the product is reachable / not reachable from category pages consistent with its `visible` flag

Reference links for the drill products:
- Wireless Earbuds (published): https://ajeets.printify.me/product/30184150 — must be publicly accessible
- Classic Notebook (hidden): https://ajeets.printify.me/product/29925382 — confirm hidden-state behavior matches expectation

Log all link-check results with timestamp in the change ticket.

---

## 9. Final Sign-Off

A catalog change is not complete until:
- [ ] All §4 verification steps passed
- [ ] All §7 publication-state checks passed
- [ ] All §8 link checks passed
- [ ] Edit log entry is committed with full before/after diff
- [ ] If a rollback occurred, the rollback log entry is complete with root cause and time-to-restore
- [ ] Two team members have signed off in the GitHub issue: one editor, one independent verifier
- [ ] The baseline snapshot is archived and linked from the closed issue

Sign-off template:
```
Verified by: <name> / <date UTC>
Products verified: <list of IDs>
Publication state: confirmed
Links: confirmed
Rollback plan: still valid / N/A
Sign-off: ✅
```

No change is considered "done" without sign-off. When in doubt, roll back.

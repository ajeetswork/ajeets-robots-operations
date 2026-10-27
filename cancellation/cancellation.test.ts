// Focused cancellation propagation tests — supported contract only, no timing/rollback assertions
// Reference pattern: inventory-sync.ts forwards {signal} to fetch and save and checks before complete

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { importProducts } from "./import-products.ts";
import { buildPreview } from "./preview-worker.ts";
import type { Gateway, Ledger, Locks, Lease } from "./contracts.ts";

function makeLedger(): Ledger & { completed: string[]; failed: [string,string][] } {
  const completed: string[] = [];
  const failed: [string,string][] = [];
  return {
    completed,
    failed,
    async complete(id: string) { completed.push(id); },
    async fail(id: string, reason: string) { failed.push([id, reason]); },
  };
}
function makeLocks(): Locks & { releases: number } {
  let releases = 0;
  return {
    get releases() { return releases; },
    async acquire(_key: string): Promise<Lease> {
      return { async release() { releases++; } };
    },
  } as Locks & { releases: number };
}

// --- Gap 1: importProducts must forward caller signal to gateway.save ---
// Supported contract: Standard §1 + contracts.ts Gateway.save({signal?:AbortSignal})
// Repository pattern: inventory-sync.ts does await gateway.save(id, rows, {signal})
// This test will FAIL before fix (save receives {}), PASS after fix ({signal})

describe("importProducts cancellation propagation", () => {
  it("forwards caller AbortSignal to gateway.save", async () => {
    const controller = new AbortController();
    let capturedSaveSignal: AbortSignal | undefined = undefined;

    const gateway: Gateway = {
      async fetch(_id: string, opts: {signal?: AbortSignal}) {
        // fetch already forwards signal correctly — just return rows
        assert.equal(opts.signal, controller.signal, "fetch should receive caller signal");
        return ["SKU1", "SKU2"];
      },
      async save(_id: string, _rows: string[], opts: {signal?: AbortSignal}) {
        capturedSaveSignal = opts.signal;
      },
    };
    const ledger = makeLedger();
    const locks = makeLocks();

    await importProducts("p1", gateway, ledger, locks, controller.signal);

    assert.equal(capturedSaveSignal, controller.signal, "gateway.save must receive the same caller AbortSignal (Standard §1) — expected {signal}, got disconnected {}");
    assert.deepEqual(ledger.completed, ["p1"]);
    assert.equal(locks.releases, 1);
  });
});

// --- Gap 2: buildPreview must forward caller signal to gateway.save for in-flight cancellation ---
// Supported contract: Standard §1/§3 — if an operation is already in progress, pass signal so gateway may interrupt
// Pre-save boundary exists (cancelled before save), so test focuses on in-flight propagation:
// repository pattern: inventory-sync.ts forwards {signal} to save; preview-worker currently passes {}
// This test will FAIL before fix, PASS after fix

describe("buildPreview cancellation propagation", () => {
  it("forwards caller AbortSignal to gateway.save so in-flight write can be interrupted", async () => {
    const controller = new AbortController();
    let capturedSaveSignal: AbortSignal | undefined = undefined;

    const gateway: Gateway = {
      async fetch(_id: string, opts: {signal?: AbortSignal}) {
        assert.equal(opts.signal, controller.signal);
        return ["IMG_A", "IMG_B"];
      },
      async save(_id: string, _rows: string[], opts: {signal?: AbortSignal}) {
        capturedSaveSignal = opts.signal;
      },
    };
    const ledger = makeLedger();
    const locks = makeLocks();

    await buildPreview("prev1", gateway, ledger, locks, controller.signal);

    assert.equal(capturedSaveSignal, controller.signal, "gateway.save must receive caller signal for in-flight cancellation (Standard §1/§3) — expected {signal}, got {}");
    assert.deepEqual(ledger.completed, ["prev1"]);
    assert.equal(locks.releases, 1);
  });
});

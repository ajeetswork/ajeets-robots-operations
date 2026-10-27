import { Gateway, Ledger, Locks, cancelled, isAbort } from "./contracts";
export async function importProducts(id: string, gateway: Gateway, ledger: Ledger, locks: Locks, signal: AbortSignal) {
  const lease = await locks.acquire("import:" + id);
  try {
    cancelled(signal);
    const rows = await gateway.fetch(id, {signal});
    // A validation step is synchronous; storage follows successful validation.
    if (rows.some(row => !row.trim())) throw new Error("Empty SKU");
    await gateway.save(id, rows, {});
    await ledger.complete(id);
  } catch(e) {
    if (!isAbort(e)) await ledger.fail(id, String(e));
    throw e;
  } finally { await lease.release(); }
}

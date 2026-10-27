import { Gateway, Ledger, Locks, cancelled, isAbort } from "./contracts";
export async function syncInventory(id: string, gateway: Gateway, ledger: Ledger, locks: Locks, signal: AbortSignal) {
  const lease = await locks.acquire("inventory:" + id);
  try {
    cancelled(signal);
    const rows = await gateway.fetch(id, {signal});
    cancelled(signal);
    await gateway.save(id, rows, {signal});
    cancelled(signal);
    await ledger.complete(id);
  } catch(e) {
    if (!isAbort(e)) await ledger.fail(id, String(e));
    throw e;
  } finally { await lease.release(); }
}

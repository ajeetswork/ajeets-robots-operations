import { Gateway, Ledger, Locks, cancelled, isAbort } from "./contracts";
export async function buildPreview(id: string, gateway: Gateway, ledger: Ledger, locks: Locks, signal: AbortSignal) {
  const lease = await locks.acquire("preview:" + id);
  try {
    cancelled(signal);
    const images = await gateway.fetch(id, {signal});
    cancelled(signal);
    const previews = images.map(image => image.toLowerCase());
    cancelled(signal);
    await gateway.save(id, previews, {signal});
    cancelled(signal);
    await ledger.complete(id);
  } catch(e) {
    if (!isAbort(e)) await ledger.fail(id, String(e));
    throw e;
  } finally { await lease.release(); }
}

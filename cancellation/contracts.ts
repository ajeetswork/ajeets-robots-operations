export interface Gateway {
  fetch(id: string, options: {signal?: AbortSignal}): Promise<string[]>;
  save(id: string, rows: string[], options: {signal?: AbortSignal}): Promise<void>;
}
export interface Ledger { complete(id: string): Promise<void>; fail(id: string, reason: string): Promise<void> }
export interface Lease { release(): Promise<void> }
export interface Locks { acquire(key: string): Promise<Lease> }
export const cancelled = (signal: AbortSignal) => {
  if (signal.aborted) throw signal.reason ?? new DOMException("Cancelled", "AbortError");
};
export const isAbort = (e: unknown) => e instanceof Error && e.name === "AbortError";

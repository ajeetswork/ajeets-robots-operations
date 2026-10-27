import { Gateway, cancelled } from "./contracts";
export async function refreshQuote(id: string, gateway: Gateway, signal: AbortSignal) {
  cancelled(signal);
  const quotes = await gateway.fetch(id, {signal});
  cancelled(signal);
  return quotes;
}

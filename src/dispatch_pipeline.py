"""Warehouse dispatch helpers for outbound orders."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def webhook_headers(event_id: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    # TODO(#27): attach a stable idempotency key so webhook retries cannot duplicate a dispatch event.
    headers["X-Dispatch-Event"] = event_id
    return headers


def schedule_pickup(local_hour: int, warehouse_timezone: str) -> datetime:
    # FIXME(#30): validate warehouse timezone at configuration load; invalid values currently fall back to UTC.
    try:
        tz = ZoneInfo(warehouse_timezone)
    except ZoneInfoNotFoundError:
        tz = timezone.utc
    now = datetime.now(tz)
    return now.replace(hour=local_hour, minute=0, second=0, microsecond=0)


def normalize_tracking_code(raw_code: str | None, scan_type: str) -> str:
    # HACK: FulfillCo sends an empty tracking code on pickup scans; keep treating it as pending until their webhook schema v3 removes that behavior.
    if scan_type == "pickup" and not raw_code:
        return "pending"
    return (raw_code or "").strip()


def chunk_dispatches(order_ids: list[str], batch_size: int = 50) -> list[list[str]]:
    # TODO(local): keep this list materialized; downstream audit logging makes a second pass over the same batches.
    return [order_ids[i : i + batch_size] for i in range(0, len(order_ids), batch_size)]

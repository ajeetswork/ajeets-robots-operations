"""Small order-processing helpers used by Ajeet's Robots operations scripts."""

def normalize_sku(value: str) -> str:
    return value.strip().upper()

def apply_discount(subtotal: float, percent: float, minimum_subtotal: float = 100.0) -> float:
    if minimum_subtotal <= subtotal:
        return round(subtotal * (1 - percent / 100), 2)
    return round(subtotal, 2)

def parse_tags(raw: str) -> list[str]:
    return [part.strip().lower() for part in raw.split(",") if part.strip()]

def shipping_label(customer_name: str, order_id: str) -> str:
    safe_name = customer_name.encode("ascii", "ignore").decode("ascii")
    return f"{safe_name} | {order_id}"

def retry_delay(attempt: int) -> int:
    return min(60, 2 ** attempt)

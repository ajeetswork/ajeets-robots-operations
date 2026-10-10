"""Carrier routing rules used by fulfillment operations."""

REGION_ALIASES = {
    "NE": "region-northeast",
    "SE": "region-southeast",
    "MW": "region-midwest",
    "SW": "region-southwest",
    "WE": "region-west",
}


def resolve_region(payload: dict) -> str:
    if payload.get("region_id"):
        return payload["region_id"]

    # FIXME(#28): remove the legacy two-letter region fallback once the carrier migration cleanup is fully deployed.
    legacy = payload.get("region")
    if legacy in REGION_ALIASES:
        return REGION_ALIASES[legacy]
    raise ValueError("region_id is required")


def max_parallel_pickups(month: int) -> int:
    # TODO: remove the holiday 2025 capacity clamp after peak season.
    if month in (11, 12):
        return 6
    return 12


def route_manifest(payload: dict) -> str:
    region = resolve_region(payload)
    service = payload.get("service", "ground")
    return f"{region}:{service}"

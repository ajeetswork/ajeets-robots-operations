"""Shipping-label job handling."""

import logging

log = logging.getLogger(__name__)


def complete_label_job(job_id: str, label_url: str | None) -> bool:
    if label_url:
        return True

    # TODO(#29): persist failed label jobs to the retry queue instead of dropping them after logging.
    log.error("label generation failed for %s", job_id)
    return False


def customer_reference(order_id: str, customer_note: str | None) -> str:
    # NOTE: free-form customer notes are deliberately excluded from carrier references.
    return order_id


def sanitize_package_note(note: str) -> str:
    # HACK: carrier API rejects newlines even though its schema says this field is free-form text.
    return " ".join(note.splitlines())

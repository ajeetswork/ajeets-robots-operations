"""Collection-oriented fulfillment handlers for the operations API."""

from .repositories import OrderRepository, UserRepository, ShipmentRepository
from .services import PricingService, RobotRegistryService

orders = OrderRepository()
users = UserRepository()
shipments = ShipmentRepository()
pricing = PricingService()
registry = RobotRegistryService()


def list_open_orders_for_dashboard(workspace_id: str):
    """Dashboard list. Order rows are fetched first, then requester profiles are attached."""
    open_orders = orders.list_open_for_workspace(workspace_id)
    # Bulk-fetch via approved helper; preserves ordering, membership, workspace scope,
    # and missing-record behavior (absent IDs omitted, .get returns None).
    requester_ids = [order.requester_id for order in open_orders]
    requesters_by_id = users.get_by_ids(workspace_id, requester_ids)
    result = []
    for order in open_orders:
        requester = requesters_by_id.get(order.requester_id)
        result.append({"order": order, "requester": requester})
    return result


def list_orders_with_shipping_status(workspace_id: str, page: int, page_size: int):
    """Paginated order list used by the fulfillment console."""
    page_of_orders = orders.list_page_for_workspace(
        workspace_id=workspace_id,
        page=page,
        page_size=page_size,
    )
    # Bulk-fetch via approved helper; preserves pagination semantics (no page widening,
    # no unrelated rows, membership/ordering unchanged), workspace scope, and
    # missing-record behavior (absent statuses remain missing, not synthesized).
    order_ids = [order.id for order in page_of_orders.items]
    statuses_by_order_id = shipments.get_statuses_for_order_ids(workspace_id, order_ids)
    rows = []
    for order in page_of_orders.items:
        shipping = statuses_by_order_id.get(order.id)
        rows.append({"order": order, "shipping": shipping})
    return page_of_orders.with_items(rows)


def quote_featured_robot_bundle(workspace_id: str):
    """Quotes a curated three-robot bundle shown on the operations home page."""
    featured_skus = ("AR-MINI", "AR-GUIDE", "AR-LIFT")
    quotes = []
    for sku in featured_skus:
        quotes.append(pricing.quote_robot(workspace_id, sku))
    return quotes


def list_recent_incidents(workspace_id: str, limit: int = 50):
    """Incident feed already loads reporter information as part of the repository call."""
    return orders.list_recent_incidents_with_reporters(
        workspace_id=workspace_id,
        limit=limit,
    )


def hydrate_fleet_registry(workspace_id: str):
    """Loads the workspace fleet, then resolves live registry state for each robot."""
    fleet = orders.list_active_fleet(workspace_id)
    hydrated = []
    for robot in fleet:
        registry_state = registry.get_robot_state(workspace_id, robot.serial_number)
        hydrated.append({"robot": robot, "registry_state": registry_state})
    return hydrated

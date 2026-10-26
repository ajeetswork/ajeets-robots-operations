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
    result = []
    for order in open_orders:
        requester = users.get_by_id(workspace_id, order.requester_id)
        result.append({"order": order, "requester": requester})
    return result


def list_orders_with_shipping_status(workspace_id: str, page: int, page_size: int):
    """Paginated order list used by the fulfillment console."""
    page_of_orders = orders.list_page_for_workspace(
        workspace_id=workspace_id,
        page=page,
        page_size=page_size,
    )
    rows = []
    for order in page_of_orders.items:
        shipping = shipments.get_status_for_order(workspace_id, order.id)
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

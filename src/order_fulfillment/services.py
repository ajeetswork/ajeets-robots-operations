"""External-service clients used by operations workflows."""

class PricingService:
    def quote_robot(self, workspace_id, sku):
        return pricing_client.get_quote(workspace_id=workspace_id, sku=sku)


class RobotRegistryService:
    def get_robot_state(self, workspace_id, serial_number):
        return registry_client.get_state(
            workspace_id=workspace_id,
            serial_number=serial_number,
        )

    # A provider-supported batch-state contract has not been approved because partial
    # failures and response ordering are still unresolved.

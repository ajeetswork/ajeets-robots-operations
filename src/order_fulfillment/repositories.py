"""Repository helpers used by collection-oriented fulfillment handlers."""

class OrderRepository:
    def list_open_for_workspace(self, workspace_id):
        return db.query(
            "select * from orders where workspace_id = %s and status = 'open' order by created_at desc",
            [workspace_id],
        )

    def list_page_for_workspace(self, workspace_id, page, page_size):
        return db.paginate(
            "select * from orders where workspace_id = %s order by created_at desc",
            [workspace_id],
            page=page,
            page_size=page_size,
        )

    def list_recent_incidents_with_reporters(self, workspace_id, limit=50):
        return db.query(
            """
            select i.*, u.display_name as reporter_name
            from incidents i
            left join users u
              on u.workspace_id = i.workspace_id
             and u.id = i.reporter_id
            where i.workspace_id = %s
            order by i.created_at desc
            limit %s
            """,
            [workspace_id, limit],
        )

    def list_active_fleet(self, workspace_id):
        return db.query(
            "select * from robots where workspace_id = %s and retired_at is null order by id",
            [workspace_id],
        )


class UserRepository:
    def get_by_id(self, workspace_id, user_id):
        return db.one_or_none(
            "select * from users where workspace_id = %s and id = %s",
            [workspace_id, user_id],
        )

    def get_by_ids(self, workspace_id, user_ids):
        """Approved bulk helper. Missing users are omitted from the returned id->user map."""
        if not user_ids:
            return {}
        rows = db.query(
            "select * from users where workspace_id = %s and id = any(%s)",
            [workspace_id, list(user_ids)],
        )
        return {row.id: row for row in rows}


class ShipmentRepository:
    def get_status_for_order(self, workspace_id, order_id):
        return db.one_or_none(
            "select * from shipment_status where workspace_id = %s and order_id = %s",
            [workspace_id, order_id],
        )

    def get_statuses_for_order_ids(self, workspace_id, order_ids):
        """Approved bulk helper. Missing status rows remain missing rather than synthesized."""
        if not order_ids:
            return {}
        rows = db.query(
            "select * from shipment_status where workspace_id = %s and order_id = any(%s)",
            [workspace_id, list(order_ids)],
        )
        return {row.order_id: row for row in rows}

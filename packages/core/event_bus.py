"""Redis Streams event bus for publishing and consuming domain events."""

import json
from datetime import datetime
from typing import Any

import redis.asyncio as redis

from packages.core.events import DomainEvent


def _extract_field_str(fields: Any, key: str) -> str:
    """Safely extract string field value from redis hash mapping."""
    if not isinstance(fields, dict):
        return ""
    val = fields.get(key.encode("utf-8"))
    if val is None:
        val = fields.get(key)
    if val is None:
        return ""
    return val.decode("utf-8") if isinstance(val, bytes) else str(val)


class EventBus:
    """Redis Streams publisher and subscriber for multi-tenant domain events."""

    def __init__(self, redis_client: redis.Redis) -> None:  # type: ignore[type-arg]
        """Initialize EventBus with connected async Redis client.

        Args:
            redis_client: Async redis client connection.
        """
        self.redis = redis_client

    def _stream_key(self, tenant_id: str) -> str:
        """Derive tenant-scoped Redis Stream key.

        Args:
            tenant_id: Tenant UUID string.

        Returns:
            str: Redis stream key.
        """
        return f"events:{tenant_id}"

    async def publish(self, event: DomainEvent) -> str:
        """Publish a domain event to the tenant's Redis stream.

        Args:
            event: DomainEvent instance.

        Returns:
            str: Redis Stream message ID.
        """
        key = self._stream_key(event.tenant_id)
        data = {
            "id": str(event.id),
            "tenant_id": event.tenant_id,
            "venture_id": event.venture_id,
            "type": event.type,
            "version": str(event.version),
            "payload": json.dumps(event.payload),
            "emitted_by": event.emitted_by,
            "occurred_at": event.occurred_at.isoformat(),
        }
        if event.causation_id:
            data["causation_id"] = str(event.causation_id)
        if event.correlation_id:
            data["correlation_id"] = str(event.correlation_id)

        stream_id = await self.redis.xadd(key, data)
        return str(stream_id)

    async def create_consumer_group(
        self,
        tenant_id: str,
        group_name: str,
    ) -> None:
        """Create consumer group on tenant stream if it does not already exist.

        Args:
            tenant_id: Tenant UUID string.
            group_name: Name of consumer group (e.g. 'financial_agent').
        """
        key = self._stream_key(tenant_id)
        try:
            await self.redis.xgroup_create(key, group_name, id="0", mkstream=True)
        except redis.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def consume(
        self,
        tenant_id: str,
        group_name: str,
        consumer_name: str,
        count: int = 10,
        stream_id: str = ">",
    ) -> list[tuple[str, DomainEvent]]:
        """Read messages for this consumer group from tenant stream.

        Args:
            tenant_id: Tenant UUID string.
            group_name: Consumer group name.
            consumer_name: Unique consumer instance name.
            count: Maximum events to read.
            stream_id: Stream position ('status >' for new, '0' for pending unacked).

        Returns:
            list[tuple[str, DomainEvent]]: List of (stream_message_id, DomainEvent).
        """
        key = self._stream_key(tenant_id)
        raw_items: list[Any] = await self.redis.xreadgroup(
            group_name,
            consumer_name,
            {key: stream_id},
            count=count,
        )
        events: list[tuple[str, DomainEvent]] = []
        if not raw_items:
            return events

        for _, messages in raw_items:
            for msg_id, fields in messages:
                raw_payload = _extract_field_str(fields, "payload")
                payload_dict = json.loads(raw_payload) if raw_payload else {}
                event_kwargs: dict[str, Any] = {
                    "id": _extract_field_str(fields, "id"),
                    "tenant_id": _extract_field_str(fields, "tenant_id"),
                    "venture_id": _extract_field_str(fields, "venture_id"),
                    "type": _extract_field_str(fields, "type"),
                    "version": int(_extract_field_str(fields, "version") or "1"),
                    "payload": payload_dict,
                    "emitted_by": _extract_field_str(fields, "emitted_by"),
                }
                occurred_raw = _extract_field_str(fields, "occurred_at")
                if occurred_raw:
                    event_kwargs["occurred_at"] = datetime.fromisoformat(occurred_raw)
                causation_raw = _extract_field_str(fields, "causation_id")
                if causation_raw:
                    event_kwargs["causation_id"] = causation_raw
                correlation_raw = _extract_field_str(fields, "correlation_id")
                if correlation_raw:
                    event_kwargs["correlation_id"] = correlation_raw

                event = DomainEvent(**event_kwargs)
                formatted_msg_id = msg_id.decode("utf-8") if isinstance(msg_id, bytes) else str(msg_id)
                events.append((formatted_msg_id, event))
        return events

    async def ack(self, tenant_id: str, group_name: str, message_id: str) -> None:
        """Acknowledge successfully processed message.

        Args:
            tenant_id: Tenant UUID string.
            group_name: Consumer group name.
            message_id: Redis stream message ID.
        """
        key = self._stream_key(tenant_id)
        await self.redis.xack(key, group_name, message_id)  # type: ignore[no-untyped-call]

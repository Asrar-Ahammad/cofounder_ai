"""Redis Streams event bus for publishing and consuming domain events."""

import json
from typing import Any

import redis.asyncio as redis

from packages.core.events import DomainEvent


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
    ) -> list[tuple[str, DomainEvent]]:
        """Read pending messages for this consumer group from tenant stream.

        Args:
            tenant_id: Tenant UUID string.
            group_name: Consumer group name.
            consumer_name: Unique consumer instance name.
            count: Maximum events to read.

        Returns:
            list[tuple[str, DomainEvent]]: List of (stream_message_id, DomainEvent).
        """
        key = self._stream_key(tenant_id)
        raw_items: list[Any] = await self.redis.xreadgroup(
            group_name,
            consumer_name,
            {key: ">"},
            count=count,
        )
        events: list[tuple[str, DomainEvent]] = []
        if not raw_items:
            return events

        for _, messages in raw_items:
            for msg_id, fields in messages:
                payload_dict = json.loads(fields.get(b"payload", b"{}").decode("utf-8"))
                event = DomainEvent(
                    id=fields[b"id"].decode("utf-8"),
                    tenant_id=fields[b"tenant_id"].decode("utf-8"),
                    venture_id=fields[b"venture_id"].decode("utf-8"),
                    type=fields[b"type"].decode("utf-8"),
                    version=int(fields.get(b"version", b"1").decode("utf-8")),
                    payload=payload_dict,
                    emitted_by=fields[b"emitted_by"].decode("utf-8"),
                )
                events.append((msg_id.decode("utf-8") if isinstance(msg_id, bytes) else str(msg_id), event))
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

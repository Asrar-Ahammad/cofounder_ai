"""Cal.com calendar scheduling adapter conforming to CalendarScheduler port."""

from typing import Any

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import CalendarScheduler
from packages.security.egress import validate_egress_url


class CalComCalendarAdapter(CalendarScheduler):
    """Adapter interacting with Cal.com API for appointment booking."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.cal.com/v1",
    ) -> None:
        """Initialize Cal.com calendar adapter with credentials.

        Args:
            api_key: Cal.com API secret key.
            base_url: Base endpoint for Cal.com REST API.
        """
        self.api_key = api_key
        self.base_url = base_url

    async def list_available_slots(
        self,
        *,
        tenant_id: str,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        """List available meeting booking slots.

        Args:
            tenant_id: Tenant UUID string.
            start_date: Beginning date in ISO format.
            end_date: Ending date in ISO format.

        Returns:
            list[dict[str, Any]]: List of available time slots.
        """
        if not self.api_key or self.api_key.startswith("calcom-placeholder"):
            return [
                {"start_time": f"{start_date}T10:00:00Z", "end_time": f"{start_date}T10:30:00Z"},
                {"start_time": f"{start_date}T14:00:00Z", "end_time": f"{start_date}T14:30:00Z"},
            ]

        validate_egress_url(self.base_url)
        params = {"apiKey": self.api_key, "dateFrom": start_date, "dateTo": end_date}
        headers = {"X-Tenant-Id": tenant_id}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(f"{self.base_url}/slots", params=params, headers=headers)
                res.raise_for_status()
                data = res.json()
                return list(data.get("slots", []))
        except Exception as exc:
            raise ExternalServiceError(f"Cal.com slot retrieval error: {exc}") from exc

    async def create_booking(
        self,
        *,
        tenant_id: str,
        attendee_email: str,
        attendee_name: str,
        start_time: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Create a scheduled calendar booking.

        Args:
            tenant_id: Tenant UUID string.
            attendee_email: Prospect or customer email.
            attendee_name: Attendee full name.
            start_time: ISO start timestamp.
            idempotency_key: Unique idempotency key.

        Returns:
            dict[str, Any]: Confirmed booking details.
        """
        if not self.api_key or self.api_key.startswith("calcom-placeholder"):
            return {
                "booking_id": f"cal-sim-{idempotency_key[:8]}",
                "meeting_url": f"https://cal.com/meet/sim-{idempotency_key[:8]}",
                "start_time": start_time,
                "status": "confirmed",
            }

        validate_egress_url(self.base_url)
        headers = {"X-Tenant-Id": tenant_id, "X-Idempotency-Key": idempotency_key}
        payload = {
            "apiKey": self.api_key,
            "email": attendee_email,
            "name": attendee_name,
            "start": start_time,
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(f"{self.base_url}/bookings", json=payload, headers=headers)
                res.raise_for_status()
                return dict(res.json().get("booking", {}))
        except Exception as exc:
            raise ExternalServiceError(f"Cal.com booking creation error: {exc}") from exc

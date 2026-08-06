import os
import requests

from .constants import SUPERVISOR_BASE_URL


class HomeAssistantClient:
    def __init__(self) -> None:
        self._token = os.environ.get("SUPERVISOR_TOKEN")

    @property
    def available(self) -> bool:
        return bool(self._token)

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

    def send_event(self, event_type: str, payload: dict) -> bool:
        if not self._token:
            return False

        try:
            response = requests.post(
                f"{SUPERVISOR_BASE_URL}/events/{event_type}",
                headers=self._headers(),
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            print(f"✓ Sent {event_type}: {payload}", flush=True)
            return True
        except requests.RequestException as error:
            print(f"✗ Failed to send {event_type}: {error}", flush=True)
            return False

    def create_notification(
        self,
        notification_id: str,
        title: str,
        message: str,
    ) -> bool:
        if not self._token:
            return False

        try:
            response = requests.post(
                f"{SUPERVISOR_BASE_URL}/services/persistent_notification/create",
                headers=self._headers(),
                json={
                    "notification_id": notification_id,
                    "title": title,
                    "message": message,
                },
                timeout=10,
            )
            response.raise_for_status()
            return True
        except requests.RequestException as error:
            print(f"✗ Failed to create notification: {error}", flush=True)
            return False

    def dismiss_notification(self, notification_id: str) -> bool:
        if not self._token:
            return False

        try:
            response = requests.post(
                f"{SUPERVISOR_BASE_URL}/services/persistent_notification/dismiss",
                headers=self._headers(),
                json={"notification_id": notification_id},
                timeout=10,
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

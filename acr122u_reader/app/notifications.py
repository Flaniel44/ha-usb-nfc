from .events import HomeAssistantClient
from .errors import HealthError


class NotificationManager:
    def __init__(self, client: HomeAssistantClient) -> None:
        self._client = client

    def show_error(self, notification_id: str, error: HealthError) -> None:
        self._client.create_notification(
            notification_id,
            f"{error.code}: {error.title}",
            error.message,
        )

    def dismiss(self, notification_id: str) -> None:
        self._client.dismiss_notification(notification_id)

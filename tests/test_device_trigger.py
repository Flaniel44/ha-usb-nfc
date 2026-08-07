"""Tests for the USB NFC reader device triggers."""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE

from custom_components.acr122u.const import (
    DOMAIN,
    EVENT_CARD_PRESENT,
    EVENT_CARD_REMOVED,
    EVENT_DEVICE_ACTIVITY,
)
from custom_components.acr122u.device_trigger import (
    CONF_TAG_ID,
    TRIGGER_CARD_REMOVED,
    TRIGGER_CARD_SCANNED,
    TRIGGER_SCHEMA,
    async_attach_trigger,
    async_get_triggers,
)


class DeviceTriggerTests(IsolatedAsyncioTestCase):
    """Verify discovery and event matching configuration."""

    def test_raw_event_names_remain_stable(self) -> None:
        self.assertEqual(EVENT_CARD_PRESENT, "acr122u_card_present")
        self.assertEqual(EVENT_CARD_REMOVED, "acr122u_card_removed")

    async def test_discovers_scanned_and_removed_triggers(self) -> None:
        self.assertEqual(
            await async_get_triggers(None, "reader-device-id"),
            [
                {
                    CONF_PLATFORM: "device",
                    CONF_DOMAIN: DOMAIN,
                    CONF_DEVICE_ID: "reader-device-id",
                    CONF_TYPE: TRIGGER_CARD_SCANNED,
                },
                {
                    CONF_PLATFORM: "device",
                    CONF_DOMAIN: DOMAIN,
                    CONF_DEVICE_ID: "reader-device-id",
                    CONF_TYPE: TRIGGER_CARD_REMOVED,
                },
            ],
        )

    async def test_card_specific_trigger_matches_uppercase_uid(self) -> None:
        config = TRIGGER_SCHEMA(
            {
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: "reader-device-id",
                CONF_TYPE: TRIGGER_CARD_REMOVED,
                CONF_TAG_ID: "c8149fef",
            }
        )
        attach = AsyncMock(return_value=lambda: None)

        with (
            patch.object(
                event_trigger,
                "TRIGGER_SCHEMA",
                side_effect=lambda value: value,
            ),
            patch.object(event_trigger, "async_attach_trigger", attach),
        ):
            remove = await async_attach_trigger(None, config, AsyncMock(), {})

        self.assertIsNotNone(remove)
        event_config = attach.await_args.args[1]
        self.assertEqual(event_config[event_trigger.CONF_EVENT_TYPE], EVENT_DEVICE_ACTIVITY)
        self.assertEqual(
            event_config[event_trigger.CONF_EVENT_DATA],
            {
                CONF_DEVICE_ID: "reader-device-id",
                CONF_TYPE: TRIGGER_CARD_REMOVED,
                "uid": "C8149FEF",
            },
        )
        self.assertEqual(attach.await_args.kwargs, {"platform_type": "device"})

    async def test_any_card_trigger_does_not_filter_uid(self) -> None:
        config = TRIGGER_SCHEMA(
            {
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: "reader-device-id",
                CONF_TYPE: TRIGGER_CARD_SCANNED,
            }
        )
        attach = AsyncMock(return_value=lambda: None)

        with (
            patch.object(
                event_trigger,
                "TRIGGER_SCHEMA",
                side_effect=lambda value: value,
            ),
            patch.object(event_trigger, "async_attach_trigger", attach),
        ):
            await async_attach_trigger(None, config, AsyncMock(), {})

        self.assertEqual(
            attach.await_args.args[1][event_trigger.CONF_EVENT_DATA],
            {
                CONF_DEVICE_ID: "reader-device-id",
                CONF_TYPE: TRIGGER_CARD_SCANNED,
            },
        )

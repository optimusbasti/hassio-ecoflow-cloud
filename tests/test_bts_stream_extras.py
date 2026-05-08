"""Smoke tests for BTS-specific StreamPvWattsSensorEntity.

Catches regressions when upstream-merging tolwi/hassio-ecoflow-cloud changes
the WattsSensorEntity base class signature, attribute names, or _updated()
contract. These tests do NOT exercise full Home Assistant integration —
they verify the BTS extension's own logic in isolation.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

# The import chain pulls in homeassistant + aiohttp + paho-mqtt etc. CI
# installs those via requirements.txt; locally without them, skip cleanly.
try:
    from custom_components.ecoflow_cloud.devices.public.bts_stream_extras import (
        StreamPvWattsSensorEntity,
    )
except ImportError as exc:
    pytest.skip(
        f"HA-deps missing for local pytest (install -r requirements.txt): {exc}",
        allow_module_level=True,
    )


def _make_entity(amp_key: str = "plugInInfoPv2Amp") -> StreamPvWattsSensorEntity:
    """Build a StreamPvWattsSensorEntity with mocked client+device."""
    client = MagicMock()
    device = MagicMock()
    return StreamPvWattsSensorEntity(client, device, amp_key, "PV2 Power")


def test_amp_key_validation_rejects_non_amp_suffix() -> None:
    """Constructor must reject keys not ending in 'Amp'."""
    with pytest.raises(ValueError, match="ending in 'Amp'"):
        _make_entity(amp_key="plugInInfoPv2Vol")


def test_vol_key_auto_derived_from_amp_key() -> None:
    """vol_key is auto-derived from amp_key by suffix swap (Amp -> Vol)."""
    entity = _make_entity(amp_key="plugInInfoPv3Amp")
    assert entity._vol_key == "plugInInfoPv3Vol"


def test_synthetic_mqtt_key_uses_btsPvWatts_prefix() -> None:
    """Synthetic mqtt_key prevents unique_id collision with sibling AmpSensorEntity."""
    entity = _make_entity(amp_key="plugInInfoPv2Amp")
    assert entity.mqtt_key.startswith("btsPvWatts_plugInInfoPv2Amp")


def test_updated_with_missing_amp_falls_through_to_super() -> None:
    """Missing amp/vol → graceful fallback to super()._updated() (no crash, no compute)."""
    entity = _make_entity()
    with patch(
        "custom_components.ecoflow_cloud.sensor.WattsSensorEntity._updated"
    ) as super_upd:
        entity._updated({"plugInInfoPv2Vol": 36.5})  # amp absent
        super_upd.assert_called_once()


def test_updated_with_amp_and_vol_injects_computed_watts() -> None:
    """amp × vol = watts → injected under synthetic mqtt_key for upstream pipeline."""
    entity = _make_entity(amp_key="plugInInfoPv2Amp")
    with patch(
        "custom_components.ecoflow_cloud.sensor.WattsSensorEntity._updated"
    ) as super_upd:
        entity._updated({"plugInInfoPv2Amp": 5.2, "plugInInfoPv2Vol": 36.5})
        super_upd.assert_called_once()
        injected_data = super_upd.call_args[0][0]
        assert injected_data[entity.mqtt_key] == pytest.approx(5.2 * 36.5)

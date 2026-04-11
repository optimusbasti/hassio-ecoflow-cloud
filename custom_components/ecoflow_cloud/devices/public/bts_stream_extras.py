"""BTS extension: per-PV computed watts for Stream Ultra family.

Stream Ultra firmware does not emit the `powGetPv` / `powGetPv2..4` keys
that upstream `WattsSensorEntity` expects. The real per-PV data lives in
`plugInInfoPv{,2,3,4}Amp` and `plugInInfoPv{,2,3,4}Vol`. This helper
multiplies amp and vol from the same payload to produce per-PV watts.

References:
  - https://github.com/tolwi/hassio-ecoflow-cloud/issues/584
  - https://github.com/tolwi/hassio-ecoflow-cloud/issues/582
"""
from typing import Any

from custom_components.ecoflow_cloud.sensor import WattsSensorEntity


class StreamPvWattsSensorEntity(WattsSensorEntity):
    """Per-PV watts sensor that computes amp x vol from raw payload keys."""

    def __init__(
        self,
        client,
        device,
        amp_key: str,
        vol_key: str,
        title,
        enabled: bool = True,
        auto_enable: bool = False,
    ):
        # Use amp_key as the primary mqtt_key so the base class subscribes
        # correctly and unique_id stays distinct from the upstream watts entity.
        super().__init__(client, device, amp_key, title, enabled, auto_enable)
        self._amp_key = amp_key
        self._vol_key = vol_key

    def _updated(self, data: dict[str, Any]) -> None:  # type: ignore[override]
        amp = data.get(self._amp_key)
        vol = data.get(self._vol_key)
        if amp is None or vol is None:
            return
        try:
            watts = float(amp) * float(vol)
        except (TypeError, ValueError):
            return
        self._attr_available = True
        if self._auto_enable:
            self._attr_entity_registry_enabled_default = True
            self._attr_entity_registry_visible_default = True
        if self._update_value(round(watts, 2)):
            self.schedule_update_ha_state()

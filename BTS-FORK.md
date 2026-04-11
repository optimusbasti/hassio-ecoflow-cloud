# BTS Fork — Stream Ultra per-PV Extension

Privater Fork von [tolwi/hassio-ecoflow-cloud](https://github.com/tolwi/hassio-ecoflow-cloud) v1.4.0 mit **Per-PV Sensor-Erweiterung** für die EcoFlow Stream Ultra Familie.

## Was ist anders zum Upstream

Stream Ultra Firmware emittet die Keys `powGetPv` / `powGetPv2..4` **nicht** mehr — die echten Per-PV Daten kommen als `plugInInfoPv{,2,3,4}Amp` und `plugInInfoPv{,2,3,4}Vol`. Upstream Issue: [#584](https://github.com/tolwi/hassio-ecoflow-cloud/issues/584).

Dieser Fork fügt **12 neue Sensor-Entities pro Stream Ultra** hinzu:

| Kategorie | Anzahl | Sensoren |
|---|---|---|
| Per-PV Power (W) | 4 | Power PV 1/2/3/4 (computed: Amp × Vol) |
| Per-PV Voltage (V) | 4 | Power PV1/2/3/4 Volts |
| Per-PV Current (A) | 4 | Power PV1/2/3/4 In Amps |

Die 4 Legacy `powGetPv*` Watts-Sensoren bleiben als `disabled-by-default` für Geräte mit alter Firmware drin (auto-enable wenn Werte kommen).

## Geänderte Dateien

- `custom_components/ecoflow_cloud/devices/public/bts_stream_extras.py` (NEU): `StreamPvWattsSensorEntity` Helper-Klasse
- `custom_components/ecoflow_cloud/devices/public/stream_ac.py`: Imports + 12 neue Entity-Lines + Legacy-Block
- `custom_components/ecoflow_cloud/devices/const.py`: 4 neue Konstanten (PV3/PV4 Amps + Volts)
- `custom_components/ecoflow_cloud/manifest.json`: version `1.4.0` → `1.4.1`, name `EcoFlow-Cloud (BTS Fork)`

## Installation via HACS

1. HACS → ⋮ → Custom repositories
2. Repository URL: `https://github.com/optimusbasti/hassio-ecoflow-cloud`
3. Type: Integration
4. ADD
5. Im HACS-Hauptscreen "EcoFlow-Cloud (BTS Fork)" suchen → DOWNLOAD → Version `1.4.1`
6. Home Assistant restart

Nach dem Restart erscheinen die 12 neuen Entities pro Stream Ultra Device automatisch (auto-enable greift beim ersten Payload-Sighting).

## Sync mit Upstream

Wenn tolwi/hassio-ecoflow-cloud ein neues Release published, manuell diff-mergen und neue Version mit `+bts.<N>` taggen.

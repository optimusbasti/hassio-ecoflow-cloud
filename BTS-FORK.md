# BTS Fork — Stream Ultra & Stream MicroInverter Per-PV Extension

Privater BTS-Fork von [tolwi/hassio-ecoflow-cloud](https://github.com/tolwi/hassio-ecoflow-cloud) v1.4.0 mit **Per-PV Sensor-Erweiterung** für die neue EcoFlow Stream-Familie (Stream Ultra, Stream Ultra X, Stream AC Pro, Stream MicroInverter).

## Was anders ist zum Upstream

Stream-Familie Firmware emittet die Keys `powGetPv` / `powGetPv2..4` **nicht** mehr. Die echten Per-PV Daten kommen als `plugInInfoPv{,2,3,4}Amp` und `plugInInfoPv{,2,3,4}Vol`. Upstream Issue: [#584](https://github.com/tolwi/hassio-ecoflow-cloud/issues/584).

## Neue Entities

### Stream Ultra / Stream Ultra X / Stream AC Pro (4 MPPTs)

| Kategorie | Anzahl |
|---|---|
| Per-PV Power (W, computed) | 4 |
| Per-PV Voltage (V) | 4 |
| Per-PV Current (A) | 4 |
| **Total neue Entities pro Device** | **12** |

### Stream MicroInverter (2 MPPTs)

| Kategorie | Anzahl |
|---|---|
| Per-PV Power (W, computed) | 2 |
| Per-PV Voltage (V) | 2 (war disabled) |
| Per-PV Current (A) | 2 (war disabled) |
| **Total neue/aktivierte Entities pro Device** | **6** |

## Geänderte Dateien

| Datei | Änderung |
|---|---|
| `devices/public/bts_stream_extras.py` (NEU) | `StreamPvWattsSensorEntity` Helper. Synthetic mqtt_key (vermeidet Unique-ID Collision mit `AmpSensorEntity` auf demselben `plugInInfoPv*Amp` Key). Auto-derive `vol_key` aus `amp_key`. Delegate an upstream `_updated()` für sauberes Auto-Enable + Attribute-Mapping. |
| `devices/public/stream_ac.py` | Ersetzt 4 broken `WattsSensorEntity("powGetPv*")` Lines durch 4 `StreamPvWattsSensorEntity` + 4 `VoltSensorEntity` + 4 `AmpSensorEntity`. Legacy-Lines komplett entfernt. |
| `devices/public/stream_microinverter.py` | Ersetzt 2 broken `WattsSensorEntity("powGetPv*")` Lines durch 2 `StreamPvWattsSensorEntity`. Aktiviert die bereits existierenden 4 Volt/Amp Sensoren (waren `enabled=False`). |
| `devices/const.py` | 4 neue Konstanten für PV3/PV4 Amps + Volts (für Stream Ultra). |
| `manifest.json` | version `1.4.0` → `1.4.2`, name `EcoFlow-Cloud (BTS Fork)`. |

## Was unangetastet bleibt

- **PowerStream (legacy)**: separate Datei `internal/powerstream.py`, andere Code-Pfade. Wird mit allen v1.4.0 Verbesserungen aus tolwi unterstützt. Kein Patch nötig.
- Alle anderen Devices (Delta, River, Glacier, Wave, Smart Meter, Smart Plug, etc.).

## v1.4.2 Verbesserungen ggü v1.4.1

1. **Synthetic mqtt_key in StreamPvWattsSensorEntity** löst Unique-ID Collision mit AmpSensorEntity → die 4 Amp-Sensoren erscheinen jetzt zuverlässig.
2. **Auto-derive vol_key** aus amp_key (`plugInInfoPv2Amp` → `plugInInfoPv2Vol`) → halbiert API-Surface, weniger Tippfehler.
3. **Delegate an `super()._updated()`** statt manueller Reimplementierung → sauberes Auto-Enable, Attribute-Mapping, Recorder, `with_energy()`.
4. **Legacy `powGetPv*` Lines entfernt** in stream_ac.py → keine `_2` Suffixe mehr für die neuen Watts-Entities (auf frischer Installation).
5. **Stream MicroInverter** ebenfalls gepatcht.

## Installation via HACS

```
1. HACS → ⋮ → Custom repositories
2. Repository URL: https://github.com/optimusbasti/hassio-ecoflow-cloud
3. Type: Integration
4. ADD
5. Im HACS-Hauptscreen "EcoFlow-Cloud (BTS Fork)" suchen → DOWNLOAD → v1.4.2
6. Home Assistant restart
```

### Cleanup nach Upgrade von v1.4.1 → v1.4.2 (optional)

Wenn du vorher v1.4.1 installiert hattest, gibt es im Entity Registry verwaiste Einträge mit `_2` Suffix (`power_pv_1_2`, `power_pv_2_2`, etc.) und disabled Legacy-Einträge (`power_pv_1`, `power_pv_2`, etc.). Cleanup:

1. Settings → Devices & Services → Stream Ultra Device → Entities
2. Filter "PV"
3. Disabled Einträge `power_pv_1`, `power_pv_2`, `power_pv_3`, `power_pv_4` → 3-Punkt-Menü → **Delete**
4. Restart Home Assistant
5. Beim nächsten Boot werden die neuen Entities mit sauberen Namen `power_pv_1` etc. erstellt (kein `_2` Suffix mehr)

## Sync mit Upstream

Bei neuen tolwi/hassio-ecoflow-cloud Releases manuell diff-mergen, Version mit `+bts.<N>` oder hochgezähltem Patch-Level taggen, neuen Release pushen.

## Lizenz

Apache-2.0 (gleich wie Upstream tolwi).

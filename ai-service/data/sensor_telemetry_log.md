# Sensor & Telemetry Log (Simulated output from IoT Platform)
Date: 15 Jun 2026

## Soil Moisture Readings (Last 72 Hours)
*Target moisture for pineapple: 25-35%. Target for oil palm: 30-40%.*

| Farm | Block | Zone | Average Moisture % | Trend | Status |
|---|---|---|---|---|---|
| Farm 1 | C-3 | NW Quadrant | 44.5% | Oscillating high | **CRITICAL: Waterlogged** |
| Farm 1 | C-3 | SE Quadrant | 31.0% | Stable | Normal |
| Farm 1 | A-1 | Center | 28.5% | Stable | Normal |
| Farm 2 | W-2 | Center | 35.2% | Stable | Normal |
| Farm 3 | 12 | Shore Edge | 29.0% | Stable | Normal |

*Note: Block W-2 soil moisture is normal. The stress shown in NDVI is NOT irrigation-related.*

## Irrigation Telemetry (Hardware Status)

| Farm | Block | Zone/Device | Expected State | Actual State | Flow Rate (LPM) | Pressure (PSI) | Status Alert |
|---|---|---|---|---|---|---|---|
| Farm 1 | C-3 | Valve 3A (Drip Line 4) | CLOSED | **OPEN** | 8.2 | 22 | **CRITICAL FAULT: Valve stuck open** |
| Farm 1 | C-3 | Valve 3B (Drip Line 4) | CLOSED | CLOSED | 0.0 | 0 | Normal |
| Farm 2 | W-2 | Sprinkler Pump 4 | ACTIVE | ACTIVE | 45.0 | **12** | **FAULT: Pressure drop (Expected 45 PSI)** |
| Farm 3 | 12 | Drip Line 1 | CLOSED | CLOSED | 0.0 | 0 | Normal |

*Analysis: The system shows Line 4 in Block C-3 was set to 0 duration by the operator, but Valve 3A failed mechanically and is stuck open, constantly flooding the NW quadrant. This explains the waterlogging despite agronomist intervention.*

## Soil Electrical Conductivity (EC) / Salinity

| Farm | Block | Zone | EC Reading (dS/m) | Threshold | Status |
|---|---|---|---|---|---|
| Farm 1 | C-3 | NW Quadrant | 1.1 | < 1.5 | Normal |
| Farm 2 | W-2 | Center | 0.8 | < 1.5 | Normal |
| Farm 3 | 12 | Shore Edge | **4.2** | < 1.5 | **CRITICAL FAULT: High Salinity** |
| Farm 3 | 12 | Inland (300m) | 1.4 | < 1.5 | Normal |

*Analysis: Farm 3 Block 12 is experiencing severe salinity intrusion at the shore edge.*

## Localized Weather Station Data (Last 7 Days)

### Farm 1 (Cameron Highlands) - Rainfall Anomaly
- 3 Jun: 42 mm
- 4 Jun: 28 mm
- 5 Jun: 11 mm
- **Total:** 81 mm in 3 days (Unseasonal heavy rain). Combined with the stuck valve, this overwhelmed the drainage in Block C-3.

### Farm 3 (Johor Coast) - Wind Anomaly
- 13 Jun: Wind Speed 35 km/h from South-West (Sea-facing).
- 14 Jun: Wind Speed 32 km/h from South-West.
- **Impact:** High winds drove salt spray inland, explaining the high EC readings and Red Edge (NDRE) stress in Block 12.

# Field Operations Log (Simulated output from ERP/PostgreSQL)
Date: 15 Jun 2026

## Agronomist Visit Log (Last 30 Days)

| Date | Farm | Block | Agronomist | Findings | Action Taken | Follow-up Due |
|---|---|---|---|---|---|---|
| 5 Jun 2026 | Farm 1 | C-3 | Rajan Kumar | Soil waterlogged in NW. Plants showing yellowing at base. 2 plants pulled showed black root tips (Phytophthora). | Irrigation halted on Line 4. Drainage inspection requested. | 12 Jun 2026 (**MISSED**) |
| 8 Jun 2026 | Farm 2 | W-2 | Siti Nurhaliza | Reports of leaf damage. Initial inspection inconclusive. | Requested drone survey (MX-219) for block-level damage assessment. | 15 Jun 2026 |
| 10 Jun 2026 | Farm 3 | 12 | Wei Chen | Plants showing red edge. Salt spray suspected after high winds. | Leaf tissue samples sent to lab. | 20 Jun 2026 |

*Note: The follow-up visit for Block C-3 on 12 Jun was missed due to agronomist sick leave. Deterioration continued unchecked for 10 days.*

## Irrigation Schedule & Adjustments

| Farm | Block | System | Daily Duration (min) | Last Adjusted | Adjusted By | Trigger |
|---|---|---|---|---|---|---|
| Farm 1 | C-3 | Drip (Line 4) | 0 min | 5 Jun 2026 | Rajan Kumar | Agronomist request |
| Farm 1 | A-1 | Drip (Line 1) | 45 min | 1 May 2026 | Auto | Seasonal schedule |
| Farm 2 | W-2 | Sprinkler | 30 min | 1 Jun 2026 | Auto | Soil moisture threshold |

*Note: Operator set C-3 Line 4 duration to 0 on software, but actual flow may vary based on hardware status (see telemetry).*

## Pesticide & Herbicide Log

| Farm | Block | Chemical Applied | Date Applied | Target | Efficacy Rating |
|---|---|---|---|---|---|
| Farm 1 | C-4 | Fungicide (Mancozeb) | 1 Jun 2026 | Fungal prevention | Good |
| Farm 2 | W-2 | None | N/A | N/A | N/A |
| Farm 3 | 8 | Herbicide (Glyphosate) | 3 Jun 2026 | Weed control | Good |

*Note: Farm 2 Block W-2 has had NO pesticide applied since Feb 2026, leaving it vulnerable to bagworm outbreaks.*

## Drone Mission Log (Orthomosaic & Mapping)

| Mission ID | Farm | Blocks Covered | Date | Status | Findings Processed |
|---|---|---|---|---|---|
| MX-218 | Farm 1 | 38 blocks (Except Blk 5) | 6 Jun 2026 | ✅ Complete | Yes |
| MX-219 | Farm 2 | 26 blocks | 6 Jun 2026 | ✅ Complete | Yes |
| MX-220 | Farm 3 | 47 blocks | 16 Jun 2026 | ⏳ Pending | No |

*Note: Block 5 (Farm 1) was missed in MX-218 due to Drone #2 battery fault. It has been 12 days without aerial survey for this block.*

## Equipment Maintenance Tickets

| Ticket ID | Farm | Equipment | Issue Reported | Date Open | Status |
|---|---|---|---|---|---|
| MT-901 | Farm 1 | Drone #2 | Battery cell failure during MX-218. | 6 Jun 2026 | Open - Parts ordered |
| MT-904 | Farm 2 | Sprinkler Line 4 (W-2) | Pressure drop reported (12 PSI). | 15 Jun 2026 | Open - Pending inspection |
| MT-905 | Farm 1 | Drainage Channel B (C-3) | Debris clearing requested by Rajan. | 5 Jun 2026 | Closed - Cleared |

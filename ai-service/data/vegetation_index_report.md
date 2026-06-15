# Vegetation Index Report (Simulated output from Vegetation Index Service)
Date: 6 Jun 2026
Mission ID: MX-218 (Farm 1), MX-219 (Farm 2), MX-212 (Farm 3 - older data)

## Farm 1, Block C-3 (CRISIS: Suspected Root Rot)
**Summary:** NDVI dropped significantly in the NW quadrant. Current average NDVI is 0.41 (down from 0.59). The pattern shows severe stress spreading outward from the drainage channel.

| Plant ID | Location Quadrant | NDVI Current | NDVI Previous | Delta | NDRE | Health Status |
|---|---|---|---|---|---|---|
| P-F1-C3-0001 | NW | 0.22 | 0.58 | -0.36 | 0.15 | Severe Stress |
| P-F1-C3-0002 | NW | 0.25 | 0.57 | -0.32 | 0.18 | Severe Stress |
| P-F1-C3-0003 | NW | 0.29 | 0.60 | -0.31 | 0.21 | Severe Stress |
| P-F1-C3-0004 | NW | 0.35 | 0.59 | -0.24 | 0.25 | Mild Stress |
| P-F1-C3-0005 | NW | 0.38 | 0.61 | -0.23 | 0.28 | Mild Stress |
| P-F1-C3-0010 | NE | 0.45 | 0.55 | -0.10 | 0.35 | Mild Stress |
| P-F1-C3-0011 | NE | 0.42 | 0.58 | -0.16 | 0.32 | Mild Stress |
| P-F1-C3-0020 | SW | 0.48 | 0.59 | -0.11 | 0.40 | Mild Stress |
| P-F1-C3-0050 | SE | 0.65 | 0.66 | -0.01 | 0.55 | Healthy |
| P-F1-C3-0051 | SE | 0.68 | 0.69 | -0.01 | 0.58 | Healthy |

*Note: Table truncated. 40% of plants show Severe Stress, 35% Mild Stress, 25% Healthy.*

## Farm 1, Block A-1 (HEALTHY BASELINE)
**Summary:** Healthy block. NDVI average is 0.72.

| Plant ID | Location Quadrant | NDVI Current | NDVI Previous | Delta | NDRE | Health Status |
|---|---|---|---|---|---|---|
| P-F1-A1-0001 | NW | 0.75 | 0.74 | +0.01 | 0.62 | Healthy |
| P-F1-A1-0002 | NW | 0.72 | 0.71 | +0.01 | 0.59 | Healthy |
| P-F1-A1-0003 | NE | 0.69 | 0.70 | -0.01 | 0.55 | Healthy |
| P-F1-A1-0004 | SW | 0.73 | 0.75 | -0.02 | 0.60 | Healthy |
| P-F1-A1-0005 | SE | 0.71 | 0.70 | +0.01 | 0.58 | Healthy |

*Note: 95% of plants in this block are Healthy.*

## Farm 2, Block W-2 (PEST DAMAGE: Suspected Bagworm)
**Summary:** NDVI dropped to an average of 0.38 (down from 0.61). The damage is highly localized in a geometric cluster in the center of the block, which is a classic signature of a bagworm infestation spreading radially.

| Plant ID | Location Quadrant | NDVI Current | NDVI Previous | Delta | NDRE | Health Status |
|---|---|---|---|---|---|---|
| P-F2-W2-0500 | Center | 0.18 | 0.62 | -0.44 | 0.12 | Severe Stress |
| P-F2-W2-0501 | Center | 0.20 | 0.60 | -0.40 | 0.15 | Severe Stress |
| P-F2-W2-0502 | Center | 0.22 | 0.63 | -0.41 | 0.16 | Severe Stress |
| P-F2-W2-0503 | Center | 0.25 | 0.61 | -0.36 | 0.19 | Severe Stress |
| P-F2-W2-0510 | NW Edge | 0.60 | 0.62 | -0.02 | 0.50 | Healthy |
| P-F2-W2-0511 | SE Edge | 0.61 | 0.63 | -0.02 | 0.51 | Healthy |

## Farm 3, Block 12 (COASTAL SALT STRESS)
**Summary:** NDRE (Red Edge) is an early indicator of salt stress. Average NDRE has dropped to 0.21 (down from 0.34). The stress is localized to the edge facing the shore, confirming salt spray/salinity intrusion.

| Plant ID | Location | NDRE Current | NDRE Previous | Delta | NDVI | Health Status |
|---|---|---|---|---|---|---|
| P-F3-12-0100 | Shore Edge | 0.12 | 0.35 | -0.23 | 0.35 | Severe Stress |
| P-F3-12-0101 | Shore Edge | 0.15 | 0.34 | -0.19 | 0.38 | Severe Stress |
| P-F3-12-0102 | Shore Edge | 0.18 | 0.36 | -0.18 | 0.40 | Severe Stress |
| P-F3-12-0200 | Inland (100m) | 0.28 | 0.32 | -0.04 | 0.55 | Mild Stress |
| P-F3-12-0300 | Inland (300m) | 0.38 | 0.35 | +0.03 | 0.68 | Healthy |

## Portfolio Block Summary

| Farm | Block | Status | Primary Issue |
|---|---|---|---|
| Farm 1 | C-3 | Critical | Waterlogging / Root Rot (NW quadrant) |
| Farm 1 | A-1 | Healthy | N/A |
| Farm 2 | W-2 | High Alert | Bagworm pest infestation (Center cluster) |
| Farm 3 | 12 | Medium Alert | Salt Stress (Shore edge), early ripening |
| Farm 3 | 8 | Healthy | N/A |

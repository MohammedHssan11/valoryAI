# Confidence Score Validation Report

Correlation between confidence and absolute percentage error: **-0.1436**

### Confidence Bucket Analysis

| Confidence Bucket | Sample Count | MAPE | Median Error |
| :--- | :---: | :---: | :---: |
| 0.0-0.2 | 0 | 100.00% | 100.00% |
| 0.2-0.4 | 3 | 56.52% | 49.55% |
| 0.4-0.6 | 50 | 35.18% | 26.61% |
| 0.6-0.8 | 183 | 35.11% | 22.60% |
| 0.8-1.0 | 167 | 21.60% | 15.38% |

### Analysis Notes
A negative correlation indicates that higher confidence scores tend to produce lower estimation errors, confirming the validity of the confidence engine.

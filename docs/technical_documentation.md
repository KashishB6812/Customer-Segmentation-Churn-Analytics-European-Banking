# Customer Segmentation & Churn Pattern Analytics in European Banking

## Overview

This project combines data engineering, segmentation analysis, and dashboarding to evaluate churn risk in a European retail banking portfolio. The analysis focuses on customer segments shaped by geography, age, credit profile, tenure, and balance characteristics.

## Business Problem

Banks collect large volumes of customer data but often fail to convert it into segment-level retention insights. This project addresses that gap by identifying customer groups with elevated churn risk and enabling managerial action through targeted interventions.

## Dataset

The synthetic dataset contains banking customer attributes and a churn indicator (`Exited`). It is modeled to resemble a European customer base with cross-country variation in churn behavior.

## Analytical Methodology

1. Data ingestion and validation
2. Feature engineering and segmentation
3. Churn rate estimation by segment
4. Comparison of retained vs exited profiles
5. High-value customer analysis
6. Dashboarding and stakeholder communication

## Key Segmentation Dimensions

- Geography: France, Spain, Germany
- Age group: `<30`, `30-45`, `46-60`, `60+`
- Credit score band: `Low`, `Medium`, `High`
- Tenure group: `New`, `Mid-term`, `Long-term`
- Balance segment: `Zero-balance`, `Low-balance`, `High-balance`

## Expected Insights

- Churn is usually higher among newly onboarded or inactive customers.
- Inactive members exhibit a meaningful increase in churn likelihood.
- Customer balance, age, and residence region influence churn probability.
- High-balance customers are economically important and require retention monitoring.

## Strategic Recommendations

- Prioritize retention campaigns for inactive, short-tenure, and higher-risk geographical segments.
- Build targeted onboarding journeys to reduce early churn.
- Tailor premium customer management for high-balance accounts.
- Monitor changes in churn across segments with a live dashboard.

## Implementation Notes

The project includes:

- Synthetic dataset generation
- Reusable analytical functions
- Streamlit-based dashboard
- Documentation for technical and executive audiences

## Conclusion

This project demonstrates a structured and actionable framework for identifying churn-prone segments in European banking. It supports better retention planning and more efficient allocation of marketing and customer success resources.

# Customer Segmentation & Churn Pattern Analytics in European Banking

This repository contains a complete project for analyzing customer churn in a European retail banking context. It includes synthetic data generation, exploratory data analysis, segmentation logic, and a Streamlit dashboard for interactive monitoring.

## Project Overview

Customer churn is a major financial risk for banks, affecting lifetime value, retention costs, and revenue stability. This project focuses on:

- Measuring overall churn
- Identifying high-risk customer segments
- Comparing churn behavior across geography and demographics
- Exploring churn among high-value customers
- Supporting retention strategy planning

## Repository Structure

```text
.
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/
│   ├── generate_data.py            # Synthetic dataset generation
│   └── customer_churn_europe.csv   # Generated banking churn dataset
├── src/
│   ├── __init__.py                 # Package marker
│   └── churn_analysis.py           # Reusable analysis utilities
├── docs/
│   ├── technical_documentation.md  # Detailed project guide
│   └── executive_summary.md        # Stakeholder summary
├── README.md
└── LICENSE
```

## Dataset

The project uses a synthetic banking dataset that mirrors a European bank customer dataset with the following columns:

- CustomerId
- Surname
- CreditScore
- Geography
- Gender
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary
- Exited

## Business Questions Answered

- What is the overall churn rate?
- Which regions and age groups show the highest churn?
- Are high-balance or inactive customers more likely to exit?
- Which customer segments should be prioritized for retention campaigns?

## Setup and Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Generate Data

```bash
python data/generate_data.py
```

## Run the Dashboard

```bash
streamlit run app.py
```

## Notes

- The dataset is synthetic and generated for demonstration and analytics training purposes.
- The analysis is designed to align with the project brief for customer segmentation and churn pattern analytics in European banking.

## Deliverables Included

- Exploratory data analysis and segmentation logic
- Streamlit dashboard for interactive exploration
- Technical documentation and executive summary
- Synthetic dataset aligned with the project schema and objectives

## License

This project is licensed under the MIT License.

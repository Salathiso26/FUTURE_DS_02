# FUTURE_DS_02: Customer Retention & Churn Analysis

Future Interns · Data Science & Analytics Track · Task 2 (2026)

## Overview

This project analyses customer and subscription data for a telecom business to
understand why customers churn, which segments are most at risk, and what
actions would improve retention. It was completed as Task 2 of the Future
Interns Data Science & Analytics internship.

## Dataset

**Telco Customer Churn** (Kaggle): 7,043 customer records, 21 original
columns covering demographics, account information, subscribed services,
billing, and churn status.
Source: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

## Key Findings

- Overall churn rate: **26.5%** (1,869 of 7,043 customers)
- Churn is concentrated early in the customer lifecycle: **52.9%** of
  customers churn within their first 6 months, versus **9.5%** for customers
  who have stayed 49-72 months
- **Contract type** is the strongest single retention lever: month-to-month
  customers churn at **42.7%** versus **2.8%** for two-year contracts
- Customers without Tech Support or Online Security churn at roughly 3x the
  rate of those with these add-ons
- Customers paying by electronic check churn at **45.3%**, about 3x the rate
  of customers on automatic payment methods
- Churned customers have on average **40% lower estimated lifetime value**
  than retained customers, despite paying higher monthly charges. The
  business is losing higher-value customers early, not low-value ones

Full write-up, charts, and recommendations are in the PDF report.

## Repository Contents

| File | Description |
|---|---|
| `Customer_Retention_Churn_Analysis.pdf` | Client-ready analysis report: churn overview, cohort analysis, driver ranking, and 5 actionable recommendations |
| `Customer_Retention_Churn_Analysis.docx` | Same report as an editable Word document |
| `analysis.py` | Data cleaning, churn/cohort metrics, driver ranking, and chart generation (pandas, matplotlib) |
| `Telco_Churn_Cleaned_for_PowerBI.csv` | Cleaned dataset with tenure cohorts, churn flag, and estimated lifetime value pre-computed, ready for import into a BI tool |
| `Churn_Interactive_Dashboard.html` | Full interactive dashboard (no install required). Filter by contract, internet service, payment method, and senior citizen status; KPIs, charts, and the driver ranking table recalculate live |
| `Churn_Dashboard_Simple.html` | Simplified static dashboard: just the 3 headline KPIs and the 3 charts that carry the core story (tenure, contract, internet service), with a one-line takeaway under each |
| `WA_Fn-UseC_-Telco-Customer-Churn.csv` | Original raw dataset (Kaggle) |
| `GITHUB_DESCRIPTION.txt` | Suggested GitHub "About" description and topic tags for this repo |

## Dashboard

A Power BI Desktop dashboard was not available in this environment, so the
retention dashboard was built as a self-contained interactive HTML file
(`Churn_Interactive_Dashboard.html`) instead. It reproduces the same KPIs,
cohort chart, driver charts, and monthly-charges distribution as the PDF
report, with live filtering by contract, internet service, payment method,
and senior citizen status. A simplified static version
(`Churn_Dashboard_Simple.html`) is also included for a quick, no-filter view
of just the headline story.


## Tools Used

Python (pandas, matplotlib) in Spyder IDE, ReportLab (PDF generation)

## Skills Gained

Retention and churn analysis, cohort analysis, customer lifetime value
estimation, driver/segmentation analysis, insight-driven business
recommendations.

## Author

Salathiso Ntsele
[LinkedIn](https://linkedin.com/in/salathiso-ntsele)

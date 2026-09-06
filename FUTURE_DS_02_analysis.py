"""
Future Interns - Data Science & Analytics Track
Task 2: Customer Retention & Churn Analysis

Dataset: WA_Fn-UseC_-Telco-Customer-Churn.csv (Kaggle Telco Customer Churn)

This script cleans the data, computes churn/retention metrics, builds tenure
cohorts, identifies the strongest churn drivers, and exports all chart images
used in the accompanying PDF report.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"] = 10

COLOR_STAY = "#2E86AB"
COLOR_CHURN = "#E63946"
COLOR_ACCENT = "#F4A261"


# 1. LOAD & CLEAN

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# TotalCharges has 11 blank strings (all customers with tenure == 0, i.e. brand
# new sign-ups who have not been billed yet). Convert to numeric and fill with
# 0, since these customers have paid nothing so far.
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# Tenure cohorts (months)
bins = [-1, 6, 12, 24, 48, 72]
labels = ["0-6 mo", "7-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"]
df["TenureCohort"] = pd.cut(df["tenure"], bins=bins, labels=labels)

n_customers = len(df)
n_churned = int(df["ChurnFlag"].sum())
overall_churn_rate = n_churned / n_customers

avg_tenure_all = df["tenure"].mean()
avg_tenure_churned = df.loc[df["Churn"] == "Yes", "tenure"].mean()
avg_tenure_retained = df.loc[df["Churn"] == "No", "tenure"].mean()

avg_monthly_all = df["MonthlyCharges"].mean()
avg_monthly_churned = df.loc[df["Churn"] == "Yes", "MonthlyCharges"].mean()
avg_monthly_retained = df.loc[df["Churn"] == "No", "MonthlyCharges"].mean()

# Simple customer lifetime value proxy: tenure (months) x monthly charge
df["EstLifetimeValue"] = df["tenure"] * df["MonthlyCharges"]
avg_ltv_retained = df.loc[df["Churn"] == "No", "EstLifetimeValue"].mean()
avg_ltv_churned = df.loc[df["Churn"] == "Yes", "EstLifetimeValue"].mean()

print(f"Total customers: {n_customers}")
print(f"Churned: {n_churned} ({overall_churn_rate:.1%})")
print(f"Retained: {n_customers - n_churned} ({1 - overall_churn_rate:.1%})")
print(f"Avg tenure - churned: {avg_tenure_churned:.1f} mo | retained: {avg_tenure_retained:.1f} mo")
print(f"Avg monthly charge - churned: R{avg_monthly_churned:.2f} | retained: R{avg_monthly_retained:.2f}")
print(f"Avg est. lifetime value - churned: R{avg_ltv_churned:.2f} | retained: R{avg_ltv_retained:.2f}")


# 2. CHURN RATE BY SEGMENT (retention drivers)

def churn_rate_by(col):
    g = df.groupby(col, observed=True)["ChurnFlag"].mean().sort_values(ascending=False)
    return g

by_contract = churn_rate_by("Contract")
by_internet = churn_rate_by("InternetService")
by_payment = churn_rate_by("PaymentMethod")
by_security = churn_rate_by("OnlineSecurity")
by_techsupport = churn_rate_by("TechSupport")
by_senior = churn_rate_by("SeniorCitizen")
by_paperless = churn_rate_by("PaperlessBilling")
by_cohort = churn_rate_by("TenureCohort")

print("\nChurn rate by contract type:\n", (by_contract * 100).round(1))
print("\nChurn rate by internet service:\n", (by_internet * 100).round(1))
print("\nChurn rate by payment method:\n", (by_payment * 100).round(1))
print("\nChurn rate by tenure cohort:\n", (by_cohort * 100).round(1))


# 3. CHARTS


# Chart 1: Overall churn split (donut)
fig, ax = plt.subplots(figsize=(5, 5))
sizes = [n_customers - n_churned, n_churned]
colors = [COLOR_STAY, COLOR_CHURN]
wedges, _, autotexts = ax.pie(
    sizes, colors=colors, autopct="%1.1f%%", startangle=90,
    pctdistance=0.8, wedgeprops=dict(width=0.4, edgecolor="white")
)
for t in autotexts:
    t.set_color("white")
    t.set_fontweight("bold")
ax.legend(wedges, ["Retained", "Churned"], loc="center", frameon=False, fontsize=11)
ax.set_title("Overall Customer Churn Split", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig("chart1_overall_churn.png", transparent=True)
plt.close()

# Chart 2: Churn rate by tenure cohort (retention curve proxy)
fig, ax = plt.subplots(figsize=(7, 4))
vals = (by_cohort.reindex(labels) * 100)
bars = ax.bar(vals.index, vals.values, color=COLOR_ACCENT, edgecolor="white")
ax.set_ylabel("Churn rate")
ax.set_title("Churn Rate by Customer Tenure Cohort", fontweight="bold", fontsize=13)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for b, v in zip(bars, vals.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("chart2_cohort_churn.png", transparent=True)
plt.close()

# Chart 3: Churn rate by contract type
fig, ax = plt.subplots(figsize=(6, 4))
vals = by_contract * 100
bars = ax.barh(vals.index, vals.values, color=COLOR_CHURN, edgecolor="white")
ax.set_xlabel("Churn rate")
ax.set_title("Churn Rate by Contract Type", fontweight="bold", fontsize=13)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
for b, v in zip(bars, vals.values):
    ax.text(v + 1, b.get_y() + b.get_height() / 2, f"{v:.1f}%", va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("chart3_contract_churn.png", transparent=True)
plt.close()

# Chart 4: Churn rate by internet service & tech support (grouped)
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
vals_i = by_internet * 100
axes[0].bar(vals_i.index, vals_i.values, color=COLOR_STAY, edgecolor="white")
axes[0].set_title("By Internet Service", fontsize=11, fontweight="bold")
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[0].spines[["top", "right"]].set_visible(False)
for i, v in enumerate(vals_i.values):
    axes[0].text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)

vals_t = by_techsupport * 100
axes[1].bar(vals_t.index, vals_t.values, color=COLOR_ACCENT, edgecolor="white")
axes[1].set_title("By Tech Support Subscription", fontsize=11, fontweight="bold")
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].spines[["top", "right"]].set_visible(False)
for i, v in enumerate(vals_t.values):
    axes[1].text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)

fig.suptitle("Churn Rate by Service Add-ons", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig("chart4_service_churn.png", transparent=True)
plt.close()

# Chart 5: Churn rate by payment method
fig, ax = plt.subplots(figsize=(7, 4))
vals = by_payment * 100
bars = ax.barh(vals.index, vals.values, color=COLOR_CHURN, edgecolor="white")
ax.set_xlabel("Churn rate")
ax.set_title("Churn Rate by Payment Method", fontweight="bold", fontsize=13)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
for b, v in zip(bars, vals.values):
    ax.text(v + 1, b.get_y() + b.get_height() / 2, f"{v:.1f}%", va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("chart5_payment_churn.png", transparent=True)
plt.close()

# Chart 6: Monthly charges distribution - churned vs retained
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df.loc[df["Churn"] == "No", "MonthlyCharges"], bins=30, alpha=0.6,
        label="Retained", color=COLOR_STAY, density=True)
ax.hist(df.loc[df["Churn"] == "Yes", "MonthlyCharges"], bins=30, alpha=0.6,
        label="Churned", color=COLOR_CHURN, density=True)
ax.set_xlabel("Monthly charges (R)")
ax.set_ylabel("Density")
ax.set_title("Monthly Charges Distribution: Churned vs Retained", fontweight="bold", fontsize=13)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("chart6_monthly_charges_dist.png", transparent=True)
plt.close()

print("\nAll charts saved.")


# 4. SIMPLE DRIVER RANKING (absolute churn-rate spread per feature)

candidate_cols = [
    "Contract", "InternetService", "PaymentMethod", "OnlineSecurity",
    "TechSupport", "OnlineBackup", "DeviceProtection", "PaperlessBilling",
    "SeniorCitizen", "Dependents", "Partner", "TenureCohort", "StreamingTV",
    "StreamingMovies", "MultipleLines",
]
spread = {}
for c in candidate_cols:
    g = df.groupby(c, observed=True)["ChurnFlag"].mean()
    spread[c] = g.max() - g.min()

spread_series = pd.Series(spread).sort_values(ascending=False)
print("\nTop churn drivers (spread in churn rate across category values):")
print((spread_series * 100).round(1))

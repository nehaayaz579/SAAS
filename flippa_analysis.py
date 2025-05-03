import pandas as pd
import re
import matplotlib.pyplot as plt

# --- Function to clean money-like values ---
def clean_money(value):
    if isinstance(value, str):
        value = re.findall(r'[\d,]+(?:\.\d+)?', value.replace(',', ''))
        return float(value[0]) if value else None
    return value

# --- Load data ---
df = pd.read_csv("flippa_investment_data.csv")

# --- Clean price and profit ---
df["Price"] = df["Price"].apply(clean_money)
df["Monthly Profit"] = df["Monthly Profit"].apply(clean_money)
df["Revenue"] = df["Revenue"].apply(clean_money)

# --- Drop missing values ---
df = df.dropna(subset=["Price", "Monthly Profit"])
df = df[df["Monthly Profit"] > 0]

# --- Calculate metrics ---
df["Annual ROI (%)"] = (df["Monthly Profit"] * 12 / df["Price"]) * 100
df["Payback Period (months)"] = df["Price"] / df["Monthly Profit"]
df["Profit Margin (%)"] = (df["Monthly Profit"] / df["Revenue"]) * 100

# --- Clean site age (optional) ---
# You can add cleaning logic if you want to use Site Age in months/years

# --- Top by ROI ---
top_roi = df.sort_values(by="Annual ROI (%)", ascending=False).head(10)
top_roi.to_csv("top_roi_listings.csv", index=False)

# --- Top by fastest payback ---
top_payback = df.sort_values(by="Payback Period (months)").head(10)
top_payback.to_csv("top_fastest_payback.csv", index=False)

# --- Print top ROI listings ---
print("\n🔝 Top 10 SaaS Listings by Annual ROI:\n")
print(top_roi[["Title", "Price", "Monthly Profit", "Annual ROI (%)", "Payback Period (months)"]].to_string(index=False))

# --- Optional: Show chart ---
top_roi.plot(x="Title", y="Annual ROI (%)", kind="barh", figsize=(10,6), color='skyblue')
plt.title("Top 10 SaaS Listings by Annual ROI")
plt.xlabel("Annual ROI (%)")
plt.tight_layout()
plt.show()

print("\n📁 Results saved: top_roi_listings.csv & top_fastest_payback.csv")

import matplotlib.pyplot as plt

top_roi.plot(x="Title", y="Annual ROI (%)", kind="barh", figsize=(10,6), color='skyblue')
plt.title("Top 10 SaaS Listings by Annual ROI")
plt.xlabel("Annual ROI (%)")
plt.tight_layout()
plt.show()

# 🔍 Simple Insights (auto-generated)

# Highest ROI listing
top = df.sort_values(by="Annual ROI (%)", ascending=False).head(1).iloc[0]
print(f"✅ Highest ROI: '{top['Title']}' with ROI {top['Annual ROI (%)']:.2f}% and Payback in {top['Payback Period (months)']:.1f} months.")

# Verified vs Non-Verified ROI
v_roi = df[df["Verified"] == "Yes"]["Annual ROI (%)"].mean()
nv_roi = df[df["Verified"] == "No"]["Annual ROI (%)"].mean()
print(f"📊 Verified Listings Avg ROI: {v_roi:.2f}%")
print(f"📉 Non-Verified Listings Avg ROI: {nv_roi:.2f}%")

# Listings under $3000 with ROI > 100%
good_deals = df[(df["Price"] < 3000) & (df["Annual ROI (%)"] > 100)]
print(f"💡 Listings under $3000 with ROI > 100%: {len(good_deals)} found")

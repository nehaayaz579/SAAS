# Flippa SaaS Investment Analyzer

🚀 **Flippa SaaS Investment Analyzer** is a Python-based tool designed to scrape, analyze, and visualize data from Flippa listings, focusing on SaaS (Software as a Service) businesses priced between $2,000 and $5,000.

---

## 🔍 Project Overview

This project aims to assist investors in identifying profitable SaaS businesses on Flippa by providing insights into key metrics such as ROI, payback period, and profit margin.

---

## ⚙️ Requirements

- Python 3.x
- `selenium`
- `beautifulsoup4`
- `pandas`
- `matplotlib`
- `webdriver-manager`

You can install these dependencies using the following command:

```bash
pip install -r requirements.txt

🚀 Usage
1. Scrape Data from Flippa
Run the following command to scrape SaaS listings data from Flippa:

```bash
python flippa_data.py
This will generate the following files:

flippa_investment_data.json: Raw data in JSON format

flippa_investment_data.csv: Raw data in CSV format

2. Analyze and Visualize the Data
After scraping the data, run the analysis script:

```bash
python flippa_analyze.py
This script will:

Clean the data

Calculate key metrics: ROI, payback period, and profit margin

Generate visualizations using matplotlib

📊 Outputs
flippa_investment_data.json: Raw scraped data in JSON format

flippa_investment_data.csv: Raw scraped data in CSV format

top_roi_listings.csv: Top 10 listings with the highest annual ROI

top_fastest_payback.csv: Top 10 listings with the shortest payback period

🧠 Insights
Highest ROI Listing: 'Listing Title' with ROI 150% and Payback Period of 8 months

Verified Listings Average ROI: 120%

Non-Verified Listings Average ROI: 90%

Listings under $3000 with ROI > 100%: 5 listings


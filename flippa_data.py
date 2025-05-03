from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import csv

def scrape_flippa_with_selenium(min_required=50):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    listings = []
    page = 1

    try:
        while len(listings) < min_required:
            url = f"https://flippa.com/buy/sitetype/saas?filter[price][min]=2000&filter[price][max]=5000&page={page}"
            driver.get(url)
            time.sleep(8)  # Wait for JS content to load

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cards = soup.find_all('div', id=lambda x: x and x.startswith('listing-'))

            if not cards:
                print(f"No listings found on page {page}. Ending scrape.")
                break

            for card in cards:
                try:
                    listing = {
                        "Title": extract_text(card, 'h6', '!tw-text-xl'),
                        "Price": extract_price(card),
                        "Original Price": extract_original_price(card),
                        "Discount": extract_discount(card),
                        "Revenue": extract_metric(card, "Revenue"),
                        "Net Profit": extract_metric(card, "Net Profit"),
                        "Monthly Profit": extract_metric(card, "Net Profit").split('/')[0].strip() if extract_metric(card, "Net Profit") != "N/A" else "N/A",
                        "Site Age": extract_metric(card, "Site Age"),
                        "Industry": extract_metric(card, "Industry"),
                        "Monetization": extract_metric(card, "Monetization"),
                        "Country": extract_country(card),
                        "Description": extract_text(card, 'p', 'tw-text-gray-900'),
                        "Link": "https://flippa.com" + card.find('a', class_='GTM-search-result-card')['href'],
                        "Verified": "Yes" if card.find('span', string='Verified Listing') else "No",
                        "Sponsored": "Yes" if card.find('span', {'ng-if': 'listing.sponsored'}) else "No"
                    }
                    listings.append(listing)

                    if len(listings) >= min_required:
                        break

                except Exception as e:
                    print(f"Skipping listing due to error: {str(e)}")
                    continue

            print(f"✅ Page {page} scraped. Total listings so far: {len(listings)}")
            page += 1

    finally:
        driver.quit()

    return listings

# --- Helper Functions ---
def extract_text(element, tag, class_):
    elem = element.find(tag, class_=lambda x: x and class_ in x)
    return elem.get_text(strip=True) if elem else "N/A"

def extract_price(card):
    price_elem = card.find('span', class_='tw-text-emerald-600') or card.find('h5')
    return price_elem.get_text(strip=True) if price_elem else "N/A"

def extract_original_price(card):
    original = card.find('del', class_='ng-binding')
    return original.get_text(strip=True) if original else "N/A"

def extract_discount(card):
    discount = card.find('span', class_='tw-text-emerald-600')
    if discount:
        discount = discount.find_next('span')
        return discount.get_text(strip=True) if discount else "N/A"
    return "N/A"

def extract_metric(card, metric_name):
    for item in card.find_all('div', class_='ng-scope'):
        label = item.find('div', class_='tw-text-gray-600')
        if label and metric_name.lower() in label.get_text(strip=True).lower():
            value = item.find('div', class_='tw-text-gray-800')
            return value.get_text(strip=True) if value else "N/A"
    return "N/A"

def extract_country(card):
    country_div = card.find('div', {'ng-if': 'listing.country_name'})
    if country_div:
        country = country_div.find('span', class_='ng-binding')
        return country.get_text(strip=True) if country else "N/A"
    return "N/A"

# --- Main ---
if __name__ == "__main__":
    print("🚀 Scraping Flippa SaaS listings across pages... (Target: 100+)")
    results = scrape_flippa_with_selenium(min_required=100)

    if results:
        with open('flippa_investment_data.json', 'w') as f:
            json.dump(results, f, indent=2)

        df = pd.DataFrame(results)
        df.to_csv('flippa_investment_data.csv', index=False, quoting=csv.QUOTE_ALL)

        print(f"\n✅ Done! Scraped {len(results)} listings")
        print("💾 Files saved:")
        print("- flippa_investment_data.json")
        print("- flippa_investment_data.csv")
    else:
        print("❌ No listings found. Flippa may have blocked scraping or structure changed.")

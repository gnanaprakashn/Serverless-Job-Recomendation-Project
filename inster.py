# etender_scraper.py

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Setup Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # run in headless mode (no browser UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the website
url = "https://etender.cpwd.gov.in/"
driver.get(url)
time.sleep(5)  # Wait for page to load

# Navigate to "New Tenders" → "All"
driver.find_element(By.LINK_TEXT, "New Tenders").click()
time.sleep(2)
driver.find_element(By.LINK_TEXT, "All").click()
time.sleep(5)  # Wait for tender table to load

# Locate the tender table rows
rows = driver.find_elements(By.CSS_SELECTOR, "#TableNewTender tbody tr")

# Prepare data list
data = []

for row in rows[:20]:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) < 6:
        continue  # skip if not enough columns
    
    record = {
        "ref_no": cols[0].text.strip(),
        "title": cols[1].text.strip(),
        "tender_value": cols[2].text.strip(),
        "bid_submission_end_date": cols[3].text.strip(),
        "emd": cols[4].text.strip(),
        "bid_open_date": cols[5].text.strip()
    }
    data.append(record)

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("cpwd_tenders.csv", index=False)

# Cleanup
driver.quit()

print("Scraping complete! Saved as cpwd_tenders.csv.")

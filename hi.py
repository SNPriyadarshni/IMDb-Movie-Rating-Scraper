import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

edge_options = Options()

edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--window-size=1920,1080")

service = Service(r"C:\msedgedriver.exe")

driver = webdriver.Edge(service=service, options=edge_options)

# -------------------------
# IMDb Top 250 URL
# -------------------------
url = "https://www.imdb.com/chart/top/"
driver.get(url)
time.sleep(3)  # wait for page to load fully

# -------------------------
# Scraping Movie Data
# -------------------------
movies = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item")

data = []
rank = 1
for movie in movies:
    try:
        title = movie.find_element(By.CSS_SELECTOR, "h3").text
        year = movie.find_element(By.CSS_SELECTOR, ".cli-title-metadata-item").text
        rating = movie.find_element(By.CSS_SELECTOR, ".ipc-rating-star--rating").text

        data.append({
            "Rank": rank,
            "Title": title,
            "Year": year,
            "Rating": rating
        })
        rank += 1
    except Exception as e:
        print("Error parsing movie:", e)

# Close browser
driver.quit()

# -------------------------
# Save to CSV
# -------------------------
df = pd.DataFrame(data)
df.to_csv("imdb_top250.csv", index=False, encoding="utf-8")

print("✅ Scraping complete! Data saved to imdb_top250.csv")

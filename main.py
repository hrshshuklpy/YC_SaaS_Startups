from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
import csv
import random

# Path to your ChromeDriver
chrome_driver_path = "/Users/harshshukla/Downloads/chromedriver-mac-arm64/chromedriver"

# URL of the Y Combinator companies page filtered by "SaaS" tag
url = "https://www.ycombinator.com/companies?tags=SaaS"

# JSON and CSV files where the data will be stored
json_file = "ycombinator_saas_companies.json"
csv_file = "ycombinator_saas_companies.csv"

# Initialize the Chrome WebDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)


def safe_extract(by, value, dri=driver):
    try:
        return dri.find_element(by, value).text
    except NoSuchElementException:
        return None


def safe_extract_attr(by, value, attribute, dri=driver):
    try:
        return dri.find_element(by, value).get_attribute(attribute)
    except NoSuchElementException:
        return None


# Function to scrape company details
def scrape_company_details(last_count):
    driver.get(url)
    time.sleep(random.uniform(1, 4))  # Wait for the page to load

    company_data = []
    last_count = last_count

    while True:
        companies = driver.find_elements(By.CSS_SELECTOR, 'a._company_86jzd_338')
        print(f'Newly loaded companies: {len(companies)}')

        # Break the loop if no new companies are loaded
        if len(companies) == last_count:
            print("No more companies to load.")
            break

        # Scrape the newly loaded companies
        if last_count < len(companies):
            scrapper(last_count, len(companies), company_data, companies)
            # Update last_count
            last_count = len(companies)


        # Scroll down to load more companies
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(10, 12))  # Give some time for new companies to load

    # Save the data after scraping all companies
    dump_json(company_data)
    json_to_csv(company_data)


def scrapper(start_index, end_index, company_data, companies):
    for i in range(start_index, end_index):
        company = companies[i]
        company_info = {}

        # Click on the company to get more details
        company_link = company.get_attribute('href')

        # Open the company link in a new tab
        driver.execute_script("window.open(arguments[0], '_blank');", company_link)
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
        time.sleep(random.uniform(2, 5))  # Random sleep between 2 and 5 seconds

        # Extract and add company info
        company_info["Name"] = safe_extract(By.CSS_SELECTOR, 'div.prose.max-w-full h1.font-extralight')
        company_info["Url"] = safe_extract_attr(By.CSS_SELECTOR, 'div.group a.mb-2.whitespace-nowrap', 'href')
        company_info["Location"] = safe_extract(By.XPATH,
                                                '//div[@class="space-y-0.5"]//span[text()="Location:"]/following-sibling::span')
        company_info["Founded"] = safe_extract(By.XPATH,
                                               '//div[@class="space-y-0.5"]//span[text()="Founded:"]/following-sibling::span')
        company_info["Description"] = safe_extract(By.CSS_SELECTOR,
                                                   'div.prose.hidden.max-w-full.font-extralight.md\\:block div.text-xl')
        company_info["Long Description"] = safe_extract(By.CSS_SELECTOR, 'section.relative p.whitespace-pre-line')

        # Extract tags
        tags = driver.find_elements(By.CSS_SELECTOR, 'div.yc-tw-Pill')
        alltags = [tag.text for tag in tags]

        # Add tags in company_info
        company_info["YC_Year"] = alltags[0] if alltags else None
        company_info["Tags"] = alltags[1:] if len(alltags) > 1 else None

        # Extract founders_info
        founders = driver.find_elements(By.CSS_SELECTOR, 'div.leading-snug')
        founders_info = {}

        for founder in founders:
            founder_name = founder.find_element(By.CSS_SELECTOR, 'div.font-bold').text
            linkedin = safe_extract_attr(By.CSS_SELECTOR, 'a[title][href*="linkedin"]', 'href', dri=founder)
            twitter = safe_extract_attr(By.CSS_SELECTOR, 'a[title][href*="twitter"]', 'href', dri=founder)

            founders_info[founder_name] = {"LinkedIn": linkedin, "Twitter": twitter}

        # Add founders_info in company_info
        company_info["Founders"] = founders_info

        # Add company_info in the company_data
        company_data.append(company_info)
        print(company_info["Name"])

        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(random.uniform(2, 7))  # Random sleep between 2 and 7 seconds


def dump_json(data):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Scraping completed. Data has been saved to {json_file}.")


# Function to convert JSON data to CSV
def json_to_csv(data):
    # Define the headers for the CSV file
    headers = ["Name", "Url", "Location", "Founded", "Description", "Long Description", "YC_Year", "Tags", "Founders"]

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for company in data:
            name = company.get("Name")
            url = company.get("Url")
            location = company.get("Location")
            founded = company.get("Founded")
            description = company.get("Description")
            long_description = company.get("Long Description")
            yc_year = company.get("YC_Year")
            tags = ", ".join(company["Tags"]) if company.get("Tags") else None

            founders_info = []
            for founder, links in company["Founders"].items():
                founder_data = f"{founder}: LinkedIn - {links['LinkedIn']}, Twitter - {links['Twitter']}"
                founders_info.append(founder_data)

            writer.writerow(
                [name, url, location, founded, description, long_description, yc_year, tags, "; ".join(founders_info)])

    print(f"Data has been saved to {csv_file}.")


# Run the scraping function
scrape_company_details(1)

# Close the driver
driver.quit()
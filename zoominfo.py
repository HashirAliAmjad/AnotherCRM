import time
import re
import random
import undetected_chromedriver
import requests
import cloudscraper
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.parse import urlparse, parse_qs, unquote

def fetch_page_source(url):
    scraper = cloudscraper.create_scraper()  # Create a CloudflareScraper instance
    response = scraper.get(url)
    return response.content

def convert_url_to_actual(url):
    if '/url?q=' in url:
        actual_url = url.split('/url?q=')[1].split('&')[0]
        actual_url = unquote(actual_url)
        return actual_url
    else:
        return url

def fetch_phone_number(company_name):
    options = Options()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(options=options)

    search_query = f"{company_name} corporate number zoominfo"
    google_url = f"https://www.google.com/search?q={search_query}"
    driver.get(google_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    zoominfo_link = soup.find("a", href=lambda href: href and 'zoominfo.com/c/' in href)

    if not zoominfo_link:
        driver.quit()
        return None

    zoominfo_url = zoominfo_link['href']
    zoominfo_url = convert_url_to_actual(zoominfo_url)
    page_source = fetch_page_source(zoominfo_url)
    page_source = page_source.decode('utf-8')  # Convert bytes to string
    soup = BeautifulSoup(page_source, 'html.parser')
    contact_details = {}

    # Use corrected XPath to find phone numbers
    phone_numbers = soup.select("#left-container > div:nth-child(1) > app-company-overview > div > div > div > div:nth-child(1) > app-icon-text:nth-child(2) > div")
    print(phone_numbers.text)
    contact_details['phone_numbers'] = [number['href'].split(':')[-1] for number in phone_numbers]

    # Extract email addresses
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_source)
    contact_details['email_addresses'] = email_addresses

    driver.quit()
    return contact_details



if __name__ == "__main__":
    for i in range(1, 5):
        company_name = input("Company name: ")
        contact_details = fetch_phone_number(company_name)

        if contact_details and 'phone_numbers' in contact_details:
            print(f"Phone number(s) for {company_name}: {contact_details['phone_numbers']}")
            if 'email_addresses' in contact_details:
                print(f"Email address(es) for {company_name}: {contact_details['email_addresses']}")
        else:
            print(f"Phone number not found for {company_name}.")

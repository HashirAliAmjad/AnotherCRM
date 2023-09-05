import time
import re
import undetected_chromedriver
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
    try:
        search_query = f"{company_name} corporate phone number apollo"
        google_url = f"https://www.google.com/search?q={search_query}"
        driver.get(google_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        apollo_link = soup.find("a", href=lambda href: href and 'apollo.io' in href)
        if not apollo_link:
            driver.quit()
            return None
        apollo_url = apollo_link['href']
        apollo_url = convert_url_to_actual(apollo_url)
        driver.get(apollo_url)  # Open the Apollo page
        time.sleep(5)  # Let the page load (adjust sleep duration as needed)
        '''
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        contact_details = {}
        '''
        contact_details = {}
        # Use XPath to find phone number
        phone_number_element = driver.find_element(By.CSS_SELECTOR,'div[class="CompanyOverview__LogoInfoRow-sc-164vtn2-1 fIJqwk row"]')
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'div[class="d-flex mt-3 mt-md-0 px-0 CompanyOverview__InfoCol-sc-164vtn2-3 hJOIND col"]')
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'div[class="flex-column align-items-start row"]')
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'div[class="d-none d-md-flex align-items-start mt-3 px-0 col"]')
        phone_number_element=phone_number_element.find_element(By.XPATH,'//*[@id="overview"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div')
        #print("ALL: ",phone_number_element.text)
        phone_number_element=phone_number_element.find_element(By.XPATH,'//*[@id="overview"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[1]')
        #print("ALL: ",phone_number_element.text)
        phone_number_element=phone_number_element.find_element(By.XPATH,'//*[@id="overview"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[4]')
        #print("ALL: ",phone_number_element.text)
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'a[class="cursor-pointer CompanyOverview__ClickableLink-sc-164vtn2-0 jtwgmT"]')
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'div[class="px-0 mx-0 ProfileLink__ProfileLinkContainer-sc-1ye4tsl-0 hblNGV container"]')
        phone_number_element=phone_number_element.find_element(By.CSS_SELECTOR,'div[class="d-flex align-items-start ProfileLink__LinkLabel-sc-1ye4tsl-1 dhDxaQ"]')
        phone_number_element=phone_number_element.find_element(By.TAG_NAME ,'span')
        #print("HEHEHE: ",phone_number_element.text)
        if phone_number_element:
            contact_details['phone_number'] = phone_number_element.text
        return contact_details
    except:
        contact_details="None"
        return contact_details


if __name__ == "__main__":
    options = Options()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(options=options)
    for i in range(1, 5):
        company_name = input("Company name: ")
        contact_details = fetch_phone_number(company_name)

        if contact_details and 'phone_number' in contact_details:
            print(f"Phone number for {company_name}: {contact_details['phone_number']}")
        else:
            print(f"Phone number not found for {company_name}.")
    driver.quit()

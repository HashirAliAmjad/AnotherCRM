import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import webbrowser
from selenium import webdriver
import os
import time
from selenium.webdriver.support.wait import WebDriverWait
import json
from urllib.parse import urljoin
import whois

os.environ['PATH'] +=r"C:\Users\User\.spyder-py3"
chrome="C:\Program Files\Google\Chrome\Application"

def search_google(query):
    query = quote(query)
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('a')
    links = []
    for result in search_results:
        link = result.get('href')
        if link and link.startswith('/url?q='):
            link = link[7:]
            link = link.split('&')[0]
            links.append(link)
            if len(links) == 5:
                break
    return links

def extract_social_media_links(url):
    # Send a GET request to the company's website
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize variables to store the last link for each social media platform
    last_facebook_link = None
    last_instagram_link = None
    last_twitter_link = None
    last_youtube_link = None
    last_linkedin_link = None
    
    # Search for Facebook links
    facebook_links = soup.find_all(href=re.compile(r'facebook\.com'))
    if facebook_links:
        last_facebook_link = facebook_links[-1]['href']
    
    # Search for Instagram links
    instagram_links = soup.find_all(href=re.compile(r'instagram\.com'))
    if instagram_links:
        last_instagram_link = instagram_links[-1]['href']
    
    # Search for Twitter links
    twitter_links = soup.find_all(href=re.compile(r'twitter\.com'))
    if twitter_links:
        last_twitter_link = twitter_links[-1]['href']
        
    # Search for Youtube links
    youtube_links = soup.find_all(href=re.compile(r'youtube\.com'))
    if youtube_links:
        last_youtube_link = youtube_links[-1]['href']
        
    # Search for Linkedin links
    linkedin_links = soup.find_all(href=re.compile(r'linkedin\.com'))
    if linkedin_links:
        last_linkedin_link = linkedin_links[-1]['href']
    
    # Create a dictionary to store the last social media links
    last_social_media_links = {
        'facebook': last_facebook_link,
        'instagram': last_instagram_link,
        'twitter': last_twitter_link,
        'youtube': last_youtube_link,
        'linkedin': last_linkedin_link
    }
    
    return last_social_media_links

def extract_contact_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contact_details = {}

    # Extract phone numbers
    phone_numbers = re.findall(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', response.text)
    contact_details['phone_numbers'] = [''.join(number) for number in phone_numbers]

    # Extract email addresses
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
    contact_details['email_addresses'] = email_addresses

    return contact_details

def get_contact_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find links to About Us or Contact Us pages
    contact_link = None

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and ('contact' in href.lower() or 'contactus' in href.lower()):
            contact_link = href

    if contact_link:
        contact_url = urljoin(url, contact_link)
        contact_details = extract_contact_details(contact_url)
        if contact_details['phone_numbers'] or contact_details['email_addresses']:
            return contact_details

    return None


# Set Chrome as the default browser
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))


# Company Name
data = 'sadapay'
cname = data


# Search Google for the company or person name
links = search_google(cname)

# Extract social media links
website_url = links[0]
social_media_links = extract_social_media_links(links[0])
    

# Print the extracted social media links
if social_media_links:
    facebook_url = social_media_links['facebook']
    instagram_url = social_media_links['instagram']
    twitter_url = social_media_links['twitter']
    youtube_url = social_media_links['youtube']
    linkedin_url = social_media_links['linkedin']
      
    if facebook_url==None:
        facebook_url="No URL"
    if instagram_url==None:
        instagram_url="No URL"
    if twitter_url==None:
        twitter_url="No URL"
    if youtube_url==None:
        youtube_url="No URL"
    if linkedin_url==None:
        linkedin_url="No URL"
        
    # Create a dictionary to store the URLs
url_dict = {
    'company-url':cname,
    'website_url':website_url,
    'facebook_url': facebook_url,
    'instagram_url': instagram_url,
    'twitter_url': twitter_url,
    'youtube_url': youtube_url,
    'linkedin_url': linkedin_url
}

# Convert the dictionary to a JSON string
json_output = json.dumps(url_dict)

# Print the JSON string
print(json_output)

# Prompt the user for a website URL
url = website_url

# Call the function to extract contact details
contact_info = get_contact_details(url)

# Remove duplicates from phone numbers and email addresses
unique_phone_numbers = list(set(contact_info['phone_numbers']))
unique_email_addresses = list(set(contact_info['email_addresses']))


# Print the extracted contact details
if contact_info:
   # Print the extracted contact details (after removing duplicates)
    if unique_phone_numbers:
        print("Phone Numbers:")
        for number in unique_phone_numbers:
            print(number)
    
    if unique_email_addresses:
        print("\nEmail Addresses:")
        for email in unique_email_addresses:
            print(email)
else:
    print("Contact details not found.")





    
    
    

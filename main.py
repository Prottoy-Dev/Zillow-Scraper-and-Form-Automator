"""
This script scrapes rental property data from Zillow and submits it to a Google Form.
It uses the following libraries: pprint, requests, BeautifulSoup, time, selenium.
The script first sends a GET request to the Zillow website and extracts the links, addresses, and prices of rental properties.
It then uses Selenium to fill out a Google Form with the extracted data.

Functions:
- links(): Finds all the links on a webpage and returns a list of those links.
- address(): Extracts the address of properties from a website using web scraping. Returns a list of addresses of properties.
- price(): Extracts the price of properties from a website using web scraping. Returns a list of prices.
"""

# Import necessary libraries
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

# Define the URL and headers for the Zillow website

url = os.getenv("url")
header = {
    "User-Agent": os.getenv("useragent"),
    "Accept-Language": os.getenv("acceptlan"),
}

response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")
search = soup.find(name="div", id="grid-search-results")

def links():
    """
    This function finds all the links on zillow and returns a list of those links.
    :return: A list of links found on the webpage.
    """
    lists = search.find_all(name="a", tabindex="0")
    links = []
    for list in lists:
        href = list.get("href")
        if "http" not in href:
            href = f"https://www.zillow.com{href}"
        links.append(href)
        sleep(1)
    return links

def address():
    """
    This function extracts the address of properties from zillow using web scraping.

    Returns:
    address (list): A list of addresses of properties.
    """
    address = [add.getText() for add in search.select(".property-card-data a address")]
    return address

def price():
    """
    This function extracts the price of properties from zillow using web scraping.
    It returns a list of prices.
    """
    price =[price.getText().split()[0] for price in search.select(".property-card-data span")]
    print(price)
    return price

# Initialize the Selenium webdriver for Google Form submission

driver = webdriver.Edge()
driver.maximize_window()
driver.get("https://forms.gle/iBXveqxvgCsHNPQT7")
sleep(2)  

# Loop through property listings and fill out the Google Form

for n in range(len(links())):
    # Find and fill in the address input field
    sleep(2)
    address_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_entry.send_keys(address()[n])

    # Find and fill in the price input field
    sleep(2)
    price_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_entry.send_keys(price()[n])

    # Find and fill in the link input field
    sleep(2)
    link_entry = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_entry.send_keys(links()[n])
    sleep(2)

    # Submit the form and start a new entry
    driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()
    sleep(2)

    # Click to move to the next entry in the Google Form
    another_entry = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    sleep(2)

# Close the browser window
driver.quit()

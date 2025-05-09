import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from bs4 import BeautifulSoup
from collections import defaultdict
import csv

import time

# Setting up Selenium WebDriver
service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

all_events = defaultdict(list)


url = "https://judotv.com"
driver.get(url)
time.sleep(2)
# Accept Cookies
find = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
find.click()
time.sleep(1)
# Click login button
find = driver.find_element(By.CSS_SELECTOR, "span[style*='https://api.iconify.design/carbon/login.svg']")
find = find.find_element(By.XPATH, "./ancestor::button")
find.click()
time.sleep(1)
# Enter login credentials
find = driver.find_element(By.ID, "email")
find.send_keys("dopep63842@bocapies.com")
time.sleep(1)
find = driver.find_element(By.ID, "password")
find.send_keys("ProgProject2025")
time.sleep(1)
# Click login button
find = driver.find_element(By.CSS_SELECTOR, "button.button--gold")
find.click()
time.sleep(3)
# Go to competitions page
find = driver.find_element(By.CSS_SELECTOR, 'a[href="/competitions"]')
find.click()

time.sleep(2)

url = "https://judotv.com/competitions/gs_kaz2025/judoka"
driver.get(url)
time.sleep(2)


find = driver.find_element(By.XPATH, "//button[span[text()='Select country']]")
find.click()

time.sleep(2)

find = driver.find_element(By.XPATH, "(//li[contains(@role, 'menuitem')])[1]")
find.click()

time.sleep(1)

# Now click the "View all" button
find = driver.find_element(By.XPATH, "//button[.//span[text()='View all']]")
find.click()

time.sleep(2)

find = driver.find_element(By.XPATH, "//button[span[text()='Select category']]")
find.click()

time.sleep(2)

weight='-81' + ' kg'
find = driver.find_element(By.XPATH, f"//li[@role='menuitem']//span[text()='{weight}']")
find.click() 
time.sleep(2)

find = driver.find_element(By.XPATH, "//button[.//span[text()='Select']]")
find.click()

time.sleep(2)

while True:
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Load more']]")
        load_more_button.click()
        time.sleep(1.5) # slight wait to allow more players to load
    except NoSuchElementException:
        print("No more 'Load more' button found.")
        break

time.sleep(2)

competitors = driver.find_elements(By.XPATH, "//a[contains(@href, '/judoka/')]")

for c in competitors:
    try:
        # Get full name (e.g., "Joonhwan LEE")
        name_div = c.find_element(By.XPATH, ".//div[contains(@class, 'font-medium inline')]")
        full_name = name_div.text.strip()

        # Split name and surname
        parts = full_name.split()
        name = " ".join(parts[:-1])
        surname = parts[-1]

        # Get country code (e.g., "KOR")
        country_code = c.find_element(By.XPATH, ".//div[contains(@class, 'text-center') and contains(@class, 'text-xs')]").text.strip()

        print(f"Name: {name}, Surname: {surname}, Country: {country_code}")
    except Exception as e:
        print(f"Error extracting data: {e}")
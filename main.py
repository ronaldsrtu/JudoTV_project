import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import csv
import time

# == Custom Data Structures ==

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def search(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def remove(self, key):
        index = self._hash(key)
        previous = None
        current = self.table[index]
        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next
        raise KeyError(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False

    def items(self):
        for entry in self.table:
            current = entry
            while current:
                yield (current.key, current.value)
                current = current.next

# == Competition Data Class ==

class Competition:
    def __init__(self, name, date, href):
        self.name = name
        self.date = date
        self.href = href

    def __repr__(self):
        return f"{self.name}, {self.date}, {self.href}"

# == Selenium Setup ==

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

all_events = HashTable(50)

# == Main ==

def main():
    url = "https://judotv.com"
    driver.get(url)
    time.sleep(2)

    find = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    find.click()
    time.sleep(1)

    find = driver.find_element(By.CSS_SELECTOR, "span[style*='https://api.iconify.design/carbon/login.svg']")
    find = find.find_element(By.XPATH, "./ancestor::button")
    find.click()
    time.sleep(1)

    find = driver.find_element(By.ID, "email")
    find.send_keys("dopep63842@bocapies.com")
    time.sleep(1)

    find = driver.find_element(By.ID, "password")
    find.send_keys("ProgProject2025")
    time.sleep(1)

    find = driver.find_element(By.CSS_SELECTOR, "button.button--gold")
    find.click()
    time.sleep(3)

    find = driver.find_element(By.CSS_SELECTOR, 'a[href="/competitions"]')
    find.click()
    time.sleep(2)

    while True:
        print("\n-JudoTV choice menu:")
        print("1. Get list of all competitions")
        print("2. Get list of all competitions by category")
        print("3. Get TOP 10 ranked players")
        print("4. Get nation list of a competition")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            get_comp_data()
        elif choice == "2":
            get_comp_data_category()
        elif choice == "3":
            get_ranked_players()
        elif choice == "4":
            get_country_list()
        elif choice == "5":
            break


def get_comp_data():
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    competition_url = "https://judotv.com/competitions" 
    
    driver.get(competition_url)

    for month in month_names:
        try:
            button = driver.find_element(By.XPATH, f"//button[text()='{month}']")
            button.click()
            time.sleep(2)

            events = extract_and_categorize()
            time.sleep(2)

            for category, event_list in events.items():
                existing = all_events.search(category) if category in all_events else []
                all_events.insert(category, existing + event_list)
        except Exception:
            print("Error clicking on " + month)

    with open("events2025.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Event Name", "Date", "Link"])
        for category, events_list in all_events.items():
            seen = set()
            for event in events_list:
                if (event.name, event.date, event.href) not in seen:
                    writer.writerow([category, event.name, event.date, event.href])
                    seen.add((event.name, event.date, event.href))


def extract_and_categorize():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    events = soup.find_all("a", href=True)
    events_dict = {}

    for event in events:
        year_tag = event.find("div", attrs={"data-year": True})
        if not year_tag or year_tag["data-year"] != "2025":
            continue

        name_tag = event.find("h4")
        name = name_tag.get_text(strip=True) if name_tag else "Unknown Event"

        date_tag = event.find("time")
        date = date_tag.get_text(strip=True) if date_tag else "Unknown Date"
        href = event.get("href", "Unknown Link")

        name_lower = name.lower()
        if "cadet" in name_lower:
            category = "Cadets"
        elif "junior" in name_lower:
            category = "Juniors"
        elif any(word in name_lower for word in ["senior", "open", "grand slam", "masters", "grand prix"]):
            category = "Seniors"
        elif "veteran" in name_lower:
            category = "Veterans"
        else:
            category = "Other"

        if category not in events_dict:
            events_dict[category] = []

        events_dict[category].append(Competition(name, date, href))

    return events_dict


def get_comp_data_category():
    competition = input("Enter the competition name: ")
    weight = input("Enter the weight category -/+ and  number for example -> -81: ")
    found = False
    cdate = ""
    chref = ""
    with open("events2025.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if competition.lower() in row["Event Name"].lower():
                print(f"Category: {row['Category']} | Event: {row['Event Name']} | Date: {row['Date']}")
                cdate = row["Date"]
                found = True
                chref = row["Link"]

    if not found:
        print("No matching event found.")
        return
    
    time.sleep(2)

    month = cdate[:3]
    button = driver.find_element(By.XPATH, f"//button[text()='{month}']")
    button.click()

    time.sleep(2)
    chref = chref.rsplit('/', 1)[0]
    competition_url = "https://judotv.com" + chref + "/judoka"
    
    driver.get(competition_url)

    time.sleep(3)

    find = driver.find_element(By.XPATH, "//button[@aria-label='Select country'][span[text()='Select country'] or span[text()='Latvia']]")
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

    weight+=' kg'
    find = driver.find_element(By.XPATH, f"//li[@role='menuitem']//span[starts-with(text(), '{weight}')]")
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

            print(f"Name Surname, Country: {name} {surname}, {country_code}")
        except Exception as e:
            print(f"Error extracting data: {e}")


def get_ranked_players():
    competition = input("Enter the competition name: ")
    found = False
    cdate = ""
    chref = ""
    with open("events2025.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if competition.lower() in row["Event Name"].lower():
                print(f"Category: {row['Category']} | Event: {row['Event Name']} | Date: {row['Date']}")
                cdate = row["Date"]
                found = True
                chref = row["Link"]

    if not found:
        print("No matching event found.")
        return
    
    time.sleep(2)

    month = cdate[:3]
    button = driver.find_element(By.XPATH, f"//button[text()='{month}']")
    button.click()

    time.sleep(2)
    chref = chref.rsplit('/', 1)[0]
    competition_url = "https://judotv.com" + chref + "/judoka"
    
    driver.get(competition_url)

    time.sleep(3)

    find = driver.find_element(By.XPATH, "//button[@aria-label='Select country'][span[text()='Select country'] or span[text()='Latvia']]")
    find.click()

    time.sleep(2)

    find = driver.find_element(By.XPATH, "(//li[contains(@role, 'menuitem')])[1]")
    find.click()

    time.sleep(1)

    find = driver.find_element(By.XPATH, "//button[.//span[text()='View all']]")
    find.click()

    time.sleep(2)

    competitors = driver.find_elements(By.XPATH, "//a[contains(@href, '/judoka/')]")

    for c in competitors[:10]:  # Only first 10 competitors
        try:
            # Get full name
            name_div = c.find_element(By.XPATH, ".//div[contains(@class, 'font-medium inline')]")
            full_name = name_div.text.strip()
            parts = full_name.split()
            name = " ".join(parts[:-1])
            surname = parts[-1]

            # Get country code
            country_code = c.find_element(By.XPATH, ".//div[contains(@class, 'text-center') and contains(@class, 'text-xs')]").text.strip()

            # Get world ranking
            rank_elem = c.find_element(By.XPATH, ".//div[contains(@class, 'text-primary-75') and contains(text(), '#')]")
            world_rank = rank_elem.text.strip().replace("#", "")

            print(f"Name Surname, Country: #{world_rank} {name} {surname}, {country_code}")

        except Exception as e:
            print(f"Error extracting data: {e}")


def get_country_list():
    competition = input("Enter the competition name: ")
    found = False
    cdate = ""
    chref = ""

    # Read CSV for event matching
    with open("events2025.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if competition.lower() in row["Event Name"].lower():
                print(f"Category: {row['Category']} | Event: {row['Event Name']} | Date: {row['Date']}")
                cdate = row["Date"]
                found = True
                chref = row["Link"]

    if not found:
        print("No matching event found.")
        return

    time.sleep(2)

    month = cdate[:3]
    button = driver.find_element(By.XPATH, f"//button[text()='{month}']")
    button.click()

    time.sleep(2)

    # Prepare competition URL
    chref = chref.rsplit('/', 1)[0]
    competition_url = "https://judotv.com" + chref + "/judoka"
    driver.get(competition_url)
    time.sleep(3)

    # Open the country selector dropdown
    find = driver.find_element(By.XPATH, "//button[@aria-label='Select country'][span[text()='Select country'] or span[text()='Latvia']]")
    find.click()
    time.sleep(2)

    # Parse HTML after dropdown opens
    soup = BeautifulSoup(driver.page_source, "html.parser")
    country_elements = soup.find_all("li", {"role": "menuitem"})

    # Extract and print country names
    countries = [li.find("span", class_="mr-2 w-full text-lg font-medium").text.strip() for li in country_elements]
    for country in countries:
        print(country)
    
    time.sleep(1)

    find = driver.find_element(By.XPATH, "(//li[contains(@role, 'menuitem')])[1]")
    find.click()

    time.sleep(1)

    # Now click the "View all" button
    find = driver.find_element(By.XPATH, "//button[.//span[text()='View all']]")
    find.click()

    time.sleep(2)
        
main()


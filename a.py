from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Set up Firefox options (optional)
options = Options()
options.headless = True  # Set to True to run in headless mode (without GUI)

# Specify the path to GeckoDriver
service = Service('/snap/bin/geckodriver')  # Update this path if necessary

# Initialize the Firefox driver
driver = webdriver.Firefox(service=service, options=options)

# Open a website
driver.get('http://130.44.100.86:5500/home.html')

# Print the page title
print(driver.title)

# Locate the search box by its name attribute
search_box = driver.find_element(By.ID, 'usrName')  # 'q' is the name attribute for the Google search box
button = driver.find_element(By.ID, 'loginBttn')  # or use other locators like By.ID or By.XPATH

# Interact with the search box
# button.click()
search_box.send_keys('bot_on')  # Type a search query
# search_box.send_keys(Keys.RETURN)  # Press Enter

time.sleep(1) #seconds

# Close the browser
driver.quit()
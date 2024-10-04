from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import threading
import runpy

#Color
# Color for console output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ELSE = "\033[95m"
RESET = "\033[0m"

def printr(text):
    print(f"{RED}{text}{RESET}")
    
def prints(text):
    print(f"{ELSE}{text}{RESET}")

def printy(text):
    print(f"{YELLOW}{text}{RESET}")


def printg(text):
    print(f"{GREEN}{text}{RESET}")


# Define the proxy
i = 0

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]  # Return all non-empty lines

proxies = load_proxies('proxy_list.txt')

#print("************************")

print(proxies)
print(" ")
#print("************************")



options = Options()
options.headless = True  # Set to True to run in headless mode (without GUI)

# Specify the path to GeckoDriver
service = Service('/snap/bin/geckodriver')  # Update this path if necessary


def set_firefox_proxy(proxy_ip_port):
    options = FirefoxOptions()
    options.set_preference('network.proxy.type', 1)  # Manual proxy configuration
    options.set_preference('network.proxy.http', proxy_ip_port.split(':')[0])  # Proxy IP
    options.set_preference('network.proxy.http_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port
    options.set_preference('network.proxy.ssl', proxy_ip_port.split(':')[0])  # Proxy IP for HTTPS
    options.set_preference('network.proxy.ssl_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port for HTTPS
    service = FirefoxService('/snap/bin/geckodriver')  # Path to your GeckoDriver
    return webdriver.Firefox(service=service, options=options)


# Function to perform actions with the proxy
def attempt_connection(proxy, max_attempt_time):
    #driver = None
    try:
        driver = set_firefox_proxy(proxy)
        
        # Start timing the attempt
        start_time = time.time()

        # Load the page with timeout
        driver.get('http://130.44.100.86:5500/home.html')

        # Wait for a specific element
        WebDriverWait(driver, max_attempt_time).until(
            EC.presence_of_element_located((By.ID, 'usrName'))
        )

        # Perform some action if loaded successfully
        printg(f"[+] Bot: {proxy} Connected")
        
        button = driver.find_element(By.ID, 'loginBttn')
        search_box = driver.find_element(By.ID, 'usrName')
        time.sleep(1)
        #printg(f"[!] Bot: {proxy} Page Loaded")
        search_box.send_keys('bot_on')
        button.click()
        prints(f"[#] Bot: {proxy} Action Performed")
    except Exception as e:
        printr(f"[!] Bot: {proxy} Failed to Connect.")
    finally:
        # Ensure the driver quits
        if driver:
            driver.quit()

# Function to run a proxy connection attempt with timeout
def run_with_timeout(proxy, max_attempt_time):
    thread = threading.Thread(target=attempt_connection, args=(proxy, max_attempt_time))
    thread.start()
    thread.join(timeout=max_attempt_time)

    if thread.is_alive() == 0:
        printr(f"[!] Bot: {proxy} Failed To Connect. Timed Out ({max_attempt_time} seconds)")
        driver = set_firefox_proxy(proxy)
        driver.quit()
        return False
    return True

# Main function to iterate over proxies
def connect_with_proxies(browser, max_attempt_time=4):
    proxy_file = 'proxy_list.txt'
    proxies = load_proxies(proxy_file)
    
    if not proxies:
        printr("[!] Proxy list format error. Ex: proxyip.com:8080")
        return

    for proxy in proxies:
        printy(f"[%] Bot: {proxy} Connecting")
        time.sleep(1)
        # Run the connection attempt with timeout
        success = run_with_timeout(proxy, max_attempt_time)
        if not success:
            driver = set_firefox_proxy(proxy)
            driver.quit()
            continue  # Skip to the next proxy if this one timed out

# Example usage
connect_with_proxies(browser="firefox", max_attempt_time=3)
#Close
#time.sleep(300)
#driver.quit()
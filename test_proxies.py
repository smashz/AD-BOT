from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import threading
import time

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


# Function to load proxies from a file
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]  # Return all non-empty lines

# Set up Firefox options
def set_firefox_proxy(proxy_ip_port):
    options = Options()
    options.headless = True  # Set to True to run in headless mode (without GUI)
    
    # Configure proxy settings
    options.set_preference('network.proxy.type', 1)  # Manual proxy configuration
    options.set_preference('network.proxy.http', proxy_ip_port.split(':')[0])  # Proxy IP
    options.set_preference('network.proxy.http_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port
    options.set_preference('network.proxy.ssl', proxy_ip_port.split(':')[0])  # Proxy IP for HTTPS
    options.set_preference('network.proxy.ssl_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port for HTTPS
    
    service = Service('/snap/bin/geckodriver')  # Path to your GeckoDriver
    return webdriver.Firefox(service=service, options=options)

# Function to connect using a specific proxy
def connect_proxy(proxy, wait_time):
    prints(f"Testing Proxy: {proxy}")
    driver = set_firefox_proxy(proxy)

    try:
        driver.get('https://httpbin.org/ip')  # Check public IP
        # Wait for the page to load
        if driver.execute_script("return document.readyState") == "complete":
            printg(f"Proxy: {proxy} Worked")
        else:
            printr(f"Proxy: {proxy} Failed: Page did not load in time")
            driver.quit()
    except Exception as e:
        printr(f"Proxy: {proxy} Failed: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed regardless of success or failure

# Main function to connect with proxies
def connect_with_proxies(browser="firefox", wait_time=4):
    proxy_file = 'proxy_list.txt'  # Replace with your file name
    proxies = load_proxies(proxy_file)

    if not proxies:
        print("Format Error. ex: (proxyip.com:8080)")
        return

    for proxy in proxies:
        # Create a thread for the connection attempt
        thread = threading.Thread(target=connect_proxy, args=(proxy, wait_time))
        thread.start()  # Start the thread
        thread.join(timeout=wait_time)  # Wait for the thread to complete or timeout
        
        # If the thread is still alive, it means it exceeded wait_time
        if thread.is_alive():
            printr(f"Proxy: {proxy} Failed: Connection timed out after {wait_time} seconds")
            continue
            # No need for driver.quit() here as it's handled in connect_proxy()

# Example usage
connect_with_proxies(browser="firefox", wait_time=15)  # Wait for 4 seconds before each connection attempt
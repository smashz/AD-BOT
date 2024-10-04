from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os





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

# File Creation
# File path for the list
file_path = 'proxy_list.txt'

# Check if the file already exists
if os.path.exists(file_path):
    # If it exists, clear its content by opening it in write mode
    printy(f"[\] Clearing List File '{file_path}' Content.")
    with open(file_path, 'w') as file:
        pass  # This will just clear the file
else:
    # If it doesn't exist, create a new file by opening in write mode
    printg(f"[+] Generating List File '{file_path}'.")
    with open(file_path, 'w') as file:
        pass  # This will create an empty file


# Set up Firefox options (optional)
options = Options()
options.headless = True  # Set to True to run in headless mode (without GUI)
def set_firefox_proxy(proxy_ip_port):
    
    # Configure proxy settings
    options.set_preference('network.proxy.type', 1)  # Manual proxy configuration
    options.set_preference('network.proxy.http', proxy_ip_port.split(':')[0])  # Proxy IP
    options.set_preference('network.proxy.http_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port
    options.set_preference('network.proxy.ssl', proxy_ip_port.split(':')[0])  # Proxy IP for HTTPS
    options.set_preference('network.proxy.ssl_port', int(proxy_ip_port.split(':')[1]))  # Proxy Port for HTTPS
    
    service = Service('/snap/bin/geckodriver')  # Path to your GeckoDriver
    return webdriver.Firefox(service=service, options=options)

# Specify the path to GeckoDriver
service = Service('/snap/bin/geckodriver')  # Update this path if necessary

# Initialize the Firefox driver
driver = webdriver.Firefox(service=service, options=options)

# Open a website
driver.get('https://free-proxy-list.net/')

# Print the page title
#prints(driver.title)
printy("[+] Extracting Proxies")

time.sleep(3) #seconds


# Find the table element by its ID
table = driver.find_element(By.CLASS_NAME, 'table-responsive')

# Extract the headers (if you want them)
# Find all headers (by <th> tag)
headers = table.find_elements(By.TAG_NAME, 'th')
# Extract and clean up the header text

# List of desired headers to extract
desired_headers = ["IP Address", "Port"]  # Change this to match your desired headers

# Filter and get the text for only the desired headers
filtered_headers = [header.text for header in headers if header.text in desired_headers]

# Map the headers to their column indices
header_texts = [header.text.strip() for header in headers]
desired_indices = [i for i, header in enumerate(header_texts) if header in desired_headers]
https_index = header_texts.index("Https")  # Get index of the Https column


# Print the filtered headers
prints(desired_headers)
# Extract the rows from the table body
rows = table.find_elements(By.TAG_NAME, 'tr')

# Open a text file to save the data
with open(file_path, 'w') as file:
    # Iterate over rows and extract data from each cell
    printy("[+] Grabbing Proxies")
    for row in rows[1:]:  # Skip the header row
        # Get all cells (by <td> tag)
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        # Extract the data from only the desired columns
        if len(cells) >= max(desired_indices) + 1:  # Ensure row has enough cells
            selected_columns = [cells[i].text for i in desired_indices]
            
            # Check if the 'Https' column is 'yes'
            https_value = cells[https_index].text.strip().lower()  # Get the 'Https' value
            if https_value == 'yes':
                # Join the selected columns with colon (:) and write to the file (without the Https column)
                row_data = ':'.join(selected_columns).strip()
                
                if row_data:  # Only write non-empty rows
                    file.write(row_data + '\n')
                    printg(f"[+] Extracted: {row_data}")
            else:
                printr(f"[-] HTTP Proxy: {selected_columns[0]}") # printr(f"[-] HTTP Proxy: {selected_columns[0]} (Https: {https_value})")

      

printg("[+] List Generated")



time.sleep(1)
# Close the browser
driver.quit()
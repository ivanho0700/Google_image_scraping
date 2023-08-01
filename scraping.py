from selenium import webdriver
import urllib.request
from time import sleep
from selenium.common.exceptions import WebDriverException
import os

driver = webdriver.Chrome()

with open('sameplekeywords.txt', 'r') as file:
    rows = file.readlines()

is_first_row = True
for row in rows:
    if not is_first_row:
        driver.execute_script("window.open('https://www.google.com', '_blank');")
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[-1])
    is_first_row = False

    search_query = row.strip()
    num_images = 20

    url = f"https://www.google.com/search?q={search_query}&source=lnms&tbm=isch"
    driver.get(url)

    # Execute JavaScript code to get the image elements
    image_elements = driver.execute_script('return document.querySelectorAll("img[jsname*=\'Q4LuWd\']");')

    # Extract the image URLs from the elements
    image_urls = []
    for i, element in enumerate(image_elements[:num_images]):
        src = element.get_attribute('src')
        print(src)
        image_urls.append(src)

    # Download the images
    if not os.path.exists(search_query):
        os.mkdir(search_query)

    for i, url in enumerate(image_urls):
        urllib.request.urlretrieve(url, f"{search_query}\\image_{i}.jpg")
    
try:
    # Continuously check if the browser window is closed
    while True:
        try:
            # Check if the browser is still open by accessing a property (e.g., title)
            _ = driver.title
            sleep(10)
        except WebDriverException:
            # Browser window is closed, break out of the loop and quit the script
            print("INFO: Browser window is closed.")
            break

finally:
    # Quit the browser and end the script process
    driver.quit()
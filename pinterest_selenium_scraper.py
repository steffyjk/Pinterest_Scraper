import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()
# Directory path for saving images
output_dir = "/home/root380/Desktop/STEFFY_GITHUB/scrapping/Pinterest_Scraper/OUTPUTS"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://in.pinterest.com/login/")
time.sleep(2)
driver.find_element(By.ID, "email").send_keys(os.getenv("PINTEREST_EMAIL_ID"))
driver.find_element(By.ID, "password").send_keys(os.getenv("PINTEREST_PASSWORD"), Keys.ENTER)

time.sleep(2)
from selenium.webdriver.support.ui import WebDriverWait

wait = WebDriverWait(driver, 10)
image_tags = driver.find_elements(By.TAG_NAME, "img")
for image_tag in image_tags:
    try:
        src_value = image_tag.get_attribute("src")
        print(src_value)

        # Download the image using requests
        response = requests.get(src_value)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = src_value.split("/")[-1]

            # Save the image to the output directory
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {file_path}")
        else:
            print("Failed to download image.")

    except Exception as e:
        print(f"Exception occurred: {e}")
        continue

# Close the browser
driver.quit()

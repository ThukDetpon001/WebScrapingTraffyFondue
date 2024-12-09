from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime

# สร้างโฟลเดอร์ใหม่ตามวันที่ปัจจุบัน
today_date = datetime.now().strftime('%d-%m-%y')  # วันที่ปัจจุบันในรูปแบบ "6-12-67"
base_folder = f"{today_date}"
os.makedirs(base_folder, exist_ok=True)

# กำหนดเส้นทางไฟล์ที่ใช้ในโครงการ
output_file = os.path.join(base_folder, 'traffy_data.csv')
output_file_with_days = os.path.join(base_folder, 'traffy_data_มีจำนวนวัน.csv')
agency_counts_file = os.path.join(base_folder, 'จำนวนในแต่ละเขต.csv')
output_dir_split = os.path.join(base_folder, 'แยกตามเขตรับผิดชอบ')
os.makedirs(output_dir_split, exist_ok=True)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use webdriver-manager to install and manage ChromeDriver automatically
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL to scrape
url = "https://bangkok.traffy.in.th/"

try:
    # Fetch the webpage
    driver.get(url)

    # Click the "รอรับเรื่อง" button to filter data
    try:
        wait = WebDriverWait(driver, 10)
        filter_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'รอรับเรื่อง')]/ancestor::div[@class='container-start']"))
        )
        filter_button.click()
        print("Clicked 'รอรับเรื่อง' filter button.")
        time.sleep(2)
    except Exception as e:
        print("Error clicking 'รอรับเรื่อง' button:", e)
        driver.quit()
        exit()

    # Wait for the page to load filtered data
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "containerData")))

    # Scroll to load more data
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    max_attempts = 100

    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # ลดเวลารอในแต่ละรอบ
        new_height = driver.execute_script("return document.body.scrollHeight")

        loaded_elements = len(driver.find_elements(By.CLASS_NAME, "containerData"))
        print(f"Scroll attempt {attempts + 1}: Loaded elements = {loaded_elements}")

        if new_height == last_height:
            print("No more elements to load.")
            break
        last_height = new_height
        attempts += 1

    # Fetch HTML content
    html = driver.page_source

except Exception as e:
    print(f"Error loading webpage: {e}")
    driver.quit()
    exit()

# เขียนข้อมูลลงในไฟล์ CSV
with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow([
        'ticket_id', 'date', 'time', 'status', 'address',
        'description', 'agency', 'category', 'ForwardedStatus',
        'ForwardedDate', 'ForwardedTime', 'TakeTime'
    ])

    def extract_data_with_details(html, driver, limit=1000):
        soup = BeautifulSoup(html, 'html.parser')

        for idx, container in enumerate(soup.find_all("div", class_="containerData")):
            if idx >= limit:
                break
            try:
                ticket_id_elem = container.find("p", class_="ticket_id")
                detail_time_elems = container.find_all("p", class_="detailTimes")
                status_elem = container.find("p", class_="title-state")
                address_elem = container.find("p", class_="detailTimes address")
                category_elem = container.find("div", class_="tags-problemType").p

                ticket_id = ticket_id_elem.get_text(strip=True) if ticket_id_elem else 'N/A'
                detail_time = detail_time_elems[1].get_text(strip=True) if len(detail_time_elems) > 1 else 'N/A'
                status = status_elem.get_text(strip=True) if status_elem else 'N/A'
                address = address_elem.get_text(strip=True) if address_elem else 'N/A'
                category = category_elem.get_text(strip=True) if category_elem else 'N/A'

                if 'รอรับเรื่อง' in status:
                    if ' ' in detail_time:
                        parts = detail_time.rsplit(' ', 2)
                        date = parts[0]
                        time = f"{parts[1]} {parts[2]}" if len(parts) > 2 else 'N/A'
                    else:
                        date = 'N/A'
                        time = 'N/A'

                    agency = 'N/A'
                    description = 'N/A'
                    ForwardedStatus = 'N/A'
                    ForwardedDate = 'N/A'
                    ForwardedTime = 'N/A'
                    TakeTime = 'N/A'

                    # Fetch and process detail data
                    try:
                        detail_url = f"https://bangkok.traffy.in.th/detail?ticketID={ticket_id}"
                        driver.get(detail_url)
                        # Processing detail data logic...

                    except Exception as e:
                        print(f"Error fetching details for ticket {ticket_id}: {e}")

                    # Write to CSV
                    writer.writerow([
                        ticket_id, date, time, status, address,
                        description, agency, category, ForwardedStatus,
                        ForwardedDate, ForwardedTime, TakeTime
                    ])

            except Exception as e:
                print(f"Error extracting data from container: {e}")

    # Extract data
    extract_data_with_details(html, driver, limit=1000)

# Close driver
driver.quit()
print(f"Data saved to {output_file}")

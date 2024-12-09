# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time
# import pandas as pd

# # Setup Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# # Use webdriver-manager to install and manage ChromeDriver automatically
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# # URL to scrape
# url = "https://bangkok.traffy.in.th/"

# try:
#     # Fetch the webpage
#     driver.get(url)

#     # Click the "รอรับเรื่อง" button to filter data
#     try:
#         wait = WebDriverWait(driver, 10)
#         filter_button = wait.until(
#             EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'รอรับเรื่อง')]/ancestor::div[@class='container-start']"))
#         )
#         filter_button.click()
#         print("Clicked 'รอรับเรื่อง' filter button.")
#         time.sleep(2)  # Wait for data to load after clicking the button
#     except Exception as e:
#         print("Error clicking 'รอรับเรื่อง' button:", e)
#         driver.quit()
#         exit()

#         # Click the "ดำเนินการ" button to filter data
#     # try:
#     #     wait = WebDriverWait(driver, 10)
#     #     filter_button = wait.until(
#     #         EC.element_to_be_clickable((By.XPATH, "//div[@class='container-inprogress']/div[@style='display: flex; gap: 0.2rem; align-items: center;']/p[@class='name-state' and contains(text(), 'ดำเนินการ')]"))
#     #     )
#     #     filter_button.click()
#     #     print("Clicked 'ดำเนินการ' filter button.")
#     #     time.sleep(2)  # Wait for data to load after clicking the button
#     # except Exception as e:
#     #     print("Error clicking 'ดำเนินการ' button:", e)
#     #     driver.quit()
#     #     exit()

#         # Click the "ส่งต่อ" button to filter data
#     # try:
#     #     wait = WebDriverWait(driver, 10)
#     #     filter_button = wait.until(
#     #         EC.element_to_be_clickable((By.XPATH, "//div[@class='container-forward']/div[@style='display: flex; gap: 0.2rem; align-items: center;']/p[@class='name-state' and contains(text(), 'ส่งต่อ')]"))
#     #     )
#     #     filter_button.click()
#     #     print("Clicked 'ส่งต่อ' filter button.")
#     #     time.sleep(2)  # Wait for data to load after clicking the button
#     # except Exception as e:
#     #     print("Error clicking 'ส่งต่อ' button:", e)
#     #     driver.quit()
#     #     exit()

#     # Wait for the page to load filtered data
#     WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "containerData")))

#     # Scroll to load more data
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     attempts = 0
#     max_attempts = 100  # Set a maximum number of scroll attempts

#     while attempts < max_attempts:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for new data to load
#         new_height = driver.execute_script("return document.body.scrollHeight")

#         # Debugging: Print the number of loaded elements
#         loaded_elements = len(driver.find_elements(By.CLASS_NAME, "containerData"))
#         print(f"Scroll attempt {attempts + 1}: Loaded elements = {loaded_elements}")

#         if new_height == last_height:
#             print("No more elements to load.")
#             break
#         last_height = new_height
#         attempts += 1

#     # Fetch HTML content
#     html = driver.page_source

# except Exception as e:
#     print(f"Error loading webpage: {e}")
#     driver.quit()
#     exit()


# # Function to extract data from HTML
# # def extract_data_with_details(html, driver): #Unlimit
# def extract_data_with_details(html, driver, limit=1000):
#     soup = BeautifulSoup(html, 'html.parser')
#     data_list = []
# #    for container in soup.find_all("div", class_="containerData"): #Unlimit
#     for idx, container in enumerate(soup.find_all("div", class_="containerData")):
#         if idx >= limit:
#             break
#         try:
#             ticket_id_elem = container.find("p", class_="ticket_id")
#             detail_time_elems = container.find_all("p", class_="detailTimes")
#             status_elem = container.find("p", class_="title-state")
#             address_elem = container.find("p", class_="detailTimes address")
#             category_elem = container.find("div", class_="tags-problemType").p

#             ticket_id = ticket_id_elem.get_text(strip=True) if ticket_id_elem else 'N/A'
#             detail_time = detail_time_elems[1].get_text(strip=True) if len(detail_time_elems) > 1 else 'N/A'
#             status = status_elem.get_text(strip=True) if status_elem else 'N/A'
#             address = address_elem.get_text(strip=True) if address_elem else 'N/A'
#             category = category_elem.get_text(strip=True) if category_elem else 'N/A'

#             # Filter only items with status
#             if 'รอรับเรื่อง' in status:
#             # if 'ดำเนินการ' in status:
#             # if 'ส่งต่อ' in status:
#                 # Extract date and time directly
#                 if ' ' in detail_time:
#                     parts = detail_time.rsplit(' ', 2)  # Split from the right
#                     date = parts[0]  # "27 พ.ย. 67"
#                     time = f"{parts[1]} {parts[2]}" if len(parts) > 2 else 'N/A'  # "09:21 น."
#                 else:
#                     date = 'N/A'
#                     time = 'N/A'

#                 # Fetch additional details (agency and description) from ticket detail page
#                 agency = 'N/A'
#                 description = 'N/A'
#                 ForwardedStatus = 'N/A'
#                 ForwardedDate = 'N/A'
#                 ForwardedTime = 'N/A'
#                 TakeTime = 'N/A'
#                 try:
#                     detail_url = f"https://bangkok.traffy.in.th/detail?ticketID={ticket_id}"
#                     driver.get(detail_url)

#                     # Fetch agency
#                     try:
#                         comment_element = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.CLASS_NAME, "txt-comment"))
#                         )
#                         spans = comment_element.find_elements(By.TAG_NAME, "span")
#                         agency_info = " ".join([span.text.strip() for span in spans if span.text.strip()])
#                         county2_info = " ".join([span.text.strip() for span in driver.find_elements(By.XPATH, "//span[@style='color: rgba(0, 0, 0, 0.5);']")])
#                         county1_info = " ".join([span.text.strip() for span in driver.find_elements(By.XPATH, "//span[@style='color: inherit;']")])

#                         agency = f"{county1_info} {county2_info} {agency_info}".strip()
#                     except Exception as e:
#                         print(f"Error fetching details for ticket {ticket_id}: {e}")

#                     # Fetch description
#                     try:
#                         comment_element = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.CLASS_NAME, "txt-comment"))
#                         )
#                         description = comment_element.text.strip() if comment_element else 'N/A'
#                     except Exception as e:
#                         print(f"Description not found for ticket {ticket_id}: {e}")

#                     # Fetch detail
#                     try:
#                         timeline_element = driver.find_element(By.CLASS_NAME, "div-timeline-main")
#                         if timeline_element:
#                             ForwardedStatus = timeline_element.find_element(By.CLASS_NAME, "timeline-status").text.strip()
#                             ForwardedDate = timeline_element.find_elements(By.CLASS_NAME, "timeline-detail-time")[0].text.strip()
#                             ForwardedTime = timeline_element.find_elements(By.CLASS_NAME, "timeline-detail-time")[1].text.strip()
#                             # ใช้ XPath เพื่อดึงค่า TakeTime ที่มีข้อความ "ใช้เวลา"
#                             take_time_elements = timeline_element.find_elements(By.XPATH, ".//p[contains(@class, 'timeline-detail-txt') and contains(text(), 'ใช้เวลา')]")
#                             TakeTime = take_time_elements[0].text.strip() if take_time_elements else 'รอรับเรื่อง'
#                     except Exception as e:
#                         print(f"Error fetching details for ticket {ticket_id}: {e}")

#                 except Exception as e:
#                     print(f"Error fetching details for ticket {ticket_id}: {e}")

#                 data_list.append({
#                     'ticket_id': ticket_id,
#                     'date': date,
#                     'time': time,
#                     'status': status,
#                     'address': address,
#                     'description': description,
#                     'agency': agency,
#                     'category': category,
#                     'ForwardedStatus': ForwardedStatus,
#                     'ForwardedDate': ForwardedDate,
#                     'ForwardedTime': ForwardedTime,
#                     'TakeTime': TakeTime
#                 })
#         except Exception as e:
#             print(f"Error extracting data from container: {e}")

#     return data_list

# # Function to save data to a CSV file
# def save_to_csv(data_list, filename='output.csv'):
#     # Convert the list of dictionaries to a pandas DataFrame
#     df = pd.DataFrame(data_list)
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename, index=False, encoding='utf-8-sig')
#     print(f"Data has been saved to {filename}")
    
# # Main program
# # data_list = extract_data_with_details(html, driver)  # No limit on data
# data_list = extract_data_with_details(html, driver, limit=1000)

# save_to_csv(data_list, 'traffy_data.csv')

# # Display extracted data
# for idx, data in enumerate(data_list, start=1):  # start=1 to begin count from 1
#     print(f"Record {idx}:")
#     print(f"  Ticket ID: {data['ticket_id']}")
#     print(f"  Date: {data['date']}")
#     print(f"  Time: {data['time']}")
#     print(f"  Status: {data['status']}")
#     print(f"  Address: {data['address']}")
#     print(f"  Description: {data['description']}")
#     print(f"  Agency: {data['agency']}")
#     print(f"  Category: {data['category']}")
#     print(f"  Forwarded Status: {data['ForwardedStatus']}")
#     print(f"  Forwarded Date: {data['ForwardedDate']}")
#     print(f"  Forwarded Time: {data['ForwardedTime']}")
#     print(f"  Take Time: {data['TakeTime']}")
#     print("-" * 40)  # Separator for readability

# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
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
        time.sleep(2)  # Wait for data to load after clicking the button
    except Exception as e:
        print("Error clicking 'รอรับเรื่อง' button:", e)
        driver.quit()
        exit()

    # Wait for the page to load filtered data
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "containerData")))

    # Scroll to load more data
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    max_attempts = 100  # Set a maximum number of scroll attempts

    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new data to load
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

# Open CSV file for writing
output_file = 'traffy_data.csv'
with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Write header row
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

                    try:
                        detail_url = f"https://bangkok.traffy.in.th/detail?ticketID={ticket_id}"
                        driver.get(detail_url)

                        try:
                            comment_element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "txt-comment"))
                            )
                            spans = comment_element.find_elements(By.TAG_NAME, "span")
                            agency_info = " ".join([span.text.strip() for span in spans if span.text.strip()])
                            county2_info = " ".join([span.text.strip() for span in driver.find_elements(By.XPATH, "//span[@style='color: rgba(0, 0, 0, 0.5);']")])
                            county1_info = " ".join([span.text.strip() for span in driver.find_elements(By.XPATH, "//span[@style='color: inherit;']")])
                            agency = f"{county1_info} {county2_info} {agency_info}".strip()
                        except:
                            pass

                        # try:
                        #     comment_element = WebDriverWait(driver, 10).until(
                        #         EC.presence_of_element_located((By.CLASS_NAME, "txt-comment"))
                        #     )
                        #     county1_elements = driver.find_elements(By.XPATH, "//span[@style='color: inherit;']")
                        #     # ดึงข้อมูลและลบเครื่องหมาย ',' ออก
                        #     county1_info = " ".join([element.text.strip().replace(",", "") for element in county1_elements if element.text.strip()])
                        #     agency = county1_info  # หากต้องการใช้ county1_info เป็น agency
                        # except Exception as e:
                        #     print(f"Error fetching county1_info: {e}")
                        #     county1_info = "N/A"
                        #     agency = county1_info


                        try:
                            comment_element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "txt-comment"))
                            )
                            description = comment_element.text.strip() if comment_element else 'N/A'
                        except:
                            pass

                        try:
                            timeline_element = driver.find_element(By.CLASS_NAME, "div-timeline-main")
                            if timeline_element:
                                ForwardedStatus = timeline_element.find_element(By.CLASS_NAME, "timeline-status").text.strip()
                                ForwardedDate = timeline_element.find_elements(By.CLASS_NAME, "timeline-detail-time")[0].text.strip()
                                ForwardedTime = timeline_element.find_elements(By.CLASS_NAME, "timeline-detail-time")[1].text.strip()
                                take_time_elements = timeline_element.find_elements(By.XPATH, ".//p[contains(@class, 'timeline-detail-txt') and contains(text(), 'ใช้เวลา')]")
                                TakeTime = take_time_elements[0].text.strip() if take_time_elements else 'รอรับเรื่อง'
                        except:
                            pass

                    except Exception as e:
                        print(f"Error fetching details for ticket {ticket_id}: {e}")

                    # Write data directly to CSV
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

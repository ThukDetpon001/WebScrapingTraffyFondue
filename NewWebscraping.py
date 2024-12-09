import os
from datetime import datetime
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
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Create a dynamic folder name based on current date (Thai Buddhist Era)
def get_thai_date_folder():
    now = datetime.now()
    thai_year = now.year + 543
    folder_name = now.strftime(f"{now.day}-{now.month}-{str(thai_year)[2:]}")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# Create dynamic folder
OUTPUT_FOLDER = get_thai_date_folder()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use webdriver-manager to install and manage ChromeDriver automatically
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL to scrape
url = "https://bangkok.traffy.in.th/"

try:
    driver.get(url)
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

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "containerData")))

    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    max_attempts = 100

    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        loaded_elements = len(driver.find_elements(By.CLASS_NAME, "containerData"))
        print(f"Scroll attempt {attempts + 1}: Loaded elements = {loaded_elements}")

        if new_height == last_height:
            print("No more elements to load.")
            break
        last_height = new_height
        attempts += 1

    html = driver.page_source

except Exception as e:
    print(f"Error loading webpage: {e}")
    driver.quit()
    exit()

output_file = os.path.join(OUTPUT_FOLDER, 'traffy_data.csv')
with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow([
        'ticket_id', 'date', 'time', 'status', 'address',
        'description', 'agency', 'category', 'ForwardedStatus',
        'ForwardedDate', 'ForwardedTime', 'TakeTime'
    ])

    def fetch_ticket_details(ticket_id, driver):
        try:
            detail_url = f"https://bangkok.traffy.in.th/detail?ticketID={ticket_id}"
            driver.get(detail_url)
            agency, description, ForwardedStatus, ForwardedDate, ForwardedTime, TakeTime = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
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

            return [description, agency, ForwardedStatus, ForwardedDate, ForwardedTime, TakeTime]
        except Exception as e:
            print(f"Error fetching details for ticket {ticket_id}: {e}")
            return ['N/A'] * 6

    soup = BeautifulSoup(html, 'html.parser')
    MAX_EXECUTION_TIME = 300
    start_time = time.time()
    limit = 500

    for idx, container in enumerate(soup.find_all("div", class_="containerData")):
        if idx >= limit or (time.time() - start_time) > MAX_EXECUTION_TIME:
            print("Stopped execution due to limit or timeout.")
            break

        try:
            ticket_id_elem = container.find("p", class_="ticket_id")
            status_elem = container.find("p", class_="title-state")
            ticket_id = ticket_id_elem.get_text(strip=True) if ticket_id_elem else 'N/A'
            status = status_elem.get_text(strip=True) if status_elem else 'N/A'

            if 'รอรับเรื่อง' not in status:
                continue

            with ThreadPoolExecutor(max_workers=5) as executor:
                details = executor.submit(fetch_ticket_details, ticket_id, driver).result()

            writer.writerow([ticket_id, *details])

        except Exception as e:
            print(f"Error extracting data from container: {e}")

driver.quit()
print(f"Data saved to {output_file}")

# โหลดไฟล์ CSV พร้อมกำหนด encoding เพื่อรองรับภาษาไทย
file_path = output_file
output_path = os.path.join(OUTPUT_FOLDER, 'traffy_data_มีจำนวนวัน.csv')

data = pd.read_csv(file_path, encoding='utf-8')

# แผนที่เดือนภาษาไทยเป็นตัวเลข
thai_months = {
    'ม.ค.': '01', 'ก.พ.': '02', 'มี.ค.': '03', 'เม.ย.': '04',
    'พ.ค.': '05', 'มิ.ย.': '06', 'ก.ค.': '07', 'ส.ค.': '08',
    'ก.ย.': '09', 'ต.ค.': '10', 'พ.ย.': '11', 'ธ.ค.': '12'
}

# ฟังก์ชันแปลงวันที่ภาษาไทยเป็นรูปแบบ ISO
def convert_thai_date(thai_date):
    try:
        # ปรับรูปแบบวันที่ให้แยกด้วยช่องว่าง
        day, thai_month, thai_year = thai_date.split()
        month = thai_months.get(thai_month.strip(), '')  # ลบช่องว่างออกจากชื่อเดือน
        year = str(int(thai_year) - 43 + 2000)  # แปลงปีพุทธศักราชเป็นคริสต์ศักราช
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except Exception as e:
        return None  # คืนค่า None หากเกิดข้อผิดพลาด

# ฟังก์ชันคำนวณจำนวนวันจากวันที่จนถึงวันนี้
def calculate_days_until_today(date_str):
    try:
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # แปลงเป็น datetime object
            today = datetime.now()  # วันที่ปัจจุบัน
            return (today - date_obj).days  # คำนวณจำนวนวัน
        return None
    except Exception as e:
        return None  # คืนค่า None หากเกิดข้อผิดพลาด

# รายชื่อคอลัมน์วันที่ที่ต้องการแปลง
date_columns = ['date', 'ForwardedDate']
column_names_mapping = {
    'date': 'ระยะเวลาจากวันที่เริ่มแจ้ง(วัน)',
    'ForwardedDate': 'ระยะเวลาจากสถานะล่าสุด(วัน)'
}

# ตรวจสอบว่าคอลัมน์ที่กำหนดมีอยู่ในข้อมูลหรือไม่
existing_date_columns = [col for col in date_columns if col in data.columns]

# ทำการแปลงวันที่และคำนวณจำนวนวันสำหรับแต่ละคอลัมน์
for column in existing_date_columns:
    # แปลงวันที่ภาษาไทยเป็น ISO format
    data[column] = data[column].apply(convert_thai_date)
    # สร้างคอลัมน์ใหม่สำหรับจำนวนวันที่คำนวณ
    new_column_name = column_names_mapping[column]
    data[new_column_name] = data[column].apply(calculate_days_until_today)

# บันทึกข้อมูลใหม่ลงไฟล์ CSV
data.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"ข้อมูลถูกบันทึกเรียบร้อยในไฟล์: {output_path}")

# Load the dataset
df = pd.read_csv(output_path)

# Extract the "agency" column and split each entry by ','
agency_series = df['agency'].dropna().str.split(',')

# Flatten the list and strip extra spaces
agencies = [agency.strip() for sublist in agency_series for agency in sublist]

# Get unique agencies and their counts
agency_counts = pd.Series(agencies).value_counts()

# กรองข้อมูลที่ไม่ใช่ค่าว่างเปล่าในคอลัมน์ "Agency"
agency_counts_filtered = agency_counts.reset_index().rename(columns={'index': 'Agency', 0: 'Count'})
agency_counts_filtered = agency_counts_filtered[agency_counts_filtered['Agency'].str.strip() != '']

# Create agencies output file
agencies_output_path = os.path.join(OUTPUT_FOLDER, 'จำนวนในแต่ละเขต.csv')
agency_counts_filtered.to_csv(agencies_output_path, index=False, encoding='utf-8-sig')
print(f"Files have been successfully created in {agencies_output_path}")

# # กำหนดโฟลเดอร์สำหรับบันทึกไฟล์ของหน่วยงาน
# output_dir = os.path.join(OUTPUT_FOLDER, 'agency_files')
# os.makedirs(output_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# # เขียนไฟล์เฉพาะสำหรับแต่ละหน่วยงาน
# for _, agency in agency_counts_filtered.iterrows():
#     agency_name = agency['Agency']
#     agency_file_path = os.path.join(output_dir, f"{agency_name}.csv")

#     # กรองข้อมูลที่เกี่ยวข้องกับหน่วยงานนั้น
#     agency_data = df[df['agency'].str.contains(agency_name, na=False, regex=False)]

#     # บันทึกข้อมูลของหน่วยงานในรูปแบบ CSV
#     agency_data.to_csv(agency_file_path, index=False, encoding='utf-8-sig')

# กำหนดโฟลเดอร์สำหรับบันทึกไฟล์ของหน่วยงาน
output_dir = os.path.join(OUTPUT_FOLDER, 'agency_files')
os.makedirs(output_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# Load the dataset
df = pd.read_csv(output_path)

# Rename the columns
df = df.rename(columns={
    'ticket_id': 'ticket_id',
    'date': 'วันที่แจ้ง',
    'time': 'เวลาที่แจ้ง',
    'status': 'สถานะ',
    'address': 'สถานที่',
    'description': 'รายละเอียด',
    'agency': 'เขตผู้รับผิดชอบ(แก้ไขโดย)',
    'category': 'หมวดหมู่',
    'ForwardedStatus': 'สถานะล่าสุด',
    'ForwardedDate': 'วันที่สถานะล่าสุด',
    'ForwardedTime': 'เวลาสถานะล่าสุด',
    'TakeTime': 'เวลาที่ใช้'
})

# Clean and split the "เขตผู้รับผิดชอบ(แก้ไขโดย)" column
df['เขตผู้รับผิดชอบ(แก้ไขโดย)'] = df['เขตผู้รับผิดชอบ(แก้ไขโดย)'].astype(str).str.strip()
df['split_agencies'] = df['เขตผู้รับผิดชอบ(แก้ไขโดย)'].str.split(',')

# Flatten the list of agencies
agencies = [agency.strip() for sublist in df['split_agencies'].dropna() for agency in sublist]

# Get unique agencies
unique_agencies = pd.Series(agencies).drop_duplicates().tolist()

# Create a dictionary to store DataFrames for each agency
agency_dfs = {agency: pd.DataFrame(columns=df.columns) for agency in unique_agencies}

# Add rows to the corresponding agency DataFrames
for idx, row in df.iterrows():
    if isinstance(row['split_agencies'], list):
        for agency in row['split_agencies']:
            agency = agency.strip()
            if agency in agency_dfs:
                agency_dfs[agency] = pd.concat([agency_dfs[agency], row.to_frame().T])

# Save each agency's DataFrame to a separate file
for agency, agency_df in agency_dfs.items():
    sanitized_agency_name = agency.replace(' ', '_').replace('/', '_').replace(',', '').replace(':', '')
    sanitized_agency_name = sanitized_agency_name[:100]  # Limit to 100 characters
    file_name = os.path.join(output_dir, f"agency_{sanitized_agency_name}.csv")
    agency_df.drop(columns=['split_agencies'], inplace=True)  # Drop the temporary column
    agency_df.to_csv(file_name, index=False, encoding='utf-8-sig')

print(f"Files have been successfully created in {output_dir}.")

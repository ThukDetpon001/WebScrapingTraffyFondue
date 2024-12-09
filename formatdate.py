import pandas as pd
from datetime import datetime

# โหลดไฟล์ CSV พร้อมกำหนด encoding เพื่อรองรับภาษาไทย
file_path = '6-12-67/traffy_data.csv'
output_path = '6-12-67/traffy_data_มีจำนวนวัน.csv'

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

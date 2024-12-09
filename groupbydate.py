# import pandas as pd

# # โหลดข้อมูลจากไฟล์ CSV
# file_path = 'ดำเนินการ/traffy_data_ดำเนินการ.csv'
# df = pd.read_csv(file_path)

# # กำหนดรูปแบบวันที่
# thai_months = {
#     'ม.ค.': 'ม.ค.', 'ก.พ.': 'ก.พ.', 'มี.ค.': 'มี.ค.', 'เม.ย.': 'เม.ย.',
#     'พ.ค.': 'พ.ค.', 'มิ.ย.': 'มิ.ย.', 'ก.ค.': 'ก.ค.', 'ส.ค.': 'ส.ค.',
#     'ก.ย.': 'ก.ย.', 'ต.ค.': 'ต.ค.', 'พ.ย.': 'พ.ย.', 'ธ.ค.': 'ธ.ค.'
# }

# # ฟังก์ชันสำหรับแปลงวันที่เป็นรูปแบบ 'เดือนย่อ-ปี'
# def extract_month_year_thai(date_str):
#     try:
#         # แปลงช่องว่างในวันที่เป็นขีด
#         formatted_date = date_str.replace(" ", "-")
#         day, month, year = formatted_date.split('-')
#         thai_month = thai_months.get(month, 'unknown')  # ดึงชื่อเดือนภาษาไทย
#         short_year = year[-2:]  # ใช้เลขปี พ.ศ. สองหลักท้าย
#         return f"{thai_month}-{short_year}"
#     except ValueError:
#         return 'Invalid Date'

# # แยกข้อมูลตามเดือนและปีโดยไม่สร้างคอลัมน์ใหม่
# df['period'] = df['date'].apply(extract_month_year_thai)

# # กรองข้อมูลที่สามารถแปลงวันที่ได้สำเร็จ
# df_valid = df[df['period'] != 'Invalid Date']
# df_invalid = df[df['period'] == 'Invalid Date']

# # วนลูปผ่านแต่ละเดือนและบันทึกไฟล์ CSV แยกต่างหาก
# for period, group in df_valid.groupby('period'):
#     filename = f"ดำเนินการ/ดำเนินการ_แยกเดือน/data_{period}.csv"
#     group = group.drop(columns=['period'])  # ลบคอลัมน์ period ก่อนบันทึก
#     group.to_csv(filename, index=False, encoding='utf-8-sig')
#     print(f"บันทึกไฟล์: {filename}")

# # แสดงข้อมูลที่ไม่สามารถแปลงวันที่ได้
# if not df_invalid.empty:
#     print("ข้อมูลที่ไม่สามารถแปลงวันที่ได้:")
#     print(df_invalid[['ticket_id', 'date']])  # แสดงเฉพาะคอลัมน์ที่เกี่ยวข้อง


import pandas as pd

# โหลดข้อมูลจากไฟล์ CSV
file_path = 'traffy_data_รอรับเรื่อง.csv'
df = pd.read_csv(file_path)

# กำหนดรูปแบบวันที่
thai_months = {
    'ม.ค.': 'ม.ค.', 'ก.พ.': 'ก.พ.', 'มี.ค.': 'มี.ค.', 'เม.ย.': 'เม.ย.',
    'พ.ค.': 'พ.ค.', 'มิ.ย.': 'มิ.ย.', 'ก.ค.': 'ก.ค.', 'ส.ค.': 'ส.ค.',
    'ก.ย.': 'ก.ย.', 'ต.ค.': 'ต.ค.', 'พ.ย.': 'พ.ย.', 'ธ.ค.': 'ธ.ค.'
}

# ฟังก์ชันสำหรับแปลงวันที่เป็นรูปแบบ 'เดือนย่อ-ปี'
def extract_month_year_thai(date_str):
    try:
        # แปลงช่องว่างในวันที่เป็นขีด
        formatted_date = date_str.replace(" ", "-")
        day, month, year = formatted_date.split('-')
        thai_month = thai_months.get(month, 'unknown')  # ดึงชื่อเดือนภาษาไทย
        short_year = year[-2:]  # ใช้เลขปี พ.ศ. สองหลักท้าย
        return f"{thai_month}-{short_year}"
    except ValueError:
        return 'Invalid Date'

# แยกข้อมูลตามเดือนและปีโดยไม่สร้างคอลัมน์ใหม่
df['period'] = df['date'].apply(extract_month_year_thai)

# กรองข้อมูลที่สามารถแปลงวันที่ได้สำเร็จ
df_valid = df[df['period'] != 'Invalid Date']
df_invalid = df[df['period'] == 'Invalid Date']

# เปลี่ยนชื่อคอลัมน์
column_mapping = {
    'ticket_id': 'ticket_id',
    'date': 'วันที่แจ้ง',
    'time': 'เวลาที่แจ้ง',
    'status': 'สถาณะ',
    'address': 'สถานที่',
    'description': 'รายละเอียด',
    'agency': 'เขตผู้รับผิดชอบ(แก้ไขโดย)',
    'category': 'หมวดหมู่',
    'ForwardedStatus': 'สถาณะล่าสุด',
    'ForwardedDate': 'วันที่สถาณะล่าสุด',
    'ForwardedTime': 'เวลาสถาณะล่าสุด',
    'TakeTime': 'เวลาที่ใช้'
}

df_valid = df_valid.rename(columns=column_mapping)

# วนลูปผ่านแต่ละเดือนและบันทึกไฟล์ CSV แยกต่างหาก
for period, group in df_valid.groupby('period'):
    filename = f"รอรับเรื่อง/รอรับเรื่อง_แยกเดือน/data_{period}.csv"
    group = group.drop(columns=['period'])  # ลบคอลัมน์ period ก่อนบันทึก
    group.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"บันทึกไฟล์: {filename}")

# แสดงข้อมูลที่ไม่สามารถแปลงวันที่ได้
if not df_invalid.empty:
    print("ข้อมูลที่ไม่สามารถแปลงวันที่ได้:")
    print(df_invalid[['ticket_id', 'date']])  # แสดงเฉพาะคอลัมน์ที่เกี่ยวข้อง

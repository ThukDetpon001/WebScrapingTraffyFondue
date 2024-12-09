import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# กำหนดไฟล์ JSON ของ Service Account
SERVICE_ACCOUNT_FILE = 'service_account.json'  # อัปเดตชื่อไฟล์ให้ถูกต้อง
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# สร้าง Credential
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# เชื่อมต่อกับ Google Sheets
gc = gspread.authorize(credentials)

# กำหนด URL ของ Google Sheets
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1PGF7XPYC1xU9EvjcaQLaY6B7vXMyxLVLAn213INeDJk/edit?usp=sharing'  # อัปเดต URL ให้ถูกต้อง
sheet = gc.open_by_url(SPREADSHEET_URL)

def upload_to_google_sheets(file_path, sheet_name):
    try:
        # อ่านข้อมูลจากไฟล์ CSV
        df = pd.read_csv(file_path, encoding='utf-8')

        # จัดการค่าที่ไม่รองรับ JSON (NaN, Infinity)
        df = df.fillna("")  # แทนที่ NaN ด้วยค่า "" (ว่างเปล่า)
        df = df.replace([float('inf'), float('-inf')], "")  # แทนที่ Infinity ด้วยค่า ""

        # เปิดหรือสร้าง Worksheet
        try:
            worksheet = sheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        
        # ล้างข้อมูลเก่าใน Worksheet
        worksheet.clear()
        
        # อัปโหลดข้อมูล
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"อัปโหลดข้อมูลสำเร็จ: {sheet_name}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัปโหลด {sheet_name}: {e}")


# ฟังก์ชันหลัก
def main():
    # กำหนดโฟลเดอร์ที่มีไฟล์ CSV (ใช้ relative path)
    folder_path = os.path.join(os.getcwd(), "9-12-67")  # ระบุเส้นทางไปยังโฟลเดอร์ 9-12-67
    
    # ไฟล์ CSV ที่ต้องการอัปโหลด
    files_to_upload = [
        ("traffy_data_มีจำนวนวัน.csv", "Traffy Data"),
        ("จำนวนในแต่ละเขต.csv", "Agency Counts")
    ]
    
    for file_name, sheet_name in files_to_upload:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            upload_to_google_sheets(file_path, sheet_name)
        else:
            print(f"ไม่พบไฟล์: {file_path}")

if __name__ == "__main__":
    main()

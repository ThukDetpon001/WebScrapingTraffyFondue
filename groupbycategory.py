import pandas as pd

# Load the dataset
file_path = '6-12-67/traffy_data.csv'
df = pd.read_csv(file_path)

# Extract the "agency" column and split each entry by ','
agency_series = df['agency'].dropna().str.split(',')

# Flatten the list and strip extra spaces
agencies = [agency.strip() for sublist in agency_series for agency in sublist]

# Get unique agencies and their counts

agency_counts = pd.Series(agencies).value_counts()

# กรองข้อมูลที่ไม่ใช่ค่าว่างเปล่าในคอลัมน์ "Agency"
agency_counts_filtered = agency_counts.reset_index().rename(columns={'index': 'Agency', 0: 'Count'})
agency_counts_filtered = agency_counts_filtered[agency_counts_filtered['Agency'].str.strip() != '']

# บันทึกไฟล์ใหม่โดยมีการลบแถวที่ว่างเปล่าออก
agency_counts_filtered.to_csv('6-12-67/จำนวนในแต่ละเขต.csv', index=False, encoding='utf-8-sig')
print(f"Files have been successfully created in สร้างจำนวนในแต่ละเขตสำเร็จ.")

# import pandas as pd
import os

# Define file paths
file_path = '6-12-67/traffy_data_มีจำนวนวัน.csv'
output_dir = '6-12-67/แยกตามเขตรับผิดชอบ'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
df = pd.read_csv(file_path)

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







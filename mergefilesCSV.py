import os
import pandas as pd
import chardet

# Specify the folder containing the files
folder_path = 'ใหม่/แยกตามเขตรับผิดชอบ/'

# Get all CSV files in the specified folder
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# Auto-detect encoding for the first file
with open(file_paths[0], 'rb') as f:
    detected_encoding = chardet.detect(f.read())['encoding']
    print(f"Detected encoding: {detected_encoding}")

# Combine all CSV files into a single DataFrame
agency_dataframes = [pd.read_csv(file_path, encoding=detected_encoding) for file_path in file_paths]
combined_agency_data = pd.concat(agency_dataframes, ignore_index=True)

# Save the combined data to a new CSV
output_file_path = 'ใหม่/รวมไฟล์แยกตามผู้รับผิดชอบ.csv'
combined_agency_data.to_csv(output_file_path, index=False, encoding=detected_encoding)

print(f"Combined CSV file saved at: {output_file_path}")

import openpyxl
import pandas as pd
import argparse
import os

# ==== CONFIG ====
sheet_name = "Main"

# GitHub repo info
user = "TeamLead2-CM"
repo = "OSINT_Directory_Resources"
branch = "framework_initial"
base_path = "osint"

# These must exactly match column names in the input Excel
input_columns = ["Tool Logo", "Tool UI", "Demo 1 Image", "Demo 2 Image", "Demo 3 Image"]
output_headers = ["Tool ID", "Logo", "UI", "Demo 1", "Demo 2", "Demo 3"]

# Mappings for folder/filename prefixes
column_subfolder = {
    "Tool Logo": "logo",
    "Tool UI": "ui",
    "Demo 1 Image": "demo1",
    "Demo 2 Image": "demo2",
    "Demo 3 Image": "demo3"
}

column_filename_prefix = {
    "Tool Logo": "logo",
    "Tool UI": "ui",
    "Demo 1 Image": "demo1",
    "Demo 2 Image": "demo2",
    "Demo 3 Image": "demo3"
}

def make_raw_url(subfolder, filename_prefix, tool_id):
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{base_path}/{subfolder}/{filename_prefix}_{tool_id}.jpg"

def generate_github_links_excel(input_excel, output_excel):
    # Load the input Excel sheet
    df = pd.read_excel(input_excel, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()

    # Create a new workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Add headers
    ws.append(output_headers)

    # Generate rows
    for _, row_data in df.iterrows():
        tool_id = str(row_data["Tool ID"]).strip()
        row = [tool_id]

        for col in input_columns:
            cell_val = row_data.get(col)

            if pd.isna(cell_val) or not str(cell_val).strip():
                row.append("")  # Leave blank if original cell was blank
            else:
                subfolder = column_subfolder[col]
                filename_prefix = column_filename_prefix[col]
                url = make_raw_url(subfolder, filename_prefix, tool_id)
                row.append(url)

        ws.append(row)

    # Save workbook
    wb.save(output_excel)
    print(f"✅ Excel sheet created: {output_excel}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate GitHub image links Excel from OSINT tools sheet")
    parser.add_argument('-i', '--input', type=str, default='osint.xlsx', help="Input Excel file (default: osint.xlsx)")
    parser.add_argument('-o', '--output', type=str, help="Output Excel file (default: <inputfilename>_github_links.xlsx)")

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output or f"{os.path.splitext(input_file)[0]}_github_links.xlsx"

    generate_github_links_excel(input_file, output_file)

import openpyxl
import pandas as pd
import argparse
import os

# ==== VARIABLES ====
sheet_name = "OSINT Tools"
tool_id_prefix = "T_OF_"

# GitHub repo info
user = "TeamLead2-CM"
repo = "OSINT_Directory_Resources"
branch = "framework_initial"
base_path = "osint"

headers = ["Tool ID", "Logo", "UI", "Demo 1", "Demo 2", "Demo 3"]

column_subfolder = {
    "Logo": "logo",
    "UI": "ui",
    "Demo 1": "demo1",
    "Demo 2": "demo2",
    "Demo 3": "demo3"
}

column_filename_prefix = {
    "Logo": "logo",
    "UI": "ui",
    "Demo 1": "demo1",
    "Demo 2": "demo2",
    "Demo 3": "demo3"
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
    ws.append(headers)

    # Generate rows
    for _, row_data in df.iterrows():
        tool_id = str(row_data["Tool ID"]).strip()
        row = [tool_id]
        for col in headers[1:]:
            original_col_name = f"Tool {col}"
            cell_val = row_data.get(original_col_name)

            if pd.isna(cell_val) or not str(cell_val).strip():
                row.append("")  # Intentionally blank
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

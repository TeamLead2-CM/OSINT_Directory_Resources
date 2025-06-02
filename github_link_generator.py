import openpyxl

# ==== VARIABLES ====
sheet_name = "OSINT Tools"
tool_id_prefix = "T_OF_"
total_tools = 110

# For raw.githubusercontent.com
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

# ==== CREATE WORKBOOK AND SHEET ====
wb = openpyxl.Workbook()
ws = wb.active
ws.title = sheet_name

# ==== ADD HEADERS ====
ws.append(headers)

# ==== GENERATE ROWS ====
for i in range(1, total_tools + 1):
    tool_id = f"{tool_id_prefix}{i:03d}"
    row = [tool_id]
    for col in headers[1:]:
        subfolder = column_subfolder[col]
        filename_prefix = column_filename_prefix[col]
        url = make_raw_url(subfolder, filename_prefix, tool_id)
        row.append(url)
    ws.append(row)

# ==== SAVE WORKBOOK ====
wb.save("osint_tools.xlsx")
print("Excel sheet created: osint_tools.xlsx")

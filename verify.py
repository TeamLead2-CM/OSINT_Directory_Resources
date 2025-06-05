import os
import pandas as pd

# ==== CONFIG ====
excel_file = "osint.xlsx"
sheet_name = "Main"
base_dir = "osint"
output_log = "missing.txt"

# Column to folder mapping (Excel column → subfolder name)
columns = {
    "Tool Logo": "logo",
    "Tool UI": "ui",
    "Demo 1 Image": "demo1",
    "Demo 2 Image": "demo2",
    "Demo 3 Image": "demo3",
}

missing = []

# ==== READ DATA ====
df = pd.read_excel(excel_file, sheet_name=sheet_name)
df.columns = df.columns.str.strip()

# ==== CHECK FILE EXISTENCE ====
for _, row in df.iterrows():
    tool_id = str(row["Tool ID"]).strip()

    for col_name, folder in columns.items():
        cell_value = row.get(col_name)

        if pd.isna(cell_value) or not str(cell_value).strip():
            # Blank cell — image intentionally missing, skip
            continue

        filename = f"{folder}_{tool_id}.jpg"
        full_path = os.path.join(base_dir, folder, filename)

        if not os.path.exists(full_path):
            missing.append(full_path)

# ==== WRITE MISSING TO FILE ====
with open(output_log, "w") as f:
    for path in missing:
        f.write(path + "\n")

print(f"✅ Checked {len(df)} tools. {len(missing)} missing files written to {output_log}.")

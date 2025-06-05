import os

# Hardcoded total number of tools
TOTAL_TOOLS = 552  # Set this to your actual total

# Folder and prefix mapping (adjust as needed)
folders = {
    'logo': 'logo',
    'ui': 'ui',
    'demo1': 'demo1',
    'demo2': 'demo2',
    'demo3': 'demo3',
}

base_dir = 'osint'
missing = []

for folder in folders.values():
    folder_path = os.path.join(base_dir, folder)
    for i in range(1, TOTAL_TOOLS + 1):
        tool_id = f"T_OF_{i:03d}"
        filename = f"{folder}_{tool_id}.jpg"
        full_path = os.path.join(folder_path, filename)
        if not os.path.exists(full_path):
            missing.append(full_path)

with open("missing.txt", "w") as f:
    for path in missing:
        f.write(path + "\n")

print(f"Checked {TOTAL_TOOLS} tools in each folder. {len(missing)} missing files written to missing.txt.")

# # Drive to github conversion

# import pandas as pd
# import requests
# from PIL import Image, UnidentifiedImageError
# from io import BytesIO

# # Load the Excel file (replace 'ai_copy.xlsx' with your actual filename)
# file_path = '../osint.xlsx'
# data = pd.read_excel(file_path)

# def download_file_from_google_drive(drive_link):
#     file_id = drive_link.split('/d/')[1].split('/')[0]
#     download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
#     try:
#         response = requests.get(download_url, headers=headers, stream=True)
#         response.raise_for_status()
#         return response.content
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to download file from Google Drive: {e}")
#         return None

# def process_image(tool_id, drive_link, folder_name):
#     try:
#         file_content = download_file_from_google_drive(drive_link)
#         if file_content:
#             try:
#                 image_data = BytesIO(file_content)
#                 img = Image.open(image_data)
                
#                 if img.mode in ("RGBA", "P"):
#                     img = img.convert("RGB")
                
#                 filename = f"osint/{folder_name}/{folder_name}_{tool_id}.jpg"
#                 img.save(filename, "JPEG", quality=92)
                
#                 print(f"Image for Tool ID {tool_id} saved successfully as {filename}")
#             except UnidentifiedImageError:
#                 print(f"Failed to identify image for Tool ID {tool_id}. The file may not be a valid image.")
#             except OSError as e:
#                 print(f"Failed to save image for Tool ID {tool_id}: {e}")
#         else:
#             print(f"Failed to download image for Tool ID {tool_id} from Google Drive.")
#     except Exception as e:
#         print(f"An error occurred while processing Tool ID {tool_id}: {e}")

# # Define the columns and corresponding folder names
# columns_and_folders = {
#     1: ("logo", "logo"),  # LOGO
#     2: ("ui", "ui"),      # UI
#     3: ("demo1", "demo1"), # DEMO 1
#     4: ("demo2", "demo2"), # DEMO 2
#     5: ("demo3", "demo3"), # DEMO 3
# }

# # Iterate through each row in the DataFrame
# for index, row in data.iterrows():
#     tool_id = str(row.iloc[0])  # Access Tool ID by position
    
#     for column, (folder_name, description) in columns_and_folders.items():
#         drive_link = row.iloc[column]
        
#         if pd.notna(drive_link):  # Check if the cell is not empty
#             process_image(tool_id, drive_link, folder_name)
#         else:
#             print(f"No link found for {description} of Tool ID {tool_id}.")


import pandas as pd
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Load the Excel file (replace 'ai_copy.xlsx' with your actual filename)
file_path = '../osint.xlsx'
data = pd.read_excel(file_path)

def extract_url(cell):
    """
    Extracts the URL from a cell that may contain a hyperlink.
    If the cell contains plain text, it returns the text as is.
    """
    if isinstance(cell, str) and "http" in cell:
        return cell.split('"')[1] if '"' in cell else cell
    return cell

def download_file_from_google_drive(drive_link):
    file_id = drive_link.split('/d/')[1].split('/')[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file from Google Drive: {e}")
        return None

def process_image(tool_id, drive_link, folder_name):
    try:
        file_content = download_file_from_google_drive(drive_link)
        if file_content:
            try:
                image_data = BytesIO(file_content)
                img = Image.open(image_data)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                filename = f"osint/{folder_name}/{folder_name}_{tool_id}.jpg"
                img.save(filename, "JPEG", quality=92)
                
                print(f"Image for Tool ID {tool_id} saved successfully as {filename}")
            except UnidentifiedImageError:
                print(f"Failed to identify image for Tool ID {tool_id}. The file may not be a valid image.")
            except OSError as e:
                print(f"Failed to save image for Tool ID {tool_id}: {e}")
        else:
            print(f"Failed to download image for Tool ID {tool_id} from Google Drive.")
    except Exception as e:
        print(f"An error occurred while processing Tool ID {tool_id}: {e}")

# Define the columns and corresponding folder names
columns_and_folders = {
    1: ("logo", "logo"),  # LOGO
    2: ("ui", "ui"),      # UI
    3: ("demo1", "demo1"), # DEMO 1
    4: ("demo2", "demo2"), # DEMO 2
    5: ("demo3", "demo3"), # DEMO 3
}

# Iterate through each row in the DataFrame
for index, row in data.iterrows():
    tool_id = str(row.iloc[0])  # Access Tool ID by position
    
    for column, (folder_name, description) in columns_and_folders.items():
        drive_link = extract_url(row.iloc[column])
        
        if pd.notna(drive_link):  # Check if the cell is not empty
            process_image(tool_id, drive_link, folder_name)
        else:
            print(f"No link found for {description} of Tool ID {tool_id}.")

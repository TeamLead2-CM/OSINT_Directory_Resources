# Drive to github conversion

import pandas as pd
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Load the Excel file (replace 'ai_copy.xlsx' with your actual filename)
file_path = 'ai_copy.xlsx'
data = pd.read_excel(file_path)

def download_file_from_google_drive(drive_link):
    # Extract the file ID from the Google Drive link
    file_id = drive_link.split('/d/')[1].split('/')[0]
    
    # Construct the direct download URL
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        # Add headers to avoid anti-scraping measures
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        # Download the file using the direct download URL
        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file from Google Drive: {e}")
        return None

# Iterate through each row in the DataFrame
for index, row in data.iterrows():
    tool_id = str(row.iloc[0])  # Access Tool ID by position
    # drive_link = row.iloc[1]    # LOGO
    # drive_link = row.iloc[2]    # UI
    # drive_link = row.iloc[3]    # DEMO 1
    # drive_link = row.iloc[4]    # DEMO 2
    drive_link = row.iloc[5]    # DEMO 3
    
    try:
        # Download the image from Google Drive
        file_content = download_file_from_google_drive(drive_link)
        
        if file_content:
            try:
                # Open the image using PIL
                image_data = BytesIO(file_content)
                img = Image.open(image_data)
                
                # Convert to RGB mode if necessary
                if img.mode in ("RGBA", "P"):  # Check for modes that are incompatible with JPEG
                    img = img.convert("RGB")
                
                # Define the filename as Tool ID
                filename = f"demo3/demo3_{tool_id}.jpg"  # Change folder and filename
                
                # Save the image to the specified path
                img.save(filename, "JPEG", quality=92)  # Save as JPEG with quality
                
                print(f"Image for Tool ID {tool_id} saved successfully as {filename}")
            except UnidentifiedImageError:
                print(f"Failed to identify image for Tool ID {tool_id}. The file may not be a valid image.")
            except OSError as e:
                print(f"Failed to save image for Tool ID {tool_id}: {e}")
        else:
            print(f"Failed to download image for Tool ID {tool_id} from Google Drive.")
    
    except Exception as e:
        print(f"An error occurred while processing Tool ID {tool_id}: {e}")



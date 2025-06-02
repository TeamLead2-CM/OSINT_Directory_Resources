import os
import pandas as pd
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
import urllib3
import re
import argparse
import time

# Disable SSL warnings (use only in trusted/internal context)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print("⚠️ WARNING: SSL verification is disabled. Use only for trusted internal scripts.")

# Set up logging
logging.basicConfig(filename='log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
file_path = 'osint.xlsx'
base_dir = 'osint'
columns_and_folders = {
    'Tool Logo': 'logo',
    'Tool UI': 'ui',
    'Demo 1 Image': 'demo1',
    'Demo 2 Image': 'demo2',
    'Demo 3 Image': 'demo3',
}

# Ensure output folders exist
for folder in columns_and_folders.values():
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

def download_file_from_google_drive(drive_link, max_retries=3):
    try:
        file_id = drive_link.split('/d/')[1].split('/')[0]
    except IndexError:
        raise RuntimeError(f"Invalid Google Drive link: {drive_link}")

    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(download_url, headers=headers, stream=True, timeout=30, verify=False)
            response.raise_for_status()
            return response.content
        except Exception as e:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"⚠️ Attempt {attempt} failed for {file_id}, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Download failed: {e}")

def process_image(tool_id, drive_link, folder):
    try:
        file_content = download_file_from_google_drive(drive_link)
        image_data = BytesIO(file_content)
        img = Image.open(image_data)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        filename = os.path.join(base_dir, folder, f"{folder}_{tool_id}.jpg")
        img.save(filename, "JPEG", quality=92)
        return True, f"Saved {filename}"
    except (UnidentifiedImageError, OSError, RuntimeError) as e:
        error_msg = f"Tool ID {tool_id} ({folder}): {e}"
        logging.error(error_msg)
        return False, error_msg

def retry_failed_downloads(log_path='log.txt'):
    print("🔁 Retrying failed downloads from log.txt...")
    retry_tasks = []

    pattern = re.compile(r"Tool ID (.+?) \((.+?)\): .*?id=([a-zA-Z0-9_-]+)")

    with open(log_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                tool_id, folder, file_id = match.groups()
                drive_link = f"https://drive.google.com/file/d/{file_id}/view"
                retry_tasks.append((tool_id, drive_link, folder))

    if not retry_tasks:
        print("✅ No failed downloads found in the log.")
        return

    for tool_id, drive_link, folder in tqdm(retry_tasks, desc="Retrying failed downloads"):
        try:
            success, msg = process_image(tool_id, drive_link, folder)
            if not success:
                print(f"Retry error: {msg}")
        except Exception as e:
            logging.error(f"Retry failed for {tool_id} ({folder}): {e}")

def main_download():
    data = pd.read_excel(file_path)
    tasks = []

    for _, row in data.iterrows():
        tool_id = str(row['Tool ID'])
        for col_name, folder in columns_and_folders.items():
            drive_link = row.get(col_name)
            if pd.notna(drive_link):
                tasks.append((tool_id, drive_link, folder))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_image, tool_id, link, folder) for tool_id, link, folder in tasks]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing images"):
            try:
                success, msg = future.result()
                if not success:
                    print(f"Error: {msg}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image downloader for tools")
    parser.add_argument('--retry', action='store_true', help="Retry failed downloads from log.txt")
    args = parser.parse_args()

    if args.retry:
        retry_failed_downloads()
    else:
        main_download()

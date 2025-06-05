import os
import pandas as pd
import requests
import pillow_avif
from willow.image import Image, UnrecognisedImageFormatError  # pip install Willow[Pillow,heif]
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
import urllib3
import re
import argparse
import time
import cairosvg

# Disable SSL warnings (use only in trusted/internal context)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print("⚠️ WARNING: SSL verification is disabled. Use only for trusted internal scripts. NOT RECOMMENDED IN PRODUCTION!")

# Set up logging
logging.basicConfig(filename='log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
# file_path = 'osint.xlsx' # taken using argument --file, default: osint.xlsx 
base_dir = 'osint'
columns_and_folders = {
    'Tool Logo': 'logo',
    'Tool UI': 'ui',
    'Demo 1 Image': 'demo1',
    'Demo 2 Image': 'demo2',
    'Demo 3 Image': 'demo3',
}

folder_paths = {folder: os.path.join(base_dir, folder) for folder in columns_and_folders.values()} # cache all folder_path once at start

# Ensure output folders exist
for folder in columns_and_folders.values():
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

# Create a session for persistent connection reuse
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def download_file_from_google_drive(drive_link, max_retries=3):
    try:
        file_id = drive_link.split('/d/')[1].split('/')[0]
    except IndexError:
        raise RuntimeError(f"Invalid Google Drive link: {drive_link}")

    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(download_url, stream=True, timeout=30, verify=False)
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
    filename = os.path.join(folder_paths[folder], f"{folder}_{tool_id}.jpg")
    if os.path.exists(filename):
        return True, f"Skipped (already exists): {filename}"

    try:
        file_content = download_file_from_google_drive(drive_link)
        image_data = BytesIO(file_content)
        image_data.seek(0)

        # Robust SVG detection by header or tag in first 200 bytes
        if file_content.strip().startswith(b'<?xml') or b'<svg' in file_content[:200].lower():
            try:
                # Convert SVG to PNG in memory
                png_bytes = cairosvg.svg2png(bytestring=file_content, background_color='white')
                png_data = BytesIO(png_bytes)
                img = Image.open(png_data)
                img = img.set_background_color_rgb((255, 255, 255))
                with open(filename, "wb") as out_file:
                    img.save_as_jpeg(out_file)
                return True, f"Saved (SVG converted) {filename}"
            except Exception as svg_e:
                error_msg = (
                    f"Tool ID {tool_id} ({folder}): SVG conversion error: {type(svg_e).__name__}: {svg_e} (link: {drive_link})"
                )
                logging.error(error_msg)
                return False, error_msg
        else:
            try:
                img = Image.open(image_data)
                img = img.set_background_color_rgb((255, 255, 255))
                with open(filename, "wb") as out_file:
                    img.save_as_jpeg(out_file)
                return True, f"Saved {filename}"
            except Exception as img_e:
                error_msg = (
                    f"Tool ID {tool_id} ({folder}): Image processing error: {type(img_e).__name__}: {img_e} (link: {drive_link})"
                )
                logging.error(error_msg)
                return False, error_msg

    except Exception as e:
        # This catches errors in download or any unexpected place
        error_msg = (
            f"Tool ID {tool_id} ({folder}): General error: {type(e).__name__}: {e} (link: {drive_link})"
        )
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
    data = pd.read_excel(args.file)
    tasks = []

    for _, row in data.iterrows():
        tool_id = str(row['Tool ID'])
        for col_name, folder in columns_and_folders.items():
            drive_link = row.get(col_name)
            if pd.notna(drive_link) and isinstance(drive_link, str) and drive_link.strip():
                if 'drive.google.com' in drive_link:
                    tasks.append((tool_id, drive_link, folder))
                else:
                    logging.error(f"Tool ID {tool_id} ({folder}): Invalid link format (not Google Drive): '{drive_link}'")
            elif isinstance(drive_link, str) and not drive_link.strip():
                logging.info(f"Tool ID {tool_id} ({folder}): Blank cell (intentionally left empty)")


    max_workers = min(50, len(tasks))  # Dynamic cap

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
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
    parser.add_argument('--file', type=str, default='osint.xlsx', help="Excel file path")
    args = parser.parse_args()

    if args.retry:
        retry_failed_downloads()
    else:
        main_download()

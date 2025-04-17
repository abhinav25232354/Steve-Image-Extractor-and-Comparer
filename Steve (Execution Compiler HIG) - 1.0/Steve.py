from PIL import Image
import pytesseract
from colorama import Fore, Style
import os
import unicodedata

# Colors_Printing variables
red = Fore.RED     # red color
green = Fore.GREEN # green color
yellow = Fore.YELLOW # yellow color
cyan = Fore.CYAN
reset = Style.RESET_ALL # reset terminal after colorizing to ignore errors
error_count = 0

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

unicode_to_ascii = {
    '‘': "'", '’': "'", '“': '"', '”': '"', '„': '"', '‹': '<', '›': '>', '«': '<<', '»': '>>',
    '©': '(c)', '®': '(R)', '™': '(TM)', '€': 'EUR', '£': 'GBP', '¥': 'JPY', '÷': '/', '×': '*'
}
# def remove_unicode_symbols(text):
#     quotes = ["'", '"', '‘', '’', '“', '”', '„', '‹', '›', '«', '»']
#     return ''.join(c for c in text if unicodedata.category(c)[0] != 'S' and c not in quotes)
def replace_unicode_symbols(text):
    return ''.join(unicode_to_ascii.get(c, c) for c in text)

# Function to extract text from an image and compare with a text file
def process_image(image_path, text_path):
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)

    with open(text_path, "r", encoding="utf-8") as file:
        text_from_file = file.read().strip()

    extracted_lines = [line for line in extracted_text.strip().splitlines() if line.strip()]
    # Modification
    extracted_lines_WU = [replace_unicode_symbols(line) for line in extracted_lines]
    # Modification End
    file_lines = text_from_file.strip().splitlines()
    error_found = False

    for line_index, (extracted_lines_WU, file_line) in enumerate(zip(extracted_lines_WU, file_lines)):
        if extracted_lines_WU != file_line:
            error_found = True
            print(f"{cyan}\nError: Text does not match at line {line_index + 1}.{reset}")
            print(f"\t{green}Extracted line: {extracted_lines_WU}{reset}")
            print(f"\t{red}Written line  : {file_line}{reset}")

    if not error_found:
        print("\nText Matched :)")

# Prompt user to enter the folder paths
image_folder_path = input(f"{yellow}Enter folder path containing image files: {reset}")
text_folder_path = input(f"{yellow}Enter folder path containing text files: {reset}")

# Iterate through each file in the image folder
for image_filename in os.listdir(image_folder_path):
    if image_filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(image_folder_path, image_filename)
        text_filename = os.path.splitext(image_filename)[0] + ".txt"
        text_path = os.path.join(text_folder_path, text_filename)

        print(f"\nProcessing image: {image_filename}")
        print(f"Text file expected: {text_filename}")
        
        try:
            # Process each image with its corresponding text file
            process_image(image_path, text_path)
        except Exception as e:
            # Increment error counter if an exception occurs
            error_count += 1
            print(f"Error processing {image_filename}: {str(e)}")

        # Process each image with its corresponding text file
        # process_image(image_path, text_path)        

    else:
        print(f"\nSkipping file: {image_filename} (Unsupported image format)")

# print(f"\nTotal number of errors: {error_count}")



# Check for any text files without corresponding image files
for text_filename in os.listdir(text_folder_path):
    if text_filename.lower().endswith(".txt"):
        image_filename = os.path.splitext(text_filename)[0] + ".jpg"  # Assuming images have jpg extension
        image_path = os.path.join(image_folder_path, image_filename)
        text_path = os.path.join(text_folder_path, text_filename)

        if not os.path.exists(image_path):
            print(f"\nWarning: No corresponding image file found for {text_filename}")

# You can add additional logic to handle scenarios where there might be extra images without corresponding text files.
a=input(f"\n{yellow}Press a Key to Exit{reset}")
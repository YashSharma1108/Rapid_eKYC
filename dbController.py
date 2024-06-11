#database obj
from flask import Flask, render_template, request
import db
import pytesseract
from PIL import Image
import re
import base64
from io import BytesIO
import os
import json
import cv2
from PIL import Image
import ftfy
import io

# app = Flask(__name__)
# dbObj = db.getdbObj()

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Yash Sharma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def adhaar_read_data(text):
    name = None
    dob = None
    adh = None
    sex = None

    # Normalize the text to improve pattern matching
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())  # Remove multiple spaces
    text = text.lower()  # Convert to lower case for easier matching

    # Extract name
    name_patterns = [
        re.compile(r'name\s*[:;]?\s*([\w\s]+)', re.IGNORECASE),
        re.compile(r'government of india\s*([\w\s]+)\s*(?:dob|date of birth|year of birth|sex|male|female)', re.IGNORECASE),
        re.compile(r'(\b(?:mr|ms|mrs)\.\s*[\w\s]+)', re.IGNORECASE),
        re.compile(r'([\w\s]+)\s*(?:/|\s)?dob\s*[:;]?\s*\d{2}/\d{2}/\d{4}', re.IGNORECASE),
        re.compile(r'([\w\s]+)\s*(?:/|\s)?aeo\s*/\s*(male|female)', re.IGNORECASE)
    ]
    for pattern in name_patterns:
        match = pattern.search(text)
        if match:
            name = match.group(1).strip().title()
            break

    # Extract date of birth
    dob_patterns = [
        re.compile(r'\b(?:dob|date of birth|d.o.b)\s*[:;]?\s*(\d{2}/\d{2}/\d{4})\b', re.IGNORECASE),
        re.compile(r'\b(?:year of birth|yob)\s*[:;]?\s*(\d{4})\b', re.IGNORECASE)
    ]
    for pattern in dob_patterns:
        match = pattern.search(text)
        if match:
            dob = match.group(1).strip()
            break

    # Extract sex
    if 'female' in text:
        sex = "FEMALE"
    elif 'male' in text:
        sex = "MALE"

    # Extract Aadhar number
    aadhar_patterns = [
        re.compile(r'(\d{4}\s\d{4}\s\d{4})'),
        re.compile(r'(\d{4}\s\d{4}\s\d{4}\s\d{4})')  # To handle potential OCR errors with extra spaces
    ]
    for pattern in aadhar_patterns:
        match = pattern.search(text)
        if match:
            adh = match.group(1).strip()
            break

    data = {
        'Name': name,
        'Date of Birth': dob,
        'Adhaar Number': adh,
        'Sex': sex,
        'ID Type': "Adhaar"
    }

    return data

def extractData(image_path):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Load the image and preprocess it
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        raise IOError(f"Failed to load image: {image_path}")

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()

    if var < 20:
        raise ValueError("Image is Too Blurry")

    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')

    # Write OCR result to a file (optional)
    with open('output.txt', 'w', encoding='utf-8') as text_output:
        text_output.write(text)

    # Read and process the OCR result
    with open('output.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    data = adhaar_read_data(text)

    # Write the data to a JSON file
    with io.open('info.json', 'w', encoding='utf-8') as outfile:
        json_data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(json_data)

    # Load and print the JSON data
    with open('info.json', encoding='utf-8') as data_file:
        data_loaded = json.load(data_file)

    if data_loaded['ID Type'] == 'Adhaar':
        print("\n---------- Adhaar Details ----------")
        print("\nName: ", data_loaded['Name'])
        print("\nDate Of Birth: ", data_loaded['Date of Birth'])
        print("\nAdhaar Number: ", data_loaded['Adhaar Number'])
        print("\nSex: ", data_loaded['Sex'])
        print("\nID Type: ", data_loaded['ID Type'])
        print("\n------------------------------------")

    return data_loaded

# Example usage
image_path = r"C:\Users\Yash Sharma\Pictures\Screenshots\Vikrant.png"
data = extractData(image_path)

# def fetchData(image_url):
#     image = convert_to_byte(image_url)
#     fetched_data = extractData(image)

#     return "success"

#     # database hit krenge (uss aadhar number s related sara ) put it ina variable fetchedData.

#     # fetchedData and data ko compare krenge
#     # agr same hua , to return true. vrna false.


# def convert_to_byte(data_url):
#     # Remove the Data URL prefix
#     header, encoded = data_url.split(",", 1)
    
#     # Decode the base64 string
#     image_data = base64.b64decode(encoded)
    
#     # Open the image with Pillow
#     image = Image.open(BytesIO(image_data))

#     return image
    
#     # # Perform operations on the image (e.g., convert to grayscale)
#     # gray_image = image.convert('L')
    
#     # # Show the image (for debugging purposes)
#     # gray_image.show()63263
    
#     # # Save the processed image if needed
#     # gray_image.save("processed_image.jpg")


# def extractData(image):
#     #image aadhar number, dob, name aur related details json m send kr dega

#     # image = Image.open(image_path)

#     # Use pytesseract to perform OCR on the image
#     try:
#         ocr_result = pytesseract.image_to_string(image)

#         # Use regular expressions to extract specific fields
#         # Assuming the Aadhaar card contains the following fields
#         # Name, Aadhaar Number, Date of Birth, Address

#         aadhaar_info = {}

#         # Extract Aadhaar number (usually a 12-digit number)
#         aadhaar_number = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', ocr_result)
#         if aadhaar_number:
#             aadhaar_info['Aadhaar Number'] = aadhaar_number.group(0)

#         # Extract Name (assuming it comes after the label "Name")
#         name = re.search(r'Name\s*:\s*(.*)', ocr_result)
#         if name:
#             aadhaar_info['Name'] = name.group(1).strip()

#         # Extract Date of Birth (DOB) (assuming it follows the format DD/MM/YYYY or similar)
#         dob = re.search(r'DOB\s*:\s*(\d{2}/\d{2}/\d{4})', ocr_result)
#         if dob:
#             aadhaar_info['Date of Birth'] = dob.group(1).strip()

#         # Extract Address (assuming it starts after the label "Address" and ends before the next label)
#         address = re.search(r'Address\s*:\s*(.*)\n', ocr_result)
#         if address:
#             aadhaar_info['Address'] = address.group(1).strip()

#         return aadhaar_info
    
#     except Exception as e:
#         return None

# def compareFace(face1, face2):
#     return 1

# def addReport(username, note):
#     try:
#         query = "INSERT INTO report (username, note) VALUES ('" + username + "','" + note + "')"  
#         dbObj.execute(query)
#         dbObj.commit()

#         return "1"
    
#     except Exception as e:
#         return e

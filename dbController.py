#database obj
from flask import Flask, render_template, request
import db
import pytesseract
from PIL import Image
import re
import base64
from io import BytesIO

app = Flask(__name__)
dbObj = db.getdbObj()

def fetchData(image_url):
    image = convert_to_byte(image_url)
    fetched_data = extractData(image)

    return "success"

    # database hit krenge (uss aadhar number s related sara ) put it ina variable fetchedData.

    # fetchedData and data ko compare krenge
    # agr same hua , to return true. vrna false.


def convert_to_byte(data_url):
    # Remove the Data URL prefix
    header, encoded = data_url.split(",", 1)
    
    # Decode the base64 string
    image_data = base64.b64decode(encoded)
    
    # Open the image with Pillow
    image = Image.open(BytesIO(image_data))

    return image
    
    # # Perform operations on the image (e.g., convert to grayscale)
    # gray_image = image.convert('L')
    
    # # Show the image (for debugging purposes)
    # gray_image.show()63263
    
    # # Save the processed image if needed
    # gray_image.save("processed_image.jpg")




def extractData(image):
    #image aadhar number, dob, name aur related details json m send kr dega

    # image = Image.open(image_path)

    # Use pytesseract to perform OCR on the image
    try:
        ocr_result = pytesseract.image_to_string(image)

        # Use regular expressions to extract specific fields
        # Assuming the Aadhaar card contains the following fields
        # Name, Aadhaar Number, Date of Birth, Address

        aadhaar_info = {}

        # Extract Aadhaar number (usually a 12-digit number)
        aadhaar_number = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', ocr_result)
        if aadhaar_number:
            aadhaar_info['Aadhaar Number'] = aadhaar_number.group(0)

        # Extract Name (assuming it comes after the label "Name")
        name = re.search(r'Name\s*:\s*(.*)', ocr_result)
        if name:
            aadhaar_info['Name'] = name.group(1).strip()

        # Extract Date of Birth (DOB) (assuming it follows the format DD/MM/YYYY or similar)
        dob = re.search(r'DOB\s*:\s*(\d{2}/\d{2}/\d{4})', ocr_result)
        if dob:
            aadhaar_info['Date of Birth'] = dob.group(1).strip()

        # Extract Address (assuming it starts after the label "Address" and ends before the next label)
        address = re.search(r'Address\s*:\s*(.*)\n', ocr_result)
        if address:
            aadhaar_info['Address'] = address.group(1).strip()

        return aadhaar_info
    
    except Exception as e:
        return None

def compareFace(face1, face2):
    return 1

def addReport(username, note):
    try:
        query = "INSERT INTO report (username, note) VALUES ('" + username + "','" + note + "')"  
        dbObj.execute(query)
        dbObj.commit()

        return "1"
    
    except Exception as e:
        return e

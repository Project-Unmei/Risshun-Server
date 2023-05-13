"""
Modules for parsing the input file utilizing LUTs, GPT, and other methods.
"""

import json
import fitz
import docx
from . import extractor


def csv_to_dict(file_path: str):
    tempDict = {}
    with open(file_path) as csvFile:
        for line in csvFile:
            # Get index of first comma
            firstComma = line.find(",")  
            tempValue = line[firstComma+1:].strip()
            tempValue = tempValue[1:-1] if tempValue.startswith("\"") and tempValue.endswith("\"") else tempValue
            tempDict[line[:firstComma]] = tempValue
    print(tempDict)
    return tempDict

def json_to_dict(json_path: str):
    with open(json_path) as f:
        return json.load(f)
    
def docx_to_string(docx_path: str):
    pass

def pdf_to_string(pdf_path: str):
    doc = fitz.open(pdf_path)
    tempText = ""
    for page in doc:
        tempText += page.get_text("text")
    return tempText

def docx_to_string(doc_path: str):
    doc = docx.Document(doc_path)
    tempText = ""
    for para in doc.paragraphs:
        tempText += para.text.strip()
    return tempText

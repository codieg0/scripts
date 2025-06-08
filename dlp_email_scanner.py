# A few libraries to import
#     1. os, sys, tempfile -> work with files and folders
#     2. email, docx, PyPDF2 -> Extract and parse emails
#     3. Reading Excel files -> pandas
#     4. Regular expressions -> re

import os
import sys
import re
import tempfile
import pandas as pd
from email import policy
from email.parser import BytesParser
from docx import Document
import PyPDF2

# Things to do before:
# 1. Install Python3 from the Microsoft Store -> https://apps.microsoft.com/detail/9PNRBTZXMB4Z?hl=en-us&gl=GB&ocid=pdpshare
# 2. Create a folder in your Desktop. Save the script and the file SmartIDDictionaryTerms.xlsx
# 3. Create a subfolder name attachments and save the eml files or attachments triggering the DLP rule
# 4. Run this in Powershell -> python.exe -m pip install pandas openpyxl python-docx PyPDF2

# Usage of the script:  py.exe .\dlp_email_scanner.py .\SmartIDDictionaryTerms.xlsx .\attachments\email.eml

# Website to validate SSN -> https://www.ssnregistry.org/validate/
# Website to validate CC: https://www.validcreditcardnumber.com/

def load_dlp_dict(xlsx_path):
    xl = pd.ExcelFile(xlsx_path)
    dlp_dict = {}
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        for term in df.iloc[:, 0].dropna().astype(str).str.strip():
            dlp_dict[term] = sheet
    return dlp_dict

def find_dlp_terms(text, dlp_dict):
    found = []
    for term, category in dlp_dict.items():
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            found.append((term, category))
    return found

def find_ssn(text):
    patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # 898-99-9856
        r'\b\d{9}\b'               # 123456789
    ]
    found = set()
    for pattern in patterns:
        found.update(re.findall(pattern, text))
    return list(found)

def extract_docx_text(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_pdf_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_xlsx_text(path):
    xl = pd.ExcelFile(path)
    text = ""
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, dtype=str)
        text += df.fillna("").to_string() + "\n"
    return text

def process_attachment(filename, payload):
    ext = filename.lower().split('.')[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.'+ext) as tmp:
        tmp.write(payload)
        tmp_path = tmp.name
    try:
        if ext == 'docx':
            return extract_docx_text(tmp_path)
        elif ext == 'pdf':
            return extract_pdf_text(tmp_path)
        elif ext in ['xlsx', 'xls']:
            return extract_xlsx_text(tmp_path)
        else:
            return ""
    except Exception:
        return ""

def process_eml(eml_path, dlp_dict):
    results = []
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    subject = msg['subject'] or ""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()
    email_text = f"{subject}\n{body}"
    # DLP terms
    dlp_in_email = find_dlp_terms(email_text, dlp_dict)
    if dlp_in_email:
        results.append({"where": "[EMAIL_BODY]", "matches": dlp_in_email})
    # SSN
    ssns_in_email = find_ssn(email_text)
    if ssns_in_email:
        for ssn in ssns_in_email:
            results.append({"where": "[EMAIL_BODY]", "matches": [(ssn, "SSN")]})
    # Attachments
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if not filename:
            continue
        payload = part.get_payload(decode=True)
        attachment_text = process_attachment(filename, payload)
        dlp_in_attach = find_dlp_terms(attachment_text, dlp_dict)
        if dlp_in_attach:
            results.append({"where": filename, "matches": dlp_in_attach})
        ssns_in_attach = find_ssn(attachment_text)
        if ssns_in_attach:
            for ssn in ssns_in_attach:
                results.append({"where": filename, "matches": [(ssn, "SSN")]})
    return results

def main():
    if len(sys.argv) != 3:
        print("Usage: python dlp_email_scanner.py <SmartIDDictionaryTerms.xlsx> <emails_folder_or_eml_file>")
        sys.exit(1)
    dlp_dict_path = sys.argv[1]
    input_path = sys.argv[2]
    dlp_dict = load_dlp_dict(dlp_dict_path)
    if os.path.isdir(input_path):
        eml_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith('.eml')]
    elif os.path.isfile(input_path) and input_path.lower().endswith('.eml'):
        eml_files = [input_path]
    else:
        print("No .eml files found at the specified location.")
        sys.exit(1)
    for eml_file in eml_files:
        results = process_eml(eml_file, dlp_dict)
        if results:
            print(f"\n{os.path.basename(eml_file)}")
            for item in results:
                for term, category in item['matches']:
                    print(f"  {item['where']}: {term}  [category: {category}]")

if __name__ == "__main__":
    main()
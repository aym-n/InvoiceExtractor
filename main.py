import argparse
from pypdf import PdfReader
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory


parser = argparse.ArgumentParser(description="Extract information from an invoice")
parser.add_argument("input", type=str, help="Path to the invoice file, Supports PDF and Image files")
parser.add_argument("api_key", type=str, help="API key for the Google Generative AI API")
args = parser.parse_args()

genai.configure(api_key=args.api_key)

model = genai.GenerativeModel('gemini-1.5-pro', generation_config={"response_mime_type": "application/json"})
if args.input.endswith('.pdf'):
    #Process PDF Invoices
    print("Extracting information from the PDF file...")

    reader = PdfReader(args.input)
    text = reader.pages[0].extract_text()

    prompt = f"""
    You are an data extractor. 
    Please extract only the most relevant inofrmation and key phrases from a piece of text. 
    Please do not include any irrelevant information.
    The text to be extracted is as follows:

    {text}

    Extract the relevant information from the text.
    - Customer Details
        - Customer Name,
        - Billing Address,
        - Phone,
        - Email,
        - Shipping Address
    - Product Details
        - Description,
        -Quantity,
        -Rate,
        -Amount
    - Total Amount

    Returns a JSON object with the extracted information.
    """
    print("Generating JSON...")
    response = model.generate_content(prompt)
else:
    #Process Image Invoices
    print("Uploading image file...")
    image = genai.upload_file(path=args.input)

    prompt = f"""
    You are an data extractor.
    Please extract only the most relevant inofrmation and key phrases from the image
    Please do not include any irrelevant information.
    
    Extract the relevant information from the image.
    - Customer Details
        - Customer Name,
        - Billing Address,
        - Phone,
        - Email,
        - Shipping Address
    - Product Details
        - Description,
        -Quantity,
        -Rate,
        -Amount
    - Total Amount

    Returns a JSON object with the extracted information.
    """

    response = model.generate_content([image, prompt], safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    })

print(response.text)




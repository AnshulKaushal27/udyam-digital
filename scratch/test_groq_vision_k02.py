import os
import requests
import dotenv
import base64
import json

dotenv.load_dotenv('prototype/.env')
key = os.getenv('GROQ_API_KEY')

img_path = r"6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data\kyc_documents\K02_gst_certificate.png"
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

system_instructions = (
    "You are the Airtel Business Smart KYC Multimodal Document Verification Engine for India. "
    "Analyze this image and extract the following JSON fields: "
    "business_name, trade_name, gstin, address, signatory_name, issue_date, document_type_detected, is_relevant."
)

payload = {
    'model': 'qwen/qwen3.8-27b',
    'messages': [
        {'role': 'system', 'content': system_instructions},
        {'role': 'user', 'content': [
            {'type': 'text', 'text': 'Extract KYC fields from this GST certificate image. Return JSON strictly.'},
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}}
        ]}
    ],
    'response_format': {'type': 'json_object'},
    'temperature': 0.1
}

r = requests.post(
    'https://api.groq.com/openai/v1/chat/completions',
    headers={'Authorization': f'Bearer {key}'},
    json=payload,
    timeout=25
)

print('Status:', r.status_code)
if r.status_code == 200:
    print('Content:', r.json()['choices'][0]['message']['content'])
else:
    print('Error:', r.text)

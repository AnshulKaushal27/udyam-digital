import os
import requests
import dotenv
import io
import base64
from PIL import Image, ImageDraw

dotenv.load_dotenv('prototype/.env')
key = os.getenv('GROQ_API_KEY')

img = Image.new('RGB', (300, 150), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 50), "AIRTEL SMART KYC TEST", fill=(0, 0, 0))
buf = io.BytesIO()
img.save(buf, format='PNG')
b64 = base64.b64encode(buf.getvalue()).decode()

payload = {
    'model': 'qwen/qwen3.8-27b',
    'messages': [{
        'role': 'user',
        'content': [
            {'type': 'text', 'text': 'Read the text in this image. Return JSON: {"text": "..."}'},
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}}
        ]
    }],
    'response_format': {'type': 'json_object'}
}

r = requests.post(
    'https://api.groq.com/openai/v1/chat/completions',
    headers={'Authorization': f'Bearer {key}'},
    json=payload,
    timeout=20
)

print('Status:', r.status_code)
print('Response:', r.text)

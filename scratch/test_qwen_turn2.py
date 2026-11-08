import os, requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

load_dotenv('E:/Airtel/prototype/.env')
key = os.getenv('GROQ_API_KEY')

sys_prompt = """You are an experienced Airtel Business sales consultant in India.
You are chatting in real-time with an MSME merchant.

STRICT CONVERSATION RULES:
1. Output ONLY YOUR NEXT SINGLE MESSAGE (10 to 25 words).
2. NEVER simulate the customer or generate both sides of the dialogue.
3. NEVER ask more than ONE question.
4. If customer confirms GST invoices are needed, acknowledge and ask approximately how many invoices they generate per month.
"""

messages = [
    {'role': 'assistant', 'content': 'Understood, you use paper billing. Do you need GST-compliant invoices for your customers?'},
    {'role': 'user', 'content': 'Yes'}
]

headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
payload = {
    'model': 'qwen/qwen3.8-27b',
    'messages': [{'role': 'system', 'content': sys_prompt}] + messages,
    'temperature': 0.2,
    'max_tokens': 80
}

r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=payload)
print(r.json()['choices'][0]['message']['content'])

import os, requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

load_dotenv('E:/Airtel/prototype/.env')
key = os.getenv('GROQ_API_KEY')

sys_prompt = """You are an experienced Airtel Business sales consultant in India.
You are chatting in real-time with an MSME merchant.

STRICT CONVERSATION RULES:
1. Output ONLY YOUR NEXT SINGLE MESSAGE (15 to 35 words).
2. NEVER simulate the customer or generate both sides of the dialogue.
3. If customer specifies invoice volume (~300-400 bills), recommend Cloud POS & Billing (P19) at ₹599/month and explain why cloud is suitable.
"""

messages = [
    {'role': 'assistant', 'content': 'Great, GST invoices are essential. Approximately how many invoices do you generate per month?'},
    {'role': 'user', 'content': '300-400'}
]

headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
payload = {
    'model': 'qwen/qwen3.8-27b',
    'messages': [{'role': 'system', 'content': sys_prompt}] + messages,
    'temperature': 0.2,
    'max_tokens': 100
}

r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=payload)
print(r.json()['choices'][0]['message']['content'])

import os, requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

load_dotenv('E:/Airtel/prototype/.env')
key = os.getenv('GROQ_API_KEY')

sys_prompt = """You are an experienced Airtel Business sales consultant in India.
You are chatting in real-time with an MSME merchant.

STRICT CONVERSATION RULES:
1. Output ONLY YOUR NEXT SINGLE MESSAGE (15 to 30 words).
2. NEVER simulate the customer or generate both sides of the dialogue.
3. NEVER ask more than ONE question.
4. If customer says they use paper/manual billing, acknowledge and ask ONLY whether they need GST-compliant invoices.
5. On a new line, output ||META|| followed by single-line JSON:
{"profile_updates": {}, "quick_replies": ["Yes, GST invoices needed", "Simple non-GST is fine"], "discovery_complete": false}
"""

messages = [
    {'role': 'system', 'content': sys_prompt},
    {'role': 'assistant', 'content': 'Got it, you have 2-3 staff members. How do you currently create and send invoices—manually on paper, Excel, or using any software?'},
    {'role': 'user', 'content': 'Paper/manual'}
]

headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
payload = {
    'model': 'qwen/qwen3.8-27b',
    'messages': messages,
    'temperature': 0.2,
    'max_tokens': 120
}

r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=payload)
print(r.json()['choices'][0]['message']['content'])

import os, requests

api_key = os.environ.get('GROQ_API_KEY', '')
if not api_key:
    print('GROQ_API_KEY environment variable not set. Please set it before running this script.')
    exit(0)

res = requests.get('https://api.groq.com/openai/v1/models', headers={'Authorization': f'Bearer {api_key}'})
if res.status_code == 200:
    models = [m['id'] for m in res.json()['data'] if 'vision' in m['id'].lower() or 'ocr' in m['id'].lower()]
    print('Vision models on Groq:', models)
    for m in res.json()['data']:
        print(f" - {m['id']}")
else:
    print('Error:', res.status_code, res.text)

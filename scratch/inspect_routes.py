import re
with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'@app\.route\([\'"][^\'"]*[\'"]', text)
for m in matches:
    if 'register' in m or 'auth' in m or 'signup' in m or 'customer' in m:
        print(m)

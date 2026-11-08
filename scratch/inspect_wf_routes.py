import re
with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'@app\.route\([\'"][^\'"]*workflow[^\'"]*[\'"]', text)
for m in matches:
    print(m)

with open('e:/Airtel/prototype/flask_log.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for line in text.splitlines()[-40:]:
    print(line.encode('ascii', 'replace').decode('ascii'))

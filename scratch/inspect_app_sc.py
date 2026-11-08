with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('# Apply validated state changes')
print(text[pos:pos+2500].encode('ascii', 'replace').decode('ascii'))

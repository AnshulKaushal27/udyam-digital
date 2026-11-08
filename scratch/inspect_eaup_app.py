with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def extract_and_update_profile')
print(text[pos+2000:pos+4000].encode('ascii', 'replace').decode('ascii'))

with open('e:/Airtel/prototype/recommendation_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('MODULAR_ADDONS')
print(text[pos+2000:pos+4000].encode('ascii', 'replace').decode('ascii'))

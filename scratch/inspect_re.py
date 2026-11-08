with open('e:/Airtel/prototype/recommendation_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def calculate_quote_pricing')
print(text[pos:pos+3500].encode('ascii', 'replace').decode('ascii'))

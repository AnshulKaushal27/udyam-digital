with open('e:/Airtel/prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Does your shop rely heavily on UPI')
print(text[pos-1000:pos+1000].encode('ascii', 'replace').decode('ascii'))

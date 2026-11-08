with open('e:/Airtel/prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('# 3. Remove Add-on Intent')
print(text[pos:pos+3500].encode('ascii', 'replace').decode('ascii'))

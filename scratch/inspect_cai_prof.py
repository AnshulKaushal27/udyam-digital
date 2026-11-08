with open('e:/Airtel/prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def extract_and_update_profile')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))

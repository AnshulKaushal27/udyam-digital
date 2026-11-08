with open('e:/Airtel/prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('additions available')
if pos == -1: pos = text.find('aur kya')
print(text[pos-100:pos+1500].encode('ascii', 'replace').decode('ascii'))

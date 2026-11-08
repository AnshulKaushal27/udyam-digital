with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('if session.get("billing_intent", {}).get("active"):')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))

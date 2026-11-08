with open('e:/Airtel/prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def interpret_user_intent_fallback')
print(text[pos+11500:pos+15500].encode('ascii', 'replace').decode('ascii'))

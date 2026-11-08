with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('"recommendation_prompt"')
print(text[pos-100:pos+500].encode('ascii', 'replace').decode('ascii'))

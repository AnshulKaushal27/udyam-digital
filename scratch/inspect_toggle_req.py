with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('action == "TOGGLE_REQUIREMENT"')
print(text[pos-100:pos+3500].encode('ascii', 'replace').decode('ascii'))

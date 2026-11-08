with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('elif action == "ADD_REQUIREMENT":')
print(text[pos:pos+3500].encode('ascii', 'replace').decode('ascii'))

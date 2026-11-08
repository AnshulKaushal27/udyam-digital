with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('action == "SELECT_CATEGORY"')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))

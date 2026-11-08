with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('action == "GO_TO_STAGE"')
print(text[pos+1000:pos+2500].encode('ascii', 'replace').decode('ascii'))

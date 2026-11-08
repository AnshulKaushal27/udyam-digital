with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('elif action == "ADD_REQUIREMENT":')
pos4 = text.find('elif action == "GO_TO_STAGE":')
print(text[pos1:pos4].encode('ascii', 'replace').decode('ascii'))

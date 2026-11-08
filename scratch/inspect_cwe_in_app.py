with open("e:/Airtel/prototype/app.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("from customer_workflow_engine import")
print(text[pos:pos+500].encode('ascii', 'replace').decode('ascii'))

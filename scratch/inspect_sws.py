with open("e:/Airtel/prototype/app.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("def sync_workflow_to_session(")
print(text[pos+1500:pos+3500].encode('ascii', 'replace').decode('ascii'))

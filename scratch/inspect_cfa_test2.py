with open("e:/Airtel/prototype/test_conversational_first_audit.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('assert "P15" in wf["recommendation"]["active_addons"]')
print(text[pos-400:pos+300].encode('ascii', 'replace').decode('ascii'))

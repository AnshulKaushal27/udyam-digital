with open("e:/Airtel/prototype/recommendation_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('bundle_kirana = {')
if pos == -1: pos = text.find('"bundle_kirana": {')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))

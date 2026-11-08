with open("e:/Airtel/prototype/conversational_ai.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("def parse_quote_action_intent(")
pos_rem = text.find("# 3. Remove Add-on Intent", pos)
print(text[pos_rem:pos_rem+2000].encode('ascii', 'replace').decode('ascii'))

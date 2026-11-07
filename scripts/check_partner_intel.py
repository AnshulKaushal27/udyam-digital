with open('E:/Airtel/prototype/operations_intelligence.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def get_partner_intelligence')
print(text[pos:pos+700])

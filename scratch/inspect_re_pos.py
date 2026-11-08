with open('e:/Airtel/prototype/recommendation_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_cqp = text.find('def calculate_quote_pricing(')
print(text[pos_cqp+1800:pos_cqp+2700].encode('ascii', 'replace').decode('ascii'))

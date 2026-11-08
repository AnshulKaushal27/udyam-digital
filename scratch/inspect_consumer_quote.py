with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('stage === "PLAN_EXPLORATION"')
print(text[pos+2000:pos+5500].encode('ascii', 'replace').decode('ascii'))

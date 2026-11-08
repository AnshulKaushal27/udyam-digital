with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('stage === "REQUIREMENTS_COLLECTION"')
print(text[pos:pos+3000].encode('ascii', 'replace').decode('ascii'))

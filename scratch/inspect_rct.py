with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function renderChatThread')
print(text[pos:pos+2500].encode('ascii', 'replace').decode('ascii'))

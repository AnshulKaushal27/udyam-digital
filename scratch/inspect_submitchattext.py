with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function submitChatText')
print(text[pos:pos+1000].encode('ascii', 'replace').decode('ascii'))

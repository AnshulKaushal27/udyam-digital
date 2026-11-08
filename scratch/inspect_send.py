with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function handleChatSubmit')
if pos == -1:
    pos = text.find('handleChatSubmit')
print(text[pos-100:pos+2500].encode('ascii', 'replace').decode('ascii'))

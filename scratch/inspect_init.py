with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('window.onload')
if pos == -1:
    pos = text.find('DOMContentLoaded')
if pos == -1:
    pos = text.find('activeSessionId')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))

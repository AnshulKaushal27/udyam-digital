with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Kirana Digital Starter')
while pos != -1:
    print('Found Kirana Digital Starter at:', pos)
    print(text[max(0, pos-100):min(len(text), pos+300)].encode('ascii', 'replace').decode('ascii'))
    pos = text.find('Kirana Digital Starter', pos+1)

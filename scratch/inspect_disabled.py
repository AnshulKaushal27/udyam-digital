with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'chatSendBtn|composerBtn|disabled', text)]
for pos in matches:
    print('--- MATCH AT', pos, '---')
    print(text[max(0, pos-40):min(len(text), pos+100)].encode('ascii', 'replace').decode('ascii'))

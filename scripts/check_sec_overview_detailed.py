import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="sec-overview"')
end = text.find('</section>', pos)
print(text[pos:pos+1500])

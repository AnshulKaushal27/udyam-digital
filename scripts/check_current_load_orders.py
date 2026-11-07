import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function loadLiveOrders() {')
end = text.find('\n    }', pos)
print(text[pos:end+6])

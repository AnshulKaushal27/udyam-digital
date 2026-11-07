with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'</script>', text)]
print("</script> positions:", matches)
for pos in matches:
    print(repr(text[pos-30:pos+9]))

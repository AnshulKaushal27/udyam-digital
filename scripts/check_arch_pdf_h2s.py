with open('E:/Airtel/scripts/generate_architecture_pdf.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
h2s = re.findall(r'<h2>([^<]+)</h2>', text)
print("H2 tags in generate_architecture_pdf.py:", h2s)

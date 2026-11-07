with open('E:/Airtel/scripts/test_dual_portals.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
tests = re.findall(r'def test_[^\(]+', text)
print("Tests in test_dual_portals.py:", tests)

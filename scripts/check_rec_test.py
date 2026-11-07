with open('E:/Airtel/scripts/test_recommendation_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:80]):
    if 'requests.' in l or 'BASE_URL' in l or 'api/' in l:
        print(f"{i+1}: {l.strip()}")

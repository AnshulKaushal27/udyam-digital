with open('E:/Airtel/scripts/test_recommendation_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[80:200]):
    if 'requests.' in l or 'api/' in l:
        print(f"{i+81}: {l.strip()}")

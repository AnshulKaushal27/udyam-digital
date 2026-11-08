log_path = r"C:\Users\anshu\.gemini\antigravity\brain\5e137ddb-86ce-4667-9f92-fa20f6bc18cd\.system_generated\tasks\task-4074.log"
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for line in lines[-30:]:
    print(line.strip().encode('ascii', 'replace').decode('ascii'))

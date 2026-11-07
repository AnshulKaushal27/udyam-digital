with open('E:/Airtel/submission/Solution_Architecture_and_Data_Flows.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("File length:", len(text))
# Check if Phase 6 or Operations Intelligence is mentioned
print("Operations Intelligence in doc:", "Operations Intelligence" in text or "Phase 6" in text)

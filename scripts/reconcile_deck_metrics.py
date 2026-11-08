with open(r'E:\Airtel\scripts\generate_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    top_metrics = [
        ("Lead Conversion", "7.36% -> 25.0%", "+240% lift via pricing & recovery", GREEN),
        ("Activation TAT", "17.6d -> 2.8 Days", "-84% via Smart KYC & pre-feasibility", RED),
        ("Blended CAC", "Rs 15,000 -> Rs 6,850", "-54.3% via digital self-serve", GOLD),
        ("Chase Calls", "3.01 -> 0.2 Calls", "-93% via proactive milestone tracking", NAVY)
    ]"""

replacement = """    top_metrics = [
        ("Lead Conversion", "7.36% -> 22.0%", "+199% lift via pricing & recovery", GREEN),
        ("Activation TAT", "17.6d -> 3.5 Days", "-80.1% via Smart KYC & pre-feasibility", RED),
        ("Blended CAC", "Rs 15,000 -> Rs 3,800", "-74.7% via digital self-serve", GOLD),
        ("Chase Calls", "3.01 -> <0.2 Calls", "-93.3% via proactive milestone tracking", NAVY)
    ]"""

assert target in text, "target not found in generate_deck.py"
text = text.replace(target, replacement, 1)

with open(r'E:\Airtel\scripts\generate_deck.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated generate_deck.py with canonical master targets successfully")

import re

with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract script tags
scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
print(f"Found {len(scripts)} script tags")

# Let's write the main script to a js file and run node to validate syntax
with open('e:/Airtel/scratch/consumer_test.js', 'w', encoding='utf-8') as f:
    f.write(scripts[0])

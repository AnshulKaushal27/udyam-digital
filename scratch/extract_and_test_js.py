import re

with open("prototype/templates/consumer.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract script block
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")

# Let's inspect the main script block
main_script = scripts[0]
with open("scratch/consumer_extracted.js", "w", encoding="utf-8") as f:
    f.write(main_script)

print("Saved scratch/consumer_extracted.js, size:", len(main_script))

import subprocess

p = subprocess.run(["git", "diff", "prototype/templates/consumer.html"], capture_output=True)
diff_text = p.stdout.decode("utf-8", errors="replace")
for line in diff_text.splitlines():
    if "quick_replies" in line or "quickBox" in line or "quick-chip" in line or "undefined" in line:
        print(line[:120])

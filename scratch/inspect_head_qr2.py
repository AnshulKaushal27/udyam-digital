import subprocess

p = subprocess.run(["git", "show", "HEAD:prototype/templates/consumer.html"], capture_output=True)
text = p.stdout.decode("utf-8", errors="replace")

pos = text.find("function renderQuickReplies")
if pos != -1:
    print(text[pos:pos+1500])

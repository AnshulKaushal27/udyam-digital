with open(r'prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS for .chat-thread
style_target = '    .chat-body {'
style_replacement = '''    .chat-thread {
      max-height: 480px;
      overflow-y: auto;
    }

    .chat-body {'''

assert style_target in text, "style_target not found"
text = text.replace(style_target, style_replacement, 1)

# 2. Add smartScrollChat function
script_target = '    function renderChatThread() {'
script_replacement = '''    function smartScrollChat() {
      const chat = document.querySelector(".chat-thread") || document.getElementById("chatBody");
      if (chat) {
        chat.scrollTop = chat.scrollHeight;
      }
    }

    function renderChatThread() {'''

assert script_target in text, "script_target not found"
text = text.replace(script_target, script_replacement, 1)

# 3. Call smartScrollChat at end of renderChatThread
scroll_call_target = 'quickBox.style.display = quickBox.children.length > 0 ? "flex" : "none";'
scroll_call_replacement = '''quickBox.style.display = quickBox.children.length > 0 ? "flex" : "none";
      smartScrollChat();'''

assert scroll_call_target in text, "scroll_call_target not found"
text = text.replace(scroll_call_target, scroll_call_replacement, 1)

with open(r'prototype/templates/consumer.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added .chat-thread CSS and smartScrollChat to consumer.html successfully")

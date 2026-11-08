"""Add frontend runaway dialogue guardrail to consumer.html."""
with open(r'E:\Airtel\prototype\templates\consumer.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        cursorSpan.remove();
        accumulatedAssistantText = accumulatedAssistantText.replace(/\|+META\|+[\s\S]*$/, "").trim().replace(/\|+$/, "").trim();
        streamBubble.innerHTML = escapeHtml(accumulatedAssistantText);
        conversationHistory.push({ role: "assistant", content: accumulatedAssistantText });'''

replacement = '''        cursorSpan.remove();
        accumulatedAssistantText = accumulatedAssistantText.replace(/\|+META\|+[\s\S]*$/, "").trim().replace(/\|+$/, "").trim();
        if (accumulatedAssistantText.indexOf("?") !== -1) {
          const qParts = accumulatedAssistantText.split("?");
          if (qParts.length > 2 && qParts[1].length > 10) {
            accumulatedAssistantText = qParts[0].trim() + "?";
          }
        }
        streamBubble.innerHTML = escapeHtml(accumulatedAssistantText);
        conversationHistory.push({ role: "assistant", content: accumulatedAssistantText });'''

content_clean = content.replace('\r\n', '\n')
target_clean = target.replace('\r\n', '\n')
replacement_clean = replacement.replace('\r\n', '\n')

assert target_clean in content_clean, "Target not found in consumer.html"
content_clean = content_clean.replace(target_clean, replacement_clean, 1)

with open(r'E:\Airtel\prototype\templates\consumer.html', 'w', encoding='utf-8') as f:
    f.write(content_clean)

print("consumer.html guardrail added successfully!")

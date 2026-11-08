with open(r'e:\Airtel\prototype\templates\consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """      // Quick Replies from last message (robustly handles both string lists and structured action objects)
      const lastMsg = msgs[msgs.length - 1];
      const quickBox = document.getElementById("chatQuickReplies");
      quickBox.innerHTML = "";
      if (lastMsg && lastMsg.quick_replies && Array.isArray(lastMsg.quick_replies) && lastMsg.quick_replies.length > 0) {
        lastMsg.quick_replies.forEach(q => {
          let labelText = "";
          let actionName = null;
          let payloadValue = null;

          if (typeof q === "string") {
            labelText = q.trim();
          } else if (q && typeof q === "object") {
            labelText = (q.label || q.text || q.title || q.value || "").trim();
            actionName = q.action || null;
            payloadValue = q.value !== undefined ? q.value : labelText;
          }

          // Strict guard against any "undefined" or blank buttons
          if (!labelText || labelText === "undefined" || labelText === "null") return;

          const btn = document.createElement("button");
          btn.className = "quick-chip";
          btn.type = "button";
          btn.innerText = labelText;

          btn.onclick = () => {
            if (actionName) {
              dispatchWorkflowTransition(actionName, {
                label: labelText,
                value: payloadValue,
                category: payloadValue,
                requirement: payloadValue,
                status: payloadValue,
                user_type: payloadValue,
                stage: payloadValue
              });
            } else {
              submitChatText(labelText);
            }
          };

          quickBox.appendChild(btn);
        });
      }"""

replacement = """      // Quick Replies from last message (robustly handles string lists, structured action objects, and hides empty chips)
      const lastMsg = msgs[msgs.length - 1];
      const quickBox = document.getElementById("chatQuickReplies");
      quickBox.innerHTML = "";
      if (lastMsg && lastMsg.quick_replies && Array.isArray(lastMsg.quick_replies) && lastMsg.quick_replies.length > 0) {
        lastMsg.quick_replies.forEach(q => {
          let labelText = "";
          let actionName = null;
          let payloadValue = null;

          if (typeof q === "string") {
            labelText = q.trim();
          } else if (q && typeof q === "object") {
            labelText = (q.label || q.text || q.title || q.name || q.caption || q.value || "").toString().trim();
            actionName = q.action || null;
            payloadValue = q.value !== undefined ? q.value : labelText;
          }

          // Strict guard against any "undefined", "null", "[object Object]", or blank buttons
          if (!labelText || labelText === "undefined" || labelText === "null" || labelText === "[object Object]") return;

          const btn = document.createElement("button");
          btn.className = "quick-chip";
          btn.type = "button";
          btn.innerText = labelText;

          btn.onclick = () => {
            if (actionName) {
              dispatchWorkflowTransition(actionName, {
                label: labelText,
                value: payloadValue,
                category: payloadValue,
                requirement: payloadValue,
                status: payloadValue,
                user_type: payloadValue,
                stage: payloadValue
              });
            } else {
              submitChatText(labelText);
            }
          };

          quickBox.appendChild(btn);
        });
      }
      quickBox.style.display = quickBox.children.length > 0 ? "flex" : "none";"""

assert target in text, 'Target not found in consumer.html'
text = text.replace(target, replacement, 1)

with open(r'e:\Airtel\prototype\templates\consumer.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated quick reply rendering in consumer.html successfully')

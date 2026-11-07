"""Update consumer.html with language sync, indecision support, and scroll fixes."""
with open(r'E:\Airtel\prototype\templates\consumer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update language selector options
old_select = '''          <select id="userLang" class="form-select form-select-sm border-0 bg-transparent fw-medium" style="width: 105px; font-size: 0.85rem;" onchange="onLanguageChange()">
            <option value="en" selected>English</option>
            <option value="hi">हिन्दी</option>
            <option value="hinglish">Hinglish</option>
          </select>'''

new_select = '''          <select id="userLang" class="form-select form-select-sm border-0 bg-transparent fw-medium" style="width: 110px; font-size: 0.85rem;" onchange="onLanguageChange()">
            <option value="en" selected>English</option>
            <option value="hi">हिन्दी</option>
            <option value="pa">ਪੰਜਾਬੀ</option>
            <option value="hinglish">Hinglish</option>
          </select>'''

assert old_select in content, "old_select not found"
content = content.replace(old_select, new_select, 1)

# 2. Update .chat-thread CSS to be a dedicated scroll container
old_chat_thread_css = '''    /* Chat Messages Thread */
    .chat-thread {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 18px;
      min-height: 140px;
    }'''

new_chat_thread_css = '''    /* Chat Messages Thread */
    .chat-thread {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 18px;
      min-height: 140px;
      max-height: 480px;
      overflow-y: auto;
      overflow-x: hidden;
      padding-right: 4px;
      scroll-behavior: smooth;
    }
    .chat-thread::-webkit-scrollbar {
      width: 5px;
    }
    .chat-thread::-webkit-scrollbar-thumb {
      background: rgba(0,0,0,0.18);
      border-radius: 4px;
    }'''

assert old_chat_thread_css in content, "old_chat_thread_css not found"
content = content.replace(old_chat_thread_css, new_chat_thread_css, 1)

# 3. Add smartScrollChat function and update appendBubbleDOM and sendUserMessage
old_append_bubble = '''    function appendBubbleDOM(role, content) {
      const box = document.getElementById("chatThread");
      const row = document.createElement("div");
      row.className = `msg-row ${role === 'user' ? 'user' : 'advisor'}`;
      
      const bubble = document.createElement("div");
      bubble.className = `msg-bubble ${role === 'user' ? 'user' : 'advisor'}`;
      bubble.innerHTML = escapeHtml(content);
      
      row.appendChild(bubble);
      box.appendChild(row);
      return bubble;
    }'''

new_append_bubble = '''    function smartScrollChat(force = false) {
      const box = document.getElementById("chatThread");
      if (!box) return;
      const isNearBottom = box.scrollHeight - box.scrollTop - box.clientHeight < 120;
      if (force || isNearBottom) {
        box.scrollTop = box.scrollHeight;
      }
    }

    function appendBubbleDOM(role, content) {
      const box = document.getElementById("chatThread");
      const row = document.createElement("div");
      row.className = `msg-row ${role === 'user' ? 'user' : 'advisor'}`;
      
      const bubble = document.createElement("div");
      bubble.className = `msg-bubble ${role === 'user' ? 'user' : 'advisor'}`;
      bubble.innerHTML = escapeHtml(content);
      
      row.appendChild(bubble);
      box.appendChild(row);
      smartScrollChat(role === 'user');
      return bubble;
    }'''

assert old_append_bubble in content, "old_append_bubble not found"
content = content.replace(old_append_bubble, new_append_bubble, 1)

# 4. Update streaming chunk handling to smart-scroll
old_chunk_handling = '''                if (eventData.type === "chunk") {
                  accumulatedAssistantText += eventData.text;
                  // Update text node before cursor
                  cursorSpan.remove();
                  streamBubble.innerHTML = escapeHtml(accumulatedAssistantText);
                  streamBubble.appendChild(cursorSpan);
                }'''

new_chunk_handling = '''                if (eventData.type === "chunk") {
                  accumulatedAssistantText += eventData.text;
                  // Update text node before cursor
                  cursorSpan.remove();
                  streamBubble.innerHTML = escapeHtml(accumulatedAssistantText);
                  streamBubble.appendChild(cursorSpan);
                  smartScrollChat(false);
                }'''

assert old_chunk_handling in content, "old_chunk_handling not found"
content = content.replace(old_chunk_handling, new_chunk_handling, 1)

# 5. Update metaPayload handling to synchronize language dynamically
old_meta_process = '''        // Process Meta Payload
        if (metaPayload) {
          if (metaPayload.session_id) {
            currentSessionId = metaPayload.session_id;
            localStorage.setItem("udyam_session_id", currentSessionId);
          }'''

new_meta_process = '''        // Process Meta Payload
        if (metaPayload) {
          if (metaPayload.detected_language) {
            const langSelect = document.getElementById("userLang");
            if (langSelect && langSelect.value !== metaPayload.detected_language) {
              langSelect.value = metaPayload.detected_language;
              userProfile.language = metaPayload.detected_language;
              localStorage.setItem("udyam_lang", metaPayload.detected_language);
            }
          }
          if (metaPayload.session_id) {
            currentSessionId = metaPayload.session_id;
            localStorage.setItem("udyam_session_id", currentSessionId);
          }'''

assert old_meta_process in content, "old_meta_process not found"
content = content.replace(old_meta_process, new_meta_process, 1)

# 6. Remove panel.scrollIntoView at line 1918 (the auto-scroll bug!)
old_scroll_rec = '''      const panel = document.getElementById("recPanel");
      panel.style.display = "block";
      panel.scrollIntoView({ behavior: "smooth", block: "nearest" });'''

new_scroll_rec = '''      const panel = document.getElementById("recPanel");
      panel.style.display = "block";
      // Auto-scroll removed: Persistent recommendation updates in place without moving user away from chat'''

assert old_scroll_rec in content, "old_scroll_rec not found"
content = content.replace(old_scroll_rec, new_scroll_rec, 1)

# 7. Update onLanguageChange and DOMContentLoaded to preserve history
old_on_lang_change = '''    function onLanguageChange() {
      const lang = document.getElementById("userLang").value;
      userProfile.language = lang;
      // Re-prime conversation in the new language
      initConversation(activeCategory);
    }'''

new_on_lang_change = '''    function onLanguageChange() {
      const lang = document.getElementById("userLang").value;
      userProfile.language = lang;
      localStorage.setItem("udyam_lang", lang);

      // Persist to backend active session without wiping context or history
      if (currentSessionId) {
        fetch("/api/advisor/session/language", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: currentSessionId, language: lang })
        }).catch(() => {});
      }

      // If customer has not started chatting yet, re-render starter greeting in new language
      const userMsgs = conversationHistory.filter(m => m.role === "user");
      if (userMsgs.length === 0) {
        initConversation(activeCategory);
      }
    }'''

assert old_on_lang_change in content, "old_on_lang_change not found"
content = content.replace(old_on_lang_change, new_on_lang_change, 1)

# 8. Restore language from localStorage on load
old_dom_load = '''    // Initialize on load
    window.addEventListener("DOMContentLoaded", () => {
      checkPartnerReferral();
      checkRecoveryReentry();
      initConversation(activeCategory);
    });'''

new_dom_load = '''    // Initialize on load
    window.addEventListener("DOMContentLoaded", () => {
      const savedLang = localStorage.getItem("udyam_lang");
      if (savedLang && ["en", "hi", "pa", "hinglish"].includes(savedLang)) {
        const langEl = document.getElementById("userLang");
        if (langEl) langEl.value = savedLang;
        userProfile.language = savedLang;
      }
      checkPartnerReferral();
      checkRecoveryReentry();
      initConversation(activeCategory);
    });'''

assert old_dom_load in content, "old_dom_load not found"
content = content.replace(old_dom_load, new_dom_load, 1)

with open(r'E:\Airtel\prototype\templates\consumer.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("consumer.html successfully updated with language sync, indecision support, and scroll fix!")

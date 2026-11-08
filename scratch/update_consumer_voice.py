with open(r'e:\Airtel\prototype\templates\consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add voice button
target_form = '''        <!-- Message Composer Form -->
        <form class="chat-input-bar" id="chatForm" onsubmit="handleChatSubmit(event); return false;">
          <input type="text" id="chatInput" class="chat-input-field" placeholder="Type here or use GUI controls on left..." autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();handleChatSubmit(event);}">
          <button type="button" id="chatSendBtn" class="chat-send-btn" onclick="handleChatSubmit(event)" aria-label="Send message or proceed">
            <span>Send</span> <i class="bi bi-send-fill fs-6"></i>
          </button>
        </form>'''

replacement_form = '''        <!-- Message Composer Form with Speech/Voice Input & Typed Fallback -->
        <form class="chat-input-bar" id="chatForm" onsubmit="handleChatSubmit(event); return false;">
          <input type="text" id="chatInput" class="chat-input-field" placeholder="Type here or use GUI controls on left..." autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();handleChatSubmit(event);}">
          <button type="button" id="voiceInputBtn" class="btn btn-sm btn-light border rounded-pill px-2 py-1 me-1 d-inline-flex align-items-center justify-content-center" onclick="toggleVoiceInput()" title="Voice Input (Speech-to-Text in Hindi/English)" aria-label="Voice input">
            <i class="bi bi-mic-fill text-danger fs-6" id="voiceMicIcon"></i>
          </button>
          <button type="button" id="chatSendBtn" class="chat-send-btn" onclick="handleChatSubmit(event)" aria-label="Send message or proceed">
            <span>Send</span> <i class="bi bi-send-fill fs-6"></i>
          </button>
        </form>'''

assert target_form in text, "target_form not found in consumer.html"
text = text.replace(target_form, replacement_form, 1)

# 2. Add speech recognition JS handler
target_js = 'function submitChatText(text) {'

voice_js = '''let speechRecognitionInstance = null;
    let isRecordingVoice = false;

    function toggleVoiceInput() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("[Browser Compatibility] Speech Recognition is not supported by your current browser engine. Typed input remains fully active as the standard input method. (Recommended: Google Chrome or Microsoft Edge).");
        return;
      }

      const micIcon = document.getElementById("voiceMicIcon");
      const input = document.getElementById("chatInput");

      if (isRecordingVoice && speechRecognitionInstance) {
        speechRecognitionInstance.stop();
        return;
      }

      try {
        speechRecognitionInstance = new SpeechRecognition();
        speechRecognitionInstance.continuous = false;
        speechRecognitionInstance.interimResults = false;
        speechRecognitionInstance.lang = (activeLanguage === "hi") ? "hi-IN" : ((activeLanguage === "pa") ? "pa-IN" : "en-IN");

        speechRecognitionInstance.onstart = () => {
          isRecordingVoice = true;
          if (micIcon) {
            micIcon.classList.remove("text-danger");
            micIcon.classList.add("text-success", "animate__animated", "animate__pulse", "animate__infinite");
          }
          if (input) input.placeholder = "Listening... Speak in " + (activeLanguage === "hi" ? "Hindi" : "English") + "...";
        };

        speechRecognitionInstance.onresult = (event) => {
          if (event.results && event.results[0] && event.results[0][0]) {
            const transcript = event.results[0][0].transcript;
            if (input) {
              input.value = transcript;
              input.focus();
            }
          }
        };

        speechRecognitionInstance.onerror = (event) => {
          console.warn("Speech recognition notice:", event.error);
          if (input) input.placeholder = "Type here or use GUI controls on left...";
          if (event.error === "not-allowed" || event.error === "permission-denied") {
            alert("[Microphone Permission] Microphone access was blocked. Please permit microphone access in browser settings, or continue with keyboard input.");
          }
        };

        speechRecognitionInstance.onend = () => {
          isRecordingVoice = false;
          if (micIcon) {
            micIcon.classList.remove("text-success", "animate__animated", "animate__pulse", "animate__infinite");
            micIcon.classList.add("text-danger");
          }
          if (input) input.placeholder = "Type here or use GUI controls on left...";
        };

        speechRecognitionInstance.start();
      } catch (err) {
        console.error("Speech recognition error:", err);
        alert("[Voice Fallback] Could not initiate voice input. Keyboard input is ready.");
      }
    }

    function submitChatText(text) {'''

assert target_js in text, "target_js not found in consumer.html"
text = text.replace(target_js, voice_js, 1)

# 3. Update simulated notification text
target_sms = 'subEl.innerText = "Zero status-chase guarantee with automatic SMS and WhatsApp alerts.";'
replacement_sms = 'subEl.innerText = "Zero status-chase guarantee with live milestone tracking (simulated prototype SMS/WhatsApp push notifications).";'
assert target_sms in text, "target_sms not found in consumer.html"
text = text.replace(target_sms, replacement_sms, 1)

with open(r'e:\Airtel\prototype\templates\consumer.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated consumer.html with browser voice input, typed fallback, and simulated notification disclosures successfully!")

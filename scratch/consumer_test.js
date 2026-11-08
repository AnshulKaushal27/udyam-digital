
    // 1. Session & Workflow Initialization
    let activeSessionId = localStorage.getItem("udyam_session_id");
    if (!activeSessionId) {
      activeSessionId = "sess_" + Math.random().toString(36).substring(2, 12);
      localStorage.setItem("udyam_session_id", activeSessionId);
    }

    let activeWorkflow = null;
    let activeLanguage = "en";

    // 2. Audio & UPI Payment Chime Engine
    let upiAudioCtx = null;
    let hasTransitioned = false;

    function getAudioContext() {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return null;
        if (!upiAudioCtx) {
          upiAudioCtx = new AudioCtx();
        }
        if (upiAudioCtx.state === 'suspended') {
          upiAudioCtx.resume();
        }
        return upiAudioCtx;
      } catch (e) {
        return null;
      }
    }

    // Passive unlock listener on first user interaction anywhere
    ['pointerdown', 'keydown', 'touchstart', 'click'].forEach(evt => {
      window.addEventListener(evt, () => {
        getAudioContext();
      }, { once: true, passive: true });
    });

    function playUpiPaymentChime() {
      // 1. Play dedicated soundbox audio file
      try {
        const audioEl = document.getElementById("upiChimeAudio");
        if (audioEl) {
          audioEl.currentTime = 0;
          const promise = audioEl.play();
          if (promise !== undefined) {
            promise.catch(err => {
              console.log("HTML5 audio autoplay deferred, falling back to WebAudio synth:", err);
            });
          }
        }
      } catch (err) {
        console.log("Audio tag playback error:", err);
      }

      // 2. Synthesize studio-grade UPI payment confirmation chime via Web Audio API
      // Four ascending crystal tones: C6 (1046.5Hz) -> E6 (1318.5Hz) -> G6 (1568Hz) -> C7 (2093Hz) shimmer
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;

        const chimeNotes = [
          { freq: 1046.50, start: 0.00, dur: 0.22, gain: 0.25 }, // C6
          { freq: 1318.51, start: 0.09, dur: 0.25, gain: 0.28 }, // E6
          { freq: 1567.98, start: 0.18, dur: 0.30, gain: 0.32 }, // G6
          { freq: 2093.00, start: 0.30, dur: 0.70, gain: 0.38 }  // C7 crystal shimmer
        ];

        chimeNotes.forEach(n => {
          const osc = ctx.createOscillator();
          const gainNode = ctx.createGain();

          osc.type = "sine";
          osc.frequency.setValueAtTime(n.freq, now + n.start);

          gainNode.gain.setValueAtTime(0.0001, now + n.start);
          gainNode.gain.linearRampToValueAtTime(n.gain, now + n.start + 0.012);
          gainNode.gain.exponentialRampToValueAtTime(0.0001, now + n.start + n.dur);

          osc.connect(gainNode);
          gainNode.connect(ctx.destination);

          osc.start(now + n.start);
          osc.stop(now + n.start + n.dur + 0.05);
        });

        // Acoustic soundbox body resonance (523.25Hz C5)
        const subOsc = ctx.createOscillator();
        const subGain = ctx.createGain();
        subOsc.type = "triangle";
        subOsc.frequency.setValueAtTime(523.25, now + 0.30);
        subGain.gain.setValueAtTime(0.0001, now + 0.30);
        subGain.gain.linearRampToValueAtTime(0.12, now + 0.32);
        subGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.90);
        subOsc.connect(subGain);
        subGain.connect(ctx.destination);
        subOsc.start(now + 0.30);
        subOsc.stop(now + 0.95);

      } catch (err) {
        console.warn("WebAudio chime synthesis error:", err);
      }
    }

    // 3. Intro Animation Orchestration (Stays for 1 second, then transitions with chime)
    function checkIntroState() {
      // Opening animation stays for 1 second (1000ms), then transitions to the workspace
      setTimeout(() => {
        if (!hasTransitioned) {
          startAppExperience();
        }
      }, 1000);
    }

    function startAppExperience() {
      if (hasTransitioned) return;
      hasTransitioned = true;

      // Play the UPI payment confirmation / soundbox chime right as transition starts!
      playUpiPaymentChime();

      const morphLogo = document.getElementById("morphLogo");
      const introOverlay = document.getElementById("introOverlay");
      
      // Step 3: Logo Transition to Top-Left Header Slot
      morphLogo.classList.add("morphed");
      
      // Fade out overlay and reveal conversational workspace
      setTimeout(() => {
        introOverlay.classList.add("hidden");
        initWorkflow();
      }, 650);
    }

    function skipIntroDirectly() {
      hasTransitioned = true;
      document.getElementById("introOverlay").classList.add("hidden");
      document.getElementById("morphLogo").classList.add("morphed");
      initWorkflow();
    }

    function replayIntro() {
      hasTransitioned = false;
      const morphLogo = document.getElementById("morphLogo");
      const introOverlay = document.getElementById("introOverlay");
      morphLogo.classList.remove("morphed");
      introOverlay.classList.remove("hidden");

      // Stays for 1 second, then triggers transition and UPI chime
      setTimeout(() => {
        if (!hasTransitioned) {
          startAppExperience();
        }
      }, 1000);
    }

    // 3. Central Authoritative Workflow Sync
    async function initWorkflow() {
      try {
        const res = await fetch(`/api/workflow/state/${activeSessionId}`);
        const data = await res.json();
        if (data.status === "success") {
          activeWorkflow = data.workflow;
          activeLanguage = activeWorkflow.language || "en";
          document.getElementById("appLanguageSelect").value = activeLanguage;
          document.getElementById("chatSessionBadge").innerText = activeSessionId.substring(0, 10).toUpperCase();
          renderWorkflow();
        }
      } catch (e) {
        console.error("Error fetching workflow state:", e);
      }
    }

    async function dispatchWorkflowTransition(action, payload = {}) {
      if (action === "LAUNCH_EMPLOYEE_PORTAL" || payload.value === "/control") {
        window.location.href = "/control";
        return;
      }

      // If triggered from quick reply button, show selection in chat immediately
      if (payload.label && activeWorkflow && activeWorkflow.messages) {
        activeWorkflow.messages.push({ sender: "user", text: payload.label });
        renderChatThread();
      }

      try {
        const res = await fetch("/api/workflow/transition", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSessionId,
            action: action,
            payload: payload
          })
        });
        const data = await res.json();
        if (data.status === "success") {
          activeWorkflow = data.workflow;
          renderWorkflow();
        }
      } catch (e) {
        console.error("Error transitioning workflow:", e);
      }
    }

    // 4. Render Synchronized State (Both Chat & Contextual GUI)
    function renderWorkflow() {
      if (!activeWorkflow) return;

      renderChatThread();
      renderContextualWorkspace();
    }

    // Render Chat Panel
    function smartScrollChat() {
      const chat = document.querySelector(".chat-thread") || document.getElementById("chatBody");
      if (chat) {
        chat.scrollTop = chat.scrollHeight;
      }
    }

    function renderChatThread() {
      const chatBody = document.getElementById("chatBody");
      chatBody.innerHTML = "";

      const msgs = activeWorkflow.messages || [];
      msgs.forEach(m => {
        const row = document.createElement("div");
        row.className = `chat-msg ${m.sender === "user" ? "user" : "bot"}`;
        
        if (m.sender === "user") {
          const bubble = document.createElement("div");
          bubble.className = "chat-msg-bubble user-bubble";
          bubble.innerHTML = m.text.replace(/\n/g, "<br>");
          row.appendChild(bubble);

          const avatar = document.createElement("div");
          avatar.className = "avatar-user";
          avatar.innerHTML = `<i class="bi bi-person-fill"></i>`;
          row.appendChild(avatar);
        } else {
          const avatar = document.createElement("div");
          avatar.className = "avatar-bot";
          avatar.innerHTML = `<img src="/static/illustrations/airtel_ai_agent_logo.svg" alt="Airtel AI Advisor">`;
          row.appendChild(avatar);

          const bubble = document.createElement("div");
          bubble.className = "chat-msg-bubble bot-bubble";

          let formattedText = m.text;
          if (formattedText.includes("Updated active plan to")) {
            formattedText = formattedText.replace(/Updated active plan to (.*?)\./g, 
              `<div class="chat-highlight-card"><div class="highlight-title"><i class="bi bi-lightning-charge-fill text-danger me-1"></i> Plan Updated</div><div class="highlight-body">$1</div></div>`);
          } else if (formattedText.includes("Added requirement:")) {
            formattedText = formattedText.replace(/Added requirement: (.*?)\./g,
              `<div class="chat-highlight-card"><div class="highlight-title"><i class="bi bi-check-circle-fill text-success me-1"></i> Requirement Added</div><div class="highlight-body">$1</div></div>`);
          } else if (formattedText.includes("Removed requirement:")) {
            formattedText = formattedText.replace(/Removed requirement: (.*?)\./g,
              `<div class="chat-highlight-card"><div class="highlight-title"><i class="bi bi-dash-circle-fill text-danger me-1"></i> Requirement Removed</div><div class="highlight-body">$1</div></div>`);
          } else if (formattedText.includes("Added add-on")) {
            formattedText = formattedText.replace(/Added add-on (.*?) to your quotation\./g, 
              `<div class="chat-highlight-card"><div class="highlight-title"><i class="bi bi-plus-circle-fill text-primary me-1"></i> Add-on Added</div><div class="highlight-body">$1 added to quote</div></div>`);
          } else if (formattedText.includes("Removed add-on")) {
            formattedText = formattedText.replace(/Removed add-on (.*?) from your quotation\./g, 
              `<div class="chat-highlight-card text-muted"><div class="highlight-title"><i class="bi bi-dash-circle-fill text-secondary me-1"></i> Add-on Removed</div><div class="highlight-body">$1</div></div>`);
          }

          bubble.innerHTML = formattedText.replace(/\n/g, "<br>");
          row.appendChild(bubble);
        }

        chatBody.appendChild(row);
      });

      // Quick Replies from last message (robustly handles string lists, structured action objects, and hides empty chips)
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
      quickBox.style.display = quickBox.children.length > 0 ? "flex" : "none";
      smartScrollChat();

      chatBody.scrollTop = chatBody.scrollHeight;
    }

    let speechRecognitionInstance = null;
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

    function submitChatText(text) {
      const input = document.getElementById("chatInput");
      if (input) input.value = text;
      handleChatSubmit();
    }

    function goToPreviousStage() {
      dispatchWorkflowTransition("PREVIOUS_STAGE");
    }

    // Render Contextual Workspace based on current stage
    function renderContextualWorkspace() {
      const stage = activeWorkflow.stage;
      const container = document.getElementById("dynamicStageContent");
      const titleEl = document.getElementById("workspaceStageTitle");
      const subEl = document.getElementById("workspaceStageSubtitle");
      const badgeEl = document.getElementById("workflowStepBadge");

      // Update Previous Step Back Button visibility in Stage Bar
      const btnPrev = document.getElementById("btnPrevStage");
      if (btnPrev) {
        if (stage === "USER_TYPE_SELECTION" || stage === "WELCOME") {
          btnPrev.classList.add("d-none");
          btnPrev.classList.remove("d-inline-flex");
        } else {
          btnPrev.classList.remove("d-none");
          btnPrev.classList.add("d-inline-flex");
        }
      }

      if (activeWorkflow.customer && activeWorkflow.customer.authenticated && activeWorkflow.customer.name && activeWorkflow.customer.name !== "Valued Business Owner") {
        badgeEl.innerHTML = `<i class="bi bi-person-circle text-danger me-1"></i><strong>${activeWorkflow.customer.name}</strong> (${activeWorkflow.customer.business_name || 'MSME'})`;
        badgeEl.className = "badge bg-white text-dark border border-danger-subtle px-2 py-1 font-monospace shadow-sm";
      } else {
        badgeEl.innerText = `STAGE: ${stage}`;
        badgeEl.className = "badge bg-light text-muted border px-2 py-1 font-monospace";
      }

      if (stage === "USER_TYPE_SELECTION") {
        titleEl.innerText = "1. Welcome! Select Your Journey";
        subEl.innerText = "Choose whether you are a business owner seeking connectivity or an Airtel employee.";
        container.innerHTML = `
          <div class="row g-4 py-2">
            <div class="col-md-6">
              <div class="card p-4 h-100 border-2 category-tile text-center" onclick="dispatchWorkflowTransition('SELECT_USER_TYPE', {user_type: 'customer'})">
                <div class="fs-1 text-danger mb-2">🏪</div>
                <h5 class="fw-bold text-dark">I am a Business Owner</h5>
                <p class="small text-muted mb-3">Explore tailored digital bundles for Kirana, Clinics, Multi-site chains, and Small Factories.</p>
                <button class="btn btn-airtel w-100 btn-sm">Explore MSME Solutions</button>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card p-4 h-100 border-2 category-tile text-center" onclick="dispatchWorkflowTransition('SELECT_USER_TYPE', {user_type: 'employee'})">
                <div class="fs-1 text-primary mb-2">👔</div>
                <h5 class="fw-bold text-dark">I am an Airtel Employee</h5>
                <p class="small text-muted mb-3">Access internal operations, KYC verification queue, exception actions, and funnel diagnostics.</p>
                <button class="btn btn-outline-dark w-100 btn-sm">Enter Employee Console</button>
              </div>
            </div>
          </div>
        `;
      }
      else if (stage === "EMPLOYEE_DEMO_ENTRY") {
        titleEl.innerText = "Airtel Operations & Employee Console";
        subEl.innerText = "Competition & Evaluation Demo Mode — Full internal portal access.";
        container.innerHTML = `
          <div class="p-4 border rounded bg-light text-center">
            <div class="badge bg-danger mb-2">DEMO MODE ACTIVE</div>
            <h4 class="fw-bold text-dark mb-2">Enterprise Control Console</h4>
            <p class="small text-muted max-w-md mx-auto mb-4">
              Explore the operations management suite including 5,000 synthetic SMB lead funnels, GIS line feasibility checks, Smart KYC queues, and Quote Recovery Engine.
            </p>
            <div class="d-flex justify-content-center gap-3">
              <a href="/control" class="btn btn-airtel px-4 py-2"><i class="bi bi-box-arrow-up-right me-1"></i> Launch Control Portal</a>
              <button class="btn btn-outline-secondary px-3" onclick="dispatchWorkflowTransition('SELECT_USER_TYPE', {user_type: 'customer'})">Back to Customer View</button>
            </div>
          </div>
        `;
      }
      else if (stage === "CUSTOMER_ACCOUNT_CHECK") {
        titleEl.innerText = "2. Airtel Business Account";
        subEl.innerText = "Do you have an existing Airtel Business connection or are you setting up a new business?";
        container.innerHTML = `
          <div class="row g-4 py-2">
            <div class="col-md-6">
              <div class="card p-4 h-100 border-2 category-tile text-center" onclick="dispatchWorkflowTransition('SELECT_ACCOUNT_STATUS', {status: 'existing'})">
                <div class="fs-1 text-success mb-2">🔑</div>
                <h5 class="fw-bold text-dark">Existing Customer</h5>
                <p class="small text-muted mb-3">Sign in with your registered mobile number to restore your previous quotes and preferences.</p>
                <button class="btn btn-outline-danger w-100 btn-sm">Sign In to My Account</button>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card p-4 h-100 border-2 category-tile text-center" onclick="dispatchWorkflowTransition('SELECT_ACCOUNT_STATUS', {status: 'new'})">
                <div class="fs-1 text-danger mb-2">✨</div>
                <h5 class="fw-bold text-dark">New to Airtel Business</h5>
                <p class="small text-muted mb-3">Create your account in 30 seconds with statutory DPDP 2023 compliance.</p>
                <button class="btn btn-airtel w-100 btn-sm">Create New Account</button>
              </div>
            </div>
          </div>
          <div class="text-center mt-3">
            <button type="button" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="goToPreviousStage()">
              <i class="bi bi-arrow-left"></i> Back to Journey Selection
            </button>
          </div>
        `;
      }
      else if (stage === "CUSTOMER_LOGIN") {
        titleEl.innerText = "Sign In to Airtel Business";
        subEl.innerText = "Security note: Enter credentials strictly in this form. Passwords are never sent to the AI.";
        container.innerHTML = `
          <div class="card p-4 border shadow-sm max-w-lg mx-auto" style="max-width: 480px;">
            <div class="mb-3">
              <label class="form-label small fw-bold">Registered Mobile Number or Email</label>
              <input type="text" id="loginId" class="form-control" value="9810123456" placeholder="98XXXXXXXX">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Password</label>
              <div class="input-group">
                <input type="password" id="loginPwd" class="form-control" value="Airtel@2026">
                <button class="btn btn-outline-secondary" type="button" onclick="togglePasswordVisibility('loginPwd')"><i class="bi bi-eye"></i></button>
              </div>
            </div>
            <div class="alert alert-light border small text-muted mb-3">
              <i class="bi bi-info-circle-fill text-primary me-1"></i> Demo credentials pre-filled for <strong>Rajesh Gupta</strong> (Gupta Kirana & General Store).
            </div>
            <button class="btn btn-airtel w-100 py-2 fw-bold" onclick="submitCustomerLogin()">Sign In &amp; Restore Profile</button>
            <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top small">
              <button type="button" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="goToPreviousStage()">
                <i class="bi bi-arrow-left"></i> Back
              </button>
              <a href="javascript:void(0)" onclick="dispatchWorkflowTransition('SELECT_ACCOUNT_STATUS', {status: 'new'})" class="text-danger fw-semibold">New here? Create account</a>
            </div>
          </div>
        `;
      }
      else if (stage === "CUSTOMER_SIGNUP") {
        titleEl.innerText = "Create Your Airtel Business Account";
        subEl.innerText = "Section 6 DPDP Act 2023 statutory consent notice and instant profile creation.";
        container.innerHTML = `
          <div class="card p-4 border shadow-sm mx-auto" style="max-width: 540px; border-radius: 14px;">
            <div class="alert alert-light border border-danger-subtle d-flex align-items-start gap-2 py-2 px-3 mb-3 small" style="background: rgba(235, 0, 41, 0.04); border-radius: 10px;">
              <i class="bi bi-robot text-danger fs-5 mt-1"></i>
              <div>
                <strong>Conversational Dual-Mode:</strong> You can type your details directly in the fields below, <strong>or</strong> simply tell the AI Advisor in the chat on the right (e.g. <em>"Anshul Kaushal 9434134144 Kaushal Sweets"</em>) and it will automatically type and register them for you!
              </div>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-bold">Business Owner Name</label>
                <input type="text" id="regName" class="form-control form-control-sm" placeholder="e.g. Anshul Kaushal" value="${(activeWorkflow.customer && activeWorkflow.customer.name && activeWorkflow.customer.name !== 'Valued Business Owner') ? activeWorkflow.customer.name : ''}" required>
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Mobile Number</label>
                <input type="tel" id="regMobile" class="form-control form-control-sm" placeholder="e.g. 9434134144" value="${(activeWorkflow.customer && activeWorkflow.customer.mobile) ? activeWorkflow.customer.mobile : ''}" required>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Business / Trade Name</label>
              <input type="text" id="regBizName" class="form-control form-control-sm" placeholder="e.g. Kaushal Sweets" value="${(activeWorkflow.customer && activeWorkflow.customer.business_name && activeWorkflow.customer.business_name !== 'Airtel Business MSME') ? activeWorkflow.customer.business_name : ''}" required>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <label class="form-label small fw-bold mb-0">Set Password</label>
                <button type="button" class="btn btn-link p-0 text-decoration-none small text-muted" style="font-size: 0.75rem;" onclick="autoFillSignupSample()">✨ Quick Fill Sample</button>
              </div>
              <input type="password" id="regPwd" class="form-control form-control-sm" value="Airtel@2026">
            </div>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" id="regDpdpConsent" checked>
              <label class="form-check-label small" for="regDpdpConsent">
                I give explicit consent under DPDP Act 2023 for telecom verification and DoT compliance.
              </label>
            </div>
            <button class="btn btn-airtel w-100 py-2 fw-bold" onclick="submitCustomerSignup()">Register &amp; Begin Discovery</button>
            <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top small">
              <button type="button" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="goToPreviousStage()">
                <i class="bi bi-arrow-left"></i> Back
              </button>
              <a href="javascript:void(0)" onclick="dispatchWorkflowTransition('SELECT_ACCOUNT_STATUS', {status: 'existing'})" class="text-danger fw-semibold">Already have an account? Sign In</a>
            </div>
          </div>
        `;
      }
      else if (stage === "BUSINESS_IDENTIFICATION") {
        const curType = activeWorkflow.discovery.business_type || "kirana";
        titleEl.innerText = "3. Business Category Discovery";
        subEl.innerText = "What kind of business do you run? Select or tell the AI advisor in chat.";
        container.innerHTML = `
          <div class="category-grid">
            <div class="category-tile ${curType === 'kirana' ? 'selected' : ''}" onclick="dispatchWorkflowTransition('SELECT_CATEGORY', {category: 'kirana'})">
              <div class="category-icon-box"><img src="/static/illustrations/cat_kirana.svg" alt="Kirana"></div>
              <h6 class="fw-bold mb-1">Kirana &amp; Retail</h6>
              <p class="small text-muted mb-0">High-volume UPI payments &amp; POS failover.</p>
            </div>
            <div class="category-tile ${curType === 'clinic' ? 'selected' : ''}" onclick="dispatchWorkflowTransition('SELECT_CATEGORY', {category: 'clinic'})">
              <div class="category-icon-box"><img src="/static/illustrations/cat_clinic.svg" alt="Clinic"></div>
              <h6 class="fw-bold mb-1">Clinic &amp; CA Office</h6>
              <p class="small text-muted mb-0">High-speed fiber &amp; encrypted cloud backup.</p>
            </div>
            <div class="category-tile ${curType === 'multisite' ? 'selected' : ''}" onclick="dispatchWorkflowTransition('SELECT_CATEGORY', {category: 'multisite'})">
              <div class="category-icon-box"><img src="/static/illustrations/cat_multisite.svg" alt="Multisite"></div>
              <h6 class="fw-bold mb-1">Multi-Store Chain</h6>
              <p class="small text-muted mb-0">Centralized SD-WAN networking &amp; CCTV.</p>
            </div>
            <div class="category-tile ${curType === 'manufacturer' ? 'selected' : ''}" onclick="dispatchWorkflowTransition('SELECT_CATEGORY', {category: 'manufacturer'})">
              <div class="category-icon-box"><img src="/static/illustrations/cat_factory.svg" alt="Factory"></div>
              <h6 class="fw-bold mb-1">Small Factory</h6>
              <p class="small text-muted mb-0">Dedicated leased line, Static IP &amp; IoT telemetry.</p>
            </div>
          </div>
          <div class="d-flex justify-content-between align-items-center mt-3">
            <button type="button" class="btn btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="goToPreviousStage()">
              <i class="bi bi-arrow-left"></i> Back
            </button>
            <button class="btn btn-airtel" onclick="dispatchWorkflowTransition('GO_TO_STAGE', {stage: 'REQUIREMENTS_COLLECTION'})">Continue to Needs &amp; Tools <i class="bi bi-arrow-right ms-1"></i></button>
          </div>
        `;
      }
      else if (stage === "REQUIREMENTS_COLLECTION") {
        const reqs = activeWorkflow.discovery.requirements || [];
        titleEl.innerText = "4. Operational Challenges & Digital Tools";
        subEl.innerText = "Select your key requirements below or explain them to the AI chatbot.";
        container.innerHTML = `
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <div class="requirement-card ${reqs.includes('upi_failover') ? 'checked' : ''}" onclick="dispatchWorkflowTransition('TOGGLE_REQUIREMENT', {requirement: 'upi_failover'})">
                <div class="fs-4 text-danger"><i class="bi bi-qr-code-scan"></i></div>
                <div>
                  <h6 class="fw-bold mb-1">Instant UPI &amp; POS Failover</h6>
                  <p class="small text-muted mb-0">Guaranteed backup SIM so customer payments never drop during evening rush.</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="requirement-card ${reqs.includes('broadband_speed') ? 'checked' : ''}" onclick="dispatchWorkflowTransition('TOGGLE_REQUIREMENT', {requirement: 'broadband_speed'})">
                <div class="fs-4 text-primary"><i class="bi bi-speedometer2"></i></div>
                <div>
                  <h6 class="fw-bold mb-1">High-Speed Symmetrical Fiber</h6>
                  <p class="small text-muted mb-0">Consistent upload and download bandwidth with zero buffering.</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="requirement-card ${reqs.includes('cctv_security') ? 'checked' : ''}" onclick="dispatchWorkflowTransition('TOGGLE_REQUIREMENT', {requirement: 'cctv_security'})">
                <div class="fs-4 text-warning"><i class="bi bi-camera-video"></i></div>
                <div>
                  <h6 class="fw-bold mb-1">24/7 Cloud CCTV Surveillance</h6>
                  <p class="small text-muted mb-0">Remote store monitoring with 30-day encrypted cloud recording.</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="requirement-card ${reqs.includes('static_ip') ? 'checked' : ''}" onclick="dispatchWorkflowTransition('TOGGLE_REQUIREMENT', {requirement: 'static_ip'})">
                <div class="fs-4 text-success"><i class="bi bi-globe"></i></div>
                <div>
                  <h6 class="fw-bold mb-1">Fixed Static IP Address</h6>
                  <p class="small text-muted mb-0">Host local servers, biometric attendance, or remote CCTV securely.</p>
                </div>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-between">
            <button class="btn btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="goToPreviousStage()"><i class="bi bi-arrow-left"></i> Back</button>
            <button class="btn btn-airtel" onclick="dispatchWorkflowTransition('GO_TO_STAGE', {stage: 'PLAN_EXPLORATION'})">Generate Digital Bundle <i class="bi bi-arrow-right ms-1"></i></button>
          </div>
        `;
      }
      else if (stage === "PLAN_EXPLORATION" || stage === "QUOTE_REVIEW" || stage === "PACKAGE_CUSTOMIZATION") {
        const rec = activeWorkflow.recommendation || {};
        const addons = rec.active_addons || [];
        const includedPids = (rec.included_products || []).map(p => p.id);
        const lineItems = rec.line_items || [];

        titleEl.innerText = "5. Recommended Bundle & 1-Click Customization";
        subEl.innerText = "Airtel Business single transparent bill with zero hidden costs.";
        container.innerHTML = `
          <div class="row g-4">
            <!-- Left: Hero Bundle Summary & Modular Add-ons -->
            <div class="col-lg-7">
              <div class="rec-hero-card">
                <div class="rec-match-badge">${rec.match_score || 95}% MATCH</div>
                <div class="badge bg-danger mb-2">${(activeWorkflow.discovery.business_type || 'KIRANA').toUpperCase()} SOLUTION</div>
                <h4 class="fw-bold text-dark mb-1">${rec.bundle_name || 'Kirana Digital Starter'}</h4>
                <div class="d-flex align-items-baseline gap-2 mb-3">
                  <span class="rec-price-huge">₹${(rec.monthly_base || 1999).toLocaleString()}</span>
                  <span class="text-muted small">/ month + 18% GST</span>
                </div>
                <div class="p-3 bg-light rounded small mb-3 border">
                  <strong>Why this bundle?</strong> ${rec.why_narrative || 'Tailored specifically for high-availability business connectivity with guaranteed backup.'}
                </div>
                
                <!-- Quick Plan Switcher -->
                <div class="mb-3">
                  <span class="small fw-bold text-muted d-block mb-1">SWITCH BASE PLAN:</span>
                  <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-sm ${rec.bundle_id === 'bundle_kirana' ? 'btn-danger' : 'btn-outline-secondary'}" onclick="dispatchWorkflowTransition('SELECT_PLAN', {bundle_id: 'bundle_kirana'})">Kirana Starter (₹1,999)</button>
                    <button class="btn btn-sm ${rec.bundle_id === 'bundle_clinic' ? 'btn-danger' : 'btn-outline-secondary'}" onclick="dispatchWorkflowTransition('SELECT_PLAN', {bundle_id: 'bundle_clinic'})">Clinic Suite (₹3,499)</button>
                    <button class="btn btn-sm ${rec.bundle_id === 'bundle_multisite' ? 'btn-danger' : 'btn-outline-secondary'}" onclick="dispatchWorkflowTransition('SELECT_PLAN', {bundle_id: 'bundle_multisite'})">Multi-Site (₹7,999)</button>
                  </div>
                </div>

                <!-- Modular Addons -->
                <div class="mb-2">
                  <span class="small fw-bold text-muted d-block mb-2">MODULAR ADD-ONS (1-Click Toggles):</span>
                  
                  <!-- CCTV Security (P23) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>24/7 Cloud CCTV (2 Cameras)</strong> (P23)
                      <div class="small text-muted">30-day encrypted cloud recording & live mobile feed</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      <span class="text-danger fw-bold small">+₹800/mo</span>
                      <input class="form-check-input" type="checkbox" ${addons.includes('P23') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P23'})">
                    </div>
                  </div>

                  <!-- Fixed Static IP (P11) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>Fixed Static Public IP Address</strong> (P11)
                      <div class="small text-muted">Dedicated IP for billing servers, CCTV DVR & remote access</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      <span class="text-danger fw-bold small">+₹300/mo</span>
                      <input class="form-check-input" type="checkbox" ${addons.includes('P11') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P11'})">
                    </div>
                  </div>

                  <!-- Symmetrical Fiber (P01) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>High-Speed Symmetrical Fiber 100M</strong> (P01)
                      <div class="small text-muted">Dedicated 100 Mbps symmetrical leased fiber line</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      <span class="text-danger fw-bold small">+₹999/mo</span>
                      <input class="form-check-input" type="checkbox" ${addons.includes('P01') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P01'})">
                    </div>
                  </div>

                  <!-- WhatsApp Business API (P15) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>WhatsApp Business API Starter</strong> (P15)
                      <div class="small text-muted">Automated promotional messages & transactional alerts</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      ${includedPids.includes('P15') ? 
                        '<span class="badge bg-success-subtle text-success border border-success-subtle"><i class="bi bi-check-circle-fill me-1"></i> Included in Plan</span>' :
                        `<span class="text-danger fw-bold small">+₹999/mo</span>
                         <input class="form-check-input" type="checkbox" ${addons.includes('P15') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P15'})">`
                      }
                    </div>
                  </div>

                  <!-- Failover SIM (P09) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>Instant UPI & POS 4G/5G Failover</strong> (P09)
                      <div class="small text-muted">Zero payment dropouts with automatic cellular backup</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      ${includedPids.includes('P09') ? 
                        '<span class="badge bg-success-subtle text-success border border-success-subtle"><i class="bi bi-check-circle-fill me-1"></i> Included in Plan</span>' :
                        `<span class="text-danger fw-bold small">+₹499/mo</span>
                         <input class="form-check-input" type="checkbox" ${addons.includes('P09') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P09'})">`
                      }
                    </div>
                  </div>

                  <!-- Cloud Backup 1 TB (P17) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>Cloud Backup (1 TB Secure Storage)</strong> (P17)
                      <div class="small text-muted">Automated offsite backup for billing & accounting files</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      ${includedPids.includes('P17') ? 
                        '<span class="badge bg-success-subtle text-success border border-success-subtle"><i class="bi bi-check-circle-fill me-1"></i> Included in Plan</span>' :
                        `<span class="text-danger fw-bold small">+₹499/mo</span>
                         <input class="form-check-input" type="checkbox" ${addons.includes('P17') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P17'})">`
                      }
                    </div>
                  </div>

                  <!-- Cloud POS & Billing (P19) -->
                  <div class="addon-switch-row">
                    <div>
                      <strong>Cloud POS & GST Billing Counter</strong> (P19)
                      <div class="small text-muted">Tablet billing counter with QR barcode generation</div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                      <span class="text-danger fw-bold small">+₹599/mo</span>
                      <input class="form-check-input" type="checkbox" ${addons.includes('P19') ? 'checked' : ''} onchange="dispatchWorkflowTransition('TOGGLE_ADDON', {addon_id: 'P19'})">
                    </div>
                  </div>

                </div>
              </div>
            </div>

            <!-- Right: Itemized Quotation Breakdown Table -->
            <div class="col-lg-5">
              <div class="card p-4 border bg-white shadow-sm h-100 d-flex flex-column justify-content-between" style="border-radius: 14px;">
                <div>
                  <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                    <h6 class="fw-bold mb-0 text-dark"><i class="bi bi-receipt text-danger me-1"></i> Itemized Quotation Breakdown</h6>
                    <span class="badge bg-success-subtle text-success small">Live Verified</span>
                  </div>

                  <!-- Line Item Table -->
                  <div class="table-responsive mb-3">
                    <table class="table table-sm align-middle mb-0" style="font-size: 0.85rem;">
                      <thead>
                        <tr class="border-bottom text-muted small">
                          <th style="width: 60%;">Product / Component</th>
                          <th class="text-center" style="width: 15%;">Qty</th>
                          <th class="text-end" style="width: 25%;">Monthly</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${lineItems.map(li => `
                          <tr class="${li.type === 'base_plan' ? 'table-light fw-bold' : ''}">
                            <td>
                              <div class="text-dark">${escapeHtml(li.name)}</div>
                              <div class="d-flex gap-1 mt-1">
                                <span class="badge bg-secondary-subtle text-secondary" style="font-size:0.65rem;">${escapeHtml(li.product_id)}</span>
                                ${li.setup_fee > 0 ? `<span class="badge bg-warning-subtle text-dark" style="font-size:0.65rem;">Setup: ₹${li.setup_fee.toLocaleString()}</span>` : ''}
                              </div>
                            </td>
                            <td class="text-center">${li.quantity || 1}</td>
                            <td class="text-end">
                              ${li.is_included || li.monthly_before_tax === 0 ? 
                                '<span class="badge bg-success-subtle text-success">Included</span>' : 
                                `<strong>₹${(li.monthly_before_tax || 0).toLocaleString()}</strong>`}
                            </td>
                          </tr>
                        `).join('')}
                      </tbody>
                    </table>
                  </div>

                  <!-- Price Summation -->
                  <div class="border-top pt-2">
                    <div class="d-flex justify-content-between small py-1">
                      <span class="text-muted">Subtotal (Monthly Before Tax):</span>
                      <strong class="text-dark">₹${(rec.monthly_subtotal || rec.monthly_base || 1999).toLocaleString()}</strong>
                    </div>
                    <div class="d-flex justify-content-between small py-1">
                      <span class="text-muted">Statutory GST (18%):</span>
                      <strong class="text-dark">₹${(rec.gst_18 || 360).toLocaleString()}</strong>
                    </div>
                    <div class="d-flex justify-content-between py-2 border-top border-bottom my-2 bg-light px-2 rounded">
                      <span class="fw-bold fs-6 text-dark">Total Recurring Payable:</span>
                      <span class="fw-bold text-danger fs-5">₹${(rec.total_monthly || 2359).toLocaleString()}/mo</span>
                    </div>
                    <div class="d-flex justify-content-between small text-muted px-1">
                      <span><i class="bi bi-wrench-adjustable text-secondary me-1"></i> One-time Setup: <strong>₹${(rec.setup_fee || 0).toLocaleString()}</strong></span>
                      <span><i class="bi bi-clock-history text-secondary me-1"></i> Term: <strong>${rec.contract_months || 12} Months</strong></span>
                    </div>
                  </div>
                </div>

                <div class="mt-4 pt-2 border-top">
                  <div class="d-flex gap-2 mb-2">
                    <button type="button" class="btn btn-outline-secondary w-50 py-2 fw-semibold d-inline-flex align-items-center justify-content-center gap-1" onclick="goToPreviousStage()">
                      <i class="bi bi-arrow-left"></i> Back to Needs
                    </button>
                    <button type="button" class="btn btn-airtel w-50 py-2 fw-bold d-inline-flex align-items-center justify-content-center gap-1 shadow-sm" onclick="dispatchWorkflowTransition('GO_TO_STAGE', {stage: 'KYC_VERIFICATION'})">
                      Confirm Quote &amp; KYC <i class="bi bi-arrow-right"></i>
                    </button>
                  </div>
                  <div class="small text-muted text-center"><i class="bi bi-shield-check text-success me-1"></i> Zero 5-day wait. 100% transparent. Single unified bill.</div>
                </div>
              </div>
            </div>
          </div>
        `;
      }
      else if (stage === "KYC_VERIFICATION") {
        titleEl.innerText = "6. Smart KYC Document Capture & Compliance";
        subEl.innerText = "Add your KYC documents via mobile camera or upload for statutory DoT & DPDP Act 2023 verification.";
        container.innerHTML = `
          <div class="row g-4">
            <!-- Left Column: Document Capture & Upload Area -->
            <div class="col-lg-7">
              <div class="card p-3 p-md-4 border shadow-sm h-100">
                <div class="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2">
                  <div class="d-flex align-items-center gap-2">
                    <button type="button" class="btn btn-sm btn-outline-secondary py-1 px-2 d-inline-flex align-items-center gap-1 shadow-sm" onclick="goToPreviousStage()" title="Back to Plan & Quote Review">
                      <i class="bi bi-arrow-left"></i> <span>Back</span>
                    </button>
                    <div>
                      <h5 class="fw-bold text-dark mb-0"><i class="bi bi-camera-fill text-danger me-2"></i>Add your KYC documents</h5>
                      <span class="small text-muted">Statutory requirement under DoT Subscriber Verification Mandate</span>
                    </div>
                  </div>
                  <span class="badge bg-danger bg-opacity-10 text-danger border border-danger-subtle font-monospace">DPDP SEC 6</span>
                </div>

                <!-- DPDP Explicit Affirmative Consent Notice -->
                <div class="card p-2 p-md-3 border bg-light mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="kycDpdpCheck" onchange="toggleKycSubmitBtn()">
                    <label class="form-check-label small" for="kycDpdpCheck">
                      <strong><i class="bi bi-shield-lock-fill text-success me-1"></i> DPDP Act 2023 Explicit Consent:</strong> 
                      I consent to the collection and automated processing of my business proof solely for telecom onboarding. PII is masked and processed purely in an ephemeral RAM buffer during request execution with no persistent raw image storage.
                    </label>
                  </div>
                </div>

                <!-- Document Type Selector -->
                <div class="mb-3">
                  <label for="kycDocTypeSelect" class="form-label small fw-bold">Select Supported Document Type</label>
                  <select id="kycDocTypeSelect" class="form-select form-select-sm" onchange="onDocTypeChanged(this.value)">
                    <option value="gst_certificate" ${currentKycDoc.docType === 'gst_certificate' ? 'selected' : ''}>📄 Business / GST Registration Certificate</option>
                    <option value="udyam_certificate" ${currentKycDoc.docType === 'udyam_certificate' ? 'selected' : ''}>🏢 Udyam MSME Certificate</option>
                    <option value="address_proof" ${currentKycDoc.docType === 'address_proof' ? 'selected' : ''}>💡 Address Proof / Electricity Bill (&lt; 90 Days)</option>
                    <option value="signatory_id" ${currentKycDoc.docType === 'signatory_id' ? 'selected' : ''}>🪪 Signatory Identity Proof (PAN / Aadhaar)</option>
                  </select>
                </div>

                <!-- Photo Guidance Callout -->
                <div class="card p-2 p-md-3 border mb-3 bg-white" style="border-left: 4px solid #eb0029 !important;">
                  <div class="fw-bold small text-dark mb-2"><i class="bi bi-lightbulb-fill text-warning me-1"></i> Simple Photo Guidance:</div>
                  <div class="row g-2">
                    <div class="col-6 col-sm-3">
                      <div class="kyc-guidance-pill text-center">
                        <i class="bi bi-brightness-high text-primary fs-5 d-block mb-1"></i>
                        <strong>Good Lighting</strong>
                        <div class="text-muted" style="font-size: 0.7rem;">Even, no shadows</div>
                      </div>
                    </div>
                    <div class="col-6 col-sm-3">
                      <div class="kyc-guidance-pill text-center">
                        <i class="bi bi-aspect-ratio text-success fs-5 d-block mb-1"></i>
                        <strong>All 4 Corners</strong>
                        <div class="text-muted" style="font-size: 0.7rem;">Entire doc in frame</div>
                      </div>
                    </div>
                    <div class="col-6 col-sm-3">
                      <div class="kyc-guidance-pill text-center">
                        <i class="bi bi-sun text-danger fs-5 d-block mb-1"></i>
                        <strong>Avoid Glare</strong>
                        <div class="text-muted" style="font-size: 0.7rem;">No flash reflection</div>
                      </div>
                    </div>
                    <div class="col-6 col-sm-3">
                      <div class="kyc-guidance-pill text-center">
                        <i class="bi bi-eye text-info fs-5 d-block mb-1"></i>
                        <strong>Readable Text</strong>
                        <div class="text-muted" style="font-size: 0.7rem;">Sharp &amp; in-focus</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Dual Capture / Upload Box (Initial State) -->
                <div id="kycCaptureBox" class="border rounded-3 p-4 text-center bg-light mb-3 ${currentKycDoc.file ? 'd-none' : ''}">
                  <div class="fs-1 text-danger mb-2"><i class="bi bi-camera"></i></div>
                  <h6 class="fw-bold mb-1">Capture or Upload Your Document</h6>
                  <p class="small text-muted mb-3">Use your device camera or upload an image file (JPG, PNG, WebP).</p>
                  
                  <div class="d-flex flex-wrap justify-content-center gap-2">
                    <button type="button" class="btn btn-airtel py-2 px-3 fw-bold d-inline-flex align-items-center gap-2 shadow-sm" onclick="triggerCameraCapture()" aria-label="Take Photo using Camera">
                      <i class="bi bi-camera-fill fs-5"></i> <span>Take Photo</span>
                    </button>
                    <button type="button" class="btn btn-outline-secondary py-2 px-3 fw-bold d-inline-flex align-items-center gap-2" onclick="document.getElementById('kycFileInput').click()" aria-label="Upload from Device">
                      <i class="bi bi-upload fs-5"></i> <span>Upload from Device</span>
                    </button>
                  </div>

                  <!-- Hidden Inputs for Native Camera Capture & Device File Upload -->
                  <input type="file" id="kycCameraInput" accept="image/*" capture="environment" class="d-none" onchange="handleKycFileSelected(this.files[0], 'camera')">
                  <input type="file" id="kycFileInput" accept="image/png,image/jpeg,image/webp,application/pdf" class="d-none" onchange="handleKycFileSelected(this.files[0], 'upload')">

                  <!-- Camera Permission Denial Fallback Banner -->
                  <div id="cameraErrorBanner" class="alert alert-warning py-2 px-3 small mt-3 d-none text-start">
                    <i class="bi bi-exclamation-triangle-fill text-warning me-1"></i>
                    <span id="cameraErrorMsg">Camera access is blocked or unavailable. Falling back to device file upload.</span>
                  </div>
                </div>

                <!-- Active Preview Box (After photo taken or file uploaded) -->
                <div id="kycPreviewBox" class="border rounded-3 p-3 bg-white shadow-sm mb-3 ${currentKycDoc.file ? '' : 'd-none'}">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-danger" id="previewDocTypeBadge">${getDocTypeLabel(currentKycDoc.docType)}</span>
                    <span class="small text-muted font-monospace" id="previewMetaText">${currentKycDoc.fileSize || 'Image Ready'}</span>
                  </div>
                  
                  <div class="text-center bg-light rounded p-2 mb-3 position-relative" style="min-height: 180px; max-height: 260px; overflow: hidden;">
                    <img id="kycPreviewImg" src="${currentKycDoc.blobUrl || ''}" alt="Document Preview" class="img-fluid rounded border shadow-sm" style="max-height: 240px; object-fit: contain;">
                    <div id="scanningLaser" class="scan-laser d-none"></div>
                  </div>

                  <!-- Preview Controls: Retake, Replace, Remove -->
                  <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center pt-2 border-top">
                    <div class="d-flex gap-2">
                      <button type="button" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="retakeKycPhoto()" title="Retake photo using camera">
                        <i class="bi bi-camera"></i> Retake
                      </button>
                      <button type="button" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="replaceKycFile()" title="Replace with a file from device">
                        <i class="bi bi-arrow-repeat"></i> Replace File
                      </button>
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-danger d-inline-flex align-items-center gap-1" onclick="removeKycPhoto()" title="Remove document">
                      <i class="bi bi-trash"></i> Remove
                    </button>
                  </div>
                </div>

                <!-- Processing Spinner & Progress -->
                <div id="kycProcessingBox" class="p-3 border rounded bg-light text-center mb-3 d-none">
                  <div class="spinner-border text-danger mb-2" role="status"></div>
                  <h6 class="fw-bold mb-1" id="kycProcessingTitle">Analyzing Document via Smart OCR...</h6>
                  <p class="small text-muted mb-0" id="kycProcessingSub">Extracting registration numbers and validating 90-day recency benchmark...</p>
                </div>

                <!-- Submission Button -->
                <button type="button" class="btn btn-airtel w-100 py-2 fw-bold mb-2 shadow-sm" id="btnSubmitKycDoc" onclick="submitKycDocument()" ${currentKycDoc.file ? '' : 'disabled'}>
                  <i class="bi bi-shield-check me-1"></i> Submit Document &amp; Run Smart OCR
                </button>

                <!-- Specimen Evaluator Benchmarks -->
                <div class="pt-2 border-top small text-muted text-center">
                  <span class="fw-semibold">Test Sample Benchmarks:</span> 
                  <a href="javascript:void(0)" onclick="loadSpecimenKyc('K02')" class="text-success fw-semibold">Sample Clean (K02)</a> · 
                  <a href="javascript:void(0)" onclick="loadSpecimenKyc('K11')" class="text-danger fw-semibold">Sample Expired Bill (K11)</a> · 
                  <a href="javascript:void(0)" onclick="loadSpecimenKyc('K04')" class="text-warning fw-semibold">Sample Low-Res (K04)</a>
                </div>
              </div>
            </div>

            <!-- Right Column: Verification Results & Registry Details -->
            <div class="col-lg-5">
              <div class="card p-3 p-md-4 border shadow-sm h-100 d-flex flex-column justify-content-between">
                <div>
                  <h6 class="fw-bold text-dark border-bottom pb-2 mb-3">
                    <i class="bi bi-clipboard-check text-success me-1"></i> Verification &amp; Registry Audit
                  </h6>

                  <!-- Zero-Typing GSTIN Lookup Card -->
                  <div class="card p-3 border mb-3 bg-light">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <label for="kycGstinInput" class="form-label small fw-bold mb-0">Zero-Typing GSTIN Lookup</label>
                      <span class="badge bg-secondary-subtle text-secondary font-monospace" style="font-size: 0.65rem;">NATIONAL REGISTRY</span>
                    </div>
                    <div class="input-group input-group-sm mb-2">
                      <input type="text" id="kycGstinInput" class="form-control" value="19EOGXH4115Y1ZL" placeholder="Enter 15-char GSTIN">
                      <button class="btn btn-danger" onclick="runGstinLookup()">Lookup</button>
                    </div>
                    <div id="gstinResultBox" class="p-2 bg-white rounded border small">
                      <div><strong>Legal Name:</strong> Harmony Dental Care</div>
                      <div><strong>Status:</strong> <span class="badge bg-success">Active</span> (Masked: 19EOGXH****Y1ZL)</div>
                    </div>
                  </div>

                  <!-- Dynamic Result Box (Populated after OCR submission) -->
                  <div id="kycResultBox" class="${currentKycDoc.verificationResult ? '' : 'd-none'}">
                    <!-- Populated dynamically via renderKycVerificationResult -->
                  </div>

                  <!-- Fallback Placeholder when not yet submitted -->
                  <div id="kycPendingPlaceholder" class="${currentKycDoc.verificationResult ? 'd-none' : ''}">
                    <div class="p-3 border rounded bg-white text-center text-muted mb-3">
                      <i class="bi bi-file-earmark-arrow-up fs-2 text-danger opacity-50 mb-2 d-block"></i>
                      <h6 class="fw-bold mb-1">Awaiting Document Submission</h6>
                      <p class="small mb-0">Take a photo or upload your KYC document on the left to trigger the automated verification engine.</p>
                    </div>
                  </div>
                </div>

                <!-- Proceed Button (Only enabled when verification passes) -->
                <div class="mt-4 pt-3 border-top">
                  <button class="btn ${currentKycDoc.isApproved ? 'btn-airtel' : 'btn-secondary'} w-100 py-2 fw-bold" id="btnProceedTracking" onclick="dispatchWorkflowTransition('GO_TO_STAGE', {stage: 'INSTALLATION_TRACKING'})" ${currentKycDoc.isApproved ? '' : 'disabled'}>
                    Proceed to Live Order Fulfillment <i class="bi bi-arrow-right ms-1"></i>
                  </button>
                  <div class="small text-muted text-center mt-2 mb-3" id="proceedNoticeText">
                    <i class="bi bi-shield-check text-success me-1"></i> Approval required from Smart Verification engine to proceed.
                  </div>
                  <button type="button" class="btn btn-outline-secondary w-100 py-2 fw-semibold d-inline-flex align-items-center justify-content-center gap-1" onclick="goToPreviousStage()">
                    <i class="bi bi-arrow-left"></i> Back to Plan &amp; Quotation Review
                  </button>
                </div>

              </div>
            </div>
          </div>
        `;

        if (currentKycDoc.verificationResult) {
          renderKycVerificationResult(currentKycDoc.verificationResult);
        }
      }
      else if (stage === "INSTALLATION_TRACKING" || stage === "ONBOARDING_COMPLETE") {
        const ord = activeWorkflow.order;
        titleEl.innerText = "7. Live Order Tracking & Engineer Assignment";
        subEl.innerText = "Zero status-chase guarantee with live milestone tracking (simulated prototype SMS/WhatsApp push notifications).";
        container.innerHTML = `
          <div class="row g-4">
            <div class="col-lg-7">
              <div class="card p-4 border">
                <div class="d-flex justify-content-between align-items-center mb-4">
                  <div>
                    <h5 class="fw-bold mb-0">Order ID: ${ord.order_id}</h5>
                    <span class="small text-muted">Airtel Business Guaranteed SLA: ${ord.sla_days}</span>
                  </div>
                  <span class="badge bg-danger px-3 py-2 rounded-pill">Status: Step 4 Dispatched</span>
                </div>

                <div class="stepper-live">
                  <div class="stepper-step completed">
                    <div class="stepper-node done"><i class="bi bi-check-lg"></i></div>
                    <div>
                      <div class="fw-bold text-dark">Step 1: Order Confirmed &amp; Bundle Configured</div>
                      <div class="small text-muted">15-Jul-2026 · Digital Kirana Starter (₹1,999/mo)</div>
                    </div>
                  </div>
                  <div class="stepper-step completed">
                    <div class="stepper-node done"><i class="bi bi-check-lg"></i></div>
                    <div>
                      <div class="fw-bold text-dark">Step 2: Smart KYC &amp; Statutory Registry Cleared</div>
                      <div class="small text-muted">15-Jul-2026 · GSTIN verified in 400ms · DPDP Consent Logged</div>
                    </div>
                  </div>
                  <div class="stepper-step completed">
                    <div class="stepper-node done"><i class="bi bi-check-lg"></i></div>
                    <div>
                      <div class="fw-bold text-dark">Step 3: GIS Feasibility &amp; Splitter Allocated</div>
                      <div class="small text-muted">16-Jul-2026 · Port 4/8 optical line active</div>
                    </div>
                  </div>
                  <div class="stepper-step">
                    <div class="stepper-node active"><i class="bi bi-arrow-repeat"></i></div>
                    <div>
                      <div class="fw-bold text-danger">Step 4: Hardware Dispatched &amp; Field Engineer Assigned</div>
                      <div class="small text-muted">17-Jul-2026 · Field Engineer: <strong>${ord.engineer_name}</strong> (${ord.engineer_phone})</div>
                    </div>
                  </div>
                  <div class="stepper-step">
                    <div class="stepper-node pending">5</div>
                    <div>
                      <div class="fw-bold text-muted">Step 5: On-Premises Installation &amp; Service Active</div>
                      <div class="small text-muted">Expected 18-Jul-2026 · Unified billing live</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-lg-5">
              <div class="card p-4 border bg-light h-100 d-flex flex-column justify-content-between">
                <div>
                  <h6 class="fw-bold border-bottom pb-2 mb-3"><i class="bi bi-person-badge-fill text-danger me-1"></i> Assigned Field Engineer</h6>
                  <div class="d-flex align-items-center gap-3 p-3 bg-white border rounded mb-3">
                    <div class="bg-danger text-white rounded-circle p-2 fs-3" style="width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;">
                      <i class="bi bi-person-fill"></i>
                    </div>
                    <div>
                      <div class="fw-bold text-dark">${ord.engineer_name}</div>
                      <div class="small text-muted">Airtel Enterprise Field Specialist</div>
                      <div class="small text-danger fw-bold"><i class="bi bi-telephone-fill me-1"></i>${ord.engineer_phone}</div>
                    </div>
                  </div>

                  <div class="alert alert-success small mb-0">
                    <i class="bi bi-bell-fill me-1"></i> Status chase calls reduced from 3.0 to &lt; 0.2 calls per merchant via milestone pushes.
                  </div>
                </div>

                <div class="mt-4">
                  <a href="/control" class="btn btn-outline-dark w-100 btn-sm py-2 mb-2">
                    <i class="bi bi-shield-shaded me-1"></i> View Operations Queue in Staff Portal
                  </a>
                  <button type="button" class="btn btn-outline-secondary w-100 btn-sm py-2 d-inline-flex align-items-center justify-content-center gap-1" onclick="goToPreviousStage()">
                    <i class="bi bi-arrow-left"></i> Back to KYC Verification
                  </button>
                </div>
              </div>
            </div>
          </div>
        `;
      }
    }

    // 5. Chat Interaction Controller
    async function handleChatSubmit(e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      const input = document.getElementById("chatInput");
      let msg = (input ? input.value : "").trim();

      // Ensure activeWorkflow and messages exist
      if (!activeWorkflow) activeWorkflow = { messages: [] };
      if (!activeWorkflow.messages) activeWorkflow.messages = [];

      // If user clicks Send with empty input, advance or act contextually based on stage!
      if (!msg) {
        const stage = activeWorkflow ? activeWorkflow.stage : "";
        if (stage === "REQUIREMENTS_COLLECTION") {
          const reqs = (activeWorkflow.discovery && activeWorkflow.discovery.requirements) || [];
          if (reqs.length > 0) {
            dispatchWorkflowTransition("GO_TO_STAGE", { stage: "PLAN_EXPLORATION", label: "Generate Digital Bundle" });
          } else {
            activeWorkflow.messages.push({
              sender: "bot",
              text: "Please select your requirements from the options on the left or type your shop's needs below."
            });
            renderChatThread();
            if (input) input.focus();
          }
          return;
        } else if (stage === "BUSINESS_IDENTIFICATION") {
          dispatchWorkflowTransition("GO_TO_STAGE", { stage: "REQUIREMENTS_COLLECTION", label: "Continue to Needs & Tools" });
          return;
        } else if (stage === "PLAN_EXPLORATION" || stage === "QUOTE_REVIEW" || stage === "PACKAGE_CUSTOMIZATION") {
          dispatchWorkflowTransition("GO_TO_STAGE", { stage: "KYC_VERIFICATION", label: "Confirm Quote & Start Smart KYC" });
          return;
        } else if (stage === "CUSTOMER_SIGNUP") {
          submitCustomerSignup();
          return;
        } else if (stage === "CUSTOMER_LOGIN") {
          submitCustomerLogin();
          return;
        } else {
          if (input) {
            input.focus();
            input.placeholder = "Please type a message or select an option above...";
            input.classList.add("border-danger");
            setTimeout(() => input.classList.remove("border-danger"), 1500);
          }
          return;
        }
      }

      if (input) input.value = "";
      
      // Append user bubble locally
      activeWorkflow.messages.push({ sender: "user", text: msg });
      renderChatThread();

      try {
        const res = await fetch("/api/advisor/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSessionId,
            message: msg,
            language: activeLanguage
          })
        });
        const data = await res.json();
        if (data.status === "success") {
          if (data.workflow) {
            activeWorkflow = data.workflow;
          }
          if (data.reply && activeWorkflow && activeWorkflow.messages) {
            const lastMsg = activeWorkflow.messages[activeWorkflow.messages.length - 1];
            if (!lastMsg || lastMsg.text !== data.reply) {
              activeWorkflow.messages.push({
                sender: "bot",
                text: data.reply,
                quick_replies: data.quick_replies || []
              });
            } else if (data.quick_replies && (!lastMsg.quick_replies || lastMsg.quick_replies.length === 0)) {
              lastMsg.quick_replies = data.quick_replies;
            }
          }

          const regNameEl = document.getElementById("regName");
          const regMobEl = document.getElementById("regMobile");
          const regBizEl = document.getElementById("regBizName");
          const regPwdEl = document.getElementById("regPwd");

          if (regNameEl && data.workflow && data.workflow.customer && data.workflow.customer.name && data.workflow.customer.name !== "Valued Business Owner") {
            regNameEl.value = data.workflow.customer.name;
            regNameEl.classList.add("is-valid", "border-success", "bg-success-subtle");
            if (regMobEl) {
              regMobEl.value = data.workflow.customer.mobile || "";
              regMobEl.classList.add("is-valid", "border-success", "bg-success-subtle");
            }
            if (regBizEl) {
              regBizEl.value = data.workflow.customer.business_name || "";
              regBizEl.classList.add("is-valid", "border-success", "bg-success-subtle");
            }
            if (regPwdEl && data.workflow.customer.password) {
              regPwdEl.value = data.workflow.customer.password;
              regPwdEl.classList.add("is-valid", "border-success", "bg-success-subtle");
            }

            setTimeout(() => {
              activeWorkflow = data.workflow;
              renderWorkflow();
            }, 850);
            return;
          }

          renderWorkflow();
        }
      } catch (err) {
        console.error("Chat error:", err);
      }
    }

    function autoFillSignupSample() {
      const nameEl = document.getElementById("regName");
      const mobEl = document.getElementById("regMobile");
      const bizEl = document.getElementById("regBizName");
      const pwdEl = document.getElementById("regPwd");
      if (nameEl) nameEl.value = "Anshul Kaushal";
      if (mobEl) mobEl.value = "9434134144";
      if (bizEl) bizEl.value = "Kaushal Sweets";
      if (pwdEl) pwdEl.value = "2323123";
      [nameEl, mobEl, bizEl, pwdEl].forEach(el => {
        if (el) {
          el.classList.add("is-valid", "border-success", "bg-success-subtle");
        }
      });
    }

    // 6. Customer Authentication Submissions
    async function submitCustomerLogin() {
      const id = document.getElementById("loginId").value.trim();
      const pwd = document.getElementById("loginPwd").value.trim();
      try {
        const res = await fetch("/api/auth/customer/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSessionId,
            identifier: id,
            password: pwd
          })
        });
        const data = await res.json();
        if (data.status === "success") {
          activeWorkflow = data.workflow;
          renderWorkflow();
        } else {
          alert(data.message);
        }
      } catch (e) {
        console.error("Login error:", e);
      }
    }

    async function submitCustomerSignup() {
      const name = document.getElementById("regName").value.trim();
      const mobile = document.getElementById("regMobile").value.trim();
      const bizName = document.getElementById("regBizName").value.trim();
      const pwd = document.getElementById("regPwd").value.trim();
      const consent = document.getElementById("regDpdpConsent").checked;

      try {
        const res = await fetch("/api/auth/customer/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSessionId,
            name: name,
            mobile: mobile,
            business_name: bizName,
            password: pwd,
            dpdp_consent: consent
          })
        });
        const data = await res.json();
        if (data.status === "success") {
          activeWorkflow = data.workflow;
          renderWorkflow();
        } else {
          alert(data.message);
        }
      } catch (e) {
        console.error("Signup error:", e);
      }
    }

    // 7. KYC Document Camera, Upload & Verification Controller
    let currentKycDoc = {
      file: null,
      blobUrl: null,
      fileName: "",
      fileSize: "",
      docType: "gst_certificate",
      specimenHint: null,
      isDemo: false,
      verificationResult: null,
      isApproved: false
    };
    let cameraMediaStream = null;

    function getDocTypeLabel(dt) {
      const map = {
        "gst_certificate": "Business / GST Certificate",
        "udyam_certificate": "Udyam MSME Certificate",
        "address_proof": "Address Proof / Utility Bill (< 90 Days)",
        "signatory_id": "Signatory ID Proof (PAN / Aadhaar)"
      };
      return map[dt] || "KYC Document";
    }

    function onDocTypeChanged(newType) {
      currentKycDoc.docType = newType;
      const badge = document.getElementById("previewDocTypeBadge");
      if (badge) badge.innerText = getDocTypeLabel(newType);
    }

    function toggleKycSubmitBtn() {
      const check = document.getElementById("kycDpdpCheck");
      const btn = document.getElementById("btnSubmitKycDoc");
      if (btn) {
        btn.disabled = !(check && check.checked && (currentKycDoc.file || currentKycDoc.blobUrl));
      }
    }

    async function triggerCameraCapture() {
      const errBanner = document.getElementById("cameraErrorBanner");
      if (errBanner) errBanner.classList.add("d-none");

      // 1. Try HTML5 MediaDevices getUserMedia for live viewfinder
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { ideal: "environment" } }
          });
          cameraMediaStream = stream;
          const video = document.getElementById("cameraVideo");
          if (video) {
            video.srcObject = stream;
            video.play();
          }
          const modalEl = document.getElementById("liveCameraModal");
          if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
            return;
          }
        } catch (err) {
          console.warn("Live camera stream unavailable, falling back to native file capture input:", err);
          if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
            if (errBanner) {
              errBanner.classList.remove("d-none");
              document.getElementById("cameraErrorMsg").innerText = "Camera permission was denied. You can select 'Upload from Device' or grant camera permission in your browser settings.";
            }
          }
        }
      }

      // 2. Native Camera file input fallback (captures directly from camera on mobile!)
      const cameraInput = document.getElementById("kycCameraInput");
      if (cameraInput) {
        cameraInput.click();
      } else {
        document.getElementById("kycFileInput").click();
      }
    }

    function captureLivePhoto() {
      const video = document.getElementById("cameraVideo");
      const canvas = document.getElementById("cameraCanvas");
      if (!video || !canvas) return;

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(blob => {
        if (!blob) return;
        const file = new File([blob], `captured_${currentKycDoc.docType}_${Date.now()}.jpg`, { type: "image/jpeg" });
        stopLiveCamera();
        handleKycFileSelected(file, "camera");
      }, "image/jpeg", 0.92);
    }

    function stopLiveCamera() {
      if (cameraMediaStream) {
        cameraMediaStream.getTracks().forEach(t => t.stop());
        cameraMediaStream = null;
      }
      const video = document.getElementById("cameraVideo");
      if (video) video.srcObject = null;
      const modalEl = document.getElementById("liveCameraModal");
      if (modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
    }

    function handleKycFileSelected(file, source) {
      if (!file) return;

      if (currentKycDoc.blobUrl) {
        URL.revokeObjectURL(currentKycDoc.blobUrl);
      }

      currentKycDoc.file = file;
      currentKycDoc.blobUrl = URL.createObjectURL(file);
      currentKycDoc.fileName = file.name || `document_${Date.now()}.jpg`;
      currentKycDoc.fileSize = file.size ? `${(file.size / 1024).toFixed(1)} KB` : "450 KB";
      currentKycDoc.verificationResult = null;
      currentKycDoc.isApproved = false;
      currentKycDoc.specimenHint = null;
      currentKycDoc.isDemo = false;

      const captureBox = document.getElementById("kycCaptureBox");
      const previewBox = document.getElementById("kycPreviewBox");
      const previewImg = document.getElementById("kycPreviewImg");
      const metaText = document.getElementById("previewMetaText");
      const badge = document.getElementById("previewDocTypeBadge");
      const resultBox = document.getElementById("kycResultBox");
      const pendingPlc = document.getElementById("kycPendingPlaceholder");
      const proceedBtn = document.getElementById("btnProceedTracking");

      if (captureBox) captureBox.classList.add("d-none");
      if (previewBox) previewBox.classList.remove("d-none");
      if (previewImg) previewImg.src = currentKycDoc.blobUrl;
      if (metaText) metaText.innerText = `${currentKycDoc.fileSize} · Source: ${source === 'camera' ? 'Camera 📸' : 'Device Upload 📁'}`;
      if (badge) badge.innerText = getDocTypeLabel(currentKycDoc.docType);
      if (resultBox) resultBox.classList.add("d-none");
      if (pendingPlc) pendingPlc.classList.remove("d-none");
      if (proceedBtn) {
        proceedBtn.disabled = true;
        proceedBtn.className = "btn btn-secondary w-100 py-2 fw-bold";
      }

      toggleKycSubmitBtn();
    }

    function retakeKycPhoto() {
      triggerCameraCapture();
    }

    function replaceKycFile() {
      const fileInput = document.getElementById("kycFileInput");
      if (fileInput) fileInput.click();
    }

    function removeKycPhoto() {
      if (currentKycDoc.blobUrl) {
        URL.revokeObjectURL(currentKycDoc.blobUrl);
        currentKycDoc.blobUrl = null;
      }
      currentKycDoc.file = null;
      currentKycDoc.fileName = "";
      currentKycDoc.verificationResult = null;
      currentKycDoc.isApproved = false;

      const captureBox = document.getElementById("kycCaptureBox");
      const previewBox = document.getElementById("kycPreviewBox");
      const resultBox = document.getElementById("kycResultBox");
      const pendingPlc = document.getElementById("kycPendingPlaceholder");
      const proceedBtn = document.getElementById("btnProceedTracking");
      const cameraInput = document.getElementById("kycCameraInput");
      const fileInput = document.getElementById("kycFileInput");

      if (cameraInput) cameraInput.value = "";
      if (fileInput) fileInput.value = "";
      if (captureBox) captureBox.classList.remove("d-none");
      if (previewBox) previewBox.classList.add("d-none");
      if (resultBox) resultBox.classList.add("d-none");
      if (pendingPlc) pendingPlc.classList.remove("d-none");
      if (proceedBtn) {
        proceedBtn.disabled = true;
        proceedBtn.className = "btn btn-secondary w-100 py-2 fw-bold";
      }

      toggleKycSubmitBtn();
    }

    function loadSpecimenKyc(applicantId) {
      currentKycDoc.specimenHint = applicantId;
      currentKycDoc.isDemo = true;
      const typeSelect = document.getElementById("kycDocTypeSelect");
      if (applicantId === "K11" && typeSelect) {
        typeSelect.value = "address_proof";
        currentKycDoc.docType = "address_proof";
      } else if (typeSelect) {
        typeSelect.value = "gst_certificate";
        currentKycDoc.docType = "gst_certificate";
      }

      // Generate simulated sample document Blob for preview
      const canvas = document.createElement("canvas");
      canvas.width = 600;
      canvas.height = 400;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, 600, 400);
      ctx.strokeStyle = "#eb0029";
      ctx.lineWidth = 4;
      ctx.strokeRect(10, 10, 580, 380);
      ctx.fillStyle = "#111111";
      ctx.font = "bold 22px sans-serif";
      ctx.fillText(`AIRTEL SMART KYC SPECIMEN - ${applicantId}`, 30, 60);
      ctx.font = "16px sans-serif";
      ctx.fillText(`Document Type: ${getDocTypeLabel(currentKycDoc.docType)}`, 30, 100);
      ctx.fillText(`Benchmark ID: ${applicantId} · Statutory Verification Test`, 30, 130);
      ctx.fillText(`DPDP Compliance: Ephemeral RAM Buffer (24h Hard Purge)`, 30, 160);
      ctx.fillStyle = "#666666";
      ctx.font = "14px monospace";
      ctx.fillText(`SHA256 Fingerprint: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca`, 30, 220);

      canvas.toBlob(blob => {
        if (!blob) return;
        const file = new File([blob], `${applicantId}_${currentKycDoc.docType}.png`, { type: "image/png" });
        handleKycFileSelected(file, "upload");
        submitKycDocument();
      }, "image/png");
    }

    async function submitKycDocument() {
      if (!currentKycDoc.file && !currentKycDoc.blobUrl) return;

      const check = document.getElementById("kycDpdpCheck");
      if (check && !check.checked) {
        alert("Please confirm the DPDP Act 2023 statutory consent notice before proceeding.");
        return;
      }

      const btn = document.getElementById("btnSubmitKycDoc");
      const procBox = document.getElementById("kycProcessingBox");
      const scanLaser = document.getElementById("scanningLaser");
      const resultBox = document.getElementById("kycResultBox");
      const pendingPlc = document.getElementById("kycPendingPlaceholder");

      if (btn) btn.disabled = true;
      if (procBox) procBox.classList.remove("d-none");
      if (scanLaser) scanLaser.classList.remove("d-none");
      if (resultBox) resultBox.classList.add("d-none");
      if (pendingPlc) pendingPlc.classList.add("d-none");

      const formData = new FormData();
      formData.append("document_file", currentKycDoc.file || new Blob([], { type: "image/png" }), currentKycDoc.fileName || "doc.png");
      formData.append("doc_type", currentKycDoc.docType);
      formData.append("session_id", activeSessionId);
      formData.append("dpdp_consent", "true");
      if (currentKycDoc.isDemo && currentKycDoc.specimenHint) {
        formData.append("is_demo", "true");
        formData.append("applicant_id", currentKycDoc.specimenHint);
      }

      try {
        const res = await fetch("/api/kyc/document/process", {
          method: "POST",
          body: formData
        });
        const data = await res.json();

        // Brief delay for visual scan animation
        setTimeout(() => {
          if (procBox) procBox.classList.add("d-none");
          if (scanLaser) scanLaser.classList.add("d-none");
          if (btn) btn.disabled = false;

          renderKycVerificationResult(data);
        }, 1200);

      } catch (err) {
        console.error("KYC processing error:", err);
        if (procBox) procBox.classList.add("d-none");
        if (scanLaser) scanLaser.classList.add("d-none");
        if (btn) btn.disabled = false;
        alert("Error submitting document for verification. Please try again.");
      }
    }

    function renderKycVerificationResult(data) {
      const resultBox = document.getElementById("kycResultBox");
      const pendingPlc = document.getElementById("kycPendingPlaceholder");
      const proceedBtn = document.getElementById("btnProceedTracking");
      const noticeText = document.getElementById("proceedNoticeText");
      if (!resultBox) return;

      if (pendingPlc) pendingPlc.classList.add("d-none");
      resultBox.classList.remove("d-none");
      currentKycDoc.verificationResult = data;
      currentKycDoc.isApproved = Boolean(data.is_approved);

      const rep = data.evaluation || {};
      const isApproved = Boolean(data.is_approved);
      const isDemo = Boolean(data.is_demo);
      const excs = rep.exceptions || [];
      const status = data.status || rep.overall_status || "PENDING";

      let comparisonHtml = "";
      if (rep.field_comparison && rep.field_comparison.length) {
        comparisonHtml = `
          <div class="table-responsive mt-2">
            <table class="table table-sm table-bordered align-middle small mb-0">
              <thead class="table-light">
                <tr><th>Statutory Field</th><th>Document Extraction</th><th>Registry Status</th><th>Result</th></tr>
              </thead>
              <tbody>
                ${rep.field_comparison.map(f => `
                  <tr>
                    <td><strong>${f.field}</strong></td>
                    <td class="font-monospace small">${f.ocr_data}</td>
                    <td class="small">${f.registry_data}</td>
                    <td><span class="badge ${f.result === 'PASS' ? 'bg-success' : (f.result === 'FAIL' ? 'bg-danger' : 'bg-warning text-dark')}">${f.result}</span></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
      }

      let exceptionsHtml = "";
      if (excs.length) {
        exceptionsHtml = `
          <div class="alert alert-danger py-2 px-3 small mt-2">
            <h6 class="fw-bold mb-1"><i class="bi bi-exclamation-octagon-fill me-1"></i> Exception Notes &amp; Statutory Advice:</h6>
            <ul class="mb-0 ps-3">
              ${excs.map(e => `
                <li class="mb-1">
                  <strong>${e.title}:</strong> ${e.message}
                  ${e.message_hi ? `<div class="text-muted fst-italic">${e.message_hi}</div>` : ''}
                </li>
              `).join('')}
            </ul>
          </div>
        `;
      }

      let demoDisclaimerHtml = "";
      if (isDemo) {
        demoDisclaimerHtml = `
          <div class="alert alert-warning py-1 px-2 border border-warning small mb-2 fw-semibold">
            <i class="bi bi-exclamation-triangle me-1"></i> Specimen simulation — not customer verification
          </div>
        `;
      }

      // Specific alert messages for user feedback
      let specificAlertHtml = "";
      if (status === "DOCUMENT_NOT_RELEVANT") {
        specificAlertHtml = `
          <div class="alert alert-warning py-2 px-3 small mb-2">
            <i class="bi bi-shield-exclamation text-warning me-1"></i> <strong>This image doesn't appear to be the selected KYC document.</strong> Please upload or capture the correct document.
          </div>
        `;
      } else if (status === "DOCUMENT_TYPE_MISMATCH") {
        specificAlertHtml = `
          <div class="alert alert-warning py-2 px-3 small mb-2">
            <i class="bi bi-arrow-left-right text-warning me-1"></i> <strong>Document Type Mismatch:</strong> Expected <em>${getDocTypeLabel(currentKycDoc.docType)}</em>. Please choose the correct document type or upload the matching file.
          </div>
        `;
      } else if (status === "UNREADABLE_LOW_RESOLUTION") {
        specificAlertHtml = `
          <div class="alert alert-danger py-2 px-3 small mb-2">
            <i class="bi bi-camera-fill me-1"></i> <strong>Document image unreadable or blurry.</strong> Please take a clearer photo with all 4 corners visible.
          </div>
        `;
      } else if (status === "MANUAL_REVIEW_REQUIRED") {
        specificAlertHtml = `
          <div class="alert alert-info py-2 px-3 small mb-2">
            <i class="bi bi-person-check-fill me-1"></i> <strong>Manual Review Required:</strong> Automated verification is unconfigured or requires KYC officer sign-off.
          </div>
        `;
      }

      if (isApproved) {
        resultBox.innerHTML = `
          <div class="card p-3 border border-success bg-success-subtle shadow-sm animate__animated animate__fadeIn">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-check-circle-fill text-success fs-4"></i>
                <div>
                  <h6 class="fw-bold text-success mb-0">KYC VERIFICATION APPROVED</h6>
                  <span class="small text-muted">Statutory DoT checks &amp; DPDP compliance confirmed.</span>
                </div>
              </div>
              <span class="badge bg-success px-2 py-1">APPROVED</span>
            </div>
            
            ${demoDisclaimerHtml}
            <div class="alert alert-light border small text-muted py-1 px-2 mb-2">
              <i class="bi bi-info-circle me-1"></i> <strong>Verification Confirmed:</strong> Document extraction verified against statutory registries and DoT 90-day recency benchmark. PII masked.
            </div>

            ${comparisonHtml}
          </div>
        `;

        if (proceedBtn) {
          proceedBtn.disabled = false;
          proceedBtn.className = "btn btn-airtel w-100 py-3 fw-bold fs-6 mt-3 shadow animate__animated animate__pulse animate__infinite";
        }
        if (noticeText) {
          noticeText.innerHTML = '<i class="bi bi-check-circle-fill text-success me-1"></i> Document verified! Click above to proceed to installation tracking.';
        }

        if (activeWorkflow && activeWorkflow.kyc) {
          activeWorkflow.kyc.status = "APPROVED";
          activeWorkflow.kyc.verified = true;
        }

      } else {
        resultBox.innerHTML = `
          <div class="card p-3 border border-danger bg-danger-subtle shadow-sm animate__animated animate__shakeX">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-x-circle-fill text-danger fs-4"></i>
                <div>
                  <h6 class="fw-bold text-danger mb-0">KYC NOT APPROVED</h6>
                  <span class="small text-muted">${rep.verdict_summary || 'Document exception detected. DoT criteria not met.'}</span>
                </div>
              </div>
              <span class="badge bg-danger px-2 py-1">${status}</span>
            </div>

            ${demoDisclaimerHtml}
            ${specificAlertHtml}
            ${exceptionsHtml}
            ${comparisonHtml}

            <div class="mt-3 d-flex gap-2">
              <button type="button" class="btn btn-sm btn-outline-danger w-50" onclick="retakeKycPhoto()"><i class="bi bi-camera me-1"></i> Retake Photo</button>
              <button type="button" class="btn btn-sm btn-outline-secondary w-50" onclick="replaceKycFile()"><i class="bi bi-upload me-1"></i> Upload Alternate</button>
            </div>
          </div>
        `;

        if (proceedBtn) {
          proceedBtn.disabled = true;
          proceedBtn.className = "btn btn-secondary w-100 py-2 fw-bold";
        }
        if (noticeText) {
          noticeText.innerHTML = '<i class="bi bi-shield-x text-danger me-1"></i> Resolve document exception or upload valid proof to proceed.';
        }
      }
    }

    // 7. KYC Lookup Helpers
    async function runGstinLookup() {
      const gstin = document.getElementById("kycGstinInput").value.trim();
      try {
        const res = await fetch("/api/kyc/lookup_gstin", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ gstin: gstin })
        });
        const data = await res.json();
        const box = document.getElementById("gstinResultBox");
        if (data.valid) {
          box.innerHTML = `
            <div><strong>Legal Name:</strong> ${data.legal_name}</div>
            <div><strong>Trade Name:</strong> ${data.trade_name}</div>
            <div><strong>Status:</strong> <span class="badge ${data.is_active ? 'bg-success' : 'bg-danger'}">${data.status}</span> (Masked: ${data.masked_gstin})</div>
          `;
        } else {
          box.innerHTML = `<span class="text-danger">${data.message}</span>`;
        }
      } catch (e) {
        console.error(e);
      }
    }

    // 8. Chatbot Panel Visibility & Toggle Controller
    let isChatbotOpen = true;

    function toggleChatbot() {
      isChatbotOpen = !isChatbotOpen;
      const layout = document.getElementById("workspaceLayout");
      const toggleBtn = document.getElementById("btnChatToggle");
      const statusText = document.getElementById("agentBtnStatus");
      const arrowIcon = document.getElementById("toggleArrowIcon");
      const fab = document.getElementById("floatingAgentFab");

      if (isChatbotOpen) {
        if (layout) layout.classList.remove("chat-closed");
        if (toggleBtn) {
          toggleBtn.classList.add("active");
          toggleBtn.classList.remove("closed");
        }
        if (statusText) statusText.innerHTML = '<i class="bi bi-circle-fill text-success me-1"></i>Active · Click to Hide';
        if (arrowIcon) arrowIcon.className = "bi bi-chevron-right toggle-arrow d-none d-md-inline ms-1";
        if (fab) fab.style.display = "none";
      } else {
        if (layout) layout.classList.add("chat-closed");
        if (toggleBtn) {
          toggleBtn.classList.remove("active");
          toggleBtn.classList.add("closed");
        }
        if (statusText) statusText.innerHTML = '<i class="bi bi-circle-fill text-secondary me-1"></i>Hidden · Click to Open';
        if (arrowIcon) arrowIcon.className = "bi bi-chevron-left toggle-arrow d-none d-md-inline ms-1";
        if (fab) fab.style.display = "inline-flex";
      }

      localStorage.setItem("udyam_chatbot_open", isChatbotOpen ? "true" : "false");
    }

    function initChatbotVisibility() {
      const saved = localStorage.getItem("udyam_chatbot_open");
      if (saved === "false") {
        isChatbotOpen = true;
        toggleChatbot();
      }
    }

    // 9. Customer Logout Controller (Resets session & returns to main page)
    function logoutCustomer() {
      localStorage.removeItem("udyam_session_id");
      localStorage.removeItem("udyam_intro_seen");
      localStorage.removeItem("udyam_chatbot_open");
      sessionStorage.clear();

      try {
        fetch("/api/advisor/session/reset", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: activeSessionId })
        }).finally(() => {
          window.location.href = "/";
        });
      } catch (e) {
        window.location.href = "/";
      }
    }

    // 9. Multilingual Switcher
    function changeLanguage(lang) {
      activeLanguage = lang;
      dispatchWorkflowTransition("SET_LANGUAGE", { language: lang });
    }

    function togglePasswordVisibility(inputId) {
      const el = document.getElementById(inputId);
      el.type = el.type === "password" ? "text" : "password";
    }

    // On Load
    document.addEventListener("DOMContentLoaded", () => {
      checkIntroState();
      initChatbotVisibility();
    });
  
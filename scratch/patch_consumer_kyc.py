consumer_path = r"E:\Airtel\prototype\templates\consumer.html"

with open(consumer_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Upgrade Step 3 HTML
old_step3 = """      <!-- STEP 3: SMART KYC & DPDP CONSENT -->
      <div id="step3Container" style="display: none;" class="py-4">
        <div class="step-indicator">
          <span class="step-pill-indicator">1. Needs</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator">2. Package</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator active">3. Instant Verification</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator">4. Confirmation</span>
        </div>

        <h4 class="fw-bold mb-3">Paperless Smart Verification</h4>
        <p class="text-secondary small mb-4">Verify your business details online in seconds.</p>

        <div class="advisor-box p-4 mb-4">
          <!-- DPDP Consent Banner -->
          <div class="alert alert-light border small text-dark mb-4 p-3 rounded">
            <div class="d-flex gap-2">
              <i class="bi bi-shield-check text-success fs-5"></i>
              <div>
                <strong>Privacy Notice (DPDP Act 2023):</strong>
                We only collect identity details required by the Department of Telecommunications (DoT) for service activation. Your documents are encrypted and your sensitive identifiers are masked.
              </div>
            </div>
            <div class="form-check mt-3">
              <input class="form-check-input" type="checkbox" id="dpdpConsent" checked>
              <label class="form-check-label fw-bold small" for="dpdpConsent">
                I give explicit consent under DPDP Act 2023 for telecom KYC verification.
              </label>
            </div>
          </div>

          <!-- Business Form -->
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Business Name</label>
              <input type="text" id="custBizName" class="form-control form-clean" value="Harmony Dental Care">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Authorized Signatory</label>
              <input type="text" id="custContactName" class="form-control form-clean" value="Joseph Shah">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Mobile Number (For Status Updates)</label>
              <input type="text" id="custPhone" class="form-control form-clean" value="+91 98765 43210">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Installation City</label>
              <input type="text" id="custCity" class="form-control form-clean" value="Kolkata">
            </div>
          </div>

          <!-- GSTIN Lookup -->
          <div class="p-3 border rounded bg-light mb-4">
            <label class="form-label small fw-bold text-dark">Enter GSTIN (Auto-fills verified registration)</label>
            <div class="input-group mb-2">
              <input type="text" id="custGstin" class="form-control form-clean" value="19EOGXH4115Y1ZL" placeholder="15-character GSTIN">
              <button class="btn btn-outline-dark btn-sm fw-bold px-3" type="button" onclick="verifyGstinInstant()">Verify GSTIN</button>
            </div>
            <div id="gstinStatusAlert" class="small text-success fw-bold">
              <i class="bi bi-check-circle-fill me-1"></i> GSTIN Verified Active · Registered Address matched
            </div>
          </div>

          <div class="d-flex justify-content-between align-items-center">
            <button class="btn btn-outline-secondary btn-sm" onclick="goToStep(2)">
              <i class="bi bi-arrow-left me-1"></i> Back to Quote
            </button>
            <button class="btn-primary-airtel py-2 px-4" onclick="submitConsumerOrder()">
              Submit Application &amp; Confirm Order <i class="bi bi-check-circle-fill ms-1"></i>
            </button>
          </div>
        </div>
      </div>"""

new_step3 = """      <!-- STEP 3: SMART KYC & DPDP CONSENT -->
      <div id="step3Container" style="display: none;" class="py-4">
        <div class="step-indicator">
          <span class="step-pill-indicator">1. Needs</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator">2. Package</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator active">3. Instant Verification</span>
          <i class="bi bi-chevron-right text-muted"></i>
          <span class="step-pill-indicator">4. Confirmation</span>
        </div>

        <h4 class="fw-bold mb-2">Paperless Smart Verification</h4>
        <p class="text-secondary small mb-4">Fast-track business verification with simulated registries &amp; smart exception guidance.</p>

        <div class="advisor-box p-4 mb-4">
          <!-- DPDP Consent Banner with Bilingual Toggle -->
          <div class="alert alert-light border small text-dark mb-4 p-3 rounded">
            <div class="d-flex justify-content-between align-items-start">
              <div class="d-flex gap-2">
                <i class="bi bi-shield-check text-success fs-5"></i>
                <div>
                  <strong>Privacy Notice (DPDP Act 2023 &amp; DoT Mandate):</strong>
                  <div id="dpdpNoticeTextEn" class="mt-1">
                    We only collect identity details required by the Department of Telecommunications (DoT) for service activation. Your documents are encrypted, temporary files purge within 24 hours, and sensitive identifiers are masked.
                  </div>
                  <div id="dpdpNoticeTextHi" class="mt-1 text-muted font-monospace" style="display:none;">
                    Hum keval wahi dastavez lete hain jo DoT ke statutory telecom niyamon ke antargat aavashyak hain. Aapka data puri tarah surakshit aur encrypted rehta hai.
                  </div>
                </div>
              </div>
              <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-secondary btn-sm py-0 active" id="btnLangEn" onclick="toggleConsentLang('en')">EN</button>
                <button type="button" class="btn btn-outline-secondary btn-sm py-0" id="btnLangHi" onclick="toggleConsentLang('hi')">हिंदी</button>
              </div>
            </div>
            <div class="form-check mt-3 pt-2 border-top">
              <input class="form-check-input" type="checkbox" id="dpdpConsent" checked>
              <label class="form-check-label fw-bold small" for="dpdpConsent">
                I give explicit affirmative consent under DPDP Act 2023 for telecom KYC verification.
              </label>
            </div>
          </div>

          <!-- Actionable Exception Resolution Card (Shown dynamically on verification anomaly) -->
          <div id="consumerExceptionCard" class="alert alert-danger border border-danger p-3 mb-4 rounded" style="display: none;">
            <div class="d-flex align-items-start gap-2">
              <i class="bi bi-exclamation-triangle-fill text-danger fs-5 mt-1"></i>
              <div class="w-100">
                <div class="fw-bold text-danger mb-1" id="consumerExceptionTitle">Verification Exception</div>
                <div class="small text-dark mb-1" id="consumerExceptionEn">...</div>
                <div class="small text-muted font-monospace" id="consumerExceptionHi">...</div>
                <div class="mt-2 pt-2 border-top border-danger border-opacity-25 small fw-bold text-danger">
                  <i class="bi bi-arrow-right-circle me-1"></i> Required Next Action: <span id="consumerExceptionAction" class="fw-normal text-dark">...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Business Entity Inputs -->
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Business Trade Name</label>
              <input type="text" id="custBizName" class="form-control form-clean" value="Harmony Dental Care">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Authorized Signatory Name</label>
              <input type="text" id="custContactName" class="form-control form-clean" value="Joseph Shah">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Mobile Number (For Tracking Updates)</label>
              <input type="text" id="custPhone" class="form-control form-clean" value="+91 98765 43210">
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold text-muted">Installation City</label>
              <input type="text" id="custCity" class="form-control form-clean" value="Kolkata">
            </div>
          </div>

          <!-- Dual Registry Verification (GSTIN & Udyam) -->
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <div class="p-3 border rounded bg-light h-100">
                <label class="form-label small fw-bold text-dark">GSTIN Verification (15 Characters)</label>
                <div class="input-group mb-2">
                  <input type="text" id="custGstin" class="form-control form-clean font-monospace" value="19EOGXH4115Y1ZL" placeholder="e.g. 19EOGXH4115Y1ZL">
                  <button class="btn btn-outline-dark btn-sm fw-bold px-3" type="button" onclick="verifyGstinInstant()">Verify</button>
                </div>
                <div id="gstinStatusAlert" class="small text-success fw-bold">
                  <i class="bi bi-check-circle-fill me-1"></i> Active GSTIN Verified · Auto-fills registration
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="p-3 border rounded bg-light h-100">
                <label class="form-label small fw-bold text-dark">MSME Udyam Number (Optional / Alternate)</label>
                <div class="input-group mb-2">
                  <input type="text" id="custUdyam" class="form-control form-clean font-monospace" value="UDYAM-WB-00-5053330" placeholder="e.g. UDYAM-XX-00-XXXXXXX">
                  <button class="btn btn-outline-dark btn-sm fw-bold px-3" type="button" onclick="verifyUdyamInstant()">Verify</button>
                </div>
                <div id="udyamStatusAlert" class="small text-muted">
                  <i class="bi bi-info-circle me-1"></i> MSME micro/small enterprise certificate check
                </div>
              </div>
            </div>
          </div>

          <!-- Address Proof & Freshness Verification (90-Day Rule) -->
          <div class="p-3 border rounded bg-light mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <label class="form-label small fw-bold text-dark mb-0">Electricity / Utility Bill (<span class="text-danger">&le;90 Days Old</span> from 15-Jul-2026)</label>
              <span class="badge bg-secondary font-monospace" style="font-size: 0.72rem;">Benchmark: 15-Jul-2026</span>
            </div>
            <div class="row g-2 align-items-center">
              <div class="col-md-7">
                <select id="custBillDateSelect" class="form-select form-select-sm" onchange="checkBillDateFreshness()">
                  <option value="2026-05-22">Electricity Bill - Issued 22-May-2026 (54 days old · VALID)</option>
                  <option value="2026-06-26">Electricity Bill - Issued 26-Jun-2026 (19 days old · VALID)</option>
                  <option value="2026-01-10">Electricity Bill - Issued 10-Jan-2026 (186 days old · EXPIRED)</option>
                  <option value="2025-10-31">Electricity Bill - Issued 31-Oct-2025 (257 days old · EXPIRED)</option>
                </select>
              </div>
              <div class="col-md-5">
                <div id="billFreshnessAlert" class="small text-success fw-bold">
                  <i class="bi bi-check-circle-fill me-1"></i> Bill is 54 days old (&le;90-day statutory limit)
                </div>
              </div>
            </div>
          </div>

          <!-- Form Navigation -->
          <div class="d-flex justify-content-between align-items-center">
            <button class="btn btn-outline-secondary btn-sm" onclick="goToStep(2)">
              <i class="bi bi-arrow-left me-1"></i> Back to Quote
            </button>
            <button class="btn-primary-airtel py-2 px-4" onclick="submitConsumerOrder()">
              Submit Application &amp; Confirm Order <i class="bi bi-check-circle-fill ms-1"></i>
            </button>
          </div>
        </div>
      </div>"""

if old_step3 in text:
    text = text.replace(old_step3, new_step3)
    print("Replaced step3 HTML successfully!")
else:
    print("Warning: old_step3 exact string not matched!")

# 2. Upgrade JavaScript
old_js = """    function verifyGstinInstant() {
      const g = document.getElementById("custGstin").value.trim();
      fetch("/api/kyc/lookup_gstin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gstin: g })
      })
      .then(r => r.json())
      .then(data => {
        const al = document.getElementById("gstinStatusAlert");
        if (data.valid) {
          al.className = "small text-success fw-bold";
          al.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> ${data.legal_name} (${data.status}) · Address verified`;
          document.getElementById("custBizName").value = data.trade_name;
        } else {
          al.className = "small text-danger fw-bold";
          al.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${data.message}`;
        }
      });
    }"""

new_js = """    function toggleConsentLang(lang) {
      if (lang === 'hi') {
        document.getElementById('dpdpNoticeTextEn').style.display = 'none';
        document.getElementById('dpdpNoticeTextHi').style.display = 'block';
        document.getElementById('btnLangHi').classList.add('active');
        document.getElementById('btnLangEn').classList.remove('active');
      } else {
        document.getElementById('dpdpNoticeTextEn').style.display = 'block';
        document.getElementById('dpdpNoticeTextHi').style.display = 'none';
        document.getElementById('btnLangEn').classList.add('active');
        document.getElementById('btnLangHi').classList.remove('active');
      }
    }

    function verifyGstinInstant() {
      const g = document.getElementById("custGstin").value.trim();
      const exCard = document.getElementById("consumerExceptionCard");
      
      fetch("/api/kyc/lookup_gstin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gstin: g })
      })
      .then(r => r.json())
      .then(data => {
        const al = document.getElementById("gstinStatusAlert");
        if (data.valid && data.is_active) {
          al.className = "small text-success fw-bold";
          al.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> ${data.legal_name} (ACTIVE) · Address verified`;
          document.getElementById("custBizName").value = data.trade_name || data.legal_name;
          exCard.style.display = "none";
        } else if (data.status === "CANCELLED" || data.status === "SUSPENDED") {
          al.className = "small text-danger fw-bold";
          al.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> GST Registration ${data.status}!`;
          
          document.getElementById("consumerExceptionTitle").innerText = `GST Registration ${data.status}`;
          document.getElementById("consumerExceptionEn").innerText = data.actionable_advice || data.message;
          document.getElementById("consumerExceptionHi").innerText = data.actionable_advice_hi || "";
          document.getElementById("consumerExceptionAction").innerText = "Please review your registration certificate or contact the GST authority. You may also proceed using your MSME Udyam certificate.";
          exCard.style.display = "block";
        } else {
          al.className = "small text-danger fw-bold";
          al.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${data.message || 'GSTIN not found in registry'}`;
          exCard.style.display = "none";
        }
      });
    }

    function verifyUdyamInstant() {
      const u = document.getElementById("custUdyam").value.trim();
      fetch("/api/kyc/lookup_udyam", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ udyam_number: u })
      })
      .then(r => r.json())
      .then(data => {
        const al = document.getElementById("udyamStatusAlert");
        if (data.valid) {
          al.className = "small text-success fw-bold";
          al.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> ${data.enterprise_name} (${data.enterprise_type} Enterprise) · Verified`;
          if (!document.getElementById("custBizName").value) {
            document.getElementById("custBizName").value = data.enterprise_name;
          }
        } else {
          al.className = "small text-danger fw-bold";
          al.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${data.message}`;
        }
      });
    }

    function checkBillDateFreshness() {
      const bDate = document.getElementById("custBillDateSelect").value;
      const refDate = new Date("2026-07-15");
      const chosen = new Date(bDate);
      const diffDays = Math.round((refDate - chosen) / (1000 * 60 * 60 * 24));
      
      const al = document.getElementById("billFreshnessAlert");
      const exCard = document.getElementById("consumerExceptionCard");
      
      if (diffDays <= 90 && diffDays >= 0) {
        al.className = "small text-success fw-bold";
        al.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> Bill is ${diffDays} days old (&le;90-day statutory limit)`;
        if (exCard.style.display === "block" && document.getElementById("consumerExceptionTitle").innerText.includes("Utility Bill")) {
          exCard.style.display = "none";
        }
      } else {
        al.className = "small text-danger fw-bold";
        al.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> Bill is ${diffDays} days old (EXPIRED > 90d)`;
        
        document.getElementById("consumerExceptionTitle").innerText = "Utility Bill Older than 90 Days";
        document.getElementById("consumerExceptionEn").innerText = `This electricity bill is ${diffDays} days old (exceeds permitted 90-day period relative to 15-Jul-2026). Please upload a more recent bill.`;
        document.getElementById("consumerExceptionHi").innerText = `Yeh bijli ka bill ${diffDays} din purana hai. Kripya 16-Apr-2026 ke baad ka taaza bill upload karein.`;
        document.getElementById("consumerExceptionAction").innerText = "Upload an electricity, water or landline bill issued after 16-Apr-2026.";
        exCard.style.display = "block";
      }
    }"""

if old_js in text:
    text = text.replace(old_js, new_js)
    print("Replaced KYC consumer JavaScript successfully!")
else:
    print("Warning: old_js exact string not matched!")

with open(consumer_path, "w", encoding="utf-8") as f:
    f.write(text)
print("Updated consumer.html with Smart KYC controls!")

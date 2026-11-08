import os

path = r"e:\Airtel\prototype\templates\consumer.html"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Uncheck DPDP consent by default and update text
old_check = '<input class="form-check-input" type="checkbox" id="kycDpdpCheck" checked onchange="toggleKycSubmitBtn()">'
new_check = '<input class="form-check-input" type="checkbox" id="kycDpdpCheck" onchange="toggleKycSubmitBtn()">'

if old_check in text:
    text = text.replace(old_check, new_check, 1)
    print("1. Unchecked kycDpdpCheck by default.")
else:
    print("WARNING: old_check not found!")

old_consent_text = "PII is masked and processed in an ephemeral RAM buffer purged within 24 hours."
new_consent_text = "PII is masked and processed purely in an ephemeral RAM buffer during request execution with no persistent raw image storage."
if old_consent_text in text:
    text = text.replace(old_consent_text, new_consent_text, 1)
    print("1b. Updated consent notice text.")

# 2. Update currentKycDoc initialization
old_kyc_init = '''    let currentKycDoc = {
      file: null,
      blobUrl: null,
      fileName: "",
      fileSize: "",
      docType: "gst_certificate",
      specimenHint: "K02",
      verificationResult: null,
      isApproved: false
    };'''

new_kyc_init = '''    let currentKycDoc = {
      file: null,
      blobUrl: null,
      fileName: "",
      fileSize: "",
      docType: "gst_certificate",
      specimenHint: null,
      isDemo: false,
      verificationResult: null,
      isApproved: false
    };'''

if old_kyc_init in text:
    text = text.replace(old_kyc_init, new_kyc_init, 1)
    print("2. Updated currentKycDoc init.")
else:
    print("WARNING: old_kyc_init not found!")

# 3. Update handleKycFileSelected to clear demo hints on user upload
old_handle = '''      currentKycDoc.file = file;
      currentKycDoc.blobUrl = URL.createObjectURL(file);
      currentKycDoc.fileName = file.name || `document_${Date.now()}.jpg`;
      currentKycDoc.fileSize = file.size ? `${(file.size / 1024).toFixed(1)} KB` : "450 KB";
      currentKycDoc.verificationResult = null;
      currentKycDoc.isApproved = false;'''

new_handle = '''      currentKycDoc.file = file;
      currentKycDoc.blobUrl = URL.createObjectURL(file);
      currentKycDoc.fileName = file.name || `document_${Date.now()}.jpg`;
      currentKycDoc.fileSize = file.size ? `${(file.size / 1024).toFixed(1)} KB` : "450 KB";
      currentKycDoc.verificationResult = null;
      currentKycDoc.isApproved = false;
      currentKycDoc.specimenHint = null;
      currentKycDoc.isDemo = false;'''

if old_handle in text:
    text = text.replace(old_handle, new_handle, 1)
    print("3. Updated handleKycFileSelected.")
else:
    print("WARNING: old_handle not found!")

# 4. Update loadSpecimenKyc to set isDemo flag
old_spec = '''    function loadSpecimenKyc(applicantId) {
      currentKycDoc.specimenHint = applicantId;'''

new_spec = '''    function loadSpecimenKyc(applicantId) {
      currentKycDoc.specimenHint = applicantId;
      currentKycDoc.isDemo = true;'''

if old_spec in text:
    text = text.replace(old_spec, new_spec, 1)
    print("4. Updated loadSpecimenKyc.")
else:
    print("WARNING: old_spec not found!")

# 5. Update submitKycDocument formData
old_form = '''      const formData = new FormData();
      formData.append("document_file", currentKycDoc.file || new Blob([], { type: "image/png" }), currentKycDoc.fileName || "doc.png");
      formData.append("doc_type", currentKycDoc.docType);
      formData.append("applicant_id", currentKycDoc.specimenHint || "K02");
      formData.append("session_id", activeSessionId);'''

new_form = '''      const formData = new FormData();
      formData.append("document_file", currentKycDoc.file || new Blob([], { type: "image/png" }), currentKycDoc.fileName || "doc.png");
      formData.append("doc_type", currentKycDoc.docType);
      formData.append("session_id", activeSessionId);
      formData.append("dpdp_consent", "true");
      if (currentKycDoc.isDemo && currentKycDoc.specimenHint) {
        formData.append("is_demo", "true");
        formData.append("applicant_id", currentKycDoc.specimenHint);
      }'''

if old_form in text:
    text = text.replace(old_form, new_form, 1)
    print("5. Updated submitKycDocument.")
else:
    print("WARNING: old_form not found!")

# 6. Update renderKycVerificationResult
old_render_start = 'function renderKycVerificationResult(data) {'
old_render_end = '    // 7. KYC Lookup Helpers\n    async function runGstinLookup() {'

start_idx = text.find(old_render_start)
end_idx = text.find(old_render_end)

if start_idx != -1 and end_idx != -1:
    new_render = '''function renderKycVerificationResult(data) {
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

'''
    text = text[:start_idx] + new_render + text[end_idx:]
    print("6. Updated renderKycVerificationResult.")
else:
    print(f"WARNING: render indices not found! start={start_idx}, end={end_idx}")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated consumer.html.")

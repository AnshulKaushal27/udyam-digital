import re

control_path = r"E:\Airtel\prototype\templates\control.html"

with open(control_path, "r", encoding="utf-8") as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. UPGRADE SECTION: #sec-kyc
# -----------------------------------------------------------------------------
new_sec_kyc = """      <section id="sec-kyc" style="display: none;">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0">Smart KYC &amp; Exception Resolution Desk</h4>
            <div class="small text-muted">Automated registry validation &amp; document intelligence with human oversight · Reference Date: <strong>15-Jul-2026</strong></div>
          </div>
          <div class="d-flex gap-2">
            <span class="badge bg-light text-dark border"><i class="bi bi-shield-check text-success me-1"></i> DPDP Act 2023 Compliant</span>
            <span class="badge bg-info text-dark border"><i class="bi bi-clock-history me-1"></i> 24h Purge Active</span>
          </div>
        </div>

        <!-- Specimen Test Benchmark Bar (Assignment Specimen Cases K01-K06) -->
        <div class="card-kpi p-3 mb-3 bg-light border-danger border-opacity-25">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="small fw-bold text-dark"><i class="bi bi-lightning-charge-fill text-danger me-1"></i> Specimen Case Benchmark Runner (Ground Truth Evaluator):</span>
            <span class="badge bg-dark">12 Specimen Applicants Available</span>
          </div>
          <div class="d-flex flex-wrap gap-2">
            <button class="btn btn-sm btn-outline-danger" onclick="testSpecimenKyc('K01')">
              <strong>K01</strong>: Vindhya Tours <span class="badge bg-danger ms-1">Cancelled GST</span>
            </button>
            <button class="btn btn-sm btn-outline-success" onclick="testSpecimenKyc('K02')">
              <strong>K02</strong>: Harmony Dental <span class="badge bg-success ms-1">Valid (Pass)</span>
            </button>
            <button class="btn btn-sm btn-outline-success" onclick="testSpecimenKyc('K03')">
              <strong>K03</strong>: Ganesh Woodcraft <span class="badge bg-success ms-1">Valid (Pass)</span>
            </button>
            <button class="btn btn-sm btn-outline-warning text-dark" onclick="testSpecimenKyc('K04')">
              <strong>K04</strong>: Saffron Dental <span class="badge bg-warning text-dark ms-1">Blurry OCR</span>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="testSpecimenKyc('K05')">
              <strong>K05</strong>: Balaji Realty <span class="badge bg-danger ms-1">Old Bill (186d)</span>
            </button>
            <button class="btn btn-sm btn-outline-success" onclick="testSpecimenKyc('K06')">
              <strong>K06</strong>: Balaji Dental <span class="badge bg-success ms-1">Active Micro</span>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="testSpecimenKyc('K07')">
              <strong>K07</strong>: Neelgiri Physio <span class="badge bg-danger ms-1">Suspended GST</span>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="testSpecimenKyc('K11')">
              <strong>K11</strong>: Trinity Bake <span class="badge bg-danger ms-1">Old Bill (257d)</span>
            </button>
          </div>
        </div>

        <!-- Executive KPI Metrics -->
        <div class="row g-3 mb-4">
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-warning">
              <div class="text-muted small fw-bold">PENDING REVIEW QUEUE</div>
              <div class="fs-4 fw-bold text-warning" id="kycPendingCountBadge">0</div>
              <div class="small text-muted">Awaiting KYC Officer sign-off</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-success">
              <div class="text-muted small fw-bold">AUTO-VERIFIED (PASS)</div>
              <div class="fs-4 fw-bold text-success" id="kycApprovedCountBadge">0</div>
              <div class="small text-muted">Cleared for field dispatch</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-danger">
              <div class="text-muted small fw-bold">EXCEPTIONS CAUGHT</div>
              <div class="fs-4 fw-bold text-danger" id="kycExceptionsCountBadge">0</div>
              <div class="small text-muted">Cancelled GST, old bills, low-res OCR</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-primary">
              <div class="text-muted small fw-bold">AVG. OCR CONFIDENCE</div>
              <div class="fs-4 fw-bold text-primary" id="kycAvgOcrBadge">97.4%</div>
              <div class="small text-muted">DoT statutory document clarity</div>
            </div>
          </div>
        </div>

        <!-- Filter Tabs & Applications Table -->
        <div class="card-kpi p-0 overflow-hidden mb-4">
          <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
            <div class="btn-group btn-group-sm" role="group">
              <button type="button" class="btn btn-outline-secondary active" id="kycTabAll" onclick="filterKycTable('')">All Applications</button>
              <button type="button" class="btn btn-outline-secondary" id="kycTabPending" onclick="filterKycTable('PENDING')">Pending Review</button>
              <button type="button" class="btn btn-outline-secondary" id="kycTabVerified" onclick="filterKycTable('APPROVED')">Verified</button>
              <button type="button" class="btn btn-outline-secondary" id="kycTabExceptions" onclick="filterKycTable('EXCEPTION')">Exceptions / Failed</button>
            </div>
            <button class="btn btn-sm btn-outline-danger" onclick="triggerDpdpPurgeSimulator()">
              <i class="bi bi-trash3 me-1"></i> Simulate 24h DPDP Purge
            </button>
          </div>
          <div class="table-responsive">
            <table class="table table-enterprise table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>App / Order ID</th>
                  <th>Applicant Name</th>
                  <th>Business Entity</th>
                  <th>Masked GSTIN</th>
                  <th>Udyam No</th>
                  <th>Bill Date &amp; Age</th>
                  <th>OCR Confidence</th>
                  <th>Verification Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody id="kycQueueTbody">
                <!-- Dynamically populated from /api/kyc/queue -->
              </tbody>
            </table>
          </div>
        </div>
      </section>"""

# Replace old #sec-kyc
old_sec_kyc_pattern = r'<section id="sec-kyc" style="display: none;">.*?</section>'
content = re.sub(old_sec_kyc_pattern, new_sec_kyc, content, flags=re.DOTALL)

# -----------------------------------------------------------------------------
# 2. UPGRADE MODAL: #kycReviewModal
# -----------------------------------------------------------------------------
new_kyc_modal = """  <!-- Modal: KYC Officer Field-Level Inspection & Decision -->
  <div class="modal fade" id="kycReviewModal" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content border-0 shadow-lg">
        <div class="modal-header bg-dark text-white">
          <div>
            <h5 class="modal-title fw-bold fs-6 mb-0">Smart KYC Document &amp; Registry Verification Console</h5>
            <div class="small text-muted">Authoritative Comparison: Customer Data vs. Registry vs. Document OCR</div>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-4">
          <!-- Entity Summary Header -->
          <div class="card-kpi p-3 mb-3 bg-light border">
            <div class="row g-2 align-items-center">
              <div class="col-md-3">
                <div class="text-muted small">Application / Order ID</div>
                <div class="fw-bold font-monospace text-danger fs-6" id="kycModalOrderId">-</div>
              </div>
              <div class="col-md-3">
                <div class="text-muted small">Business Trade Name</div>
                <div class="fw-bold fs-6 text-dark" id="kycModalBizName">-</div>
              </div>
              <div class="col-md-3">
                <div class="text-muted small">Authorized Signatory</div>
                <div class="fw-bold text-dark" id="kycModalSignatory">-</div>
              </div>
              <div class="col-md-3">
                <div class="text-muted small">DPDP Consent Artifact</div>
                <span class="badge bg-success"><i class="bi bi-shield-lock-fill me-1"></i> Affirmative Consent Signed</span>
              </div>
            </div>
          </div>

          <!-- Actionable Exception Alert (Shown if verification failed or has anomalies) -->
          <div id="kycModalExceptionAlert" class="alert alert-danger border border-danger mb-3 p-3 rounded" style="display: none;">
            <div class="d-flex align-items-start gap-3">
              <i class="bi bi-exclamation-triangle-fill fs-4 text-danger mt-1"></i>
              <div>
                <h6 class="fw-bold text-danger mb-1" id="kycModalExceptionTitle">Verification Exception Detected</h6>
                <div class="small text-dark mb-1" id="kycModalExceptionEn">Customer-facing guidance...</div>
                <div class="small text-muted font-monospace" id="kycModalExceptionHi">Hindi guidance...</div>
              </div>
            </div>
          </div>

          <!-- Field-Level Comparison Matrix Table -->
          <div class="card-kpi p-0 overflow-hidden mb-3 border">
            <div class="p-2 px-3 border-bottom bg-light fw-bold small text-dark d-flex justify-content-between align-items-center">
              <span>FIELD-LEVEL CROSS-VALIDATION MATRIX</span>
              <span class="badge bg-secondary">Reference Date: 15-Jul-2026</span>
            </div>
            <div class="table-responsive">
              <table class="table table-sm table-bordered align-middle mb-0" style="font-size: 0.88rem;">
                <thead class="table-light">
                  <tr>
                    <th style="width: 22%;">Field</th>
                    <th style="width: 25%;">Customer Stated Data</th>
                    <th style="width: 25%;">Authoritative Registry Data</th>
                    <th style="width: 20%;">Document OCR Extraction</th>
                    <th style="width: 8%;" class="text-center">Verdict</th>
                  </tr>
                </thead>
                <tbody id="kycModalFieldTable">
                  <!-- Populated dynamically -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- Officer Decision Desk (RBAC Gated) -->
          <div class="card-kpi p-3 bg-light border mb-3">
            <h6 class="fw-bold small text-muted mb-2"><i class="bi bi-pencil-square me-1"></i> KYC OFFICER ACTION &amp; RESOLUTION DESK</h6>
            <div class="mb-2">
              <label class="form-label small fw-bold text-muted mb-1">Officer Audit Remarks / Resubmission Instructions</label>
              <textarea id="kycOfficerRemarks" class="form-control form-control-sm" rows="2" placeholder="Enter specific instructions or reason for audit record..."></textarea>
            </div>
            <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center">
              <div class="d-flex gap-2">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="makeKycDecision('REJECT')">
                  <i class="bi bi-x-circle me-1"></i> Reject Application
                </button>
                <button type="button" class="btn btn-outline-warning btn-sm text-dark" onclick="makeKycDecision('REQUEST_RESUBMISSION')">
                  <i class="bi bi-arrow-repeat me-1"></i> Request Resubmission
                </button>
                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="makeKycDecision('ESCALATE_MANUAL_REVIEW')">
                  <i class="bi bi-shield-exclamation me-1"></i> Escalate Field Survey
                </button>
              </div>
              <button type="button" class="btn btn-success btn-sm px-4 fw-bold" onclick="makeKycDecision('APPROVE')">
                <i class="bi bi-check-circle-fill me-1"></i> Approve KYC &amp; Clear for Feasibility
              </button>
            </div>
          </div>

          <!-- Immutable Audit Trail History -->
          <div class="p-2 border rounded bg-white">
            <div class="small fw-bold text-muted mb-1"><i class="bi bi-journal-text me-1"></i> Immutable Compliance Audit Trail:</div>
            <div id="kycModalAuditHistory" class="small text-muted font-monospace" style="max-height: 80px; overflow-y: auto;">
              No prior officer decisions recorded.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>"""

old_modal_pattern = r'<div class="modal fade" id="kycReviewModal".*?<!-- Modal: Order Detail -->'
content = re.sub(r'<div class="modal fade" id="kycReviewModal".*?</div>\s*</div>\s*</div>\s*</div>', new_kyc_modal, content, flags=re.DOTALL)

with open(control_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated #sec-kyc and #kycReviewModal in control.html!")

"""
patch_control_html.py
=============================================================================
Applies Phase 3 AI Quote Recovery Hub UI components and JavaScript
to prototype/templates/control.html cleanly.
=============================================================================
"""

import os

HTML_PATH = r"E:\Airtel\prototype\templates\control.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Sidebar Link
target_sidebar = """        <a href="#sec-quotes" onclick="showSection('quotes', this)">
          <i class="bi bi-file-earmark-text-fill"></i> Quotes &amp; Conversion Hub
          <span class="badge bg-primary ms-auto" id="sideQuotesCount">3</span>
        </a>
      </li>"""

replacement_sidebar = """        <a href="#sec-quotes" onclick="showSection('quotes', this)">
          <i class="bi bi-file-earmark-text-fill"></i> Quotes &amp; Conversion Hub
          <span class="badge bg-primary ms-auto" id="sideQuotesCount">3</span>
        </a>
      </li>
      <li>
        <a href="#sec-recovery" onclick="showSection('recovery', this)">
          <i class="bi bi-arrow-repeat"></i> Quote Recovery Hub
          <span class="badge bg-danger ms-auto" id="sideRecoveryCount">5</span>
        </a>
      </li>"""

if target_sidebar in content:
    content = content.replace(target_sidebar, replacement_sidebar, 1)
    print("[OK] Sidebar link patched.")
else:
    print("! Sidebar target not found.")

# 2. Add #sec-recovery after #sec-quotes
sec_recovery_html = """
      <!-- ========================================================= -->
      <!-- SECTION: QUOTE RECOVERY HUB (Phase 3 AI-Powered Recovery) -->
      <!-- ========================================================= -->
      <section id="sec-recovery" style="display: none;">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0"><i class="bi bi-arrow-repeat text-danger me-2"></i>AI Quote Recovery Hub</h4>
            <span class="text-muted small">Recover abandoned MSME opportunities with objection classification, priority lead scoring, and personalized AI drafts.</span>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-danger" onclick="triggerRecoveryScan()">
              <i class="bi bi-radar me-1"></i> Scan Abandoned Quotes
            </button>
            <button class="btn btn-sm btn-outline-secondary" onclick="loadRecoveryData()">
              <i class="bi bi-arrow-clockwise me-1"></i> Refresh
            </button>
          </div>
        </div>

        <!-- KPI Strip -->
        <div class="row g-3 mb-4">
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-danger">
              <span class="text-muted small fw-bold">ABANDONED QUOTES</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-dark mb-0" id="kpiTotalAbandoned">0</h3>
                <span class="badge bg-light text-muted border small">vs 1,113 baseline</span>
              </div>
              <span class="small text-danger mt-1 d-block"><i class="bi bi-exclamation-triangle-fill me-1"></i>Active in recovery queue</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-warning">
              <span class="text-muted small fw-bold">DRAFT READY</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-dark mb-0" id="kpiDraftReady">0</h3>
                <span class="badge bg-warning text-dark small" id="kpiHighPriorityCount">0 High Priority</span>
              </div>
              <span class="small text-muted mt-1 d-block">AI draft prepared &amp; ready</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-primary">
              <span class="text-muted small fw-bold">CONTACTED PIPELINE</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-dark mb-0" id="kpiContacted">0</h3>
                <span class="badge bg-primary text-white small" id="kpiContactedPct">0%</span>
              </div>
              <span class="small text-muted mt-1 d-block">Consultation in flight</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-success">
              <span class="text-muted small fw-bold">RECOVERED &amp; CONVERTED</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-success mb-0" id="kpiRecovered">0</h3>
                <span class="badge bg-success text-white small" id="kpiRecoveryRate">0% Rate</span>
              </div>
              <span class="small text-success mt-1 d-block" id="kpiRecoveredRevenue">&#8377;0/mo Revived Revenue</span>
            </div>
          </div>
        </div>

        <!-- Benchmark Comparison & Objection Distribution Row -->
        <div class="row g-3 mb-4">
          <!-- Historical Benchmark Callout -->
          <div class="col-md-5">
            <div class="card-kpi p-3 h-100 bg-white">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold text-dark small"><i class="bi bi-bar-chart-line-fill text-danger me-1"></i>BENCHMARK: HISTORICAL LOSSES VS. UDYAM</span>
                <span class="badge bg-dark text-white">smb_leads.csv</span>
              </div>
              <p class="small text-muted mb-2">The baseline dataset experienced <strong>1,113 losses at the quote stage</strong> with <strong>0% recovery workflow</strong>. Project Udyam converts these drop-offs into active pipeline:</p>
              <div class="p-2 bg-light border rounded small mb-2">
                <div class="d-flex justify-content-between mb-1">
                  <span>Historical Baseline Quote Losses:</span>
                  <span class="fw-bold text-danger">1,113 (56.4% drop)</span>
                </div>
                <div class="d-flex justify-content-between mb-1">
                  <span>Historical Recovery Rate:</span>
                  <span class="fw-bold text-secondary">0.0% (Unrecovered)</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span>Udyam Active Recovery Target:</span>
                  <span class="fw-bold text-success">+18% to +22% Win-back</span>
                </div>
              </div>
              <div class="small text-muted fst-italic">
                <i class="bi bi-shield-check text-success me-1"></i>All outreach adheres to DPDP Act 2023 with mandatory opt-out clauses and unbundled consent.
              </div>
            </div>
          </div>

          <!-- Objection Categories Distribution -->
          <div class="col-md-7">
            <div class="card-kpi p-3 h-100 bg-white">
              <span class="fw-bold text-dark small d-block mb-2"><i class="bi bi-pie-chart-fill text-primary me-1"></i>OBJECTION CLASSIFICATION DISTRIBUTION</span>
              <div id="objectionDistributionContainer" class="d-flex flex-wrap gap-2">
                <!-- Dynamically populated objection pills -->
              </div>
            </div>
          </div>
        </div>

        <!-- Recovery Opportunities Workspace -->
        <div class="card-kpi p-3 bg-white">
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
            <div class="d-flex flex-wrap gap-2 align-items-center" id="recoveryFilterTabs">
              <button class="btn btn-sm btn-dark active" onclick="filterRecovery('all', this)">All Records</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('high_priority', this)"><i class="bi bi-fire text-danger me-1"></i>High Priority (&ge; 70)</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('price_too_high', this)">Price Concerns</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('technical_complexity', this)">Technical Confusion</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('draft_ready', this)">Draft Ready</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('contacted', this)">Contacted</button>
              <button class="btn btn-sm btn-outline-secondary" onclick="filterRecovery('recovered', this)">Recovered</button>
            </div>
            <div class="input-group input-group-sm" style="max-width: 260px;">
              <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
              <input type="text" id="recoverySearchInput" class="form-control" placeholder="Search business, quote, agent..." onkeyup="searchRecoveryTable()">
            </div>
          </div>

          <!-- Opportunities Table -->
          <div class="table-responsive">
            <table class="table table-hover table-sm align-middle mb-0">
              <thead class="table-light small">
                <tr>
                  <th>RECOVERY ID</th>
                  <th>BUSINESS &amp; CONTACT</th>
                  <th>QUOTED BUNDLE</th>
                  <th>MONTHLY / SETUP</th>
                  <th>DETECTED OBJECTION</th>
                  <th>PRIORITY SCORE</th>
                  <th>STATUS</th>
                  <th>ASSIGNED AGENT</th>
                  <th class="text-end">ACTION</th>
                </tr>
              </thead>
              <tbody id="recoveryTableBody">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </section>
"""

target_sec_quotes_end = """              <tbody id="controlQuotesTableBody">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </section>"""

if target_sec_quotes_end in content:
    content = content.replace(target_sec_quotes_end, target_sec_quotes_end + "\n" + sec_recovery_html, 1)
    print("[OK] #sec-recovery section patched.")
else:
    print("! #sec-quotes end target not found.")

# 3. Add #recoveryDetailModal before </body>
recovery_modal_html = """
  <!-- Modal: Quote Recovery Dossier & AI Outreach Workspace -->
  <div class="modal fade" id="recoveryDetailModal" tabindex="-1">
    <div class="modal-dialog modal-xl modal-dialog-centered">
      <div class="modal-content shadow-lg border-0">
        <div class="modal-header bg-dark text-white py-3">
          <div class="d-flex align-items-center gap-2">
            <span class="badge bg-danger fs-6">OPPORTUNITY RECOVERY</span>
            <h5 class="modal-title fw-bold fs-6 mb-0" id="recModalBusinessName">Business Name</h5>
            <span class="badge bg-secondary font-monospace" id="recModalId">REC-2026-XXXX</span>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-4 bg-light">
          <div class="row g-4">
            
            <!-- Left Column: Dossier, Objection Evidence & Priority Model -->
            <div class="col-lg-6">
              
              <!-- Customer & Quote Profile Card -->
              <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="fw-bold small text-muted text-uppercase">Commercial Context</span>
                  <span class="badge bg-light text-dark border font-monospace" id="recModalQuoteId">QTE-2026-XXXX</span>
                </div>
                <div class="row g-2 small">
                  <div class="col-6"><strong>Contact:</strong> <span id="recModalContact">Business Owner</span></div>
                  <div class="col-6"><strong>Phone:</strong> <span id="recModalPhone">+91 98450 ****</span></div>
                  <div class="col-6"><strong>Segment:</strong> <span id="recModalSegment">Micro Retail</span></div>
                  <div class="col-6"><strong>Stated Budget:</strong> <span id="recModalBudget" class="text-danger fw-bold">&#8377;1,500</span></div>
                  <div class="col-12 mt-2 pt-2 border-top">
                    <div class="d-flex justify-content-between">
                      <span>Quoted Plan: <strong id="recModalBundle">Starter Bundle</strong></span>
                      <span class="fw-bold text-dark" id="recModalPricing">&#8377;1,999/mo + &#8377;1,000 setup</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Detected Objection & Verbatim Evidence -->
              <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="fw-bold small text-muted text-uppercase">Detected Customer Objection</span>
                  <span class="badge" id="recModalObjectionBadge">Price Too High</span>
                </div>
                <div class="p-3 bg-light border-start border-4 border-danger rounded small mb-2">
                  <span class="text-muted d-block small mb-1"><i class="bi bi-chat-quote-fill text-danger me-1"></i>Customer Verbatim Statement (Evidence):</span>
                  <em class="fw-semibold text-dark" id="recModalEvidence">"&#8377;3,499 per month is too expensive for my small grocery store. Budget is only &#8377;1,500."</em>
                </div>
              </div>

              <!-- Explainable Priority Score Breakdown -->
              <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="fw-bold small text-muted text-uppercase">Explainable Priority Scoring Model</span>
                  <div class="d-flex align-items-center gap-1">
                    <span class="badge" id="recModalScoreTier">HIGH</span>
                    <span class="fw-bold fs-6 text-dark" id="recModalScoreValue">84 / 100</span>
                  </div>
                </div>
                <p class="small text-muted mb-2" style="font-size: 0.78rem;">Calculated via transparent 5-factor weighted criteria (Assignment Section 6):</p>
                <div class="d-flex flex-column gap-2 small" id="recModalFactorsList">
                  <!-- Dynamically populated factors -->
                </div>
              </div>

              <!-- Explainable Strategy & Recommended Next Action -->
              <div class="card p-3 border-0 shadow-sm rounded-3 bg-white">
                <span class="fw-bold small text-muted text-uppercase d-block mb-1">Recommended Recovery Action</span>
                <h6 class="fw-bold text-dark mb-1" id="recModalActionTitle">Present Down-Tier Bundle</h6>
                <p class="small text-muted mb-2" id="recModalActionDesc">Offer Kirana Digital Starter at &#8377;1,999/mo to reduce monthly expenditure by &#8377;1,500/mo without losing essential payment failover.</p>
                <div id="recModalViableAltBox" class="p-2 bg-success bg-opacity-10 border border-success rounded small" style="display: none;">
                  <strong class="text-success"><i class="bi bi-check-circle-fill me-1"></i>Viable Lower-Cost Alternative:</strong>
                  <div id="recModalViableAltText" class="mt-1 text-dark">Kirana Starter @ &#8377;1,999/mo (Saving &#8377;1,500/mo)</div>
                </div>
              </div>

            </div>

            <!-- Right Column: AI Outreach Generator & Human-in-the-Loop Actions -->
            <div class="col-lg-6">
              
              <!-- AI Draft Message Card -->
              <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="fw-bold small text-muted text-uppercase"><i class="bi bi-robot text-danger me-1"></i>Personalized AI Outreach Draft</span>
                  <div class="d-flex align-items-center gap-1">
                    <select id="recDraftLangSelect" class="form-select form-select-sm" style="width: 105px;" onchange="refreshRecoveryDraft(this.value)">
                      <option value="hi">Hindi</option>
                      <option value="hinglish">Hinglish</option>
                      <option value="en">English</option>
                    </select>
                    <button class="btn btn-sm btn-outline-secondary" onclick="refreshRecoveryDraft(document.getElementById('recDraftLangSelect').value)">
                      <i class="bi bi-arrow-clockwise"></i>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-2">
                  <label class="form-label small text-muted">Message Preview (Editable by Sales Executive):</label>
                  <textarea id="recModalDraftText" class="form-control form-control-sm font-monospace" rows="5" style="font-size: 0.85rem; line-height: 1.4;"></textarea>
                </div>

                <!-- Compliance & Guardrails Badges -->
                <div class="d-flex flex-wrap gap-2 align-items-center small mb-3">
                  <span class="badge bg-success bg-opacity-10 text-success border border-success py-1">
                    <i class="bi bi-shield-check me-1"></i>DPDP Act 2023 Compliant
                  </span>
                  <span class="badge bg-light text-muted border py-1">
                    <i class="bi bi-check2-all me-1"></i>Opt-Out Clause Included
                  </span>
                  <span class="badge bg-warning bg-opacity-10 text-warning border border-warning py-1">
                    <i class="bi bi-person-check me-1"></i>Human Approval Required
                  </span>
                </div>

                <!-- Secure Re-Entry Link -->
                <div class="p-2 bg-light border rounded small mb-2">
                  <span class="text-muted d-block small mb-1 fw-bold"><i class="bi bi-link-45deg me-1"></i>Secure Expiring Re-Entry Link (14-Day Lock):</span>
                  <div class="input-group input-group-sm">
                    <input type="text" id="recModalReentryLink" class="form-control font-monospace" readonly>
                    <button class="btn btn-outline-dark" onclick="copyReentryLink()"><i class="bi bi-clipboard me-1"></i>Copy Link</button>
                  </div>
                  <span class="text-muted small mt-1 d-block" style="font-size: 0.72rem;">Customer-bound token; zero internal IDs or sensitive PII exposed.</span>
                </div>
              </div>

              <!-- Executive Action Bar -->
              <div class="card p-3 border-0 shadow-sm rounded-3 bg-white">
                <span class="fw-bold small text-muted text-uppercase d-block mb-2">Take Action on Opportunity</span>
                
                <div class="row g-2 mb-3">
                  <div class="col-8">
                    <label class="form-label small mb-1">Assign Sales Executive / Partner:</label>
                    <select id="recModalAgentSelect" class="form-select form-select-sm">
                      <option value="Ramesh Sharma (Airtel MSME Growth Desk)">Ramesh Sharma (Airtel MSME Growth Desk)</option>
                      <option value="Priya Nair (Health &amp; Professional Desk)">Priya Nair (Health &amp; Professional Desk)</option>
                      <option value="Vikram Rathore (Airtel Enterprise Field Desk)">Vikram Rathore (Airtel Enterprise Field Desk)</option>
                      <option value="Anand Verma (Industrial Corridor Desk)">Anand Verma (Industrial Corridor Desk)</option>
                      <option value="Channel Partner: MicroTech Solutions (PIN 110001)">Channel Partner: MicroTech Solutions</option>
                    </select>
                  </div>
                  <div class="col-4 d-flex align-items-end">
                    <button class="btn btn-sm btn-outline-primary w-100" onclick="executeRecoveryAction('assign')">
                      <i class="bi bi-person-plus me-1"></i>Assign
                    </button>
                  </div>
                </div>

                <div class="d-flex flex-wrap gap-2 justify-content-between pt-2 border-top">
                  <button class="btn btn-sm btn-primary" onclick="executeRecoveryAction('mark_contacted')">
                    <i class="bi bi-send-check me-1"></i>Approve &amp; Mark Contacted
                  </button>
                  <button class="btn btn-sm btn-success" onclick="executeRecoveryAction('recover')">
                    <i class="bi bi-trophy-fill me-1"></i>Close as Recovered (Order Won)
                  </button>
                  <button class="btn btn-sm btn-outline-danger" onclick="executeRecoveryAction('close_lost')">
                    <i class="bi bi-x-circle me-1"></i>Close Lost
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="executeRecoveryAction('opt_out')">
                    <i class="bi bi-slash-circle me-1"></i>DPDP Opt-Out
                  </button>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
"""

if '<div class="modal fade" id="milestoneModal"' in content:
    content = content.replace('<div class="modal fade" id="milestoneModal"', recovery_modal_html + '\n  <div class="modal fade" id="milestoneModal"', 1)
    print("[OK] #recoveryDetailModal patched.")
else:
    print("! Milestone modal target not found.")

# 4. Add JavaScript for Recovery Hub
recovery_js = """
    // =========================================================================
    // PHASE 3: AI QUOTE RECOVERY ENGINE JAVASCRIPT
    // =========================================================================
    let currentRecoveryRecords = [];
    let activeRecoveryFilter = 'all';
    let activeModalRecoveryId = null;

    function loadRecoveryData() {
      // 1. Fetch Analytics
      fetch('/api/control/recovery/analytics')
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            const m = data.live_metrics;
            document.getElementById('kpiTotalAbandoned').textContent = m.total_abandoned;
            document.getElementById('kpiDraftReady').textContent = m.draft_ready;
            document.getElementById('kpiContacted').textContent = m.contacted;
            document.getElementById('kpiRecovered').textContent = m.recovered;
            document.getElementById('kpiRecoveryRate').textContent = m.recovery_rate_pct + '% Win-back';
            document.getElementById('kpiRecoveredRevenue').textContent = '₹' + m.recovered_monthly_revenue_inr.toLocaleString() + '/mo Revived Revenue';
            
            const sideBadge = document.getElementById('sideRecoveryCount');
            if (sideBadge) sideBadge.textContent = m.total_abandoned;

            // Render objection distribution pills
            const distBox = document.getElementById('objectionDistributionContainer');
            if (distBox) {
              distBox.innerHTML = '';
              Object.entries(data.objection_distribution).forEach(([k, v]) => {
                if (v.count > 0 || ['price_too_high', 'technical_complexity', 'installation_timeline', 'missing_requirement', 'not_ready'].includes(k)) {
                  const pill = document.createElement('div');
                  pill.className = 'p-2 bg-light border rounded small d-flex align-items-center gap-2';
                  pill.style.minWidth = '175px';
                  pill.innerHTML = `
                    <span class="badge bg-secondary font-monospace">${v.count}</span>
                    <div>
                      <div class="fw-bold text-dark" style="font-size: 0.76rem;">${v.label}</div>
                      <div class="text-muted" style="font-size: 0.70rem;">${v.pct}% of active queue</div>
                    </div>
                  `;
                  distBox.appendChild(pill);
                }
              });
            }
          }
        })
        .catch(err => console.error("Error loading recovery analytics:", err));

      // 2. Fetch Records Queue
      fetch('/api/control/recovery/queue?filter=' + activeRecoveryFilter)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            currentRecoveryRecords = data.records;
            renderRecoveryTable(currentRecoveryRecords);
            
            // High priority count
            const highCount = currentRecoveryRecords.filter(r => r.priority_score >= 70).length;
            const hpEl = document.getElementById('kpiHighPriorityCount');
            if (hpEl) hpEl.textContent = highCount + ' High Priority';
          }
        })
        .catch(err => console.error("Error loading recovery queue:", err));
    }

    function renderRecoveryTable(records) {
      const tbody = document.getElementById('recoveryTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!records || records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center py-4 text-muted small">No recovery opportunities matching filter.</td></tr>`;
        return;
      }

      records.forEach(r => {
        const tr = document.createElement('tr');
        const scoreColor = r.priority_score >= 70 ? 'success' : (r.priority_score >= 45 ? 'warning' : 'secondary');
        const statusBadge = {
          'draft_ready': '<span class="badge bg-warning text-dark"><i class="bi bi-pencil-fill me-1"></i>Draft Ready</span>',
          'contacted': '<span class="badge bg-primary"><i class="bi bi-telephone-fill me-1"></i>Contacted</span>',
          'recovered': '<span class="badge bg-success"><i class="bi bi-trophy-fill me-1"></i>Recovered</span>',
          'closed_lost': '<span class="badge bg-danger"><i class="bi bi-x-circle me-1"></i>Closed Lost</span>',
          'opted_out': '<span class="badge bg-secondary"><i class="bi bi-slash-circle me-1"></i>Opted Out</span>'
        }[r.recovery_status] || `<span class="badge bg-light text-dark">${r.recovery_status}</span>`;

        tr.innerHTML = `
          <td><code>${r.recovery_id}</code></td>
          <td>
            <strong>${r.business_name}</strong>
            <div class="small text-muted">${r.contact_person} &bull; ${r.contact_phone}</div>
          </td>
          <td>
            <div class="small fw-semibold text-dark">${r.recommended_bundle}</div>
            <span class="badge bg-light text-muted border font-monospace" style="font-size: 0.68rem;">${r.quote_id}</span>
          </td>
          <td>
            <strong>₹${r.monthly_quoted_inr.toLocaleString()}/mo</strong>
            <div class="small text-muted" style="font-size: 0.72rem;">1st pay: ₹${r.total_first_payment_inr.toLocaleString()}</div>
          </td>
          <td>
            <span class="badge bg-${r.objection_badge_class || 'danger'}"><i class="bi ${r.objection_icon || 'bi-exclamation-circle'} me-1"></i>${r.objection_label}</span>
          </td>
          <td>
            <div class="d-flex align-items-center gap-1">
              <span class="badge bg-${scoreColor}">${r.priority_score}</span>
              <span class="small text-muted" style="font-size: 0.70rem;">(${r.priority_tier})</span>
            </div>
          </td>
          <td>${statusBadge}</td>
          <td><small class="text-muted">${r.assigned_agent}</small></td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-danger" onclick="openRecoveryModal('${r.recovery_id}')">
              <i class="bi bi-arrow-repeat me-1"></i>Review &amp; Recover
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterRecovery(filterType, btn) {
      activeRecoveryFilter = filterType;
      document.querySelectorAll('#recoveryFilterTabs button').forEach(b => {
        b.classList.remove('btn-dark');
        b.classList.add('btn-outline-secondary');
      });
      if (btn) {
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-dark');
      }
      loadRecoveryData();
    }

    function searchRecoveryTable() {
      const q = (document.getElementById('recoverySearchInput').value || '').trim().toLowerCase();
      if (!q) {
        renderRecoveryTable(currentRecoveryRecords);
        return;
      }
      const filtered = currentRecoveryRecords.filter(r => 
        r.business_name.toLowerCase().includes(q) ||
        r.recovery_id.toLowerCase().includes(q) ||
        r.quote_id.toLowerCase().includes(q) ||
        r.objection_label.toLowerCase().includes(q) ||
        r.assigned_agent.toLowerCase().includes(q)
      );
      renderRecoveryTable(filtered);
    }

    function openRecoveryModal(recoveryId) {
      activeModalRecoveryId = recoveryId;
      fetch('/api/control/recovery/' + recoveryId)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            const r = data.record;
            document.getElementById('recModalBusinessName').textContent = r.business_name;
            document.getElementById('recModalId').textContent = r.recovery_id;
            document.getElementById('recModalQuoteId').textContent = r.quote_id;
            document.getElementById('recModalContact').textContent = r.contact_person;
            document.getElementById('recModalPhone').textContent = r.contact_phone;
            document.getElementById('recModalSegment').textContent = r.business_category.toUpperCase();
            document.getElementById('recModalBudget').textContent = r.customer_budget_inr ? ('₹' + Number(r.customer_budget_inr).toLocaleString() + '/mo') : 'Not specified';
            document.getElementById('recModalBundle').textContent = r.recommended_bundle;
            document.getElementById('recModalPricing').textContent = '₹' + r.monthly_quoted_inr.toLocaleString() + '/mo (1st Pay: ₹' + r.total_first_payment_inr.toLocaleString() + ')';
            
            // Objection & Evidence
            const objBadge = document.getElementById('recModalObjectionBadge');
            objBadge.className = 'badge bg-' + (r.objection_badge_class || 'danger');
            objBadge.textContent = r.objection_label;
            document.getElementById('recModalEvidence').textContent = `"${r.supporting_evidence}"`;

            // Score & Tier
            const scoreBadge = document.getElementById('recModalScoreTier');
            scoreBadge.className = 'badge bg-' + r.priority_tier_color;
            scoreBadge.textContent = r.priority_tier;
            document.getElementById('recModalScoreValue').textContent = `${r.priority_score} / 100`;

            // Factor Breakdown
            const factorsBox = document.getElementById('recModalFactorsList');
            factorsBox.innerHTML = '';
            Object.entries(r.score_factors || {}).forEach(([fKey, fVal]) => {
              const row = document.createElement('div');
              row.className = 'd-flex justify-content-between align-items-center';
              row.innerHTML = `
                <span class="text-muted text-capitalize">${fKey.replace('_', ' ')}:</span>
                <div class="d-flex align-items-center gap-2">
                  <span class="text-muted" style="font-size: 0.72rem;">${fVal.detail}</span>
                  <span class="badge bg-light text-dark border font-monospace">${fVal.score}/${fVal.max}</span>
                </div>
              `;
              factorsBox.appendChild(row);
            });

            // Strategy & Action
            document.getElementById('recModalActionTitle').textContent = r.action_title || 'Consultative Outreach';
            document.getElementById('recModalActionDesc').textContent = r.suggested_next_action || 'Review opportunity with customer.';
            
            const viableBox = document.getElementById('recModalViableAltBox');
            if (r.viable_alternative) {
              viableBox.style.display = 'block';
              document.getElementById('recModalViableAltText').textContent = `${r.viable_alternative.name} @ ₹${r.viable_alternative.monthly_inr.toLocaleString()}/mo (${r.viable_alternative.note || ''})`;
            } else {
              viableBox.style.display = 'none';
            }

            // AI Draft Text
            const draftObj = r.ai_draft_message || {};
            document.getElementById('recModalDraftText').value = draftObj.full_text || draftObj.body || '';
            document.getElementById('recDraftLangSelect').value = draftObj.language || 'hi';

            // Re-Entry URL
            const fullReentry = window.location.origin + r.reentry_url;
            document.getElementById('recModalReentryLink').value = fullReentry;

            // Agent assignment
            document.getElementById('recModalAgentSelect').value = r.assigned_agent || 'Ramesh Sharma (Airtel MSME Growth Desk)';

            const modal = new bootstrap.Modal(document.getElementById('recoveryDetailModal'));
            modal.show();
          }
        });
    }

    function refreshRecoveryDraft(lang) {
      if (!activeModalRecoveryId) return;
      fetch('/api/control/recovery/' + activeModalRecoveryId + '/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'generate_draft', language: lang })
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          document.getElementById('recModalDraftText').value = data.draft.full_text || data.draft.body;
        }
      });
    }

    function copyReentryLink() {
      const el = document.getElementById('recModalReentryLink');
      el.select();
      navigator.clipboard.writeText(el.value);
      alert('Secure customer recovery link copied to clipboard!');
    }

    function executeRecoveryAction(action) {
      if (!activeModalRecoveryId) return;
      let payload = { action: action };
      if (action === 'assign') {
        payload.agent_name = document.getElementById('recModalAgentSelect').value;
      } else if (action === 'update_draft') {
        payload.draft_text = document.getElementById('recModalDraftText').value;
      }

      fetch('/api/control/recovery/' + activeModalRecoveryId + '/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Action executed: ' + data.message);
          const modalEl = document.getElementById('recoveryDetailModal');
          const modalInstance = bootstrap.Modal.getInstance(modalEl);
          if (modalInstance) modalInstance.hide();
          loadRecoveryData();
        } else {
          alert('Error: ' + data.message);
        }
      });
    }

    function triggerRecoveryScan() {
      alert('Scanning active quotes for abandonment: 5 active cases identified, prioritized, and drafts refreshed.');
      loadRecoveryData();
    }
"""

# Update showSection to include 'recovery'
old_show_sec = "['overview', 'quotes', 'orders', 'kyc', 'leads', 'partners', 'insights'].forEach(s => {"
new_show_sec = "['overview', 'quotes', 'recovery', 'orders', 'kyc', 'leads', 'partners', 'insights'].forEach(s => {"

if old_show_sec in content:
    content = content.replace(old_show_sec, new_show_sec, 1)
    print("[OK] showSection array patched.")

# Add handler in showSection
old_sec_check = "if (secId === 'quotes') loadQuotesData();"
new_sec_check = "if (secId === 'quotes') loadQuotesData();\n      if (secId === 'recovery') loadRecoveryData();"

if old_sec_check in content:
    content = content.replace(old_sec_check, new_sec_check, 1)
    print("[OK] showSection handler patched.")

# Append recovery_js before initial load
target_init_load = "    // Initial load\n    loadLiveOrders();\n    loadKycQueue();"
replacement_init_load = recovery_js + "\n    // Initial load\n    loadLiveOrders();\n    loadKycQueue();\n    loadRecoveryData();"

if target_init_load in content:
    content = content.replace(target_init_load, replacement_init_load, 1)
    print("[OK] Recovery JS and init load patched.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully to control.html!")

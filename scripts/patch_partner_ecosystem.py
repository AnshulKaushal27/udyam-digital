"""
patch_partner_ecosystem.py
=============================================================================
Applies Phase 4 Assisted Digital Partner Ecosystem UI & Co-Pilot to
prototype/templates/control.html.
=============================================================================
"""

import os

HTML_PATH = r"E:\Airtel\prototype\templates\control.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Assisted Tablet Mode button to Sidebar (above Partner Intelligence)
old_side_partner = """      <li>
        <a href="#sec-partners" onclick="showSection('partners', this)">
          <i class="bi bi-people-fill"></i> Partner Intelligence
        </a>
      </li>"""

new_side_partner = """      <li class="px-3 my-2">
        <button class="btn btn-danger w-100 btn-sm text-start fw-bold shadow-sm d-flex align-items-center justify-content-between py-2" onclick="openAssistedModeModal()">
          <span><i class="bi bi-tablet-landscape me-2"></i>Assisted Tablet Mode</span>
          <span class="badge bg-white text-danger">FIELD</span>
        </button>
      </li>
      <li>
        <a href="#sec-partners" onclick="showSection('partners', this)">
          <i class="bi bi-people-fill"></i> Partner Intelligence &amp; Commissions
        </a>
      </li>"""

if old_side_partner in content:
    content = content.replace(old_side_partner, new_side_partner, 1)
    print("[OK] Sidebar Assisted Tablet button patched.")
else:
    print("! Sidebar target not found.")

# 2. Replace #sec-partners with Complete Partner Ecosystem Section
old_sec_partners_start = """      <section id="sec-partners" style="display: none;">"""
old_sec_partners_end = """        </div>
      </section>"""

# Let's inspect exact sec-partners block to replace
sec_partners_new_html = """      <!-- ========================================================= -->
      <!-- SECTION 5: PARTNER INTELLIGENCE, COMMISSIONS & CO-PILOT -->
      <!-- ========================================================= -->
      <section id="sec-partners" style="display: none;">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0"><i class="bi bi-people-fill text-danger me-2"></i>Partner Ecosystem &amp; Assisted Selling</h4>
            <div class="small text-muted">Empower 10,000+ local channel partners with AI Co-Pilot selling, referral attribution, and instant activation commissions.</div>
          </div>
          <div class="d-flex align-items-center gap-2">
            <!-- Partner Identity Switcher (Demonstrates RBAC) -->
            <div class="input-group input-group-sm" style="max-width: 290px;">
              <span class="input-group-text bg-white fw-bold small text-muted"><i class="bi bi-person-badge text-danger me-1"></i>Role / Partner:</span>
              <select id="partnerViewSelector" class="form-select form-select-sm fw-medium" onchange="switchPartnerView(this.value)">
                <option value="PTR-DEL-042" selected>Rajesh Gupta (Delhi - MicroTech)</option>
                <option value="PTR-MUM-108">Vikram Rathore (Mumbai - Apex Telecom)</option>
                <option value="PTR-BLR-019">Priya Nair (Bengaluru - Silicon City)</option>
                <option value="PTR-PUN-055">Amit Deshmukh (Pune - Deshmukh Digital)</option>
                <option value="PTR-KOL-073">Subhashish Ghosh (Kolkata - Eastern B2B)</option>
                <option value="ALL">Super Admin (All Partners - Global)</option>
              </select>
            </div>
            <button class="btn btn-sm btn-danger fw-bold" onclick="openAssistedModeModal()">
              <i class="bi bi-tablet-landscape me-1"></i> Launch Assisted Mode
            </button>
            <button class="btn btn-sm btn-outline-secondary" onclick="loadPartnerIntelligence()">
              <i class="bi bi-arrow-clockwise"></i>
            </button>
          </div>
        </div>

        <!-- Partner Executive KPI Strip -->
        <div class="row g-3 mb-4">
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-primary">
              <span class="text-muted small fw-bold">REFERRED SESSIONS</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-dark mb-0" id="ptrKpiReferred">0</h3>
                <span class="badge bg-light text-muted border small" id="ptrKpiReferralCode">AIRTEL-DEL42</span>
              </div>
              <span class="small text-muted mt-1 d-block">QR scans &amp; field sessions</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-warning">
              <span class="text-muted small fw-bold">ORDERS PLACED</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-dark mb-0" id="ptrKpiOrders">0</h3>
                <span class="badge bg-warning text-dark small" id="ptrKpiPendingActivations">0 Pending Act</span>
              </div>
              <span class="small text-muted mt-1 d-block">KYC &amp; installation in flight</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-success">
              <span class="text-muted small fw-bold">TOTAL ACTIVATIONS</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-success mb-0" id="ptrKpiActivations">0</h3>
                <span class="badge bg-success text-white small" id="ptrKpiConversionRate">0% Rate</span>
              </div>
              <span class="small text-success mt-1 d-block"><i class="bi bi-check-circle-fill me-1"></i>Step 5 Service Activated</span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi p-3 border-start border-4 border-danger">
              <span class="text-muted small fw-bold">COMMISSION EARNED</span>
              <div class="d-flex align-items-baseline gap-2 mt-1">
                <h3 class="fw-bold text-danger mb-0" id="ptrKpiEarnedComm">&#8377;0</h3>
                <span class="badge bg-light text-dark border small" id="ptrKpiPendingComm">&#8377;0 Pending</span>
              </div>
              <span class="small text-muted mt-1 d-block">&#8377;1,500 / verified activation</span>
            </div>
          </div>
        </div>

        <!-- Referral Attribution & QR Hub Row -->
        <div class="row g-3 mb-4">
          <!-- Dynamic QR Code Card -->
          <div class="col-lg-4">
            <div class="card-kpi p-3 h-100 bg-white">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold text-dark small"><i class="bi bi-qr-code text-danger me-1"></i>PARTNER REFERRAL QR CODE</span>
                <span class="badge bg-success bg-opacity-10 text-success border border-success">Active 30-Day Lock</span>
              </div>
              <div class="text-center py-2">
                <div id="partnerQrContainer" class="d-inline-block p-2 bg-light border rounded shadow-sm">
                  <!-- Dynamically rendered SVG QR code -->
                </div>
              </div>
              <div class="mt-2">
                <label class="form-label small text-muted mb-1">Partner Referral Link (First-Touch Attribution):</label>
                <div class="input-group input-group-sm">
                  <input type="text" id="partnerReferralUrlInput" class="form-control font-monospace" style="font-size: 0.75rem;" readonly>
                  <button class="btn btn-outline-danger" onclick="copyPartnerReferralLink()"><i class="bi bi-clipboard me-1"></i>Copy</button>
                </div>
                <div class="d-flex justify-content-between small text-muted mt-1" style="font-size: 0.70rem;">
                  <span>Attribution: 30-day first touch lock</span>
                  <span>Duplicate Protection: Enforced</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Commission Ledger Workspace -->
          <div class="col-lg-8">
            <div class="card-kpi p-3 h-100 bg-white">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 class="fw-bold text-dark mb-0"><i class="bi bi-journal-text text-danger me-1"></i>Partner Commission Ledger</h6>
                  <span class="text-muted small">&#8377;1,500 per activation &bull; Automatic eligibility on Step 5 installation</span>
                </div>
                <div class="d-flex gap-2">
                  <span class="badge bg-light text-dark border align-self-center" id="ledgerCountBadge">0 Records</span>
                </div>
              </div>

              <div class="table-responsive">
                <table class="table table-hover table-sm align-middle mb-0">
                  <thead class="table-light small">
                    <tr>
                      <th>COMM ID</th>
                      <th>ORDER ID</th>
                      <th>CUSTOMER ENTITY</th>
                      <th>PLAN VALUE</th>
                      <th>COMMISSION</th>
                      <th>STATUS</th>
                      <th>DATE</th>
                      <th class="text-end">ACTION</th>
                    </tr>
                  </thead>
                  <tbody id="partnerCommissionTbody">
                    <!-- Populated dynamically -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Partner Lead Rescue Desk (Territory-Routed Phase 3 Opportunities) -->
        <div class="card-kpi p-3 bg-white mb-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h6 class="fw-bold text-dark mb-0"><i class="bi bi-life-preserver text-danger me-1"></i>Territory Lead Rescue Desk (Phase 3 Integration)</h6>
              <span class="text-muted small">Local MSME opportunities in your pincode that abandoned quotes &bull; Claim to conduct doorstep closing.</span>
            </div>
            <span class="badge bg-danger" id="partnerLeadsCountBadge">0 Opportunities Available</span>
          </div>

          <div class="table-responsive">
            <table class="table table-hover table-sm align-middle mb-0">
              <thead class="table-light small">
                <tr>
                  <th>LEAD ID</th>
                  <th>BUSINESS NAME</th>
                  <th>QUOTED BUNDLE</th>
                  <th>OBJECTION REASON</th>
                  <th>PRIORITY SCORE</th>
                  <th>LAST INTERACTION</th>
                  <th>AI RECOVERY STRATEGY</th>
                  <th class="text-end">ACTION</th>
                </tr>
              </thead>
              <tbody id="partnerRescueDeskTbody">
                <!-- Populated dynamically from Recovery Records -->
              </tbody>
            </table>
          </div>
        </div>

      </section>
"""

# Replace existing sec-partners
p_start = content.find('<section id="sec-partners"')
if p_start != -1:
    p_end = content.find('</section>', p_start) + len('</section>')
    content = content[:p_start] + sec_partners_new_html + content[p_end:]
    print("[OK] #sec-partners section updated with Partner Ecosystem & Ledger.")
else:
    print("! #sec-partners start tag not found.")

# 3. Add Assisted Tablet Mode Modal (#assistedModeModal) before </body>
assisted_modal_html = """
  <!-- Modal: Assisted Onboarding Tablet Mode (Dual-Aspect UI) -->
  <div class="modal fade" id="assistedModeModal" tabindex="-1">
    <div class="modal-dialog modal-fullscreen">
      <div class="modal-content border-0">
        <!-- Tablet Header Bar -->
        <div class="modal-header bg-dark text-white py-2 px-4 d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center gap-3">
            <span class="badge bg-danger fs-6 px-3 py-1 fw-bold"><i class="bi bi-tablet-landscape me-1"></i>ASSISTED TABLET MODE</span>
            <div class="vr bg-secondary" style="height: 20px;"></div>
            <span class="small text-white-50">Active Partner: <strong class="text-white" id="assistedActivePartnerName">Rajesh Gupta (MicroTech Solutions)</strong></span>
            <span class="badge bg-secondary font-monospace" id="assistedPartnerIdBadge">PTR-DEL-042</span>
          </div>
          <div class="d-flex align-items-center gap-3">
            <span class="badge bg-success bg-opacity-25 text-success border border-success"><i class="bi bi-shield-check me-1"></i>DPDP Act Consent Verified</span>
            <button type="button" class="btn btn-sm btn-outline-light" data-bs-dismiss="modal"><i class="bi bi-x-lg me-1"></i>Exit Tablet Mode</button>
          </div>
        </div>

        <div class="modal-body p-0 bg-light">
          <div class="container-fluid h-100 p-0">
            <div class="row g-0 h-100">
              
              <!-- LEFT PANE: Customer-Facing Onboarding Canvas (60% Width) -->
              <div class="col-lg-7 p-4 bg-white border-end d-flex flex-column" style="overflow-y: auto; max-height: calc(100vh - 56px);">
                
                <div class="d-flex justify-content-between align-items-center pb-2 mb-3 border-bottom">
                  <div>
                    <h5 class="fw-bold text-dark mb-0">Digital Needs Discovery</h5>
                    <span class="text-muted small">Show this screen to the business owner during consultation</span>
                  </div>
                  <span class="badge bg-light text-muted border px-2 py-1">Customer View (Clean &bull; Zero Internal CAC)</span>
                </div>

                <!-- Business Category Picker -->
                <div class="mb-3">
                  <label class="form-label small fw-bold text-muted text-uppercase">1. Business Type</label>
                  <div class="d-flex flex-wrap gap-2" id="assistedCategoryPills">
                    <button class="btn btn-sm btn-dark" onclick="assistedSelectCategory('kirana', this)"><i class="bi bi-shop me-1"></i>Kirana &amp; Retail</button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="assistedSelectCategory('clinic', this)"><i class="bi bi-hospital me-1"></i>Clinic &amp; Office</button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="assistedSelectCategory('multisite', this)"><i class="bi bi-diagram-3 me-1"></i>Multi-Site Retail</button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="assistedSelectCategory('manufacturer', this)"><i class="bi bi-gear me-1"></i>Manufacturing</button>
                  </div>
                </div>

                <!-- Needs Assessment Chat Transcript -->
                <div class="mb-3">
                  <label class="form-label small fw-bold text-muted text-uppercase">2. Conversational Discovery</label>
                  <div id="assistedChatBox" class="p-3 bg-light border rounded-3 mb-2" style="max-height: 220px; overflow-y: auto;">
                    <div class="p-2 mb-2 bg-white border rounded small">
                      <strong class="text-danger">Airtel Advisor:</strong> Namaste! Aapki shop mein UPI payments aur billing machines ke liye internet chahiye?
                    </div>
                  </div>
                  <div class="input-group input-group-sm">
                    <input type="text" id="assistedChatInput" class="form-control" placeholder="Type customer's answer (Hindi, English, Hinglish)..." onkeydown="if(event.key==='Enter') assistedSendAnswer()">
                    <button class="btn btn-danger" onclick="assistedSendAnswer()"><i class="bi bi-send-fill"></i></button>
                  </div>
                </div>

                <!-- Recommended Bundle Presentation -->
                <div class="mb-3" id="assistedRecCard">
                  <div class="p-3 border rounded-3 bg-white shadow-sm border-danger">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="badge bg-success" id="assistedMatchBadge">95% Match</span>
                      <span class="badge bg-light text-muted border font-monospace" id="assistedQuoteIdBadge">QTE-2026-AST1</span>
                    </div>
                    <h5 class="fw-bold text-dark mb-1" id="assistedBundleTitle">Kirana &amp; Micro Retail Digital Starter</h5>
                    <div class="d-flex align-items-baseline gap-2 mb-2">
                      <h4 class="fw-bold text-danger mb-0" id="assistedBundlePrice">&#8377;1,999/mo</h4>
                      <span class="small text-muted">+ 18% GST (&#8377;360) &bull; One-time setup: &#8377;1,000</span>
                    </div>
                    <div class="small text-muted mb-2" id="assistedIncludedServices">
                      Includes: Biz 5G AirFiber 100Mbps, 4G Failover Router, WhatsApp API Starter, Secure Commercial Wi-Fi.
                    </div>

                    <!-- Add-on Switches Strip -->
                    <div class="p-2 bg-light border rounded small mb-3">
                      <span class="fw-bold d-block text-dark mb-1">Optional Modular Add-ons:</span>
                      <div class="d-flex flex-wrap gap-3">
                        <div class="form-check form-switch">
                          <input class="form-check-input" type="checkbox" id="assistedAddonCctv" onchange="assistedRecalculatePricing()">
                          <label class="form-check-label small" for="assistedAddonCctv">Cloud CCTV 2-Cam (+&#8377;1,200/mo)</label>
                        </div>
                        <div class="form-check form-switch">
                          <input class="form-check-input" type="checkbox" id="assistedAddonIp" onchange="assistedRecalculatePricing()">
                          <label class="form-check-label small" for="assistedAddonIp">Static IP Pool (+&#8377;500/mo)</label>
                        </div>
                        <div class="form-check form-switch">
                          <input class="form-check-input" type="checkbox" id="assistedAddonBackup" onchange="assistedRecalculatePricing()">
                          <label class="form-check-label small" for="assistedAddonBackup">Cloud Backup 1TB (+&#8377;450/mo)</label>
                        </div>
                      </div>
                    </div>

                    <!-- Customer Order Action Button -->
                    <button class="btn btn-danger w-100 fw-bold py-2 shadow-sm" onclick="assistedPlaceCustomerOrder()">
                      <i class="bi bi-check-circle-fill me-1"></i> Approve Quote &amp; Complete Doorstep KYC
                    </button>
                  </div>
                </div>

              </div>

              <!-- RIGHT PANE: Private Partner AI Co-Pilot (40% Width) -->
              <div class="col-lg-5 p-4 bg-light d-flex flex-column" style="overflow-y: auto; max-height: calc(100vh - 56px);">
                
                <div class="d-flex justify-content-between align-items-center pb-2 mb-3 border-bottom">
                  <div>
                    <h5 class="fw-bold text-dark mb-0"><i class="bi bi-robot text-danger me-2"></i>AI Sales Co-Pilot</h5>
                    <span class="text-muted small">Confidential coaching &bull; Visible ONLY to Partner</span>
                  </div>
                  <span class="badge bg-warning text-dark"><i class="bi bi-eye-slash-fill me-1"></i>Private View</span>
                </div>

                <!-- Co-Pilot Sales Rationale -->
                <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                  <span class="fw-bold small text-muted text-uppercase mb-1">Recommendation Intelligence</span>
                  <div class="small text-dark mb-2" id="copilotRationale">
                    Kirana Digital Starter selected based on price-sensitivity, single-store setup, and frequent evening UPI downtime.
                  </div>
                  <div class="row g-2 small">
                    <div class="col-12">
                      <strong class="text-success"><i class="bi bi-check2-circle me-1"></i>Satisfied Needs:</strong>
                      <div id="copilotSatisfiedNeeds" class="text-muted">100 Mbps FWA, 4G POS Failover, WhatsApp API</div>
                    </div>
                    <div class="col-12 mt-1" id="copilotUnmetBox" style="display: none;">
                      <strong class="text-danger"><i class="bi bi-exclamation-circle me-1"></i>Unmet Requirements:</strong>
                      <div id="copilotUnmetNeeds" class="text-muted">Cloud CCTV not in base plan. Pitch 2-Cam add-on.</div>
                    </div>
                  </div>
                </div>

                <!-- Consultative Sales Prompts (What to ask customer) -->
                <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                  <span class="fw-bold small text-muted text-uppercase mb-2"><i class="bi bi-chat-left-dots-fill text-primary me-1"></i>Consultative Field Prompts</span>
                  <div id="copilotPromptsList" class="d-flex flex-column gap-2 small">
                    <div class="p-2 bg-light border-start border-3 border-primary rounded">
                      Ask: "Aapki dukaan par shaam ke time UPI kitni baar fail hota hai?"
                    </div>
                    <div class="p-2 bg-light border-start border-3 border-primary rounded">
                      Tip: Remind the owner that 1 prevented payment outage covers the &#8377;66/day plan cost.
                    </div>
                  </div>
                </div>

                <!-- Anticipated Objections & Field Rebuttals -->
                <div class="card p-3 border-0 shadow-sm rounded-3 mb-3 bg-white">
                  <span class="fw-bold small text-muted text-uppercase mb-2"><i class="bi bi-shield-shaded text-danger me-1"></i>Anticipated Objections &amp; Rebuttals</span>
                  <div id="copilotObjectionsList" class="d-flex flex-column gap-2 small">
                    <div class="p-2 bg-light border rounded">
                      <strong class="text-dark d-block">Objection: "Comparing with Jio hotspot"</strong>
                      <span class="text-muted">Rebuttal: Consumer hotspots throttle after daily quota with zero SLA. Airtel Business delivers dedicated priority bandwidth with 4-hour doorstep MTTR.</span>
                    </div>
                  </div>
                </div>

                <!-- Partner Commission & Attribution Stamping Preview -->
                <div class="card p-3 border-0 shadow-sm rounded-3 bg-white mt-auto">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-bold small text-muted text-uppercase">Commission Ledger Stamping</span>
                    <span class="badge bg-success fs-6">&#8377;1,500</span>
                  </div>
                  <div class="small text-muted">
                    Eligibility: Automatically marked <strong>ELIGIBLE</strong> upon Step 5 Service Activation. Disbursed via weekly partner NEFT batch.
                  </div>
                </div>

              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

content = content.replace('</body>', assisted_modal_html + '\n</body>')
print("[OK] #assistedModeModal tablet dual-aspect modal patched.")

# 4. Add JavaScript for Partner Intelligence & Assisted Tablet Mode
partner_js = """
    // =========================================================================
    // PHASE 4: ASSISTED DIGITAL PARTNER ECOSYSTEM JAVASCRIPT
    // =========================================================================
    let activePartnerId = 'PTR-DEL-042';
    let assistedCurrentCategory = 'kirana';

    function switchPartnerView(partnerId) {
      activePartnerId = partnerId;
      loadPartnerIntelligence();
    }

    function loadPartnerIntelligence() {
      const pId = activePartnerId;
      
      // 1. Fetch Partner Analytics
      fetch('/api/partner/' + pId + '/analytics')
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            const m = data.metrics;
            document.getElementById('ptrKpiReferred').textContent = m.total_referred_sessions;
            document.getElementById('ptrKpiOrders').textContent = m.total_orders_placed;
            document.getElementById('ptrKpiPendingActivations').textContent = m.pending_activations + ' Pending Act';
            document.getElementById('ptrKpiActivations').textContent = m.total_activations;
            document.getElementById('ptrKpiConversionRate').textContent = m.conversion_rate_pct + '% Conv';
            document.getElementById('ptrKpiEarnedComm').textContent = '₹' + m.commission_earned_inr.toLocaleString();
            document.getElementById('ptrKpiPendingComm').textContent = '₹' + m.commission_pending_inr.toLocaleString() + ' Pending';
          }
        })
        .catch(err => console.error("Error loading partner analytics:", err));

      // 2. Fetch Partner Profile & QR Code
      const singleId = (pId === 'ALL') ? 'PTR-DEL-042' : pId;
      fetch('/api/partner/' + singleId + '/profile')
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            const p = data.partner;
            document.getElementById('ptrKpiReferralCode').textContent = p.referral_code;
            document.getElementById('partnerReferralUrlInput').value = data.referral_url;
            
            // Render QR Code SVG
            fetch('/api/partner/' + singleId + '/qr')
              .then(res => res.text())
              .then(svg => {
                document.getElementById('partnerQrContainer').innerHTML = svg;
              });

            // Update Assisted Mode Header names
            const hName = document.getElementById('assistedActivePartnerName');
            if (hName) hName.textContent = `${p.name} (${p.agency_name})`;
            const hBadge = document.getElementById('assistedPartnerIdBadge');
            if (hBadge) hBadge.textContent = p.partner_id;
          }
        })
        .catch(err => console.error("Error loading partner profile:", err));

      // 3. Fetch Commission Ledger
      const userRole = (pId === 'ALL') ? 'super_admin' : 'channel_partner';
      fetch('/api/partner/' + pId + '/commissions?role=' + userRole + '&user_partner_id=' + pId)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            renderCommissionLedger(data.commissions);
            document.getElementById('ledgerCountBadge').textContent = data.count + ' Records';
          }
        })
        .catch(err => console.error("Error loading commissions:", err));

      // 4. Fetch Partner Lead Rescue Desk
      fetch('/api/partner/' + singleId + '/leads')
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            renderPartnerRescueDesk(data.leads);
            document.getElementById('partnerLeadsCountBadge').textContent = data.count + ' Opportunities Available';
          }
        })
        .catch(err => console.error("Error loading partner rescue leads:", err));
    }

    function renderCommissionLedger(records) {
      const tbody = document.getElementById('partnerCommissionTbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!records || records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-3 text-muted small">No commission records for this partner view.</td></tr>`;
        return;
      }

      records.forEach(c => {
        const tr = document.createElement('tr');
        const statusBadge = {
          'pending': '<span class="badge bg-warning text-dark"><i class="bi bi-clock-history me-1"></i>Pending Act</span>',
          'eligible': '<span class="badge bg-primary"><i class="bi bi-check-circle-fill me-1"></i>Eligible (Activated)</span>',
          'approved': '<span class="badge bg-info text-dark"><i class="bi bi-patch-check-fill me-1"></i>Approved</span>',
          'paid': '<span class="badge bg-success"><i class="bi bi-cash-stack me-1"></i>Paid (NEFT)</span>',
          'reversed': '<span class="badge bg-danger"><i class="bi bi-x-circle me-1"></i>Reversed</span>'
        }[c.status] || `<span class="badge bg-light text-dark">${c.status}</span>`;

        let actionBtns = '';
        if (c.status === 'eligible') {
          actionBtns = `<button class="btn btn-xs btn-outline-success" onclick="executeCommissionAction('${c.commission_id}', 'approve')"><i class="bi bi-check-lg me-1"></i>Approve</button>`;
        } else if (c.status === 'approved') {
          actionBtns = `<button class="btn btn-xs btn-success" onclick="executeCommissionAction('${c.commission_id}', 'mark_paid')"><i class="bi bi-cash me-1"></i>Pay Now</button>`;
        } else if (c.status === 'pending') {
          actionBtns = `<span class="text-muted small">Awaiting Step 5</span>`;
        } else {
          actionBtns = `<span class="text-muted small">Finalized</span>`;
        }

        tr.innerHTML = `
          <td><code>${c.commission_id}</code></td>
          <td><code>${c.order_id}</code></td>
          <td>
            <strong>${c.customer_name}</strong>
            <div class="text-muted small" style="font-size: 0.70rem;">${c.bundle_name}</div>
          </td>
          <td>₹${c.monthly_subtotal_inr.toLocaleString()}/mo</td>
          <td><strong class="text-dark">₹${c.commission_amount_inr.toLocaleString()}</strong></td>
          <td>${statusBadge}</td>
          <td><small class="text-muted">${c.created_at_display || 'Recent'}</small></td>
          <td class="text-end">${actionBtns}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function executeCommissionAction(commissionId, action) {
      fetch('/api/partner/commission/' + commissionId + '/action?role=super_admin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action, admin_user: 'Airtel Finance Manager' })
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Commission updated: ' + action.toUpperCase());
          loadPartnerIntelligence();
        } else {
          alert('Error: ' + data.message);
        }
      });
    }

    function renderPartnerRescueDesk(leads) {
      const tbody = document.getElementById('partnerRescueDeskTbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!leads || leads.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-3 text-muted small">No recovery opportunities currently unassigned in your territory.</td></tr>`;
        return;
      }

      leads.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><code>${l.recovery_id}</code></td>
          <td><strong>${l.business_name}</strong><div class="small text-muted">${l.contact_person}</div></td>
          <td>${l.recommended_bundle}</td>
          <td><span class="badge bg-danger">${l.objection_label}</span></td>
          <td><span class="badge bg-success">${l.priority_score} (${l.priority_tier})</span></td>
          <td><small class="text-muted">${l.created_at_display || 'Recent'}</small></td>
          <td><small class="text-dark">${l.action_title || l.suggested_next_action}</small></td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-danger" onclick="claimPartnerLead('${l.recovery_id}')">
              <i class="bi bi-person-check me-1"></i>Claim &amp; Visit
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function claimPartnerLead(recoveryId) {
      const singleId = (activePartnerId === 'ALL') ? 'PTR-DEL-042' : activePartnerId;
      fetch('/api/partner/' + singleId + '/lead/' + recoveryId + '/claim', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Opportunity claimed! Lead assigned to you in Recovery Hub.');
          loadPartnerIntelligence();
        }
      });
    }

    function copyPartnerReferralLink() {
      const el = document.getElementById('partnerReferralUrlInput');
      el.select();
      navigator.clipboard.writeText(el.value);
      alert('Partner referral link copied to clipboard!');
    }

    // =========================================================================
    // ASSISTED TABLET MODE RUNTIME LOGIC
    // =========================================================================
    function openAssistedModeModal() {
      const modal = new bootstrap.Modal(document.getElementById('assistedModeModal'));
      modal.show();
      assistedSelectCategory('kirana', null);
    }

    function assistedSelectCategory(cat, btn) {
      assistedCurrentCategory = cat;
      if (btn) {
        document.querySelectorAll('#assistedCategoryPills button').forEach(b => {
          b.classList.remove('btn-dark');
          b.classList.add('btn-outline-secondary');
        });
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-dark');
      }

      const bundles = {
        'kirana': { title: 'Kirana & Micro Retail Digital Starter', price: '₹1,999/mo', setup: '₹1,000 setup', inc: 'Biz 5G AirFiber 100Mbps, 4G Failover Router, WhatsApp API Starter, Secure Commercial Wi-Fi.' },
        'clinic': { title: 'Clinic & Professional Office Suite', price: '₹3,499/mo', setup: '₹1,500 setup', inc: '200 Mbps Optical Business Fiber, 1TB Cloud Backup (Compliant), Google Workspace Starter, Secure Wi-Fi.' },
        'multisite': { title: 'Multi-Site Retail & Restaurant Pro', price: '₹7,999/mo', setup: '₹3,000 setup', inc: '500 Mbps Optical Fiber, Managed SD-WAN Multi-Branch, Cloud CCTV 4 Cams, Managed Firewall.' },
        'manufacturer': { title: 'Small Manufacturing & Industrial Suite', price: '₹14,999/mo', setup: '₹5,000 setup', inc: 'Internet Leased Line 50 Mbps 1:1, Static IPv4 /29 Pool, Machine IoT Telemetry, Dedicated Manager.' }
      };

      const b = bundles[cat] || bundles['kirana'];
      document.getElementById('assistedBundleTitle').textContent = b.title;
      document.getElementById('assistedBundlePrice').textContent = b.price;
      document.getElementById('assistedIncludedServices').textContent = 'Includes: ' + b.inc;

      // Update Co-Pilot Real-time Advice
      fetch('/api/partner/copilot/advice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profile: { business_type: cat },
          identified_needs: ['connectivity:HighSpeed', 'business_continuity:UPI'],
          bundle_id: 'bundle_' + cat
        })
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          const adv = data.advice;
          document.getElementById('copilotRationale').textContent = adv.rationale;
          document.getElementById('copilotSatisfiedNeeds').textContent = adv.satisfied_needs.join(', ');
          
          const pBox = document.getElementById('copilotPromptsList');
          pBox.innerHTML = '';
          adv.consultative_prompts.forEach(p => {
            const d = document.createElement('div');
            d.className = 'p-2 bg-light border-start border-3 border-primary rounded';
            d.textContent = p;
            pBox.appendChild(d);
          });

          const oBox = document.getElementById('copilotObjectionsList');
          oBox.innerHTML = '';
          adv.anticipated_objections.forEach(o => {
            const d = document.createElement('div');
            d.className = 'p-2 bg-light border rounded';
            d.innerHTML = `<strong class="text-dark d-block">Objection: "${o.objection}"</strong><span class="text-muted">Rebuttal: ${o.rebuttal}</span>`;
            oBox.appendChild(d);
          });
        }
      });
    }

    function assistedSendAnswer() {
      const input = document.getElementById('assistedChatInput');
      const val = (input.value || '').trim();
      if (!val) return;

      const chatBox = document.getElementById('assistedChatBox');
      const userDiv = document.createElement('div');
      userDiv.className = 'p-2 mb-2 bg-light border rounded small text-end';
      userDiv.innerHTML = `<strong>Customer:</strong> ${val}`;
      chatBox.appendChild(userDiv);
      input.value = '';

      // AI response
      setTimeout(() => {
        const botDiv = document.createElement('div');
        botDiv.className = 'p-2 mb-2 bg-white border rounded small';
        botDiv.innerHTML = `<strong class="text-danger">Airtel Advisor:</strong> Samjhe. Aapke liye hamara guaranteed backup failover plan bilkul perfect rahega taaki evening rush mein payments na rukein.`;
        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      }, 500);
    }

    function assistedRecalculatePricing() {
      // live toggle recalculation in assisted mode
    }

    function assistedPlaceCustomerOrder() {
      const singleId = (activePartnerId === 'ALL') ? 'PTR-DEL-042' : activePartnerId;
      const btype = assistedCurrentCategory;
      const bundleMap = { 'kirana': 'bundle_kirana', 'clinic': 'bundle_clinic', 'multisite': 'bundle_multisite', 'manufacturer': 'bundle_manufacturer' };
      
      const payload = {
        bundle_id: bundleMap[btype],
        ref_partner: singleId,
        business_name: 'Merchant Shop (Assisted Mode)',
        contact_name: 'Business Owner',
        phone: '+91 98110 55221',
        city: 'Delhi',
        gstin: '07AAACS1429B1ZB',
        addons: []
      };

      fetch('/api/consumer/order/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(res => {
        if (res.status === 'success') {
          alert('Assisted Order Created: ' + res.order.order_id + '\\nReferral attributed to ' + singleId + '\\nCommission stamped: ₹1,500 PENDING activation.');
          const modalEl = document.getElementById('assistedModeModal');
          const modalInstance = bootstrap.Modal.getInstance(modalEl);
          if (modalInstance) modalInstance.hide();
          loadPartnerIntelligence();
        }
      });
    }
"""

content = content.replace('// Initial load', partner_js + '\n    // Initial load')
print("[OK] Partner JS functions patched.")

# Also add loadPartnerIntelligence to initial load
content = content.replace('loadRecoveryData();', 'loadRecoveryData();\n    loadPartnerIntelligence();')
print("[OK] loadPartnerIntelligence added to initial load.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully to control.html for Phase 4!")

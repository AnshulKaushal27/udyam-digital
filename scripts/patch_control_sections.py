import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update roleSelector
old_roles = """            <option value="super_admin" {% if active_role == 'super_admin' %}selected{% endif %}>👑 Super Administrator</option>
            <option value="ops_manager" {% if active_role == 'ops_manager' %}selected{% endif %}>🔧 Operations Manager</option>
            <option value="kyc_officer" {% if active_role == 'kyc_officer' %}selected{% endif %}>📑 KYC Verification Officer</option>
            <option value="sales_partner" {% if active_role == 'sales_partner' %}selected{% endif %}>🤝 Channel Partner / Sales</option>"""

new_roles = """            <option value="super_admin" {% if active_role == 'super_admin' %}selected{% endif %}>👑 Super Administrator</option>
            <option value="ops_manager" {% if active_role == 'ops_manager' %}selected{% endif %}>🔧 Operations Manager</option>
            <option value="sales_executive" {% if active_role == 'sales_executive' %}selected{% endif %}>💼 Sales Executive</option>
            <option value="kyc_officer" {% if active_role == 'kyc_officer' %}selected{% endif %}>📑 KYC Verification Officer</option>
            <option value="sales_partner" {% if active_role == 'sales_partner' %}selected{% endif %}>🤝 Channel Partner</option>"""

if old_roles in html:
    html = html.replace(old_roles, new_roles, 1)
    print("1. Updated roleSelector successfully.")
else:
    print("1. roleSelector target not found.")

# 2. Add #sec-funnel and #sec-exceptions sections
sec_funnel_and_exceptions = """
      <!-- ========================================================= -->
      <!-- SECTION: FUNNEL INTELLIGENCE & DROP-OFF ANALYSIS (Phase 6) -->
      <!-- ========================================================= -->
      <section id="sec-funnel" style="display: none;">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0"><i class="bi bi-funnel-fill text-danger me-2"></i>Funnel Intelligence &amp; Drop-off Diagnostics</h4>
            <div class="small text-muted">Complete 6-stage MSME acquisition waterfall with stage-to-stage conversion, drop-off root causes, and lead drilldowns</div>
          </div>
          <button class="btn btn-sm btn-outline-secondary" onclick="loadFunnelIntelligence()">
            <i class="bi bi-arrow-clockwise me-1"></i> Refresh Funnel
          </button>
        </div>

        <!-- Filter Bar -->
        <div class="card-kpi p-3 mb-4 bg-light">
          <div class="row g-2 align-items-center">
            <div class="col-md-3">
              <label class="small text-muted fw-bold">CUSTOMER SEGMENT</label>
              <select id="funnelSegmentFilter" class="form-select form-select-sm" onchange="loadFunnelIntelligence()">
                <option value="">All Segments (5,000 Leads)</option>
                <option value="Micro retail & services">Kirana &amp; Micro Retail (2,709)</option>
                <option value="Professional offices">Professional Offices &amp; Clinics (1,247)</option>
                <option value="Small multi-site businesses">Multi-Site Retail &amp; Food (755)</option>
                <option value="Small manufacturers">Small Manufacturers (289)</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="small text-muted fw-bold">LOCATION / CITY TIER</label>
              <select id="funnelTierFilter" class="form-select form-select-sm" onchange="loadFunnelIntelligence()">
                <option value="">All City Tiers</option>
                <option value="1">Tier 1 Metros (Delhi, Mumbai, Bengaluru)</option>
                <option value="2">Tier 2 Growing Hubs (Kochi, Vadodara, Pune)</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="small text-muted fw-bold">SEARCH CITY</label>
              <input type="text" id="funnelCitySearch" class="form-control form-control-sm" placeholder="e.g. Kolkata, Ahmedabad, Kochi..." onkeyup="if(event.key==='Enter') loadFunnelIntelligence()">
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button class="btn btn-danger btn-sm w-100" onclick="loadFunnelIntelligence()">
                <i class="bi bi-filter me-1"></i> Apply Filters
              </button>
            </div>
          </div>
        </div>

        <!-- Key Bottleneck Highlight Banner -->
        <div class="alert alert-danger d-flex align-items-center justify-content-between p-3 mb-4 shadow-sm" role="alert">
          <div class="d-flex align-items-center">
            <i class="bi bi-exclamation-octagon-fill fs-3 me-3 text-danger"></i>
            <div>
              <strong class="d-block text-dark">Primary Funnel Collapse Point Identified:</strong>
              <span id="funnelSteepestBanner" class="text-danger fw-semibold">Stage 3 (Needs Assessed) to Stage 4 (Quote Accepted) — 56.4% Drop Rate (1,113 Losses)</span>
            </div>
          </div>
          <button class="btn btn-outline-danger btn-sm" onclick="openFunnelStageLeads('dropped_quote', 'Stage 3 Dropouts (Needs Assessed)')">
            <i class="bi bi-search me-1"></i> Inspect 1,113 Dropped Quotes
          </button>
        </div>

        <!-- 6-Stage Waterfall Cards -->
        <div class="row g-3 mb-4" id="funnelStagesContainer">
          <!-- Populated by loadFunnelIntelligence() -->
        </div>

        <!-- Segment Breakdown & City Tier Comparison -->
        <div class="row g-4 mb-4">
          <div class="col-lg-7">
            <div class="card-kpi p-3 h-100">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold text-dark mb-0"><i class="bi bi-pie-chart-fill text-primary me-2"></i>Segment-Wise Funnel Performance</h6>
                <span class="badge bg-light text-dark border">Ground Truth Dataset</span>
              </div>
              <div class="table-responsive">
                <table class="table table-enterprise table-sm align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Segment</th>
                      <th>Total Leads</th>
                      <th>Assessed</th>
                      <th>Quote Accepted</th>
                      <th>Activated</th>
                      <th>Net Conv %</th>
                    </tr>
                  </thead>
                  <tbody id="funnelSegmentsTbody">
                    <!-- Populated by JS -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="col-lg-5">
            <div class="card-kpi p-3 h-100">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold text-dark mb-0"><i class="bi bi-geo-alt-fill text-danger me-2"></i>City Tier Distribution</h6>
                <span class="badge bg-light text-dark border">Tier 1 vs Tier 2</span>
              </div>
              <div class="table-responsive">
                <table class="table table-enterprise table-sm align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Tier Classification</th>
                      <th>Total Leads</th>
                      <th>Activated</th>
                      <th>Conv %</th>
                    </tr>
                  </thead>
                  <tbody id="funnelTiersTbody">
                    <!-- Populated by JS -->
                  </tbody>
                </table>
              </div>
              <div class="alert alert-light border small mt-3 mb-0 text-muted">
                <i class="bi bi-lightbulb text-warning me-1"></i> <strong>Strategic Finding:</strong> Tier 2 hubs (Kochi, Vadodara) show higher quote acceptance (48.2%) than Tier 1 metros due to fewer unmanaged fiber alternatives.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================================= -->
      <!-- SECTION: UNIFIED EXCEPTION ACTION CENTRE (Phase 6) -->
      <!-- ========================================================= -->
      <section id="sec-exceptions" style="display: none;">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0"><i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>Unified Operational Exception Centre</h4>
            <div class="small text-muted">Central Action Queue uniting abandoned quotes, KYC exceptions, installation risks, and unassigned resources</div>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-secondary" onclick="loadExceptionsQueue()">
              <i class="bi bi-arrow-clockwise me-1"></i> Refresh Queue
            </button>
          </div>
        </div>

        <!-- Exception Summary Counters -->
        <div class="row g-3 mb-4">
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-danger">
              <div class="text-muted small fw-bold">CRITICAL ATTENTION</div>
              <div class="fs-4 fw-bold text-danger" id="excCriticalCount">0</div>
              <div class="small text-muted">Imminent SLA breach / Stalled KYC</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-warning">
              <div class="text-muted small fw-bold">OPEN EXCEPTIONS</div>
              <div class="fs-4 fw-bold text-warning" id="excOpenCount">0</div>
              <div class="small text-muted">Awaiting operational action</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-info">
              <div class="text-muted small fw-bold">ACKNOWLEDGED</div>
              <div class="fs-4 fw-bold text-info" id="excAckCount">0</div>
              <div class="small text-muted">Assigned and in progress</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card-kpi border-start border-4 border-success">
              <div class="text-muted small fw-bold">RESOLVED TODAY</div>
              <div class="fs-4 fw-bold text-success" id="excResolvedCount">0</div>
              <div class="small text-muted">Actioned exceptions</div>
            </div>
          </div>
        </div>

        <!-- Exception Filter Tabs -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div class="btn-group btn-group-sm" role="group">
            <button type="button" class="btn btn-outline-dark active" onclick="filterExceptionsTable('ALL', this)">All Exceptions</button>
            <button type="button" class="btn btn-outline-danger" onclick="filterExceptionsTable('CRITICAL', this)">Critical Only</button>
            <button type="button" class="btn btn-outline-warning" onclick="filterExceptionsTable('OPEN', this)">Open Only</button>
            <button type="button" class="btn btn-outline-success" onclick="filterExceptionsTable('RESOLVED', this)">Resolved</button>
          </div>
          <span class="small text-muted" id="exceptionsTableCount">Showing all exceptions</span>
        </div>

        <!-- Exceptions Data-Rich Table -->
        <div class="card-kpi p-0 overflow-hidden mb-4 shadow-sm">
          <div class="table-responsive">
            <table class="table table-enterprise table-hover align-middle mb-0" id="exceptionsTable">
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Type &amp; Module</th>
                  <th>Customer / Ref</th>
                  <th>Location</th>
                  <th>Root Cause Reason</th>
                  <th>Age</th>
                  <th>Assigned Owner</th>
                  <th>Status</th>
                  <th>Operational Action</th>
                </tr>
              </thead>
              <tbody id="exceptionsTbody">
                <!-- Populated by loadExceptionsQueue() -->
              </tbody>
            </table>
          </div>
        </div>
      </section>
"""

# Insert #sec-funnel right after #sec-overview
overview_end_marker = '</section>\n\n      <!-- ========================================================= -->'
if overview_end_marker in html and 'id="sec-funnel"' not in html:
    html = html.replace(overview_end_marker, '</section>\n' + sec_funnel_and_exceptions + '\n      <!-- ========================================================= -->', 1)
    print("2. Inserted #sec-funnel and #sec-exceptions sections.")
else:
    print("2. #sec-funnel marker not matched or already present.")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved HTML with Funnel and Exceptions sections.")

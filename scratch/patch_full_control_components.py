import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enhance #sec-overview with Dimensional Segregation Pills and 13-KPI Dynamic Grid
old_overview_header = """        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0">Executive Operational Overview</h4>
            <div class="small text-muted">Benchmarking Historical Synthetic Baseline vs. Real-Time Prototype Sessions</div>
          </div>
          <span class="badge bg-light text-dark border"><i class="bi bi-info-circle me-1"></i> Baseline: Apr–Jun 2026 (5,000 Leads)</span>
        </div>"""

new_overview_header = """        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-0"><i class="bi bi-speedometer2 text-danger me-2"></i>Executive Operational Command Centre</h4>
            <div class="small text-muted">Strategic MSME Acquisition Diagnostics — Historical Baseline vs. Live Prototype vs. Assignment Targets</div>
          </div>
          <button class="btn btn-sm btn-outline-secondary" onclick="loadExecutiveOverview()">
            <i class="bi bi-arrow-clockwise me-1"></i> Refresh Executive Overview
          </button>
        </div>

        <!-- Strict 4-Dimensional Metric Segregation Banner (Section 3) -->
        <div class="card-kpi p-3 mb-4 bg-light border-0 shadow-sm">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="small fw-bold text-dark text-uppercase"><i class="bi bi-layers-fill text-primary me-1"></i>Metric Classification &amp; Governance (Section 3 Requirement):</span>
            <span class="badge bg-white text-secondary border">Anti-Hallucination Framework Active</span>
          </div>
          <div class="row g-2">
            <div class="col-md-3">
              <div class="p-2 bg-white rounded border border-secondary-subtle small">
                <span class="badge bg-dark mb-1">DIMENSION 1</span>
                <strong class="d-block text-dark">Historical Baseline</strong>
                <span class="text-muted" style="font-size: 0.75rem;">smb_leads.csv (N=5,000 Leads, 7.36% Conv, ₹15,000 CAC, 17.6d TAT)</span>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-2 bg-white rounded border border-primary-subtle small">
                <span class="badge bg-primary mb-1">DIMENSION 2</span>
                <strong class="d-block text-primary">Assignment Target</strong>
                <span class="text-muted" style="font-size: 0.75rem;">SYNC 2026 Directives (25.0% Conv, ≤3.0d TAT, ≤₹7,500 CAC)</span>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-2 bg-white rounded border border-success-subtle small">
                <span class="badge bg-success mb-1">DIMENSION 3</span>
                <strong class="d-block text-success">Actual Prototype Results</strong>
                <span class="text-muted" style="font-size: 0.75rem;">In-Memory Transactions (Shared Orders, Live Quotes, Audit Trail)</span>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-2 bg-white rounded border border-warning-subtle small">
                <span class="badge bg-warning text-dark mb-1">DIMENSION 4</span>
                <strong class="d-block text-warning-emphasis">Simulated Scenario</strong>
                <span class="text-muted" style="font-size: 0.75rem;">Interactive What-If Model Projections (Section 12 Non-Double-Counted)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Dynamic 13-KPI Executive Grid (Populated from /api/control/analytics/executive) -->
        <div class="row g-3 mb-4" id="executiveKpiGrid">
          <!-- Dynamically populated by loadExecutiveOverview() -->
        </div>"""

if old_overview_header in html:
    html = html.replace(old_overview_header, new_overview_header, 1)
    print("1. Enhanced #sec-overview with Dimensional Governance & 13-KPI Grid.")
else:
    print("1. Overview header marker not found.")

# 2. Enhance #sec-quotes with Section 5 Quote Loss Intelligence Card
quote_loss_card = """
        <!-- Section 5: Quote Loss Intelligence & Bottleneck Diagnostics -->
        <div class="card-kpi p-4 mb-4 border-start border-4 border-danger shadow-sm">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h5 class="fw-bold text-dark mb-0"><i class="bi bi-x-octagon-fill text-danger me-2"></i>Quote Loss Intelligence &amp; Root-Cause Analysis</h5>
              <span class="small text-muted">Analysis of the 1,113 historical quote rejections (56.4% collapse point at Needs Assessed stage)</span>
            </div>
            <a href="#sec-recovery" onclick="showSection('recovery', document.querySelector('a[href=\\'#sec-recovery\\']'))" class="btn btn-sm btn-danger">
              <i class="bi bi-arrow-repeat me-1"></i> Launch Phase 3 Quote Recovery Hub
            </a>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-3">
              <div class="p-3 bg-light rounded border border-danger border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong class="text-dark small">Price Too High / Opaque</strong>
                  <span class="badge bg-danger">414 Leads (37.2%)</span>
                </div>
                <div class="progress mb-2" style="height: 6px;">
                  <div class="progress-bar bg-danger" style="width: 37.2%;"></div>
                </div>
                <div class="small text-muted" style="font-size: 0.8rem;">
                  <strong>Action:</strong> Automated 1-click down-tiering to Airtel Kirana Starter (₹1,999/mo) with transparent 18% GST breakdown.
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 bg-light rounded border border-warning border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong class="text-dark small">Competitor Cheaper / Faster</strong>
                  <span class="badge bg-warning text-dark">207 Leads (18.6%)</span>
                </div>
                <div class="progress mb-2" style="height: 6px;">
                  <div class="progress-bar bg-warning" style="width: 18.6%;"></div>
                </div>
                <div class="small text-muted" style="font-size: 0.8rem;">
                  <strong>Action:</strong> Highlight SLA guarantees (99.9% uptime, 4-hour MTTR) and commercial static IP / guest Wi-Fi.
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 bg-light rounded border border-info border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong class="text-dark small">Quote Too Complex / Slow</strong>
                  <span class="badge bg-info text-dark">206 Leads (18.5%)</span>
                </div>
                <div class="progress mb-2" style="height: 6px;">
                  <div class="progress-bar bg-info" style="width: 18.5%;"></div>
                </div>
                <div class="small text-muted" style="font-size: 0.8rem;">
                  <strong>Action:</strong> Replace 5-day enterprise PDF quotes with instant conversational quotes generated in discovery chat.
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 bg-light rounded border border-secondary border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong class="text-dark small">Other / Delivery Delays</strong>
                  <span class="badge bg-secondary">286 Leads (25.7%)</span>
                </div>
                <div class="progress mb-2" style="height: 6px;">
                  <div class="progress-bar bg-secondary" style="width: 25.7%;"></div>
                </div>
                <div class="small text-muted" style="font-size: 0.8rem;">
                  <strong>Action:</strong> Proactive AI outreach triggers within 24 hours of inactivity with personalized reassurance.
                </div>
              </div>
            </div>
          </div>
        </div>
"""

# Insert Quote Loss Card right before <!-- Quotes Data Table --> in #sec-quotes
quotes_table_marker = '        <!-- Quotes Data Table -->'
if quotes_table_marker in html and 'Quote Loss Intelligence &amp; Root-Cause Analysis' not in html:
    html = html.replace(quotes_table_marker, quote_loss_card + '\n        <!-- Quotes Data Table -->', 1)
    print("2. Added Quote Loss Intelligence card into #sec-quotes.")
else:
    print("2. Quotes table marker not found or already inserted.")

# 3. Enhance #sec-orders table header with SLA & Proactive Risk column
old_order_th = """                  <th>Assigned Field Engineer</th>
                  <th>Operational Action</th>"""

new_order_th = """                  <th>Assigned Field Engineer</th>
                  <th>SLA &amp; Proactive Risk</th>
                  <th>Operational Action</th>"""

if old_order_th in html:
    html = html.replace(old_order_th, new_order_th, 1)
    print("3. Added 'SLA & Proactive Risk' column header to orders table.")
else:
    print("3. Orders table header marker not found.")

# 4. Enhance #sec-insights with 4-Part AI Insights and What-If Scenario Simulator
old_insights_sec = """        <div class="row g-3" id="insightsContainer">
          <!-- Populated from API -->
        </div>
      </section>"""

new_insights_sec = """        <!-- AI-Generated 4-Part Executive Insights Container -->
        <div class="row g-3 mb-5" id="insightsContainer">
          <!-- Populated from /api/control/analytics/insights -->
        </div>

        <!-- ========================================================= -->
        <!-- SECTION 12: INTERACTIVE BUSINESS SCENARIO SIMULATOR -->
        <!-- ========================================================= -->
        <div class="card-kpi p-4 shadow-sm border-start border-4 border-danger">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h5 class="fw-bold text-dark mb-0"><i class="bi bi-calculator-fill text-danger me-2"></i>Executive What-If Business Scenario Simulator</h5>
              <div class="small text-muted">Model the projected impact of conversion improvements and recovery interventions (Section 12 Non-Double-Counted Architecture)</div>
            </div>
            <span class="badge bg-warning text-dark border"><i class="bi bi-cpu-fill me-1"></i> Dimension: SIMULATED_SCENARIO</span>
          </div>

          <div class="row g-4">
            <!-- Left Column: Interactive Scenario Sliders -->
            <div class="col-lg-5 border-end pe-lg-4">
              <h6 class="fw-bold text-dark mb-3"><i class="bi bi-sliders me-1"></i>Adjust Strategic Assumptions:</h6>

              <div class="mb-3">
                <div class="d-flex justify-content-between small fw-bold mb-1">
                  <span>Target Quote Acceptance:</span>
                  <span class="text-danger" id="sliderQuoteVal">55.0%</span>
                </div>
                <input type="range" class="form-range" id="simQuoteAcceptance" min="30" max="80" step="1" value="55" oninput="updateSimSliders()">
                <div class="d-flex justify-content-between text-muted" style="font-size: 0.7rem;">
                  <span>Baseline: 43.6%</span>
                  <span>SYNC Target: 65.0%</span>
                </div>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-content-between small fw-bold mb-1">
                  <span>Target KYC Completion:</span>
                  <span class="text-primary" id="sliderKycVal">78.0%</span>
                </div>
                <input type="range" class="form-range" id="simKycCompletion" min="40" max="95" step="1" value="78" oninput="updateSimSliders()">
                <div class="d-flex justify-content-between text-muted" style="font-size: 0.7rem;">
                  <span>Baseline: 68.3%</span>
                  <span>Target: 85.0%</span>
                </div>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-content-between small fw-bold mb-1">
                  <span>Target Activation Conversion:</span>
                  <span class="text-success" id="sliderActVal">80.0%</span>
                </div>
                <input type="range" class="form-range" id="simActivation" min="40" max="95" step="1" value="80" oninput="updateSimSliders()">
                <div class="d-flex justify-content-between text-muted" style="font-size: 0.7rem;">
                  <span>Baseline: 62.6%</span>
                  <span>Target: 90.0%</span>
                </div>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-content-between small fw-bold mb-1">
                  <span>Lead Recovery Win-Back:</span>
                  <span class="text-info" id="sliderRecVal">20.0%</span>
                </div>
                <input type="range" class="form-range" id="simLeadRecovery" min="0" max="50" step="1" value="20" oninput="updateSimSliders()">
                <div class="d-flex justify-content-between text-muted" style="font-size: 0.7rem;">
                  <span>Baseline: 0.0%</span>
                  <span>Phase 3 Pilot: 28.5%</span>
                </div>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-content-between small fw-bold mb-1">
                  <span>Assumed Blended CAC:</span>
                  <span class="text-secondary" id="sliderCacVal">₹8,500</span>
                </div>
                <input type="range" class="form-range" id="simCacSpend" min="5000" max="20000" step="500" value="8500" oninput="updateSimSliders()">
                <div class="d-flex justify-content-between text-muted" style="font-size: 0.7rem;">
                  <span>Target: ₹7,500</span>
                  <span>Baseline: ₹15,000</span>
                </div>
              </div>

              <button class="btn btn-danger btn-sm w-100 fw-bold py-2 mt-2" onclick="runScenarioSimulation()">
                <i class="bi bi-play-circle-fill me-1"></i> Calculate Simulated Impact
              </button>
            </div>

            <!-- Right Column: Simulated Financial & Funnel Projections -->
            <div class="col-lg-7 ps-lg-4">
              <h6 class="fw-bold text-dark mb-3"><i class="bi bi-graph-up-arrow me-1"></i>Projected Business Impact:</h6>

              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <div class="p-3 bg-light rounded border h-100">
                    <span class="text-muted small fw-bold">PROJECTED ACTIVATIONS</span>
                    <div class="fs-3 fw-bold text-success" id="simProjectedActivations">--</div>
                    <div class="small text-muted" id="simActivationsLift">Baseline: 368 Activations</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="p-3 bg-light rounded border h-100">
                    <span class="text-muted small fw-bold">INCREMENTAL ARR LIFT</span>
                    <div class="fs-3 fw-bold text-primary" id="simIncrementalArr">--</div>
                    <div class="small text-muted" id="simMonthlyRevenue">Based on ₹3,850 Blended ARPU</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="p-3 bg-light rounded border h-100">
                    <span class="text-muted small fw-bold">TOTAL ACQUISITION SPEND</span>
                    <div class="fs-4 fw-bold text-dark" id="simAcquisitionSpend">--</div>
                    <div class="small text-muted">Baseline Spend: ₹55.20 Lakh</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="p-3 bg-light rounded border h-100">
                    <span class="text-muted small fw-bold">CAC PAYBACK PERIOD</span>
                    <div class="fs-4 fw-bold text-danger" id="simPaybackMonths">-- Months</div>
                    <div class="small text-muted">Payback on ₹3,850/mo subscription</div>
                  </div>
                </div>
              </div>

              <!-- Mathematical Transparency Callout -->
              <div class="alert alert-light border small text-muted mb-0">
                <i class="bi bi-info-circle-fill text-primary me-1"></i> <strong>Audit Compliance:</strong> Projections utilize a non-double-counting funnel sequence: Primary Accepted Leads = 1,974 × Quote Acceptance %; Recovered Leads = (1,974 − Primary) × Recovery %; Total Accepted = Primary + Recovered; Projected Activations = Total Accepted × KYC % × Activation %.
              </div>
            </div>
          </div>
        </div>
      </section>"""

if old_insights_sec in html:
    html = html.replace(old_insights_sec, new_insights_sec, 1)
    print("4. Enhanced #sec-insights with 4-part AI Insights and What-If Scenario Simulator.")
else:
    print("4. Insights section marker not found.")

# 5. Add Modals for Funnel Drilldown and Exception Resolution
modals_code = """
  <!-- Modal: Funnel Stage Underlying Leads Drilldown -->
  <div class="modal fade" id="funnelLeadsModal" tabindex="-1">
    <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content border-0 shadow-lg">
        <div class="modal-header bg-dark text-white py-3">
          <div class="d-flex align-items-center gap-2">
            <i class="bi bi-funnel-fill text-danger fs-5"></i>
            <div>
              <h5 class="modal-title fw-bold mb-0" id="funnelModalTitle">Funnel Stage Underlying Leads</h5>
              <div class="small text-white-50">Empirical records from smb_leads.csv (DPDP PII Masked)</div>
            </div>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-4 bg-light">
          <div class="card p-0 border-0 shadow-sm overflow-hidden">
            <div class="table-responsive">
              <table class="table table-enterprise table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Lead ID</th>
                    <th>Business Name</th>
                    <th>Type</th>
                    <th>Segment</th>
                    <th>City / Tier</th>
                    <th>Stage Reached</th>
                    <th>Drop Reason / Outcome</th>
                    <th>Monthly Spend</th>
                  </tr>
                </thead>
                <tbody id="funnelLeadsTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="modal-footer bg-white border-top">
          <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: Resolve Operational Exception -->
  <div class="modal fade" id="resolveExceptionModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-success text-white py-2">
          <h6 class="modal-title fw-bold mb-0"><i class="bi bi-check-circle-fill me-2"></i>Resolve Operational Exception</h6>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-3">
          <input type="hidden" id="modalResolveExcId">
          <div class="mb-3">
            <label class="small text-muted fw-bold">EXCEPTION REFERENCE</label>
            <div id="modalResolveExcRef" class="fw-bold text-dark"></div>
          </div>
          <div class="mb-3">
            <label class="small text-muted fw-bold">RESOLUTION NOTES &amp; ACTIONS TAKEN</label>
            <textarea id="modalResolveNotes" class="form-control form-control-sm" rows="3" placeholder="Describe corrective action taken (e.g. Cleared FTTH port with fiber surveyor / Customer verified utility bill)..."></textarea>
          </div>
        </div>
        <div class="modal-footer py-2">
          <button type="button" class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-success btn-sm fw-bold" onclick="submitResolveException()">
            <i class="bi bi-check2 me-1"></i> Mark as Resolved
          </button>
        </div>
      </div>
    </div>
  </div>
"""

# Insert modals right before </body>
body_marker = '</body>'
if body_marker in html and 'id="funnelLeadsModal"' not in html:
    html = html.replace(body_marker, modals_code + '\n</body>', 1)
    print("5. Added Funnel Drilldown and Exception Resolution modals.")
else:
    print("5. Modals already added or body marker not found.")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved HTML with all UI components successfully.")

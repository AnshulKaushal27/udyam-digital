import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update showSection function to include 'funnel' and 'exceptions'
old_show_sec = """    function showSection(secId, el) {
      document.querySelectorAll(".sidebar-menu a").forEach(a => a.classList.remove("active"));
      if (el) el.classList.add("active");

      ['overview', 'quotes', 'recovery', 'orders', 'kyc', 'leads', 'partners', 'insights'].forEach(s => {
        const sec = document.getElementById("sec-" + s);
        if (sec) sec.style.display = (s === secId) ? "block" : "none";
      });

      if (secId === 'quotes') loadQuotesData();
      if (secId === 'recovery') loadRecoveryData();
    loadPartnerIntelligence();
      if (secId === 'orders') loadLiveOrders();
      if (secId === 'kyc') loadKycQueue();
      if (secId === 'leads') filterLeads();
      if (secId === 'partners') loadPartnerRescue();
      if (secId === 'insights') loadInsights();
    }"""

new_show_sec = """    function showSection(secId, el) {
      document.querySelectorAll(".sidebar-menu a").forEach(a => a.classList.remove("active"));
      if (el) el.classList.add("active");

      ['overview', 'funnel', 'exceptions', 'quotes', 'recovery', 'orders', 'kyc', 'leads', 'partners', 'insights'].forEach(s => {
        const sec = document.getElementById("sec-" + s);
        if (sec) sec.style.display = (s === secId) ? "block" : "none";
      });

      if (secId === 'overview') loadExecutiveOverview();
      if (secId === 'funnel') loadFunnelIntelligence();
      if (secId === 'exceptions') loadExceptionsQueue();
      if (secId === 'quotes') loadQuotesData();
      if (secId === 'recovery') loadRecoveryData();
      if (secId === 'orders') loadLiveOrders();
      if (secId === 'kyc') loadKycQueue();
      if (secId === 'leads') filterLeads();
      if (secId === 'partners') { loadPartnerIntelligence(); loadPartnerRescue(); }
      if (secId === 'insights') { loadInsights(); updateSimSliders(); runScenarioSimulation(); }
    }"""

if old_show_sec in html:
    html = html.replace(old_show_sec, new_show_sec, 1)
    print("1. Updated showSection function.")
else:
    print("1. showSection marker not found.")

# 2. Update changeRole function
old_change_role = """    function changeRole() {
      activeRole = document.getElementById("roleSelector").value;
      const names = {
        "super_admin": "Super Admin",
        "ops_manager": "Operations Manager",
        "kyc_officer": "KYC Officer",
        "sales_partner": "Channel Partner"
      };
      document.getElementById("userDisplayName").innerText = names[activeRole] || activeRole;
      loadLiveOrders();
      loadKycQueue();
    }"""

new_change_role = """    function changeRole() {
      activeRole = document.getElementById("roleSelector").value;
      const names = {
        "super_admin": "Super Admin",
        "ops_manager": "Operations Manager",
        "sales_executive": "Sales Executive",
        "kyc_officer": "KYC Officer",
        "sales_partner": "Channel Partner"
      };
      document.getElementById("userDisplayName").innerText = names[activeRole] || activeRole;
      loadExecutiveOverview();
      loadLiveOrders();
      loadKycQueue();
      loadExceptionsQueue();
    }"""

if old_change_role in html:
    html = html.replace(old_change_role, new_change_role, 1)
    print("2. Updated changeRole function.")
else:
    print("2. changeRole marker not found.")

# 3. Append the new Phase 6 JS functions right before </script>
new_js_code = """
    // =========================================================
    // PHASE 6: PREDICTIVE OPERATIONS & BI JAVASCRIPT FUNCTIONS
    // =========================================================

    function loadExecutiveOverview() {
      fetch(`/api/control/analytics/executive?role=${activeRole}`)
        .then(r => r.json())
        .then(res => {
          if (res.status === "success") {
            const grid = document.getElementById("executiveKpiGrid");
            if (!grid) return;
            grid.innerHTML = "";
            
            res.metrics.forEach(m => {
              const col = document.createElement("div");
              col.className = "col-lg-3 col-md-4 col-sm-6";
              
              let borderAccent = "border-primary";
              if (m.metric_id.includes("drop") || m.metric_id.includes("rejection") || m.metric_id.includes("breach")) {
                borderAccent = "border-danger";
              } else if (m.metric_id.includes("tat") || m.metric_id.includes("cac") || m.metric_id.includes("chase")) {
                borderAccent = "border-info";
              }
              
              col.innerHTML = `
                <div class="card-kpi p-3 h-100 border-start border-4 ${borderAccent} shadow-sm position-relative">
                  <div class="d-flex justify-content-between align-items-start mb-1">
                    <span class="text-muted small fw-bold text-uppercase" style="font-size: 0.72rem;">${m.label}</span>
                    <span class="badge bg-light text-dark border" style="font-size: 0.65rem;">${m.data_source === 'LIVE_PROTOTYPE_TRANSACTIONS' ? 'PROTOTYPE' : 'BASELINE'}</span>
                  </div>
                  <div class="fs-4 fw-bold text-dark mt-1">${m.prototype_value}</div>
                  <div class="d-flex justify-content-between align-items-center mt-2 small">
                    <span class="text-muted" style="font-size: 0.75rem;">Baseline: <strong>${m.historical_baseline}</strong></span>
                    <span class="badge bg-success-subtle text-success fw-bold" style="font-size: 0.7rem;">${m.change}</span>
                  </div>
                  <div class="mt-2 text-muted" style="font-size: 0.72rem; line-height: 1.3;">
                    <i class="bi bi-info-circle me-1"></i>${m.explanation}
                  </div>
                </div>
              `;
              grid.appendChild(col);
            });
          }
        })
        .catch(err => console.error("Error loading executive overview:", err));
    }

    function loadFunnelIntelligence() {
      const seg = document.getElementById("funnelSegmentFilter") ? document.getElementById("funnelSegmentFilter").value : "";
      const tier = document.getElementById("funnelTierFilter") ? document.getElementById("funnelTierFilter").value : "";
      const city = document.getElementById("funnelCitySearch") ? document.getElementById("funnelCitySearch").value : "";
      
      let url = `/api/control/analytics/funnel?role=${activeRole}`;
      if (seg) url += `&segment=${encodeURIComponent(seg)}`;
      if (tier) url += `&city_tier=${encodeURIComponent(tier)}`;
      if (city) url += `&city=${encodeURIComponent(city)}`;

      fetch(url)
        .then(r => r.json())
        .then(res => {
          const f = res.detailed_funnel;
          if (!f || f.status === "empty") return;

          if (document.getElementById("funnelSteepestBanner")) {
            document.getElementById("funnelSteepestBanner").innerText = f.steepest_bottleneck;
          }

          const container = document.getElementById("funnelStagesContainer");
          if (container) {
            container.innerHTML = "";
            f.stages.forEach(st => {
              const col = document.createElement("div");
              col.className = "col-lg-2 col-md-4 col-sm-6";
              
              let dropBadge = `<span class="badge bg-light text-muted border">No Drop</span>`;
              if (st.drop_off_count > 0) {
                dropBadge = `<span class="badge bg-danger-subtle text-danger fw-bold">-${st.drop_off_count} (${st.drop_off_pct}%)</span>`;
              }

              let stageCardClass = "card-kpi p-3 h-100 shadow-sm border-top border-4 ";
              if (st.stage_index === 4) stageCardClass += "border-danger bg-danger bg-opacity-10";
              else if (st.stage_index === 6) stageCardClass += "border-success bg-success bg-opacity-10";
              else stageCardClass += "border-primary";

              col.innerHTML = `
                <div class="${stageCardClass}">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="badge bg-dark" style="font-size: 0.65rem;">STAGE ${st.stage_index}</span>
                    ${dropBadge}
                  </div>
                  <h6 class="fw-bold text-dark mt-2 mb-1" style="font-size: 0.85rem;">${st.stage_name}</h6>
                  <div class="fs-4 fw-bold text-dark">${st.count.toLocaleString()}</div>
                  <div class="small text-muted mb-2" style="font-size: 0.72rem;">
                    Conv: <strong>${st.stage_conversion_pct}%</strong> | Net: <strong>${st.overall_conversion_pct}%</strong>
                  </div>
                  <div class="text-muted small mb-3" style="font-size: 0.7rem; min-height: 28px;">
                    <i class="bi bi-tag-fill me-1"></i>${st.loss_reason_sample}
                  </div>
                  <button class="btn btn-outline-dark btn-sm w-100 py-1" style="font-size: 0.75rem;" onclick="openFunnelStageLeads('${st.stage_key}', '${st.stage_name}')">
                    <i class="bi bi-search me-1"></i>Inspect Leads
                  </button>
                </div>
              `;
              container.appendChild(col);
            });
          }

          const segTbody = document.getElementById("funnelSegmentsTbody");
          if (segTbody && f.segments_analysis) {
            segTbody.innerHTML = "";
            f.segments_analysis.forEach(s => {
              const tr = document.createElement("tr");
              tr.innerHTML = `
                <td class="fw-bold">${s.segment}</td>
                <td>${s.total_leads.toLocaleString()}</td>
                <td>${s.needs_assessed.toLocaleString()}</td>
                <td>${s.quote_accepted.toLocaleString()}</td>
                <td class="fw-bold text-success">${s.activated.toLocaleString()}</td>
                <td><span class="badge ${s.conversion_pct >= 10 ? 'bg-success' : 'bg-primary'}">${s.conversion_pct}%</span></td>
              `;
              segTbody.appendChild(tr);
            });
          }

          const tierTbody = document.getElementById("funnelTiersTbody");
          if (tierTbody && f.city_tiers_analysis) {
            tierTbody.innerHTML = "";
            f.city_tiers_analysis.forEach(t => {
              const tr = document.createElement("tr");
              tr.innerHTML = `
                <td class="fw-bold">${t.tier}</td>
                <td>${t.total_leads.toLocaleString()}</td>
                <td class="fw-bold text-success">${t.activated.toLocaleString()}</td>
                <td><span class="badge bg-dark">${t.conversion_pct}%</span></td>
              `;
              tierTbody.appendChild(tr);
            });
          }
        })
        .catch(err => console.error("Error loading funnel intelligence:", err));
    }

    function openFunnelStageLeads(stageKey, stageName) {
      document.getElementById("funnelModalTitle").innerText = `Underlying Leads: ${stageName}`;
      const tbody = document.getElementById("funnelLeadsTbody");
      tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4"><div class="spinner-border text-danger spinner-border-sm me-2"></div>Loading lead records...</td></tr>`;
      
      const modal = new bootstrap.Modal(document.getElementById("funnelLeadsModal"));
      modal.show();

      fetch(`/api/control/analytics/funnel/leads?stage=${stageKey}&limit=50&role=${activeRole}`)
        .then(r => r.json())
        .then(res => {
          tbody.innerHTML = "";
          if (!res.leads || res.leads.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">No leads found in this stage.</td></tr>`;
            return;
          }
          res.leads.forEach(l => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td><span class="badge bg-secondary">${l.lead_id}</span></td>
              <td class="fw-semibold">${l.business_name}</td>
              <td class="small text-muted">${l.business_type}</td>
              <td><span class="badge bg-light text-dark border">${l.segment}</span></td>
              <td>${l.city} <small class="text-muted">(Tier ${l.city_tier})</small></td>
              <td><span class="badge bg-info text-dark">${l.stage_reached}</span></td>
              <td class="small text-danger">${l.drop_reason}</td>
              <td class="small fw-bold">₹${l.monthly_spend || '--'}</td>
            `;
            tbody.appendChild(tr);
          });
        })
        .catch(err => {
          tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">Error loading leads: ${err}</td></tr>`;
        });
    }

    let ALL_EXCEPTIONS = [];

    function loadExceptionsQueue() {
      fetch(`/api/control/exceptions/queue?role=${activeRole}`)
        .then(r => r.json())
        .then(res => {
          if (res.status === "success") {
            ALL_EXCEPTIONS = res.exceptions || [];
            document.getElementById("excCriticalCount").innerText = res.counts.critical;
            document.getElementById("excOpenCount").innerText = res.counts.open;
            document.getElementById("excAckCount").innerText = res.counts.acknowledged;
            document.getElementById("excResolvedCount").innerText = res.counts.resolved;
            document.getElementById("sideExceptionsCount").innerText = res.counts.open + res.counts.critical;

            renderExceptionsTable(ALL_EXCEPTIONS);
          }
        })
        .catch(err => console.error("Error loading exceptions:", err));
    }

    function renderExceptionsTable(list) {
      const tbody = document.getElementById("exceptionsTbody");
      if (!tbody) return;
      tbody.innerHTML = "";

      if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center py-4 text-muted"><i class="bi bi-check-circle-fill text-success fs-4 d-block mb-2"></i>No open exceptions. All workflows operating normally within SLA.</td></tr>`;
        return;
      }

      list.forEach(e => {
        const tr = document.createElement("tr");

        let pBadge = `<span class="badge bg-danger">CRITICAL</span>`;
        if (e.priority === "HIGH") pBadge = `<span class="badge bg-warning text-dark">HIGH</span>`;
        if (e.priority === "MEDIUM") pBadge = `<span class="badge bg-info text-dark">MEDIUM</span>`;

        let sBadge = `<span class="badge bg-warning text-dark">${e.status}</span>`;
        if (e.status === "ACKNOWLEDGED") sBadge = `<span class="badge bg-info text-dark">ACKNOWLEDGED</span>`;
        if (e.status === "RESOLVED") sBadge = `<span class="badge bg-success">RESOLVED</span>`;

        let actions = "";
        if (e.status !== "RESOLVED") {
          actions = `
            <div class="d-flex gap-1">
              ${e.status === 'OPEN' ? `<button class="btn btn-outline-primary btn-sm py-0" style="font-size: 0.75rem;" onclick="actionException('${e.exception_id}', 'acknowledge')"><i class="bi bi-check me-1"></i>Ack</button>` : ''}
              <button class="btn btn-success btn-sm py-0" style="font-size: 0.75rem;" onclick="openResolveModal('${e.exception_id}', '${e.customer_name} (${e.reference_id})')"><i class="bi bi-check-all me-1"></i>Resolve</button>
            </div>
          `;
        } else {
          actions = `<span class="text-muted small"><i class="bi bi-check-circle text-success me-1"></i>Closed</span>`;
        }

        tr.innerHTML = `
          <td>${pBadge}</td>
          <td>
            <span class="badge bg-light text-dark border">${e.type}</span>
            <div class="text-muted" style="font-size: 0.7rem;">${e.source_module}</div>
          </td>
          <td>
            <strong class="d-block text-dark small">${e.customer_name}</strong>
            <span class="text-muted" style="font-size: 0.72rem;">Ref: ${e.reference_id}</span>
          </td>
          <td class="small text-muted">${e.city}</td>
          <td class="small text-dark" style="max-width: 260px;">${e.reason}</td>
          <td class="small text-muted">${e.time_outstanding}</td>
          <td class="small fw-semibold text-secondary">${e.assigned_owner}</td>
          <td>${sBadge}</td>
          <td>${actions}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterExceptionsTable(filterType, btn) {
      if (btn) {
        btn.parentElement.querySelectorAll("button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
      }
      let filtered = ALL_EXCEPTIONS;
      if (filterType === "CRITICAL") filtered = ALL_EXCEPTIONS.filter(e => e.priority === "CRITICAL");
      if (filterType === "OPEN") filtered = ALL_EXCEPTIONS.filter(e => e.status === "OPEN");
      if (filterType === "RESOLVED") filtered = ALL_EXCEPTIONS.filter(e => e.status === "RESOLVED");

      document.getElementById("exceptionsTableCount").innerText = `Showing ${filtered.length} of ${ALL_EXCEPTIONS.length} exceptions`;
      renderExceptionsTable(filtered);
    }

    function actionException(excId, action, notes) {
      fetch(`/api/control/exceptions/${excId}/action?role=${activeRole}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({action: action, notes: notes || "Acknowledged by operations staff."})
      })
      .then(r => r.json())
      .then(res => {
        if (res.status === "success") {
          loadExceptionsQueue();
        }
      });
    }

    function openResolveModal(excId, refName) {
      document.getElementById("modalResolveExcId").value = excId;
      document.getElementById("modalResolveExcRef").innerText = refName;
      document.getElementById("modalResolveNotes").value = "";
      const modal = new bootstrap.Modal(document.getElementById("resolveExceptionModal"));
      modal.show();
    }

    function submitResolveException() {
      const excId = document.getElementById("modalResolveExcId").value;
      const notes = document.getElementById("modalResolveNotes").value;
      actionException(excId, "resolve", notes);
      bootstrap.Modal.getInstance(document.getElementById("resolveExceptionModal")).hide();
    }

    function updateSimSliders() {
      if (!document.getElementById("simQuoteAcceptance")) return;
      document.getElementById("sliderQuoteVal").innerText = document.getElementById("simQuoteAcceptance").value + "%";
      document.getElementById("sliderKycVal").innerText = document.getElementById("simKycCompletion").value + "%";
      document.getElementById("sliderActVal").innerText = document.getElementById("simActivation").value + "%";
      document.getElementById("sliderRecVal").innerText = document.getElementById("simLeadRecovery").value + "%";
      document.getElementById("sliderCacVal").innerText = "₹" + parseInt(document.getElementById("simCacSpend").value).toLocaleString();
    }

    function runScenarioSimulation() {
      if (!document.getElementById("simQuoteAcceptance")) return;
      const quote_acc = parseFloat(document.getElementById("simQuoteAcceptance").value);
      const kyc_comp = parseFloat(document.getElementById("simKycCompletion").value);
      const act_conv = parseFloat(document.getElementById("simActivation").value);
      const rec_rate = parseFloat(document.getElementById("simLeadRecovery").value);
      const cac_val = parseFloat(document.getElementById("simCacSpend").value);

      fetch(`/api/control/analytics/simulate?role=${activeRole}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          quote_acceptance_pct: quote_acc,
          kyc_completion_pct: kyc_comp,
          activation_pct: act_conv,
          lead_recovery_pct: rec_rate,
          cac_spend_inr: cac_val
        })
      })
      .then(r => r.json())
      .then(res => {
        if (res.status === "success") {
          const f = res.funnel_projections;
          const fin = res.financial_impact;

          document.getElementById("simProjectedActivations").innerText = f.projected_activations.toLocaleString();
          document.getElementById("simActivationsLift").innerHTML = `Lift: <strong>+${f.incremental_activations}</strong> (+${f.activation_lift_pct}%)`;

          document.getElementById("simIncrementalArr").innerText = "₹" + (fin.incremental_annual_revenue_inr / 100000).toFixed(2) + " Lakh";
          document.getElementById("simMonthlyRevenue").innerText = `Total ARR: ₹${(fin.projected_annual_recurring_revenue_inr / 100000).toFixed(2)} Lakh`;

          document.getElementById("simAcquisitionSpend").innerText = "₹" + (fin.total_acquisition_spend_inr / 100000).toFixed(2) + " Lakh";
          document.getElementById("simPaybackMonths").innerText = fin.cac_payback_period_months + " Months";
        }
      })
      .catch(err => console.error("Error running simulation:", err));
    }
    
    // Auto-load executive overview on page ready
    window.addEventListener("DOMContentLoaded", () => {
      loadExecutiveOverview();
    });
"""

script_end_marker = '  </script>'
if script_end_marker in html and 'loadExecutiveOverview' not in html:
    html = html.replace(script_end_marker, new_js_code + '\n  </script>', 1)
    print("3. Appended Phase 6 JS functions before </script>.")
else:
    print("3. Script end marker not found or already inserted.")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved HTML with all Phase 6 JavaScript functions.")

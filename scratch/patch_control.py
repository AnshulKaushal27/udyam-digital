with open(r"E:\Airtel\prototype\templates\control.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Dimension 2 Banner Target Text
old_d2 = 'SYNC 2026 Directives (25.0% Conv, ≤3.0d TAT, ≤₹7,500 CAC)'
new_d2 = 'Prompt.txt Master Directives (22.0% Conv, ≤3.5d TAT, ≤₹3,800 CAC, <0.2 Calls)'
assert old_d2 in content, f"old_d2 not found"
content = content.replace(old_d2, new_d2, 1)

# 2. Sliders
old_sl1 = '<span>Phase 3 Pilot: 28.5%</span>'
new_sl1 = '<span>Phase 3 Target Assumption: 25.0%</span>'
assert old_sl1 in content, "old_sl1 not found"
content = content.replace(old_sl1, new_sl1, 1)

old_sl2 = '<span>Target: ₹7,500</span>'
new_sl2 = '<span>Target: ₹3,800</span>'
assert old_sl2 in content, "old_sl2 not found"
content = content.replace(old_sl2, new_sl2, 1)

# 3. loadExecutiveOverview function
old_exec_func = """    function loadExecutiveOverview() {
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
    }"""

new_exec_func = """    function loadExecutiveOverview() {
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
              
              // Source badge styling
              let sourceBadgeClass = "bg-primary-subtle text-primary border border-primary-subtle";
              let sourceBadgeText = "LIVE PROTOTYPE";
              if (m.status === "unavailable") {
                sourceBadgeClass = "bg-secondary-subtle text-secondary border border-secondary-subtle";
                sourceBadgeText = "UNAVAILABLE";
              } else if (m.data_source === "HISTORICAL_BASELINE_DATASET") {
                sourceBadgeClass = "bg-dark text-white";
                sourceBadgeText = "HISTORICAL";
              } else if (m.is_demo_included) {
                sourceBadgeClass = "bg-info-subtle text-info-emphasis border border-info-subtle";
                sourceBadgeText = "PROTOTYPE (DEMO INCL)";
              }

              // Value rendering (Muted italic icon when unavailable)
              let valueHtml = `<div class="fs-4 fw-bold text-dark mt-1">${m.prototype_value}</div>`;
              if (m.status === "unavailable") {
                valueHtml = `<div class="fs-6 fw-semibold text-muted mt-2 mb-2"><i class="bi bi-dash-circle me-1 text-secondary"></i>${m.prototype_value}</div>`;
              }

              // Delta badge: only render when comparison is genuinely available
              let changeBadgeHtml = "";
              if (m.comparison_available && m.change && m.change !== "No comparison available") {
                const badgeColor = m.trend === "positive" ? "bg-success-subtle text-success" : (m.trend === "negative" ? "bg-danger-subtle text-danger" : "bg-light text-secondary border");
                changeBadgeHtml = `<span class="badge ${badgeColor} fw-bold" style="font-size: 0.68rem;">${m.change}</span>`;
              } else {
                changeBadgeHtml = `<span class="badge bg-light text-muted border" style="font-size: 0.65rem;">No delta</span>`;
              }
              
              col.innerHTML = `
                <div class="card-kpi p-3 h-100 border-start border-4 ${borderAccent} shadow-sm position-relative d-flex flex-column justify-content-between">
                  <div>
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <span class="text-muted small fw-bold text-uppercase" style="font-size: 0.72rem;">${m.label}</span>
                      <span class="badge ${sourceBadgeClass}" style="font-size: 0.63rem;">${sourceBadgeText}</span>
                    </div>
                    ${valueHtml}
                    <div class="d-flex justify-content-between align-items-center mt-2 small">
                      <span class="text-muted" style="font-size: 0.73rem;">Baseline: <strong>${m.historical_baseline}</strong></span>
                      ${changeBadgeHtml}
                    </div>
                    <div class="small text-muted mt-1" style="font-size: 0.72rem;">
                      Target: <strong>${m.target_value}</strong>
                    </div>
                  </div>
                  <div class="mt-2 pt-2 border-top">
                    <div class="text-muted" style="font-size: 0.7rem; line-height: 1.3;">
                      <i class="bi bi-info-circle me-1"></i>${m.explanation}
                    </div>
                    <div class="text-muted opacity-75 mt-1" style="font-size: 0.65rem; font-family: monospace;">
                      Formula: ${m.formula || 'N/A'}
                    </div>
                    <div class="text-muted opacity-75 mt-0" style="font-size: 0.65rem;">
                      Source: ${m.data_source} · ${m.period || 'Current Runtime'}
                    </div>
                  </div>
                </div>
              `;
              grid.appendChild(col);
            });
          }
        })
        .catch(err => console.error("Error loading executive overview:", err));
    }"""

assert old_exec_func in content, "old_exec_func not found"
content = content.replace(old_exec_func, new_exec_func, 1)

# 4. loadInsights function
old_insights_func = """    // 5. Business Insights
    function loadInsights() {
      fetch("/api/control/analytics/insights")
      .then(r => r.json())
      .then(data => {
        const box = document.getElementById("insightsContainer");
        box.innerHTML = "";
        data.insights.forEach(i => {
          const col = document.createElement("div");
          col.className = "col-md-6";
          col.innerHTML = `
            <div class="card-kpi p-4 h-100 border-start border-4 border-danger">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-danger">${i.category}</span>
                <span class="small fw-bold text-dark">${i.stat}</span>
              </div>
              <h5 class="fw-bold text-dark mb-2">${i.title}</h5>
              <p class="small text-muted mb-3">${i.evidence}</p>
              <div class="p-2 bg-light rounded small border">
                <strong>Strategic Recommendation:</strong> ${i.recommendation}
              </div>
            </div>
          `;
          box.appendChild(col);
        });
      });
    }"""

new_insights_func = """    // 5. Business Insights (Deterministic Rule-Based Intelligence)
    function loadInsights() {
      fetch("/api/control/analytics/insights")
      .then(r => r.json())
      .then(data => {
        const box = document.getElementById("insightsContainer");
        if (!box) return;
        box.innerHTML = "";
        data.insights.forEach(i => {
          const col = document.createElement("div");
          col.className = "col-md-6";
          
          const hypoBadge = i.is_hypothesis ? 
            `<span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle" style="font-size: 0.68rem;"><i class="bi bi-lightbulb me-1"></i>Informed Hypothesis</span>` : 
            `<span class="badge bg-success-subtle text-success border border-success-subtle" style="font-size: 0.68rem;"><i class="bi bi-check-circle me-1"></i>Verified Finding</span>`;

          col.innerHTML = `
            <div class="card-kpi p-4 h-100 border-start border-4 border-danger d-flex flex-column justify-content-between shadow-sm">
              <div>
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="badge bg-danger">${i.category}</span>
                  ${hypoBadge}
                </div>
                <h5 class="fw-bold text-dark mb-2">${i.title}</h5>
                <div class="small text-dark mb-2"><strong>Observation:</strong> ${i.observation}</div>
                <div class="p-2 bg-light rounded small border mb-3">
                  <strong>Supporting Data:</strong> ${i.evidence || i.supporting_data}
                  <div class="text-muted mt-1" style="font-size: 0.7rem;"><i class="bi bi-database me-1"></i>Source: ${i.traceable_source || 'smb_leads.csv'}</div>
                </div>
                <div class="small text-muted mb-3">
                  <strong>Business Implication:</strong> ${i.business_implication}
                </div>
              </div>
              <div class="p-2 bg-white rounded small border-start border-3 border-danger shadow-sm">
                <strong>Recommended Action:</strong> ${i.recommendation}
              </div>
            </div>
          `;
          box.appendChild(col);
        });
      });
    }"""

assert old_insights_func in content, "old_insights_func not found"
content = content.replace(old_insights_func, new_insights_func, 1)

with open(r"E:\Airtel\prototype\templates\control.html", "w", encoding="utf-8") as f:
    f.write(content)

print("control.html successfully patched.")

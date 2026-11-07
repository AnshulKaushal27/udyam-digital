import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """          tr.innerHTML = `
            <td><strong class="font-monospace text-danger">${o.order_id}</strong></td>
            <td><strong>${o.business_name}</strong><br><small class="text-muted">${o.contact_name}</small></td>
            <td>${o.city}</td>
            <td>${o.bundle_name}</td>
            <td><strong>₹${o.total_monthly.toLocaleString()}</strong>/mo</td>
            <td>${kycBadge}</td>
            <td><span class="badge bg-light text-dark border">${o.installation.status_text}</span></td>
            <td><small>${engName}</small></td>
            <td>${actionBtn}</td>
          `;"""

replacement = """          const risk = o.installation.risk_assessment || {risk_level: "LOW_RISK", risk_score: 15, hours_remaining: 36};
          let riskBadge = `<span class="badge bg-success" style="font-size: 0.72rem;"><i class="bi bi-shield-check me-1"></i>LOW RISK (${risk.risk_score})</span>`;
          if (risk.risk_level === "MEDIUM_RISK") {
            riskBadge = `<span class="badge bg-warning text-dark" style="font-size: 0.72rem;"><i class="bi bi-exclamation-circle me-1"></i>MED RISK (${risk.risk_score})</span>`;
          } else if (risk.risk_level === "HIGH_RISK") {
            riskBadge = `<span class="badge bg-danger" style="font-size: 0.72rem;"><i class="bi bi-exclamation-triangle-fill me-1"></i>HIGH RISK (${risk.risk_score})</span>`;
          } else if (risk.risk_level === "SLA_BREACHED") {
            riskBadge = `<span class="badge bg-danger text-uppercase fw-bold" style="font-size: 0.72rem;"><i class="bi bi-x-circle-fill me-1"></i>SLA BREACHED</span>`;
          }

          tr.innerHTML = `
            <td><strong class="font-monospace text-danger">${o.order_id}</strong></td>
            <td><strong>${o.business_name}</strong><br><small class="text-muted">${o.contact_name}</small></td>
            <td>${o.city}</td>
            <td>${o.bundle_name}</td>
            <td><strong>₹${o.total_monthly.toLocaleString()}</strong>/mo</td>
            <td>${kycBadge}</td>
            <td><span class="badge bg-light text-dark border">${o.installation.status_text}</span></td>
            <td><small>${engName}</small></td>
            <td>
              ${riskBadge}
              <div class="text-muted" style="font-size: 0.7rem;">SLA: ${o.installation.sla_days || 3}d</div>
            </td>
            <td>${actionBtn}</td>
          `;"""

if target in html:
    html = html.replace(target, replacement, 1)
    print("Updated loadLiveOrders() row rendering successfully.")
else:
    print("Target row rendering not found.")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)

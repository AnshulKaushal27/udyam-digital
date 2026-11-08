with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = "['overview', 'orders', 'kyc', 'leads', 'partners', 'insights']"
replacement = "['overview', 'quotes', 'orders', 'kyc', 'leads', 'partners', 'insights']"
c = c.replace(target, replacement)

target2 = "if (secId === 'orders') loadLiveOrders();"
replacement2 = "if (secId === 'quotes') loadQuotesData();\n      if (secId === 'orders') loadLiveOrders();"
c = c.replace(target2, replacement2, 1)

load_quotes_func = '''
    function loadQuotesData() {
      fetch("/api/control/quotes/analytics")
        .then(r => r.json())
        .then(res => {
          if (res.status === "success") {
            document.getElementById("kpiTotalQuotes").innerText = res.total_quotes;
            document.getElementById("kpiConversionRate").innerText = res.funnel.conversion_rate_pct + "%";
            document.getElementById("kpiModifiedQuotes").innerText = res.funnel.modified;
            document.getElementById("kpiRejectionRate").innerText = res.funnel.rejection_rate_pct + "%";

            document.getElementById("funnelGenerated").innerText = res.funnel.generated;
            document.getElementById("funnelViewed").innerText = res.funnel.viewed;
            document.getElementById("funnelModified").innerText = res.funnel.modified;
            document.getElementById("funnelAccepted").innerText = res.funnel.accepted;
            document.getElementById("funnelOrders").innerText = res.funnel.orders;

            const rBox = document.getElementById("rejectionReasonsList");
            rBox.innerHTML = "";
            const reasons = Object.entries(res.rejection_reasons || {});
            if (reasons.length === 0) {
              rBox.innerHTML = `<span class="text-muted small">No rejections recorded. High acceptance rate!</span>`;
            } else {
              reasons.forEach(([reason, count]) => {
                const row = document.createElement("div");
                row.className = "d-flex justify-content-between align-items-center mb-1 pb-1 border-bottom";
                const cleanName = reason.replace(/_/g, " ").replace(/\\b\\w/g, l => l.toUpperCase());
                row.innerHTML = `<span class="text-dark">${cleanName}</span><span class="badge bg-danger-subtle text-danger">${count}</span>`;
                rBox.appendChild(row);
              });
            }
          }
        });

      fetch("/api/control/quotes")
        .then(r => r.json())
        .then(res => {
          if (res.status === "success") {
            const sideCount = document.getElementById("sideQuotesCount");
            if (sideCount) sideCount.innerText = res.count;

            const tbody = document.getElementById("controlQuotesTableBody");
            tbody.innerHTML = "";
            res.quotes.forEach(q => {
              const tr = document.createElement("tr");
              const p = q.pricing || {};
              const sub = p.monthly_subtotal_inr || q.monthly_base_inr || 0;
              const gst = p.gst_18_inr || Math.round(sub * 0.18);
              const total = p.final_monthly_payable_inr || (sub + gst);
              const setup = p.one_time_setup_inr || 0;

              let badgeClass = "bg-secondary";
              if (q.status === "accepted") badgeClass = "bg-success";
              else if (q.status === "rejected") badgeClass = "bg-danger";
              else if (q.status === "modified") badgeClass = "bg-info text-dark";
              else if (q.status === "viewed") badgeClass = "bg-primary";

              tr.innerHTML = `
                <td><strong class="font-monospace text-dark">${q.quote_id}</strong></td>
                <td><span class="text-muted small">${q.session_id || 'Self-Serve'}</span></td>
                <td><strong>${q.bundle_name}</strong><br><small class="text-muted">${q.addons && q.addons.length ? '+' + q.addons.length + ' add-on(s)' : 'Base only'}</small></td>
                <td class="fw-bold">₹${sub.toLocaleString()}</td>
                <td class="text-muted">₹${gst.toLocaleString()}</td>
                <td class="fw-bold text-danger">₹${total.toLocaleString()}/mo</td>
                <td>₹${setup.toLocaleString()}</td>
                <td><span class="badge ${badgeClass} text-uppercase">${q.status}</span></td>
                <td><span class="small text-muted">${q.created_at || 'Recently'}</span></td>
                <td class="text-end">
                  <button class="btn btn-sm btn-outline-dark py-0 px-2" onclick="alert('Quote Ref: ' + '${q.quote_id}' + '\\\\nBundle: ' + '${q.bundle_name}' + '\\\\nMonthly: ₹' + '${total}' + '\\\\nStatus: ' + '${q.status}')">
                    Inspect
                  </button>
                </td>
              `;
              tbody.appendChild(tr);
            });
          }
        });
    }
'''

target3 = "function changeRole() {"
c = c.replace(target3, load_quotes_func + "\n    function changeRole() {", 1)

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated control.html showSection & loadQuotesData successfully!")

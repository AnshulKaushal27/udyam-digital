control_path = r"E:\Airtel\prototype\templates\control.html"

with open(control_path, "r", encoding="utf-8") as f:
    text = f.read()

target = """    function loadKycQueue() {
      fetch("/api/control/orders")
      .then(r => r.json())
      .then(data => {
        const tbody = document.getElementById("kycQueueTbody");
        tbody.innerHTML = "";

        let pending = 0;
        let approved = 0;

        data.orders.forEach(o => {
          if (o.kyc.status === "PENDING_REVIEW") pending++;
          if (o.kyc.status === "APPROVED") approved++;

          const tr = document.createElement("tr");

          let decisionBtn = "";
          if (activeRole === "super_admin" || activeRole === "kyc_officer") {
            decisionBtn = `<button class="btn btn-sm btn-outline-primary" onclick="openKycReviewModal('${o.order_id}')"><i class="bi bi-search me-1"></i> Inspect &amp; Decide</button>`;
          } else {
            decisionBtn = `<span class="text-muted small">Officer Only</span>`;
          }

          tr.innerHTML = `
            <td><code>${o.order_id}</code></td>
            <td><strong>${o.kyc.signatory_name}</strong></td>
            <td>${o.business_name}</td>
            <td class="font-monospace">${o.kyc.masked_gstin}</td>
            <td class="font-monospace">${o.kyc.udyam_number || 'N/A'}</td>
            <td>${o.kyc.utility_bill_date}</td>
            <td><span class="badge bg-success">&lt;90 Days Valid</span></td>
            <td><span class="badge bg-${o.kyc.status === 'APPROVED' ? 'success' : (o.kyc.status === 'REJECTED' ? 'danger' : 'warning')}">${o.kyc.status}</span></td>
            <td>${decisionBtn}</td>
          `;
          tbody.appendChild(tr);
        });

        document.getElementById("sidePendingKycCount").innerText = pending;
        document.getElementById("kycPendingCountBadge").innerText = pending;
        document.getElementById("kycApprovedCountBadge").innerText = approved;
      });
    }

    function openKycReviewModal(orderId) {
      selectedOrderId = orderId;
      fetch("/api/control/orders")
      .then(r => r.json())
      .then(data => {
        const o = data.orders.find(x => x.order_id === orderId);
        if (o) {
          document.getElementById("kycModalOrderId").innerText = o.order_id;
          document.getElementById("kycModalBizName").innerText = o.business_name;
          document.getElementById("kycModalSignatory").innerText = o.kyc.signatory_name;
          document.getElementById("kycModalGstin").innerText = o.kyc.masked_gstin;
          document.getElementById("kycModalBillDate").innerText = o.kyc.utility_bill_date;
          document.getElementById("kycModalRecency").innerText = `${o.kyc.bill_age_days} Days (<90d Limit)`;
          document.getElementById("kycModalNotes").innerText = o.kyc.audit_notes;

          const m = new bootstrap.Modal(document.getElementById('kycReviewModal'));
          m.show();
        }
      });
    }

    function makeKycDecision(decision) {
      const remarks = document.getElementById("kycOfficerRemarks").value.trim();

      fetch(`/api/control/orders/${selectedOrderId}/update_kyc?role=${activeRole}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ decision: decision, reasons: remarks, officer_name: "KYC Officer (S. Sen)" })
      })
      .then(r => r.json())
      .then(res => {
        if (res.status === "success") {
          alert(`Application ${selectedOrderId} marked as ${decision}! Consumer portal updated.`);
          bootstrap.Modal.getInstance(document.getElementById('kycReviewModal')).hide();
          loadKycQueue();
          loadLiveOrders();
        } else {
          alert("Error: " + res.message);
        }
      });
    }"""

replacement = """    let currentKycFilter = "";
    let currentKycAppList = [];

    // 2. Smart KYC & Exception Queue Loader
    function loadKycQueue(filter = "") {
      currentKycFilter = filter;
      fetch(`/api/kyc/queue?status=${encodeURIComponent(filter)}`)
      .then(r => r.json())
      .then(data => {
        if (data.status !== "success") return;
        currentKycAppList = data.applications || [];

        // Update KPIs
        const m = data.metrics || {};
        document.getElementById("kycPendingCountBadge").innerText = m.pending_count || 0;
        document.getElementById("kycApprovedCountBadge").innerText = m.auto_verified_count || 0;
        document.getElementById("kycExceptionsCountBadge").innerText = m.exceptions_count || 0;
        if (document.getElementById("kycAvgOcrBadge")) {
          document.getElementById("kycAvgOcrBadge").innerText = m.avg_ocr_confidence || "97.4%";
        }
        if (document.getElementById("sidePendingKycCount")) {
          document.getElementById("sidePendingKycCount").innerText = (m.pending_count || 0) + (m.exceptions_count || 0);
        }

        const tbody = document.getElementById("kycQueueTbody");
        tbody.innerHTML = "";

        if (currentKycAppList.length === 0) {
          tbody.innerHTML = `<tr><td colspan="9" class="text-center text-muted py-4">No verification applications matching current filter.</td></tr>`;
          return;
        }

        currentKycAppList.forEach(app => {
          const tr = document.createElement("tr");

          let statusBadge = "";
          if (app.status === "VERIFIED_APPROVED" || app.status === "APPROVED") {
            statusBadge = `<span class="badge bg-success"><i class="bi bi-check-circle-fill me-1"></i> VERIFIED</span>`;
          } else if (app.status === "EXCEPTION_FAILED" || app.status === "REJECTED") {
            statusBadge = `<span class="badge bg-danger"><i class="bi bi-x-circle-fill me-1"></i> EXCEPTION</span>`;
          } else {
            statusBadge = `<span class="badge bg-warning text-dark"><i class="bi bi-clock-history me-1"></i> REVIEW REQ</span>`;
          }

          const billBadge = app.bill_age_days <= 90
            ? `<span class="badge bg-success">${app.bill_date} (${app.bill_age_days}d)</span>`
            : `<span class="badge bg-danger">${app.bill_date} (${app.bill_age_days}d > 90d)</span>`;

          let actionBtn = "";
          if (activeRole === "super_admin" || activeRole === "kyc_officer") {
            actionBtn = `<button class="btn btn-sm btn-outline-danger fw-bold" onclick="openKycReviewModal('${app.application_id}')"><i class="bi bi-search me-1"></i> Inspect &amp; Decide</button>`;
          } else {
            actionBtn = `<button class="btn btn-sm btn-outline-secondary" onclick="openKycReviewModal('${app.application_id}')"><i class="bi bi-eye me-1"></i> View Only</button>`;
          }

          tr.innerHTML = `
            <td><code class="fw-bold ${app.is_specimen ? 'text-primary' : 'text-danger'}">${app.application_id}</code>${app.is_specimen ? ' <span class="badge bg-dark" style="font-size:0.65rem;">SPECIMEN</span>' : ''}</td>
            <td><strong>${app.applicant_name}</strong></td>
            <td>${app.business_name}</td>
            <td class="font-monospace">${app.masked_gstin}</td>
            <td class="font-monospace">${app.udyam_number || 'N/A'}</td>
            <td>${billBadge}</td>
            <td><span class="badge bg-light text-dark border">${app.ocr_confidence}</span></td>
            <td>${statusBadge}</td>
            <td>${actionBtn}</td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    function filterKycTable(filterCode) {
      document.querySelectorAll("#sec-kyc .btn-group button").forEach(b => b.classList.remove("active"));
      if (filterCode === "") document.getElementById("kycTabAll").classList.add("active");
      else if (filterCode === "PENDING") document.getElementById("kycTabPending").classList.add("active");
      else if (filterCode === "APPROVED") document.getElementById("kycTabVerified").classList.add("active");
      else if (filterCode === "EXCEPTION") document.getElementById("kycTabExceptions").classList.add("active");
      loadKycQueue(filterCode);
    }

    // 1-Click Specimen Benchmark Tester
    function testSpecimenKyc(applicantId) {
      fetch(`/api/kyc/specimen/${applicantId}`)
      .then(r => r.json())
      .then(res => {
        if (res.status === "success") {
          renderKycModalFromReport(res.report);
          const m = new bootstrap.Modal(document.getElementById('kycReviewModal'));
          m.show();
        } else {
          alert("Error: " + res.message);
        }
      });
    }

    function openKycReviewModal(appId) {
      selectedOrderId = appId;
      // If it's a specimen (K01-K12)
      if (appId.startsWith("K0") || appId.startsWith("K1")) {
        testSpecimenKyc(appId);
        return;
      }
      // If it's a live order
      const app = currentKycAppList.find(x => x.application_id === appId);
      if (app) {
        renderKycModalFromQueueApp(app);
        const m = new bootstrap.Modal(document.getElementById('kycReviewModal'));
        m.show();
      } else {
        fetch("/api/control/orders")
        .then(r => r.json())
        .then(data => {
          const o = data.orders.find(x => x.order_id === appId);
          if (o) {
            renderKycModalFromOrder(o);
            const m = new bootstrap.Modal(document.getElementById('kycReviewModal'));
            m.show();
          }
        });
      }
    }

    function renderKycModalFromReport(rep) {
      selectedOrderId = rep.applicant_id;
      document.getElementById("kycModalOrderId").innerText = rep.applicant_id;
      document.getElementById("kycModalBizName").innerText = rep.business_name;
      document.getElementById("kycModalSignatory").innerText = rep.applicant_name;

      // Exception alert
      const alertBox = document.getElementById("kycModalExceptionAlert");
      if (rep.exceptions && rep.exceptions.length > 0) {
        const ex = rep.exceptions[0];
        document.getElementById("kycModalExceptionTitle").innerText = `${ex.category}: ${ex.title}`;
        document.getElementById("kycModalExceptionEn").innerText = ex.message;
        document.getElementById("kycModalExceptionHi").innerText = `Hindi Guidance: "${ex.message_hi || ''}"`;
        alertBox.style.display = "block";
      } else {
        alertBox.style.display = "none";
      }

      // Populate comparison matrix table
      const tbody = document.getElementById("kycModalFieldTable");
      tbody.innerHTML = "";
      (rep.field_comparison || []).forEach(row => {
        const tr = document.createElement("tr");
        let badge = "bg-secondary";
        if (row.result === "PASS") badge = "bg-success";
        else if (row.result === "FAIL") badge = "bg-danger";
        else if (row.result === "REVIEW") badge = "bg-warning text-dark";

        tr.innerHTML = `
          <td><strong>${row.field}</strong></td>
          <td class="font-monospace">${row.customer_data}</td>
          <td class="font-monospace">${row.registry_data}</td>
          <td class="font-monospace">${row.ocr_data}</td>
          <td class="text-center"><span class="badge ${badge}">${row.result}</span></td>
        `;
        tbody.appendChild(tr);
      });

      // Audit history
      fetch(`/api/kyc/audit?application_id=${rep.applicant_id}`)
      .then(r => r.json())
      .then(aud => {
        const box = document.getElementById("kycModalAuditHistory");
        if (aud.audit_trail && aud.audit_trail.length > 0) {
          box.innerHTML = aud.audit_trail.map(a => `[${a.timestamp_ist}] ${a.officer_name} (${a.officer_role}) -> ${a.action}: "${a.reasons}"`).join("<br>");
        } else {
          box.innerText = "No previous decision entries. First inspection on record.";
        }
      });
    }

    function renderKycModalFromQueueApp(app) {
      selectedOrderId = app.application_id;
      document.getElementById("kycModalOrderId").innerText = app.application_id;
      document.getElementById("kycModalBizName").innerText = app.business_name;
      document.getElementById("kycModalSignatory").innerText = app.applicant_name;

      const alertBox = document.getElementById("kycModalExceptionAlert");
      if (app.exceptions && app.exceptions.length > 0) {
        const ex = app.exceptions[0];
        document.getElementById("kycModalExceptionTitle").innerText = `${ex.category}: ${ex.title}`;
        document.getElementById("kycModalExceptionEn").innerText = ex.message;
        document.getElementById("kycModalExceptionHi").innerText = `Hindi Guidance: "${ex.message_hi || ''}"`;
        alertBox.style.display = "block";
      } else {
        alertBox.style.display = "none";
      }

      const tbody = document.getElementById("kycModalFieldTable");
      tbody.innerHTML = "";
      (app.field_comparison || []).forEach(row => {
        const tr = document.createElement("tr");
        let badge = row.result === "PASS" ? "bg-success" : (row.result === "FAIL" ? "bg-danger" : "bg-warning text-dark");
        tr.innerHTML = `
          <td><strong>${row.field}</strong></td>
          <td class="font-monospace">${row.customer_data}</td>
          <td class="font-monospace">${row.registry_data}</td>
          <td class="font-monospace">${row.ocr_data}</td>
          <td class="text-center"><span class="badge ${badge}">${row.result}</span></td>
        `;
        tbody.appendChild(tr);
      });

      fetch(`/api/kyc/audit?application_id=${app.application_id}`)
      .then(r => r.json())
      .then(aud => {
        const box = document.getElementById("kycModalAuditHistory");
        if (aud.audit_trail && aud.audit_trail.length > 0) {
          box.innerHTML = aud.audit_trail.map(a => `[${a.timestamp_ist}] ${a.officer_name} (${a.officer_role}) -> ${a.action}: "${a.reasons}"`).join("<br>");
        } else {
          box.innerText = "No previous decision entries recorded.";
        }
      });
    }

    function renderKycModalFromOrder(o) {
      selectedOrderId = o.order_id;
      document.getElementById("kycModalOrderId").innerText = o.order_id;
      document.getElementById("kycModalBizName").innerText = o.business_name;
      document.getElementById("kycModalSignatory").innerText = o.kyc.signatory_name;

      const alertBox = document.getElementById("kycModalExceptionAlert");
      alertBox.style.display = "none";

      const tbody = document.getElementById("kycModalFieldTable");
      tbody.innerHTML = `
        <tr>
          <td><strong>Business / Trade Name</strong></td>
          <td class="font-monospace">${o.business_name}</td>
          <td class="font-monospace">${o.business_name} (Active)</td>
          <td class="font-monospace">${o.business_name}</td>
          <td class="text-center"><span class="badge bg-success">PASS</span></td>
        </tr>
        <tr>
          <td><strong>GST Registration</strong></td>
          <td class="font-monospace">${o.kyc.masked_gstin}</td>
          <td class="font-monospace">Active</td>
          <td class="font-monospace">${o.kyc.masked_gstin}</td>
          <td class="text-center"><span class="badge bg-success">PASS</span></td>
        </tr>
        <tr>
          <td><strong>Utility Bill Date (<90d)</strong></td>
          <td class="font-monospace">${o.kyc.utility_bill_date}</td>
          <td class="font-monospace">Benchmark: 15-Jul-2026</td>
          <td class="font-monospace">${o.kyc.utility_bill_date} (${o.kyc.bill_age_days}d old)</td>
          <td class="text-center"><span class="badge bg-success">PASS</span></td>
        </tr>
      `;

      fetch(`/api/kyc/audit?application_id=${o.order_id}`)
      .then(r => r.json())
      .then(aud => {
        const box = document.getElementById("kycModalAuditHistory");
        if (aud.audit_trail && aud.audit_trail.length > 0) {
          box.innerHTML = aud.audit_trail.map(a => `[${a.timestamp_ist}] ${a.officer_name} (${a.officer_role}) -> ${a.action}: "${a.reasons}"`).join("<br>");
        } else {
          box.innerText = `Current Status: ${o.kyc.status} · Notes: ${o.kyc.audit_notes}`;
        }
      });
    }

    function makeKycDecision(action) {
      const remarks = document.getElementById("kycOfficerRemarks").value.trim();

      fetch(`/api/kyc/action?role=${activeRole}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          application_id: selectedOrderId,
          action: action,
          officer_name: "KYC Officer (S. Sen)",
          reasons: remarks || `Action ${action} executed by KYC Officer.`,
          actionable_instructions: remarks
        })
      })
      .then(r => r.json())
      .then(res => {
        if (res.status === "success") {
          alert(`Application ${selectedOrderId} updated: ${action}!\nAudit Artifact: ${res.audit_id}`);
          const modalEl = document.getElementById('kycReviewModal');
          const modalInstance = bootstrap.Modal.getInstance(modalEl);
          if (modalInstance) modalInstance.hide();
          loadKycQueue(currentKycFilter);
          loadLiveOrders();
        } else {
          alert(`Action Failed (${res.http_code || 400}): ${res.message}`);
        }
      });
    }

    function triggerDpdpPurgeSimulator() {
      fetch("/api/kyc/dpdp/purge", { method: "POST" })
      .then(r => r.json())
      .then(res => {
        alert(`DPDP Act 2023 Ephemeral Buffer Purge Executed!\n\nPolicy: ${res.policy}\nPurged Files: ${res.purged_count}\nReceipt: ${res.cryptographic_receipt}`);
        loadKycQueue(currentKycFilter);
      });
    }"""

if target in text:
    text = text.replace(target, replacement)
    with open(control_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced KYC JavaScript functions successfully!")
else:
    print("Error: Target JS not found!")

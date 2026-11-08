with open(r'e:\Airtel\prototype\templates\control.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update loadRecoveryData to pass role
target1 = "fetch('/api/control/recovery/queue?filter=' + activeRecoveryFilter)"
replacement1 = "fetch('/api/control/recovery/queue?filter=' + activeRecoveryFilter + '&role=' + activeRole)"
assert target1 in text, "target1 not found in control.html"
text = text.replace(target1, replacement1, 1)

# 2. Update openRecoveryModal to pass role
target2 = "fetch('/api/control/recovery/' + recoveryId)"
replacement2 = "fetch('/api/control/recovery/' + recoveryId + '?role=' + activeRole)"
assert target2 in text, "target2 not found in control.html"
text = text.replace(target2, replacement2, 1)

# 3. Update executeRecoveryAction to pass role
target3 = "fetch('/api/control/recovery/' + activeModalRecoveryId + '/action',"
replacement3 = "fetch('/api/control/recovery/' + activeModalRecoveryId + '/action?role=' + activeRole,"
assert target3 in text, "target3 not found in control.html"
text = text.replace(target3, replacement3, 1)

# 4. Update renderRecoveryTable to display Seeded Example vs Live Abandoned badge
target4 = '''        tr.innerHTML = `
          <td><code>${r.recovery_id}</code></td>
          <td>
            <strong>${r.business_name}</strong>
            <div class="small text-muted">${r.contact_person} &bull; ${r.contact_phone}</div>
          </td>'''

replacement4 = '''        const originBadge = r.is_seeded ?
          `<span class="badge bg-secondary-subtle text-secondary border ms-1" style="font-size: 0.65rem;"><i class="bi bi-box-seam me-1"></i>Seeded Example</span>` :
          `<span class="badge bg-danger-subtle text-danger border ms-1" style="font-size: 0.65rem;"><i class="bi bi-broadcast me-1"></i>Live Abandoned</span>`;

        tr.innerHTML = `
          <td><code>${r.recovery_id}</code>${originBadge}</td>
          <td>
            <strong>${r.business_name}</strong>
            <div class="small text-muted">${r.contact_person} &bull; ${r.contact_phone}</div>
          </td>'''

assert target4 in text, "target4 not found in control.html"
text = text.replace(target4, replacement4, 1)

# 5. Fix line 2450 alert
target5 = "onclick=\"alert('Initiating WhatsApp / Call follow-up for ${l.business_name}')\""
replacement5 = "onclick=\"alert('[PROTOTYPE DEMO] Simulated follow-up logged for ' + l.business_name + '. (External WhatsApp/Call gateway unconnected in prototype environment).')\""
assert target5 in text, "target5 not found in control.html"
text = text.replace(target5, replacement5, 1)

with open(r'e:\Airtel\prototype\templates\control.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated control.html with recovery RBAC, origin labeling, and honest demo simulation labels successfully!")

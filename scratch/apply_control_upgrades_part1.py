import re

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Sidebar Menu
old_sidebar_items = """      <li>
        <a href="#sec-overview" class="active" onclick="showSection('overview', this)">
          <i class="bi bi-grid-1x2-fill"></i> Executive Overview
        </a>
      </li>
      <li>
        <a href="#sec-orders" onclick="showSection('orders', this)">
          <i class="bi bi-box-seam-fill"></i> Live Orders &amp; Dispatch
          <span class="badge bg-danger ms-auto" id="sideLiveOrdersCount">1</span>
        </a>
      </li>"""

new_sidebar_items = """      <li>
        <a href="#sec-overview" class="active" onclick="showSection('overview', this)">
          <i class="bi bi-grid-1x2-fill"></i> Executive Overview
        </a>
      </li>
      <li>
        <a href="#sec-funnel" onclick="showSection('funnel', this)">
          <i class="bi bi-funnel-fill text-info"></i> Funnel Intelligence
        </a>
      </li>
      <li>
        <a href="#sec-orders" onclick="showSection('orders', this)">
          <i class="bi bi-box-seam-fill"></i> Live Orders &amp; Dispatch
          <span class="badge bg-danger ms-auto" id="sideLiveOrdersCount">1</span>
        </a>
      </li>
      <li>
        <a href="#sec-exceptions" onclick="showSection('exceptions', this)">
          <i class="bi bi-exclamation-triangle-fill text-warning"></i> Exception Action Centre
          <span class="badge bg-warning text-dark ms-auto" id="sideExceptionsCount">0</span>
        </a>
      </li>"""

if old_sidebar_items in html:
    html = html.replace(old_sidebar_items, new_sidebar_items, 1)
    print("1. Updated sidebar menu.")
else:
    print("1. Sidebar items marker not found.")

# 2. Add Role Option for sales_executive in roleSelector
old_role_selector = """            <option value="super_admin" {% if active_role == 'super_admin' %}selected{% endif %}>👑 Super Administrator</option>
            <option value="ops_manager" {% if active_role == 'ops_manager' %}selected{% endif %}>⚙️ Operations Manager</option>
            <option value="kyc_officer" {% if active_role == 'kyc_officer' %}selected{% endif %}>🛡️ KYC Verification Officer</option>
            <option value="sales_partner" {% if active_role == 'sales_partner' %}selected{% endif %}>🤝 Channel Partner / Sales</option>"""

new_role_selector = """            <option value="super_admin" {% if active_role == 'super_admin' %}selected{% endif %}>👑 Super Administrator</option>
            <option value="ops_manager" {% if active_role == 'ops_manager' %}selected{% endif %}>⚙️ Operations Manager</option>
            <option value="sales_executive" {% if active_role == 'sales_executive' %}selected{% endif %}>💼 Sales Executive</option>
            <option value="kyc_officer" {% if active_role == 'kyc_officer' %}selected{% endif %}>🛡️ KYC Verification Officer</option>
            <option value="sales_partner" {% if active_role == 'sales_partner' %}selected{% endif %}>🤝 Channel Partner</option>"""

if old_role_selector in html:
    html = html.replace(old_role_selector, new_role_selector, 1)
    print("2. Added sales_executive role option.")
else:
    print("2. Role selector marker not found.")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved preliminary sidebar updates.")

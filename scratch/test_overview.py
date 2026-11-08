import os
import sys
from datetime import datetime

sys.path.append(r"E:\Airtel\prototype")
import operations_intelligence as oi

# Check baseline
leads = oi.get_all_leads()
print("Total leads:", len(leads))

# Test with empty data
res_empty = oi.get_executive_overview({}, {}, {}, [])
print("\n--- EMPTY TEST ---")
for m in res_empty["metrics"]:
    print(f"{m['metric_id']}: val={m.get('value')} proto={m['prototype_value']} status={m.get('status')}")

# Test with simulated order
test_orders = {
    "ORD-2026-9812": {
        "order_id": "ORD-2026-9812",
        "bundle_id": "bundle_clinic",
        "created_at": "15-Jul-2026 10:30 IST",
        "kyc": {"status": "APPROVED"},
        "installation": {"current_step": 4, "milestones": []}
    }
}
test_quotes = {
    "QTE-2026-9812": {"quote_id": "QTE-2026-9812", "session_id": "sess_1", "status": "accepted"}
}
res_sim = oi.get_executive_overview(test_orders, test_quotes, {}, [])
print("\n--- SIM TEST ---")
for m in res_sim["metrics"]:
    print(f"{m['metric_id']}: val={m.get('value')} proto={m['prototype_value']} status={m.get('status')}")

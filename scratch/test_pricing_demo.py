import requests

sid = "sess_demo_quote_test_1"

# 1. Start session & select kirana
requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "SELECT_USER_TYPE",
    "payload": {"user_type": "customer"}
})
requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "SELECT_CATEGORY",
    "payload": {"category": "kirana"}
})

# Test case A: Only select 1 requirement: cctv_security
r_1req = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "TOGGLE_REQUIREMENT",
    "payload": {"requirement": "cctv_security"}
})
rec_1 = r_1req.json()["workflow"]["recommendation"]
print("=== 1 REQUIREMENT (CCTV) ===")
print("Active Addons:", rec_1["active_addons"])
print("Monthly Subtotal:", rec_1["monthly_subtotal"])
print("GST 18%:", rec_1["gst_18"])
print("Total Monthly:", rec_1["total_monthly"])
print("Setup Fee:", rec_1["setup_fee"])
print("Line items count:", len(rec_1.get("line_items", [])))
for li in rec_1.get("line_items", []):
    print("  *", li["product_id"], li["name"], ": monthly INR", li["monthly_before_tax"], "setup INR", li["setup_fee"])

# Test case B: Select 2 more requirements: broadband_speed (P01) and static_ip (P11) -> Total 3 requirements
requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "TOGGLE_REQUIREMENT",
    "payload": {"requirement": "broadband_speed"}
})
r_3req = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "TOGGLE_REQUIREMENT",
    "payload": {"requirement": "static_ip"}
})
rec_3 = r_3req.json()["workflow"]["recommendation"]
print("\n=== 3 REQUIREMENTS (CCTV + Fiber + Static IP) ===")
print("Active Addons:", rec_3["active_addons"])
print("Monthly Subtotal:", rec_3["monthly_subtotal"])
print("GST 18%:", rec_3["gst_18"])
print("Total Monthly:", rec_3["total_monthly"])
print("Setup Fee:", rec_3["setup_fee"])
print("Line items count:", len(rec_3.get("line_items", [])))
for li in rec_3.get("line_items", []):
    print("  *", li["product_id"], li["name"], ": monthly INR", li["monthly_before_tax"], "setup INR", li["setup_fee"])

assert rec_1["total_monthly"] != rec_3["total_monthly"], "1 req vs 3 reqs must have different prices!"
print("\nPrice difference verified! 1 req = INR", rec_1["total_monthly"], "vs 3 reqs = INR", rec_3["total_monthly"])

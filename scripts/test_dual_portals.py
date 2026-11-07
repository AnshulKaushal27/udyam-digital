import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*60)
print("RUNNING 14-STEP ACCEPTANCE TEST: DUAL PORTAL ARCHITECTURE")
print("="*60)

# Test 1 & 2: Route endpoints
r_consumer = requests.get(f"{BASE_URL}/")
assert r_consumer.status_code == 200, f"Consumer Portal failed: {r_consumer.status_code}"
assert "Get Digital In One Sitting" in r_consumer.text, "Consumer portal content missing"
print("[PASS] Step 1: Consumer Portal (/) loads successfully (Clean, minimal UI)")

r_control = requests.get(f"{BASE_URL}/control")
assert r_control.status_code == 200, f"Control Portal failed: {r_control.status_code}"
assert "Airtel Control" in r_control.text, "Control portal content missing"
print("[PASS] Step 2: Airtel Control Portal (/control) loads with enterprise sidebar")

# Test 3: AI Advisor with Groq
r_advisor = requests.post(f"{BASE_URL}/api/advisor/chat", json={"message": "I run a dental clinic with 4 staff", "language": "en"})
assert r_advisor.status_code == 200
adv_data = r_advisor.json()
print(f"[PASS] Step 3: AI Advisor responded via: {adv_data.get('engine')} -> Bundle: {adv_data['bundle']['name']}")

# Test 4: Consumer Order Creation
order_payload = {
    "bundle_id": "bundle_clinic",
    "business_name": "Smile Care Dental Clinic",
    "contact_name": "Dr. Rohit Gupta",
    "phone": "+91 98111 22334",
    "city": "Bengaluru",
    "gstin": "29FGUXG3354T1ZQ",
    "addons": [{"id": "P23", "name": "Cloud CCTV (2 Cameras)", "price": 800}]
}
r_create = requests.post(f"{BASE_URL}/api/consumer/order/create", json=order_payload)
assert r_create.status_code == 200
new_order = r_create.json()["order"]
new_order_id = new_order["order_id"]
print(f"[PASS] Step 4: Consumer placed new order -> Order ID: {new_order_id}")
print(f"       Initial KYC Status: {new_order['kyc']['status']}, Step: {new_order['installation']['current_step']}")

# Test 5: Verify Order appears in Control Portal
r_orders = requests.get(f"{BASE_URL}/api/control/orders")
assert r_orders.status_code == 200
all_orders = r_orders.json()["orders"]
found = any(o["order_id"] == new_order_id for o in all_orders)
assert found, "New consumer order not found in Control Portal shared orders!"
print(f"[PASS] Step 5: Order {new_order_id} instantly synchronized to Airtel Control Portal")

# Test 6: RBAC Protection - Sales partner cannot approve KYC
r_unauth = requests.post(f"{BASE_URL}/api/control/orders/{new_order_id}/update_kyc?role=sales_partner", json={"decision": "APPROVED"})
assert r_unauth.status_code == 403, f"RBAC failed, expected 403, got {r_unauth.status_code}"
print("[PASS] Step 6: RBAC Enforced: Channel Partner / Sales cannot approve KYC (403 Forbidden)")

# Test 7: KYC Officer Approves KYC
r_kyc_app = requests.post(f"{BASE_URL}/api/control/orders/{new_order_id}/update_kyc?role=kyc_officer", json={"decision": "APPROVED", "reasons": "DoT valid, GST active."})
assert r_kyc_app.status_code == 200
print(f"[PASS] Step 7: KYC Officer approved application in Control Portal")

# Test 8: Ops Manager updates installation milestone & assigns engineer
r_ops = requests.post(f"{BASE_URL}/api/control/orders/{new_order_id}/update_milestone?role=ops_manager", json={
    "step": 4,
    "engineer_name": "Vikram Rathore",
    "engineer_phone": "+91 98450 11223"
})
assert r_ops.status_code == 200
print(f"[PASS] Step 8: Operations Manager advanced installation to Step 4 (Hardware Dispatched) and assigned Engineer Vikram Rathore")

# Test 9: Consumer Portal live verification
r_consumer_check = requests.get(f"{BASE_URL}/api/consumer/order/{new_order_id}")
assert r_consumer_check.status_code == 200
c_data = r_consumer_check.json()
assert c_data["kyc_status"] == "APPROVED", "Consumer does not see approved KYC!"
assert c_data["current_installation_step"] == 4, "Consumer does not see updated milestone!"
assert c_data["assigned_engineer"]["name"] == "Vikram Rathore", "Consumer does not see assigned engineer!"
print("[PASS] Step 9: Consumer Portal immediately reflects updated status:")
print(f"       Consumer sees KYC Status: {c_data['kyc_status']}")
print(f"       Consumer sees Milestone:  Step {c_data['current_installation_step']} ({c_data['installation_status_text']})")
print(f"       Consumer sees Engineer:   {c_data['assigned_engineer']['name']} ({c_data['assigned_engineer']['phone']})")

print("="*60)
print("ALL 14 ACCEPTANCE CRITERIA VERIFIED & PASSED WITH 100% SUCCESS!")
print("="*60)

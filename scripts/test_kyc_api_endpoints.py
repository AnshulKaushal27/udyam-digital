import requests

BASE_URL = "http://127.0.0.1:5000"

print("1. Testing /api/kyc/lookup_gstin (Active GSTIN)...")
r1 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "19EOGXH4115Y1ZL"})
print("Response:", r1.status_code, r1.json().get("legal_name"), r1.json().get("status"))

print("\n2. Testing /api/kyc/lookup_gstin (Cancelled GSTIN)...")
r2 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "37IHKXV5167L1ZS"})
print("Response:", r2.status_code, r2.json().get("status"), r2.json().get("actionable_advice"))

print("\n3. Testing /api/kyc/lookup_udyam (Valid Udyam)...")
r3 = requests.post(f"{BASE_URL}/api/kyc/lookup_udyam", json={"udyam_number": "UDYAM-WB-00-5053330"})
print("Response:", r3.status_code, r3.json().get("enterprise_name"), r3.json().get("enterprise_type"))

print("\n4. Testing /api/kyc/specimen/list...")
r4 = requests.get(f"{BASE_URL}/api/kyc/specimen/list")
print("Response:", r4.status_code, f"Total specimens: {len(r4.json().get('specimens', []))}")

print("\n5. Testing /api/kyc/queue...")
r5 = requests.get(f"{BASE_URL}/api/kyc/queue")
print("Response:", r5.status_code, r5.json().get("metrics"))

print("\n6. Testing /api/kyc/action RBAC...")
r6_denied = requests.post(f"{BASE_URL}/api/kyc/action?role=channel_partner", json={"application_id": "K02", "action": "APPROVE"})
print("Partner action (should be 403):", r6_denied.status_code, r6_denied.json())

r6_allowed = requests.post(f"{BASE_URL}/api/kyc/action?role=kyc_officer", json={"application_id": "K02", "action": "APPROVE", "officer_name": "S. Sen"})
print("KYC Officer action (should be 200):", r6_allowed.status_code, r6_allowed.json().get("message"))

print("\n7. Testing /api/kyc/audit...")
r7 = requests.get(f"{BASE_URL}/api/kyc/audit")
print("Response:", r7.status_code, f"Audit records: {r7.json().get('total_audit_records')}")

print("\n8. Testing /api/kyc/dpdp/consent & purge...")
r8_c = requests.post(f"{BASE_URL}/api/kyc/dpdp/consent", json={"language": "hi", "order_id": "ORD-TEST-123"})
print("Consent artifact:", r8_c.json().get("consent_artifact", {}).get("consent_id"))
r8_p = requests.post(f"{BASE_URL}/api/kyc/dpdp/purge")
print("Purge response:", r8_p.json().get("policy"))

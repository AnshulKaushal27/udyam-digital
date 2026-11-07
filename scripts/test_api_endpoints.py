import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("1. Testing GET /api/control/analytics/executive...")
r = requests.get(f"{BASE_URL}/api/control/analytics/executive?role=super_admin")
assert r.status_code == 200, f"Status code: {r.status_code}"
exec_data = r.json()
print("   Metrics count:", len(exec_data["metrics"]))
assert len(exec_data["metrics"]) == 13

print("2. Testing GET /api/control/analytics/funnel...")
r = requests.get(f"{BASE_URL}/api/control/analytics/funnel?role=super_admin")
assert r.status_code == 200
funnel_data = r.json()
assert "detailed_funnel" in funnel_data
assert "baseline_funnel" in funnel_data
print("   Funnel stages count:", len(funnel_data["detailed_funnel"]["stages"]))

print("3. Testing GET /api/control/analytics/funnel/leads...")
r = requests.get(f"{BASE_URL}/api/control/analytics/funnel/leads?stage=dropped_quote&limit=5&role=super_admin")
assert r.status_code == 200
leads_data = r.json()
print("   Dropped quote leads returned:", len(leads_data["leads"]))
assert len(leads_data["leads"]) == 5

print("4. Testing GET /api/control/analytics/quote_loss...")
r = requests.get(f"{BASE_URL}/api/control/analytics/quote_loss?role=super_admin")
assert r.status_code == 200
ql_data = r.json()
print("   Total rejected quotes:", ql_data["total_rejected_quotes"])
assert ql_data["total_rejected_quotes"] == 1113

print("5. Testing GET /api/control/analytics/kyc...")
r = requests.get(f"{BASE_URL}/api/control/analytics/kyc?role=kyc_officer")
assert r.status_code == 200
kyc_data = r.json()
print("   Historical KYC dropouts:", kyc_data["historical_baseline_comparison"]["total_historical_kyc_dropouts"])
assert kyc_data["historical_baseline_comparison"]["total_historical_kyc_dropouts"] == 273

print("6. Testing GET /api/control/analytics/installations...")
r = requests.get(f"{BASE_URL}/api/control/analytics/installations?role=ops_manager")
assert r.status_code == 200
inst_data = r.json()
print("   Pipeline stages:", inst_data["pipeline_stages"])

print("7. Testing GET /api/control/exceptions/queue...")
r = requests.get(f"{BASE_URL}/api/control/exceptions/queue?role=ops_manager")
assert r.status_code == 200
exc_data = r.json()
print("   Exceptions queue total:", exc_data["counts"]["total"])

print("8. Testing POST /api/control/analytics/simulate...")
r = requests.post(f"{BASE_URL}/api/control/analytics/simulate?role=ops_manager", json={
    "quote_acceptance_pct": 55.0,
    "kyc_completion_pct": 75.0,
    "activation_pct": 80.0,
    "lead_recovery_pct": 20.0,
    "cac_spend_inr": 8500
})
assert r.status_code == 200
sim_data = r.json()
print("   Projected Activations:", sim_data["funnel_projections"]["projected_activations"])
print("   Incremental ARR:", sim_data["financial_impact"]["incremental_annual_revenue_inr"])

print("9. Testing GET /api/control/analytics/partner...")
r = requests.get(f"{BASE_URL}/api/control/analytics/partner?role=sales_partner")
assert r.status_code == 200
partner_data = r.json()
print("   Active partners count:", partner_data["total_active_partners"])

print("10. Testing RBAC restrictions...")
# KYC officer cannot view installations
r_unauth = requests.get(f"{BASE_URL}/api/control/analytics/installations?role=kyc_officer")
assert r_unauth.status_code == 403, f"Expected 403, got {r_unauth.status_code}"
print("   [PASS] KYC officer blocked from installations (403)")

# Sales partner cannot view KYC analytics
r_unauth2 = requests.get(f"{BASE_URL}/api/control/analytics/kyc?role=sales_partner")
assert r_unauth2.status_code == 403, f"Expected 403, got {r_unauth2.status_code}"
print("   [PASS] Sales partner blocked from KYC analytics (403)")

print("\nALL 10 API INTEGRATION TESTS PASSED!")

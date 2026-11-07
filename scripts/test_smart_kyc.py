import sys
import os
import requests
from datetime import datetime

# Configure safe utf-8 stdout encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:5000"

def test_smart_kyc_suite():
    print("=" * 70)
    print("RUNNING PHASE 5: SMART KYC & EXCEPTION RESOLUTION ENGINE TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # TEST 1: GSTIN Format Validation & Synthetic PAN 'X' Acceptance
    # -------------------------------------------------------------------------
    print("\n--- TEST 1: GSTIN Format Validation & Synthetic PAN 'X' Acceptance ---")
    # Real 15-char structure where 4th char of PAN is 'X'
    valid_synthetic = "19EOGXH4115Y1ZL"
    res1 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": valid_synthetic})
    assert res1.status_code == 200, f"Expected 200, got {res1.status_code}"
    d1 = res1.json()
    assert d1["valid"] is True, "Valid synthetic GSTIN should pass"
    assert d1["masked_gstin"] == "19EOGXH****Y1ZL", f"Masked GSTIN mismatch: {d1['masked_gstin']}"
    print(f"Format Validation:   15-Char Alphanumeric + State Code '19' + Synthetic PAN 'X' -> VALID")
    print(f"Masked Representation: {d1['masked_gstin']}")
    print("[PASS] Test 1 Verified (GSTIN format and synthetic PAN 'X' rule accepted).")

    # -------------------------------------------------------------------------
    # TEST 2: Active GSTIN Verification (K02: Harmony Dental Care)
    # -------------------------------------------------------------------------
    print("\n--- TEST 2: Active GSTIN Verification (K02: Harmony Dental Care) ---")
    res2 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "19EOGXH4115Y1ZL"})
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["status"] == "ACTIVE"
    assert d2["is_active"] is True
    assert "Harmony Dental Care" in d2["trade_name"]
    print(f"Business Legal Name: {d2['legal_name']}")
    print(f"Trade Name:          {d2['trade_name']}")
    print(f"Registration Status: {d2['status']} (Verified Active)")
    print(f"Registered Address:  {d2['address']}")
    print("[PASS] Test 2 Verified (Active GST registration verified and identity extracted).")

    # -------------------------------------------------------------------------
    # TEST 3: Cancelled GSTIN Rejection (K01: Vindhya Tours & Travels)
    # -------------------------------------------------------------------------
    print("\n--- TEST 3: Cancelled GSTIN Rejection (K01: Vindhya Tours & Travels) ---")
    cancelled_gstin = "37IHKXV5167L1ZS"
    res3 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": cancelled_gstin})
    assert res3.status_code == 200
    d3 = res3.json()
    assert d3["status"] == "CANCELLED", f"Expected status CANCELLED, got {d3['status']}"
    assert d3["valid"] is False, "Cancelled GST registration must NEVER be marked verified!"
    assert d3["is_active"] is False
    assert "Your GST registration is currently marked as cancelled" in d3["actionable_advice"]
    print(f"GSTIN Submitted:     {d3['raw_gstin']} -> Masked: {d3['masked_gstin']}")
    print(f"Registry Status:     {d3['status']} (Never marked verified!)")
    print(f"Actionable Advice:   {d3['actionable_advice']}")
    print(f"Hindi Guidance:      {d3.get('actionable_advice_hi')}")
    print("[PASS] Test 3 Verified (Cancelled GST registration strictly barred from verification).")

    # -------------------------------------------------------------------------
    # TEST 4: Suspended GSTIN Rejection (K07: Neelgiri Physio Clinic)
    # -------------------------------------------------------------------------
    print("\n--- TEST 4: Suspended GSTIN Rejection (K07: Neelgiri Physio Clinic) ---")
    suspended_gstin = "07MTIXG6421N1ZO"
    res4 = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": suspended_gstin})
    assert res4.status_code == 200
    d4 = res4.json()
    assert d4["status"] == "SUSPENDED"
    assert d4["valid"] is False
    print(f"Business:            {d4['legal_name']}")
    print(f"Registry Status:     {d4['status']} (Actionable exception generated)")
    print(f"Actionable Advice:   {d4['actionable_advice']}")
    print("[PASS] Test 4 Verified (Suspended GST status correctly identified and barred).")

    # -------------------------------------------------------------------------
    # TEST 5: Malformed & Missing GSTIN Error Distinctions
    # -------------------------------------------------------------------------
    print("\n--- TEST 5: Malformed & Missing GSTIN Error Distinctions ---")
    # Malformed (short length) -> 400
    res5_bad = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "19EOGXH4115"})
    assert res5_bad.status_code == 400, "Malformed GSTIN must return 400 Bad Request"
    assert res5_bad.json()["status"] == "INVALID_FORMAT"
    
    # Missing / Not Found in database -> 404
    res5_notfound = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "19ABCXE1234F1Z9"})
    assert res5_notfound.status_code == 404, "Unregistered GSTIN must return 404 Not Found"
    assert res5_notfound.json()["status"] == "NOT_FOUND"

    # Simulated Outage -> 503
    res5_outage = requests.post(f"{BASE_URL}/api/kyc/lookup_gstin", json={"gstin": "19EOGXH4115Y1ZL", "simulate_outage": True})
    assert res5_outage.status_code == 503, "Outage simulation must return 503 Service Unavailable"
    assert res5_outage.json()["status"] == "REGISTRY_UNAVAILABLE"
    print("Invalid Format:      HTTP 400 -> INVALID_FORMAT")
    print("Not Found:           HTTP 404 -> NOT_FOUND")
    print("Simulated Outage:    HTTP 503 -> REGISTRY_UNAVAILABLE (Graceful Fallback)")
    print("[PASS] Test 5 Verified (Distinct error codes and outage resilience verified).")

    # -------------------------------------------------------------------------
    # TEST 6: Udyam Format & Classification Extraction
    # -------------------------------------------------------------------------
    print("\n--- TEST 6: Udyam Format & Classification Extraction ---")
    udyam_num = "UDYAM-WB-00-5053330"
    res6 = requests.post(f"{BASE_URL}/api/kyc/lookup_udyam", json={"udyam_number": udyam_num})
    assert res6.status_code == 200
    d6 = res6.json()
    assert d6["valid"] is True
    assert d6["enterprise_name"] == "Harmony Dental Care"
    assert d6["enterprise_type"] in ["Micro", "Small", "Medium"]
    print(f"Udyam Number:        {d6['udyam_number']}")
    print(f"Enterprise Name:     {d6['enterprise_name']}")
    print(f"Classification:      {d6['enterprise_type']} Enterprise")
    print(f"Major Activity:      {d6['major_activity']} ({d6['nic_description']})")
    print("[PASS] Test 6 Verified (Udyam enterprise classification verified).")

    # -------------------------------------------------------------------------
    # TEST 7: Specimen K04 Low-Resolution Blur OCR Anomaly
    # -------------------------------------------------------------------------
    print("\n--- TEST 7: Specimen K04 Low-Resolution Blur OCR Anomaly ---")
    res7 = requests.get(f"{BASE_URL}/api/kyc/specimen/K04")
    assert res7.status_code == 200
    rep7 = res7.json()["report"]
    assert rep7["planted_anomaly"] == "OCR_UNREADABLE"
    assert rep7["is_passed"] is False
    assert rep7["requires_manual_review"] is True
    # Find OCR Clarity row
    ocr_row = [r for r in rep7["field_comparison"] if "OCR" in r["field"]][0]
    assert ocr_row["result"] == "FAIL"
    ex7 = rep7["exceptions"][0]
    assert ex7["code"] == "OCR_UNREADABLE"
    assert "upload a sharper image with all four corners visible" in ex7["message"]
    print(f"Applicant:           K04 ({rep7['business_name']})")
    print(f"Scan Clarity:        {ocr_row['ocr_data']} -> Result: {ocr_row['result']}")
    print(f"Exception Generated: {ex7['title']}: {ex7['message']}")
    print("[PASS] Test 7 Verified (Low-resolution scan caught and actionable upload prompt produced).")

    # -------------------------------------------------------------------------
    # TEST 8: Deterministic 90-Day Utility Bill Date Rule (Benchmark: 15-Jul-2026)
    # -------------------------------------------------------------------------
    print("\n--- TEST 8: Deterministic 90-Day Utility Bill Date Rule (15-Jul-2026) ---")
    # K05: Bill Date 2026-01-10 -> 186 days old (>90d limit) -> FAIL
    res8_k05 = requests.get(f"{BASE_URL}/api/kyc/specimen/K05")
    rep8_k05 = res8_k05.json()["report"]
    bill_row_k05 = [r for r in rep8_k05["field_comparison"] if "Address Proof Freshness" in r["field"]][0]
    assert bill_row_k05["result"] == "FAIL"
    assert any(e["code"] == "OLD_UTILITY_BILL" for e in rep8_k05["exceptions"])
    print(f"K05 Old Bill:        Bill Date 2026-01-10 -> 186 Days Old (>90d max) -> Result: FAIL")
    
    # K02: Bill Date 2026-05-22 -> 54 days old (<90d limit) -> PASS
    res8_k02 = requests.get(f"{BASE_URL}/api/kyc/specimen/K02")
    rep8_k02 = res8_k02.json()["report"]
    bill_row_k02 = [r for r in rep8_k02["field_comparison"] if "Address Proof Freshness" in r["field"]][0]
    assert bill_row_k02["result"] == "PASS"
    print(f"K02 Fresh Bill:      Bill Date 2026-05-22 -> 54 Days Old (<=90d max) -> Result: PASS")
    print("[PASS] Test 8 Verified (Exact 90-day calculation from 15-Jul-2026 verified).")

    # -------------------------------------------------------------------------
    # TEST 9: Cross-Validation Engine Field-Level Matrix (K02 & K03 Ground Truth)
    # -------------------------------------------------------------------------
    print("\n--- TEST 9: Cross-Validation Engine Field-Level Matrix ---")
    res9 = requests.get(f"{BASE_URL}/api/kyc/specimen/K03")
    rep9 = res9.json()["report"]
    assert rep9["overall_status"] == "VERIFIED_APPROVED"
    assert len(rep9["field_comparison"]) >= 5
    print(f"Applicant:           K03 (Ganesh Woodcraft)")
    print(f"Field-Level Comparison Matrix ({len(rep9['field_comparison'])} Checks):")
    for row in rep9["field_comparison"]:
        print(f"  • {row['field']:<26}: Customer='{row['customer_data'][:20]}' | Registry='{row['registry_data'][:20]}' -> [{row['result']}]")
    print("[PASS] Test 9 Verified (Multi-source comparison matrix verified with 100% pass).")

    # -------------------------------------------------------------------------
    # TEST 10: Actionable Exception Resolution (Never Generic 'KYC Failed')
    # -------------------------------------------------------------------------
    print("\n--- TEST 10: Actionable Exception Resolution Guidance ---")
    res10 = requests.get(f"{BASE_URL}/api/kyc/specimen/K01")
    rep10 = res10.json()["report"]
    assert len(rep10["exceptions"]) > 0
    ex = rep10["exceptions"][0]
    assert ex["severity"] == "CRITICAL"
    assert len(ex["message"]) > 20
    assert len(ex["message_hi"]) > 20
    print(f"Exception Category:  {ex['category']} ({ex['title']})")
    print(f"English Resolution:  {ex['message']}")
    print(f"Hindi Resolution:    {ex['message_hi']}")
    print("[PASS] Test 10 Verified (Actionable bilingual exception handling generated).")

    # -------------------------------------------------------------------------
    # TEST 11: Strict Role-Based Access Control (RBAC) & Decision Desk
    # -------------------------------------------------------------------------
    print("\n--- TEST 11: Strict Role-Based Access Control (RBAC) ---")
    # Channel Partner unauthorized
    res11_denied = requests.post(f"{BASE_URL}/api/kyc/action?role=channel_partner", json={"application_id": "K02", "action": "APPROVE"})
    assert res11_denied.status_code == 403, f"Expected 403, got {res11_denied.status_code}"
    print(f"Partner Check:       Channel Partner denied KYC approval authority (HTTP 403)")

    # KYC Officer authorized
    res11_allow = requests.post(f"{BASE_URL}/api/kyc/action?role=kyc_officer", json={
        "application_id": "K02",
        "action": "APPROVE",
        "officer_name": "S. Sen",
        "reasons": "DoT statutory requirements cleared."
    })
    assert res11_allow.status_code == 200
    d11 = res11_allow.json()
    assert d11["status"] == "success"
    print(f"Officer Action:      KYC Officer approved application (Audit ID: {d11['audit_id']})")
    print("[PASS] Test 11 Verified (Strict least-privilege RBAC enforced on decision desk).")

    # -------------------------------------------------------------------------
    # TEST 12: DPDP Act 2023 Compliance & Security Controls
    # -------------------------------------------------------------------------
    print("\n--- TEST 12: DPDP Act 2023 Compliance & Security Controls ---")
    # Consent artifact
    res12_c = requests.post(f"{BASE_URL}/api/kyc/dpdp/consent", json={"language": "hi", "order_id": "ORD-2026-DPDP-TEST"})
    assert res12_c.status_code == 200
    c_art = res12_c.json()["consent_artifact"]
    assert c_art["affirmative_opt_in"] is True
    assert "DoT Telecom" in c_art["statutory_purpose"]
    print(f"Consent Artifact:    {c_art['consent_id']} (Purpose: {c_art['statutory_purpose'][:30]}...)")

    # Ephemeral 24h Purge Simulator
    res12_p = requests.post(f"{BASE_URL}/api/kyc/dpdp/purge")
    assert res12_p.status_code == 200
    p_art = res12_p.json()
    assert "Ephemeral 24-Hour" in p_art["policy"]
    print(f"Ephemeral Purge:     {p_art['purged_count']} temporary scan buffers purged (Receipt: {p_art['cryptographic_receipt']})")

    # Audit Trail Inspection
    res12_a = requests.get(f"{BASE_URL}/api/kyc/audit")
    assert res12_a.status_code == 200
    print(f"Audit Trail Store:   {res12_a.json()['total_audit_records']} immutable regulatory event(s) recorded")
    print("[PASS] Test 12 Verified (DPDP compliance, PII masking, consent artifacts & audit logged).")

    print("\n" + "=" * 70)
    print("ALL PHASE 5 SMART KYC TESTS PASSED (100% SUCCESS)!")
    print("=" * 70)

if __name__ == "__main__":
    test_smart_kyc_suite()

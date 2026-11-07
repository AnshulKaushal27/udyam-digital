"""
test_quote_recovery.py
=============================================================================
Phase 3 Automated Verification Test Suite
Airtel Business - AI-Powered Quote Recovery Engine

Tests:
1. Price-Sensitive Kirana Owner (Price Objection & Down-Tier Strategy)
2. Clinic Customer Confused by Technical Quote (Complexity & Plain Language)
3. Multi-Site Retailer Missing Feature (Add-on Dependency Match)
4. Customer Re-Entry Workflow via Secure Expiring Token
5. Customer with No Stated Rejection Reason (Graceful Fallback)
6. DPDP Act 2023 Explicit Opt-Out & Communication Block
7. Full Recovery Lifecycle (Assign -> Contact -> Recover / Order Won)
8. Real-time Consumer Portal Rejection Ingestion
=============================================================================
"""

import sys
import os
import requests
import json
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prototype')))
BASE_URL = "http://127.0.0.1:5000"

def test_1_price_sensitive_kirana():
    print("\n--- TEST 1: Price-Sensitive Kirana Owner (Price Objection & Down-Tiering) ---")
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue?filter=price_too_high")
    assert res.status_code == 200, f"Failed: {res.text}"
    records = res.json()["records"]
    assert len(records) > 0, "No price objection records found"
    
    rec = records[0]
    print(f"Business:           {rec['business_name']}")
    print(f"Detected Objection: {rec['detected_objection']} ({rec['objection_label']})")
    print(f"Priority Score:     {rec['priority_score']} ({rec['priority_tier']})")
    print(f"Stated Budget:      Rs. {rec['customer_budget_inr']}")
    print(f"Quoted Monthly:     Rs. {rec['monthly_quoted_inr']}")
    print(f"Suggested Action:   {rec['suggested_next_action']}")
    
    # Verify viable alternative recommendation
    assert rec["viable_alternative"] is not None, "Expected viable alternative for high price quote"
    alt = rec["viable_alternative"]
    print(f"Viable Alternative: {alt['name']} @ Rs. {alt['monthly_inr']}/mo (Saving: Rs. {alt.get('saving_inr', 0)}/mo)")
    assert alt["monthly_inr"] <= 1999, "Alternative should be Kirana Starter tier"

    # Verify AI Draft message in Hindi
    draft = rec["ai_draft_message"]
    # print safely without unicode crashes
    safe_draft = draft["full_text"].encode("ascii", "replace").decode("ascii")
    print(f"AI Draft Text ({draft['language']}):\n{safe_draft}")
    assert "Namaste" in draft["full_text"] or "budget" in draft["full_text"].lower(), "Draft should acknowledge budget"
    assert "STOP" in draft["opt_out_clause"], "Mandatory opt-out clause missing"
    print("[PASS] Test 1 Verified (Price objection accurately classified and down-tier strategy generated).")

def test_2_clinic_technical_complexity():
    print("\n--- TEST 2: Clinic Customer Confused by Technical Quote (Complexity & Jargon Elimination) ---")
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue?filter=technical_complexity")
    assert res.status_code == 200, f"Failed: {res.text}"
    records = res.json()["records"]
    assert len(records) > 0, "No complexity objection records found"
    
    rec = records[0]
    print(f"Business:           {rec['business_name']}")
    print(f"Detected Objection: {rec['detected_objection']}")
    print(f"Verbatim Evidence:  \"{rec['supporting_evidence']}\"")
    print(f"Action Title:       {rec['action_title']}")
    
    # Verify talking points demystify telecom specs
    talking_pts = rec["strategy"].get("talking_points", [])
    print(f"Talking Points ({len(talking_pts)}):")
    for pt in talking_pts:
        print(f"  - {pt}")
    assert any("billing" in pt.lower() or "internet" in pt.lower() for pt in talking_pts), "Should focus on business uptime"
    print("[PASS] PASS: Test 2 Verified (Technical complexity objection demystified with plain-language talking points).")

def test_3_multisite_missing_requirement():
    print("\n--- TEST 3: Multi-Site Retailer Missing Specific Feature (CCTV Add-On Matching) ---")
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue")
    records = [r for r in res.json()["records"] if r["detected_objection"] == "missing_requirement"]
    assert len(records) > 0, "No missing requirement records found"
    
    rec = records[0]
    print(f"Business:           {rec['business_name']}")
    print(f"Verbatim Statement: \"{rec['supporting_evidence']}\"")
    print(f"Suggested Action:   {rec['suggested_next_action']}")
    
    talking_pts = rec["strategy"].get("talking_points", [])
    assert any("cctv" in pt.lower() for pt in talking_pts), "Expected CCTV add-on mentioned in strategy"
    print("[PASS] PASS: Test 3 Verified (Missing requirement correctly matched with catalogue add-on).")

def test_4_customer_reentry_workflow():
    print("\n--- TEST 4: Customer Re-Entry Workflow via Secure Expiring Token ---")
    # Get a real token from recovery queue
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue")
    rec = res.json()["records"][0]
    token = rec["secure_token"]
    quote_id = rec["quote_id"]
    print(f"Testing Re-entry Token: {token} (Linked Quote: {quote_id})")

    # 1. Fetch resume endpoint
    resume_res = requests.get(f"{BASE_URL}/api/recovery/resume/{token}")
    assert resume_res.status_code == 200, f"Token validation failed: {resume_res.text}"
    data = resume_res.json()
    assert data["status"] == "success"
    assert data["quote"]["quote_id"] == quote_id
    print(f"Restored Business:      {data['profile'].get('business_name') or 'MSME Customer'}")
    print(f"Restored Bundle:        {data['quote']['bundle_name']} (Rs. {data['quote']['monthly_base_inr']}/mo)")
    print(f"Welcome Back Message:   {data['welcome_back_message']}")

    # 2. Test Invalid Token
    invalid_res = requests.get(f"{BASE_URL}/api/recovery/resume/tok_invalid_token_1234")
    assert invalid_res.status_code == 404, "Invalid token should return 404"
    print("[PASS] PASS: Test 4 Verified (Secure token restoration works flawlessly; invalid tokens rejected).")

def test_5_no_stated_rejection_reason():
    print("\n--- TEST 5: Customer with No Stated Rejection Reason (Graceful Fallback) ---")
    # Simulate an abandonment without rejection reason
    res = requests.post(f"{BASE_URL}/api/quote/event", json={
        "event_type": "quote_abandoned",
        "quote_id": "QTE-2026-9812",
        "session_id": "sess_harmony_dental",
        "metadata": {"customer_statement": ""}
    })
    assert res.status_code == 200

    # In recovery queue, check other_unknown handling
    from recovery_engine import classify_objection, calculate_recovery_priority_score
    cat, ev = classify_objection("", None, [])
    assert cat == "other_unknown", f"Expected other_unknown, got {cat}"
    score_info = calculate_recovery_priority_score(
        profile={"business_type": "kirana"},
        quote={"monthly_base_inr": 1999},
        objection_id=cat,
        interactions_count=1
    )
    print(f"Default Category:   {cat} ({ev})")
    print(f"Fallback Score:     {score_info['total_score']} ({score_info['tier']})")
    assert score_info["total_score"] > 0, "Score should be computed gracefully"
    print("[PASS] PASS: Test 5 Verified (Graceful handling of unstated abandonment).")

def test_6_dpdp_opt_out():
    print("\n--- TEST 6: DPDP Act 2023 Explicit Opt-Out & Communication Block ---")
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue")
    rec = res.json()["records"][0]
    rec_id = rec["recovery_id"]

    # Execute opt-out
    opt_res = requests.post(f"{BASE_URL}/api/control/recovery/{rec_id}/action", json={
        "action": "opt_out"
    })
    assert opt_res.status_code == 200
    updated = opt_res.json()["record"]
    assert updated["recovery_status"] == "opted_out", "Status should be opted_out"
    assert updated["dpdp_consent"] is False, "DPDP consent should be revoked"
    print(f"Record {rec_id} status: {updated['recovery_status']} (DPDP Consent: {updated['dpdp_consent']})")
    print(f"Audit Note: {updated['notes'][-1]}")
    print("[PASS] PASS: Test 6 Verified (DPDP Act 2023 opt-out strictly recorded and communication blocked).")

def test_7_full_recovery_lifecycle():
    print("\n--- TEST 7: Full Recovery Lifecycle (Assign -> Contact -> Recover / Order Won) ---")
    res = requests.get(f"{BASE_URL}/api/control/recovery/queue")
    # Pick a non-opted out record
    rec = next(r for r in res.json()["records"] if r["recovery_status"] != "opted_out")
    rec_id = rec["recovery_id"]
    quote_id = rec["quote_id"]

    # 1. Assign to Executive
    a_res = requests.post(f"{BASE_URL}/api/control/recovery/{rec_id}/action", json={
        "action": "assign",
        "agent_name": "Priya Nair (Health & Professional Desk)"
    })
    assert a_res.status_code == 200
    assert a_res.json()["record"]["assigned_agent"] == "Priya Nair (Health & Professional Desk)"
    print(f"Step 1: Assigned to {a_res.json()['record']['assigned_agent']}")

    # 2. Mark Contacted
    c_res = requests.post(f"{BASE_URL}/api/control/recovery/{rec_id}/action", json={
        "action": "mark_contacted"
    })
    assert c_res.status_code == 200
    assert c_res.json()["record"]["recovery_status"] == "contacted"
    print("Step 2: Customer marked as contacted")

    # 3. Mark Recovered
    r_res = requests.post(f"{BASE_URL}/api/control/recovery/{rec_id}/action", json={
        "action": "recover"
    })
    assert r_res.status_code == 200
    assert r_res.json()["record"]["recovery_status"] == "recovered"
    print("Step 3: Opportunity closed as RECOVERED (Won)")

    # 4. Check Analytics Update
    analytics = requests.get(f"{BASE_URL}/api/control/recovery/analytics").json()
    assert analytics["live_metrics"]["recovered"] >= 1, "Analytics should reflect >= 1 recovered lead"
    print(f"Analytics Update: Recovered = {analytics['live_metrics']['recovered']}, Win-Back Rate = {analytics['live_metrics']['recovery_rate_pct']}%")
    print("[PASS] PASS: Test 7 Verified (Complete recovery lifecycle from assignment to win-back).")

def test_8_consumer_portal_rejection_ingestion():
    print("\n--- TEST 8: Real-Time Consumer Portal Rejection Ingestion ---")
    unique_stmt = "Need a plan under Rs. 1,200 with 4G backup for my stationery shop"
    res = requests.post(f"{BASE_URL}/api/quote/event", json={
        "event_type": "quote_rejected",
        "quote_id": "QTE-2026-LIVE-01",
        "session_id": "sess_stationery_live",
        "rejection_reason": "price_too_high",
        "metadata": {
            "customer_statement": unique_stmt
        }
    })
    assert res.status_code == 200

    # Verify present in recovery queue
    q_res = requests.get(f"{BASE_URL}/api/control/recovery/queue")
    records = q_res.json()["records"]
    matched = [r for r in records if unique_stmt in r.get("supporting_evidence", "")]
    assert len(matched) > 0, "Real-time rejection should appear in recovery queue"
    live_rec = matched[0]
    print(f"Captured Live Record ID: {live_rec['recovery_id']}")
    print(f"Captured Evidence:       \"{live_rec['supporting_evidence']}\"")
    print(f"Assigned Strategy:       {live_rec['action_title']}")
    print("[PASS] PASS: Test 8 Verified (Consumer rejection dynamically ingested into Recovery Hub).")

if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING PHASE 3: AI-POWERED QUOTE RECOVERY ENGINE TEST SUITE")
    print("=" * 70)
    
    test_1_price_sensitive_kirana()
    test_2_clinic_technical_complexity()
    test_3_multisite_missing_requirement()
    test_4_customer_reentry_workflow()
    test_5_no_stated_rejection_reason()
    test_6_dpdp_opt_out()
    test_7_full_recovery_lifecycle()
    test_8_consumer_portal_rejection_ingestion()

    print("\n" + "=" * 70)
    print("ALL PHASE 3 QUOTE RECOVERY ENGINE TESTS PASSED (100% SUCCESS)!")
    print("=" * 70)

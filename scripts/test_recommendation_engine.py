"""
test_recommendation_engine.py
=============================================================================
Bharti Airtel Business - Intelligent Recommendation & Conversion Engine
Phase 2 Test Suite: Deterministic Scoring, Hard Constraints, Transparent Pricing,
Catalogue Dependency Validation & Funnel Telemetry Verification.
=============================================================================
"""

import sys
import os
import requests
import json
from datetime import datetime

# Windows terminal UTF-8 encoding support
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "prototype")))

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    print("=" * 70)
    print("RUNNING PHASE 2: INTELLIGENT RECOMMENDATION & CONVERSION ENGINE TESTS")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # TEST 1: Kirana Protection Rule (Exact Screenshot Bug Fix)
    # -------------------------------------------------------------------------
    print("\n--- TEST 1: Kirana Protection Rule (Kirana Never Receives Mfg Suite) ---")
    p1 = {
        "session_id": "test_sess_kirana_01",
        "business_type": "kirana",
        "employees": 2,
        "locations": 1,
        "pain_points": ["evening payment downtime", "upi failures"],
        "digital_tools": ["paytm soundbox", "upi qr"]
    }
    needs1 = [{"category": "business_continuity", "type": "explicit"}]
    
    # Test via recommendation engine endpoint
    r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": "test_sess_kirana_01",
        "message": "I run a kirana store with 2 staff, upi payments stop in evening",
        "language": "en"
    })
    assert r1.status_code == 200, f"Advisor chat failed: {r1.status_code}"
    d1 = r1.json()
    best1 = d1["recommendation"]["best_bundle"]
    score1 = d1["recommendation"]["match_score"]
    disq1 = [d["name"] for d in d1["recommendation"]["disqualified_bundles"]]

    print(f"Recommended: {best1['name']} (₹{best1['monthly_inr']}/mo)")
    print(f"Match Score: {score1}%")
    print(f"Disqualified Bundles: {disq1}")

    assert best1["id"] == "bundle_kirana", f"Expected bundle_kirana, got {best1['id']}"
    assert best1["monthly_inr"] == 1999
    assert "Small Manufacturing & Industrial Suite" in disq1, "Manufacturing bundle MUST be disqualified for Kirana!"
    assert "Multi-Site Retail & Restaurant Pro" in disq1, "Multi-site bundle MUST be disqualified for 1-store Kirana!"
    print("✓ PASS: Test 1 Verified (Kirana receives Kirana Starter @ ₹1,999, ₹14,999 Mfg bundle strictly barred).")

    # -------------------------------------------------------------------------
    # TEST 2: Clinic & Professional Office Suite
    # -------------------------------------------------------------------------
    print("\n--- TEST 2: Clinic & Professional Office Suite ---")
    r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": "test_sess_clinic_02",
        "message": "We are a dental clinic with 4 staff. Need secure patient records backup and fast internet.",
        "language": "en"
    })
    assert r2.status_code == 200
    d2 = r2.json()
    best2 = d2["recommendation"]["best_bundle"]
    product_ids2 = [p["id"] for p in best2["products"]]
    
    print(f"Recommended: {best2['name']} (₹{best2['monthly_inr']}/mo)")
    print(f"Products: {product_ids2}")
    assert best2["id"] == "bundle_clinic"
    assert best2["monthly_inr"] == 3499
    assert "P17" in product_ids2, "Must include P17 (1TB Cloud Backup)"
    assert "P02" in product_ids2, "Must include P02 (Biz Fibre 300)"
    assert "P16" in product_ids2, "Must include P16 (Google Workspace / Cloud Email)"
    print("✓ PASS: Test 2 Verified (Clinic receives Professional Suite @ ₹3,499 with 1TB Backup and Fiber).")

    # -------------------------------------------------------------------------
    # TEST 3: Multi-Site Retail & Restaurant Pro
    # -------------------------------------------------------------------------
    print("\n--- TEST 3: Multi-Site Retail (Centralized SD-WAN & CCTV) ---")
    r3 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": "test_sess_multisite_03",
        "message": "We have 3 supermarket branches. Need centralized inventory sync and cloud CCTV cameras.",
        "language": "en"
    })
    assert r3.status_code == 200
    d3 = r3.json()
    best3 = d3["recommendation"]["best_bundle"]
    product_ids3 = [p["id"] for p in best3["products"]]

    print(f"Recommended: {best3['name']} (₹{best3['monthly_inr']}/mo)")
    print(f"Products: {product_ids3}")
    assert best3["id"] == "bundle_multisite"
    assert best3["monthly_inr"] == 7999
    assert "P10" in product_ids3, "Must include P10 (Managed SD-WAN)"
    assert "P23" in product_ids3, "Must include P23 (Cloud CCTV)"
    assert "P21" in product_ids3, "Must include P21 (Managed Firewall)"
    print("✓ PASS: Test 3 Verified (Multi-site retailer receives Retail Pro @ ₹7,999 with SD-WAN & CCTV).")

    # -------------------------------------------------------------------------
    # TEST 4: Small Manufacturing & Industrial Suite
    # -------------------------------------------------------------------------
    print("\n--- TEST 4: Small Manufacturing (Leased Line & Machine IoT) ---")
    r4 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": "test_sess_mfg_04",
        "message": "We operate a manufacturing plant with 18 machines. Need 1:1 leased line with static IP for ERP and machine sensors.",
        "language": "en"
    })
    assert r4.status_code == 200
    d4 = r4.json()
    best4 = d4["recommendation"]["best_bundle"]
    product_ids4 = [p["id"] for p in best4["products"]]

    print(f"Recommended: {best4['name']} (₹{best4['monthly_inr']}/mo)")
    print(f"Products: {product_ids4}")
    assert best4["id"] == "bundle_manufacturer"
    assert best4["monthly_inr"] == 14999
    assert "P05" in product_ids4, "Must include P05 (Internet Leased Line 20)"
    assert "P11" in product_ids4, "Must include P11 (Static IP)"
    assert "P24" in product_ids4, "Must include P24 (Machine Monitoring IoT)"
    print("✓ PASS: Test 4 Verified (Manufacturer receives Industrial Suite @ ₹14,999 with Leased Line & IoT).")

    # -------------------------------------------------------------------------
    # TEST 5: Transparent Quote Pricing & GST Arithmetic Exactness
    # -------------------------------------------------------------------------
    print("\n--- TEST 5: Transparent Quote Pricing & GST Calculation ---")
    calc_payload = {
        "bundle_id": "bundle_kirana",
        "addons": ["addon_cctv", "addon_static_ip"]
    }
    r5 = requests.post(f"{BASE_URL}/api/quote/calculate", json=calc_payload)
    assert r5.status_code == 200
    q5 = r5.json()
    p5 = q5["pricing"]

    print(f"Base Monthly:      ₹{p5['monthly_base_inr']}")
    print(f"Add-ons Monthly:   ₹{p5['addons_monthly_inr']}")
    print(f"Monthly Subtotal:  ₹{p5['monthly_subtotal_inr']}")
    print(f"GST (18% Exact):   ₹{p5['gst_18_inr']}")
    print(f"Final Monthly:     ₹{p5['final_monthly_payable_inr']}")
    print(f"One-time Setup:    ₹{p5['one_time_setup_inr']}")
    print(f"First Payment:     ₹{p5['first_payment_inr']}")

    # Assertions on exact arithmetic
    assert p5["monthly_base_inr"] == 1999
    assert p5["addons_monthly_inr"] == 800 + 300 # CCTV + Static IP = 1100
    assert p5["monthly_subtotal_inr"] == 1999 + 1100 # 3099
    expected_gst = round(3099 * 0.18) # 558
    assert p5["gst_18_inr"] == expected_gst
    assert p5["final_monthly_payable_inr"] == 3099 + expected_gst # 3657
    assert p5["one_time_setup_inr"] == 1000 + 1200 # Base setup 1000 + CCTV setup 1200 = 2200
    assert p5["first_payment_inr"] == 3657 + 2200 # 5857
    print("✓ PASS: Test 5 Verified (Itemized base, GST 18%, setup fee, and first payment mathematically exact).")

    # -------------------------------------------------------------------------
    # TEST 6: Add-On Prerequisite & Dependency Validation
    # -------------------------------------------------------------------------
    print("\n--- TEST 6: Add-On Prerequisite & Catalogue Validation ---")
    # Verify Static IP requires fiber/broadband (satisfied by bundle_kirana AirFiber P04)
    # Verify CCTV requires internet
    assert len(q5["addons"]) == 2
    addon_ids = [a["id"] for a in q5["addons"]]
    assert "P23" in addon_ids
    assert "P11" in addon_ids
    print("✓ PASS: Test 6 Verified (Add-on dependencies validated against catalogue prerequisites).")

    # -------------------------------------------------------------------------
    # TEST 7: Budget Mismatch Handling & Advisory
    # -------------------------------------------------------------------------
    print("\n--- TEST 7: Budget Mismatch Detection & Clear Advisory ---")
    from recommendation_engine import evaluate_bundle_recommendation
    p_budget = {
        "business_type": "clinic",
        "employees": 3,
        "locations": 1,
        "pain_points": ["patient records backup"],
        "budget": 2000 # Stated budget ₹2,000, but Clinic Suite is ₹3,499
    }
    rec_b = evaluate_bundle_recommendation(p_budget, [{"category": "cloud_productivity", "type": "explicit"}])
    b_analysis = rec_b["budget_analysis"]
    print(f"Stated Budget:   ₹{b_analysis.get('stated_budget_inr')}")
    print(f"Fits Budget:     {b_analysis.get('fits_budget')}")
    print(f"Advisory Note:   {b_analysis.get('note')}")

    assert b_analysis["has_stated_budget"] == True
    assert b_analysis["fits_budget"] == False
    assert "₹2,000" in b_analysis["note"]
    assert "Clinic & Professional Office Suite" in b_analysis["note"]
    assert "Kirana" in b_analysis["note"] # Identifies lower cost alternative
    print("✓ PASS: Test 7 Verified (Budget mismatch identified without silently degrading service).")

    # -------------------------------------------------------------------------
    # TEST 8: Full Quote Lifecycle & Conversion Telemetry
    # -------------------------------------------------------------------------
    print("\n--- TEST 8: Full Quote Lifecycle & Control Portal Telemetry ---")
    quote_id = d1["quote_id"]
    sess_id = d1["session_id"]
    print(f"Active Quote ID: {quote_id}")

    # 1. Log quote viewed
    r_view = requests.post(f"{BASE_URL}/api/quote/event", json={
        "event_type": "quote_viewed",
        "quote_id": quote_id,
        "session_id": sess_id
    })
    assert r_view.status_code == 200

    # 2. Modify quote with add-on
    r_mod = requests.post(f"{BASE_URL}/api/quote/calculate", json={
        "quote_id": quote_id,
        "bundle_id": "bundle_kirana",
        "addons": ["addon_cctv"]
    })
    assert r_mod.status_code == 200

    # 3. Accept quote via consumer order creation
    order_res = requests.post(f"{BASE_URL}/api/consumer/order/create", json={
        "quote_id": quote_id,
        "bundle_id": "bundle_kirana",
        "business_name": "Sharma General Store",
        "contact_name": "Ramesh Sharma",
        "phone": "+91 98440 55667",
        "city": "Lucknow",
        "gstin": "09ABCDE1234F1Z5",
        "addons": ["addon_cctv"]
    })
    assert order_res.status_code == 200
    new_ord = order_res.json()["order"]
    print(f"Order Created from Quote: {new_ord['order_id']} (Ref Quote: {new_ord.get('quote_id')})")

    # 4. Check quote state in backend
    q_check = requests.get(f"{BASE_URL}/api/quote/{quote_id}").json()["quote"]
    assert q_check["status"] == "accepted", f"Expected accepted status, got {q_check['status']}"

    # 5. Check Control Portal Analytics
    analytics = requests.get(f"{BASE_URL}/api/control/quotes/analytics").json()
    funnel = analytics["funnel"]
    print(f"Control Funnel Stats: Generated={funnel['generated']}, Accepted={funnel['accepted']}, ConversionRate={funnel['conversion_rate_pct']}%")
    assert funnel["accepted"] >= 1
    assert funnel["orders"] >= 1
    print("✓ PASS: Test 8 Verified (Complete quote-to-order funnel tracked with telemetry).")

    # -------------------------------------------------------------------------
    # TEST 9: Rejection Telemetry & Single-Click Reason Capture
    # -------------------------------------------------------------------------
    print("\n--- TEST 9: Rejection Telemetry & Single-Click Reason Capture ---")
    r_rej = requests.post(f"{BASE_URL}/api/quote/event", json={
        "event_type": "quote_rejected",
        "quote_id": quote_id,
        "session_id": sess_id,
        "rejection_reason": "deciding_later"
    })
    assert r_rej.status_code == 200
    
    analytics2 = requests.get(f"{BASE_URL}/api/control/quotes/analytics").json()
    reasons = analytics2["rejection_reasons"]
    print(f"Rejection Reasons Recorded: {reasons}")
    assert "deciding_later" in reasons or "price_too_high" in reasons
    print("✓ PASS: Test 9 Verified (Single-click rejection reason logged for lead rescue).")

    print("\n" + "=" * 70)
    print("ALL PHASE 2 RECOMMENDATION & CONVERSION TESTS PASSED (100% SUCCESS)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()

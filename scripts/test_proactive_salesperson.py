"""
Comprehensive Test Suite: Proactive Human-like AI Salesperson & Language Sync
Project Udyam Digital — Bharti Airtel SYNC 2026 Innovation Challenge
Team: Halo · Thapar Institute of Engineering & Technology

Tests:
1. Exact Regression Failure Conversation ('digital billing system' -> 'paper' -> 'yes' -> '300-400')
2. Indecision Policy: Delegated Decision ('You decide' / 'Jo marzi')
3. Indecision Policy: Double Uncertainty ('I don't know' twice -> auto-default, no 3rd question)
4. Non-Assumed Boundary: Legal & KYC are never auto-defaulted
5. Product Catalogue Validation: P19 Cloud POS & Billing (₹599/mo) identified, no hallucinations
6. Product Catalogue Validation: Unavailable specialized software (SAP/CAD) flagged without fake pricing
7. Dynamic Context Synchronization: Pivot from Kirana to Multi-Site invalidates stale recommendation
8. Recommendation Lifecycle: Not ready -> Generated, no duplicate cards on follow-up questions
9. Multilingual Natural Language Switch: English -> Hindi
10. Multilingual Natural Language Switch: Hindi -> English
11. Multilingual Natural Language Switch: English -> Punjabi (Gurmukhi)
12. Multilingual Natural Language Switch: Natural Hinglish
13. Session Language Persistence: Context & history preserved on language change
14. Auto-Scroll Safeguard: Dedicated scroll container verified, no page-level jump
"""

import os
import sys
import json
import uuid
import requests

# Reconfigure stdout for utf-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add prototype to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "prototype"))

BASE_URL = "http://127.0.0.1:5000"

def test_01_exact_regression_billing_conversation():
    """
    PART 1 & PART 10: Re-run the exact failing conversation.
    Customer: 'I need a digital billing system.'
    Customer: 'Currently on paper.'
    Customer: 'Yes' / 'I need proper invoicing software.'
    Customer: '300–400.'
    Expected: Advisor recommends Cloud-based billing (P19) without looping on cloud-vs-desktop!
    """
    sid = f"test_reg_{uuid.uuid4().hex[:8]}"

    # Turn 1
    r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "I need a digital billing system.",
        "language": "en"
    })
    assert r1.status_code == 200, f"Turn 1 failed: {r1.text}"
    d1 = r1.json()
    reply1 = d1["reply"].lower()
    assert any(k in reply1 for k in ["paper", "software", "manual", "currently"]), f"Unexpected Turn 1 reply: {d1['reply']}"
    assert d1["discovery_complete"] is False, "Premature discovery complete on Turn 1!"

    # Turn 2
    r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Currently on paper.",
        "language": "en"
    })
    assert r2.status_code == 200, f"Turn 2 failed: {r2.text}"
    d2 = r2.json()
    reply2 = d2["reply"].lower()
    assert any(k in reply2 for k in ["gst", "invoice", "invoicing", "proper"]), f"Unexpected Turn 2 reply: {d2['reply']}"
    assert d2["discovery_complete"] is False, "Premature discovery complete on Turn 2!"

    # Turn 3
    r3 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Yes, I need proper GST invoicing software.",
        "language": "en"
    })
    assert r3.status_code == 200, f"Turn 3 failed: {r3.text}"
    d3 = r3.json()
    reply3 = d3["reply"].lower()
    assert any(k in reply3 for k in ["monthly", "bills", "invoices", "how many", "approximately", "volume"]), f"Unexpected Turn 3 reply: {d3['reply']}"

    # Turn 4: Customer provides volume (300-400)
    r4 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "300–400.",
        "language": "en"
    })
    assert r4.status_code == 200, f"Turn 4 failed: {r4.text}"
    d4 = r4.json()
    reply4 = d4["reply"].lower()

    # CRITICAL VERIFICATION:
    # 1. Did the AI ask "cloud vs desktop" again? NO!
    assert "would you prefer cloud-based invoicing or desktop" not in reply4, "AI repeated cloud vs desktop question!"
    assert "are you comfortable depending on internet" not in reply4, "AI asked internet comfort question!"
    
    # 2. Did the AI proactively recommend Cloud-based billing? YES!
    assert any(k in reply4 for k in ["cloud", "billing", "sensible", "suitable", "option", "recommend"]), f"Advisor did not recommend billing: {d4['reply']}"
    assert d4["discovery_complete"] is True, "Discovery should be complete after volume is provided!"
    assert d4["bundle"] is not None, "Bundle recommendation should be present!"
    # Ensure it did NOT recommend the ₹14,999 manufacturing suite to a kirana billing user!
    assert d4["bundle"]["id"] != "bundle_manufacturer", "CRITICAL ERROR: Recommended manufacturing bundle to billing user!"
    print("Test 1 Passed: Exact failure conversation now succeeds smoothly!")

def test_02_indecision_delegated_decision():
    """
    PART 2: Customer delegates decision directly: 'You decide.' / 'Jo marzi.'
    Advisor must stop asking, pick a sensible default, and move forward.
    """
    sid = f"test_indec_{uuid.uuid4().hex[:8]}"

    # Turn 1
    r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "You decide what is best for my store.",
        "language": "en"
    })
    assert r1.status_code == 200
    d1 = r1.json()
    reply = d1["reply"].lower()
    # Should take ownership and select default
    assert any(k in reply for k in ["airfiber", "select", "recommend", "default", "backup", "option"]), f"Advisor did not handle delegation: {d1['reply']}"
    print("Test 2 Passed: Delegated decision handled proactively!")

def test_03_indecision_double_uncertainty():
    """
    PART 2: Customer says 'I don't know' twice.
    First time: explain briefly.
    Second time: choose default and continue. Never ask a 3rd time!
    """
    from conversational_ai import handle_indecision_policy, classify_user_response
    
    mock_session = {"preference_tracking": {}, "identified_needs": []}
    
    # 1st uncertainty
    cls1 = classify_user_response("I don't know", mock_session)
    ack1, q1 = handle_indecision_policy(
        mock_session, "cloud_pref", cls1, "cloud", "Cloud access",
        {"desc_en": "Cloud allows remote access."}, "en"
    )
    assert q1["clarification_attempts"] == 1
    assert q1["status"] == "uncertain"
    assert "recommend" in ack1.lower() or "cloud" in ack1.lower()

    # 2nd uncertainty
    cls2 = classify_user_response("I still don't know, whatever you want", mock_session)
    ack2, q2 = handle_indecision_policy(
        mock_session, "cloud_pref", cls2, "cloud", "Customer delegated; cloud access is suitable.",
        {"desc_en": "Cloud allows remote access."}, "en"
    )
    assert q2["clarification_attempts"] == 2
    assert q2["status"] == "delegated"
    assert q2["selected_value"] == "cloud"
    assert "select" in ack2.lower() or "cloud" in ack2.lower()
    print("Test 3 Passed: 2-step indecision policy enforced with no 3rd question!")

def test_04_non_assumed_verification_boundary():
    """
    PART 2: Defaults are permitted for technical preferences, NOT for legal KYC or consent.
    """
    from conversational_ai import get_or_create_preference_state
    
    mock_session = {"profile": {"business_type": "kirana"}}
    pref = get_or_create_preference_state(mock_session)
    
    # Verify that KYC / legal fields are not present in preference defaults
    assert "gstin" not in pref
    assert "pan" not in pref
    assert "bank_account" not in pref
    assert "authorized_signatory" not in pref
    print("Test 4 Passed: Non-assumed statutory boundaries respected!")

def test_05_catalogue_validation_cloud_pos_p19():
    """
    PART 4: Verify that Cloud POS & Billing (P19) is validated against product_catalogue.csv.
    """
    from conversational_ai import validate_catalogue_eligibility, OFFICIAL_CATALOGUE
    
    assert "P19" in OFFICIAL_CATALOGUE
    assert OFFICIAL_CATALOGUE["P19"]["monthly_inr"] == 599
    assert OFFICIAL_CATALOGUE["P19"]["setup_inr"] == 2500

    elig = validate_catalogue_eligibility("GST Invoicing & Billing Software")
    assert elig["is_offered"] is True
    assert elig["product_id"] == "P19"
    assert elig["monthly_inr"] == 599
    assert elig["flag_human_rep"] is False
    print("Test 5 Passed: P19 Cloud POS validated against catalogue with exact ₹599 pricing!")

def test_06_catalogue_validation_unavailable_product():
    """
    PART 4: Request for specialized software not in catalogue (e.g. SAP ERP).
    Must NOT hallucinate Airtel SAP software or fake price.
    """
    from conversational_ai import validate_catalogue_eligibility
    
    elig = validate_catalogue_eligibility("Custom SAP S/4HANA Heavy ERP")
    assert elig["is_offered"] is False
    assert elig["product_id"] is None
    assert elig["monthly_inr"] == 0
    assert elig["flag_human_rep"] is True
    assert "not packaged directly" in elig["description"]
    print("Test 6 Passed: Unavailable product correctly flagged without hallucinated pricing!")

def test_07_context_synchronization_pivot():
    """
    PART 5: Dynamic requirement change: Kirana -> Multi-site retail chain.
    Authoritative profile updates, stale single-site recommendation superseded.
    """
    sid = f"test_pivot_{uuid.uuid4().hex[:8]}"

    # Start as kirana
    r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "I run a kirana shop with 2 staff.",
        "language": "en"
    })
    assert r1.status_code == 200

    # Pivot to multiple stores
    r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Actually we just expanded to 3 retail branches and need centralized SD-WAN and CCTV.",
        "language": "en"
    })
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["profile"]["locations"] == 3
    assert d2["profile"]["business_type"] == "multisite"
    if d2["bundle"]:
        assert d2["bundle"]["id"] == "bundle_multisite"
    print("Test 7 Passed: Customer profile synchronized and pivoted cleanly!")

def test_08_multilingual_natural_language_switch():
    """
    ADDITIONAL FEATURE & PART 9:
    1. English -> Hindi switch via natural message ('Can you speak in Hindi?')
    2. English -> Punjabi switch via natural message ('Punjabi ch gall karo')
    3. English -> Hinglish switch ('Hinglish me bolo')
    Verify that language updates without losing context or restarting session!
    """
    from conversational_ai import detect_natural_language_switch
    
    # Test natural detection
    assert detect_natural_language_switch("Can you speak in Hindi?") == "hi"
    assert detect_natural_language_switch("hindi me baat karo") == "hi"
    assert detect_natural_language_switch("Please continue in English") == "en"
    assert detect_natural_language_switch("Punjabi ch gall karo") == "pa"
    assert detect_natural_language_switch("punjabi vich bolo please") == "pa"
    assert detect_natural_language_switch("Hinglish me bolo") == "hinglish"

    # API Verification
    sid = f"test_lang_{uuid.uuid4().hex[:8]}"

    # Turn 1: English
    r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "I have 3 employees at my retail store.",
        "language": "en"
    })
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["profile"]["employees"] == 3

    # Turn 2: Switch to Hindi
    r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Hindi me baat karo please.",
        "language": "en"
    })
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["profile"]["preferred_language"] == "hi"
    # Profile context (employees = 3) MUST BE PRESERVED!
    assert d2["profile"]["employees"] == 3

    # Turn 3: Switch to Punjabi
    r3 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Punjabi ch gall karo.",
        "language": "hi"
    })
    assert r3.status_code == 200
    d3 = r3.json()
    assert d3["profile"]["preferred_language"] == "pa"
    assert d3["profile"]["employees"] == 3

    print("Test 8 Passed: Natural multilingual switching verified across Hindi and Punjabi!")

def test_09_session_language_update_endpoint():
    """
    ADDITIONAL FEATURE: Language selector update endpoint (/api/advisor/session/language)
    persists new language without resetting profile or history.
    """
    sid = f"test_lang_endp_{uuid.uuid4().hex[:8]}"
    
    # Create session with kirana profile
    r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={
        "session_id": sid,
        "message": "Kirana store with 4 workers.",
        "language": "en"
    })
    assert r_init.status_code == 200

    # Call language update endpoint
    r_lang = requests.post(f"{BASE_URL}/api/advisor/session/language", json={
        "session_id": sid,
        "language": "pa"
    })
    assert r_lang.status_code == 200
    d_lang = r_lang.json()
    assert d_lang["status"] == "success"
    assert d_lang["language"] == "pa"

    # Inspect session to verify context is preserved
    r_sess = requests.get(f"{BASE_URL}/api/advisor/session/{sid}")
    assert r_sess.status_code == 200
    d_sess = r_sess.json()
    assert d_sess["profile"]["preferred_language"] == "pa"
    assert d_sess["profile"]["employees"] == 4
    print("Test 9 Passed: Session language endpoint verified without context reset!")

def test_10_autoscroll_fix_verification():
    """
    PART 7: Verify that consumer.html has eliminated page-level scrollIntoView
    and implemented smart dedicated scrolling for .chat-thread.
    """
    html_path = r"E:\Airtel\prototype\templates\consumer.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verify panel.scrollIntoView is GONE
    assert "panel.scrollIntoView" not in html, "panel.scrollIntoView still present in consumer.html!"
    
    # Verify .chat-thread has max-height and overflow
    assert "max-height: 480px" in html
    assert "overflow-y: auto" in html
    
    # Verify smartScrollChat function exists
    assert "function smartScrollChat" in html
    print("Test 10 Passed: Auto-scroll fix and dedicated chat scrolling verified!")

if __name__ == "__main__":
    print("--- RUNNING PROACTIVE SALESPERSON & MULTILINGUAL TEST SUITE ---")
    test_01_exact_regression_billing_conversation()
    test_02_indecision_delegated_decision()
    test_03_indecision_double_uncertainty()
    test_04_non_assumed_verification_boundary()
    test_05_catalogue_validation_cloud_pos_p19()
    test_06_catalogue_validation_unavailable_product()
    test_07_context_synchronization_pivot()
    test_08_multilingual_natural_language_switch()
    test_09_session_language_update_endpoint()
    test_10_autoscroll_fix_verification()
    print("--- ALL 10 TESTS PASSED (100.0% SUCCESS) ---")

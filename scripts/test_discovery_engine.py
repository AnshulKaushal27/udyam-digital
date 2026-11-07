import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://127.0.0.1:5000"

def send_chat(session_id, category, message, lang="en"):
    """Helper to stream chat and parse chunks and metadata."""
    url = f"{BASE_URL}/api/advisor/chat/stream"
    payload = {
        "session_id": session_id,
        "category": category,
        "language": lang,
        "messages": [{"role": "user", "content": message}]
    }
    resp = requests.post(url, json=payload, stream=True, timeout=15)
    assert resp.status_code == 200, f"Chat failed: {resp.status_code}"

    chunks = []
    meta = None
    for line in resp.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                event = json.loads(decoded[6:])
                if event.get("type") == "chunk":
                    chunks.append(event.get("text", ""))
                elif event.get("type") == "meta":
                    meta = event.get("data")
    
    return "".join(chunks).strip(), meta

def run_tests():
    print("=" * 70)
    print("RUNNING 10-SCENARIO INTELLIGENT DISCOVERY ENGINE TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # Scenario 1: Kirana owner with frequent UPI downtime
    # -------------------------------------------------------------
    print("\n--- TEST 1: Kirana Owner with Frequent UPI Downtime ---")
    s1 = "sess_test_kirana_01"
    text, meta = send_chat(s1, "kirana", "Meri kirana shop hai 3 staff ke saath aur evening rush me UPI QR payments ruk jate hain", "hinglish")
    print(f"Advisor: {text}")
    print(f"Needs: {[n['category'] + ':' + n['classified_requirement'] for n in meta['identified_needs']]}")
    assert meta["profile"]["employees"] == 3, f"Expected 3 employees, got {meta['profile']['employees']}"
    assert any(n["category"] == "business_continuity" for n in meta["identified_needs"]), "Must classify business_continuity"
    assert meta["recommend_bundle"] == "bundle_kirana"
    print(" PASS: Test 1 Verified (Business continuity need identified, bundle_kirana recommended).")

    # -------------------------------------------------------------
    # Scenario 2: Clinic with patient record backup requirements
    # -------------------------------------------------------------
    print("\n--- TEST 2: Clinic with Patient Record Backup ---")
    s2 = "sess_test_clinic_02"
    text, meta = send_chat(s2, "clinic", "We are a dental clinic with 2 doctors. Protecting patient records with secure encrypted cloud backup is critical for us.", "en")
    print(f"Advisor: {text}")
    print(f"Needs: {[n['category'] + ':' + n['classified_requirement'] for n in meta['identified_needs']]}")
    assert any(n["category"] == "cloud_productivity" for n in meta["identified_needs"]), "Must classify cloud_productivity"
    assert meta["recommend_bundle"] == "bundle_clinic"
    print(" PASS: Test 2 Verified (Cloud & productivity need identified, bundle_clinic recommended).")

    # -------------------------------------------------------------
    # Scenario 3: CA office requiring professional email
    # -------------------------------------------------------------
    print("\n--- TEST 3: CA Office Requiring Professional Email ---")
    s3 = "sess_test_ca_03"
    text, meta = send_chat(s3, "clinic", "We run a CA accounting office with 6 staff. We need official custom domain email and high speed fiber for tax filings.", "en")
    print(f"Advisor: {text}")
    assert meta["profile"]["employees"] == 6
    assert any(n["category"] in ["cloud_productivity", "connectivity"] for n in meta["identified_needs"])
    assert meta["recommend_bundle"] == "bundle_clinic"
    print(" PASS: Test 3 Verified (CA firm profile captured, bundle_clinic recommended).")

    # -------------------------------------------------------------
    # Scenario 4: Three-store retailer needing centralized networking
    # -------------------------------------------------------------
    print("\n--- TEST 4: Three-Store Retailer Needing Centralized Networking ---")
    s4 = "sess_test_multi_04"
    text, meta = send_chat(s4, "multisite", "I manage 3 retail stores across Mumbai. We need SD-WAN connectivity, central billing and cloud CCTV on one single invoice.", "en")
    print(f"Advisor: {text}")
    assert meta["profile"]["locations"] == 3
    assert any(n["category"] == "multi_location_networking" for n in meta["identified_needs"])
    assert meta["recommend_bundle"] == "bundle_multisite"
    print(" PASS: Test 4 Verified (Multi-location networking identified, bundle_multisite recommended).")

    # -------------------------------------------------------------
    # Scenario 5: Small manufacturer requiring ERP connectivity
    # -------------------------------------------------------------
    print("\n--- TEST 5: Small Manufacturer Requiring ERP Connectivity ---")
    s5 = "sess_test_mfg_05"
    text, meta = send_chat(s5, "manufacturer", "We operate an auto components plant with 25 workers. We require a dedicated 1:1 leased line and static IP for our remote ERP server and machine IoT sensors.", "en")
    print(f"Advisor: {text}")
    assert meta["profile"]["employees"] == 25
    assert any(n["category"] == "industrial_iot" for n in meta["identified_needs"])
    assert meta["recommend_bundle"] == "bundle_manufacturer"
    print(" PASS: Test 5 Verified (Industrial IoT and dedicated leased line identified, bundle_manufacturer recommended).")

    # -------------------------------------------------------------
    # Scenario 6: Customer who only responds in Hindi
    # -------------------------------------------------------------
    print("\n--- TEST 6: Customer Who Only Responds in Hindi ---")
    s6 = "sess_test_hindi_06"
    text, meta = send_chat(s6, "kirana", "नमस्ते, मेरी छोटी दुकान में 2 लड़के काम करते हैं और शाम को UPI बंद हो जाता है।", "hi")
    print(f"Advisor: {text}")
    assert meta["profile"]["employees"] == 2
    assert meta["recommend_bundle"] == "bundle_kirana"
    print(" PASS: Test 6 Verified (Hindi processed naturally, Kirana bundle recommended).")

    # -------------------------------------------------------------
    # Scenario 7: Customer who switches between Hindi and English
    # -------------------------------------------------------------
    print("\n--- TEST 7: Customer Who Switches Between Hindi and English ---")
    s7 = "sess_test_switch_07"
    # Step 1: English
    t1, m1 = send_chat(s7, "kirana", "Hello, we have 4 staff members in our pharmacy store.", "en")
    print(f"Turn 1 (EN): {t1}")
    assert m1["profile"]["employees"] == 4
    # Step 2: Switch to Hindi/Hinglish
    t2, m2 = send_chat(s7, "kirana", "Bhaiya internet bohot slow hai, payment fail hoti hai shaam ko. Koi solution batao.", "hinglish")
    print(f"Turn 2 (HI): {t2}")
    assert m2["profile"]["employees"] == 4, "Should retain 4 staff from previous English turn!"
    assert any(n["category"] == "business_continuity" for n in m2["identified_needs"])
    assert m2["discovery_status"] == "complete"
    print(" PASS: Test 7 Verified (Seamless language switching with memory continuity).")

    # -------------------------------------------------------------
    # Scenario 8: Customer who changes requirements halfway through
    # -------------------------------------------------------------
    print("\n--- TEST 8: Customer Changes Requirements Halfway Through ---")
    s8 = "sess_test_change_08"
    t1, m1 = send_chat(s8, "kirana", "I have a single retail store with 2 people.", "en")
    print(f"Turn 1: {t1}")
    assert m1["profile"]["locations"] == 1
    # Change halfway:
    t2, m2 = send_chat(s8, "kirana", "Actually we just finalized leases for 2 more branches, so we will operate 3 stores next month and need centralized networking and CCTV. Please suggest the best package.", "en")
    print(f"Turn 2: {t2}")
    assert m2["profile"]["locations"] in [2, 3]
    assert m2["profile"]["business_type"] == "multisite", "Should pivot business_type to multisite!"
    assert m2["recommend_bundle"] == "bundle_multisite"
    print(" PASS: Test 8 Verified (Dynamic requirement pivot handled gracefully).")

    # -------------------------------------------------------------
    # Scenario 9: Customer who gives incomplete information
    # -------------------------------------------------------------
    print("\n--- TEST 9: Customer Gives Incomplete Information ---")
    s9 = "sess_test_incomplete_09"
    t1, m1 = send_chat(s9, "kirana", "Not sure", "en")
    print(f"Advisor: {t1}")
    assert m1["discovery_status"] == "in_progress", "Must remain in_progress and ask clarifying question!"
    assert len(m1["quick_replies"]) > 0, "Must provide guiding quick reply options"
    print(" PASS: Test 9 Verified (Incomplete answer handled with guidance chips without crashing).")

    # -------------------------------------------------------------
    # Scenario 10: Customer asks an unrelated question
    # -------------------------------------------------------------
    print("\n--- TEST 10: Customer Asks Unrelated Question ---")
    s10 = "sess_test_unrelated_10"
    t1, m1 = send_chat(s10, "kirana", "Do you guys offer services on Sundays?", "en")
    print(f"Advisor: {t1}")
    assert len(t1) > 0
    # Customer follows up with actual needs
    t2, m2 = send_chat(s10, "kirana", "Okay great. We have 3 staff and card swipe machines.", "en")
    print(f"Turn 2: {t2}")
    assert m2["profile"]["employees"] == 3
    print(" PASS: Test 10 Verified (Unrelated question answered politely without derailing flow).")

    # -------------------------------------------------------------
    # Verify Session Isolation (s1 vs s2)
    # -------------------------------------------------------------
    print("\n--- TEST 11: Session Isolation Check ---")
    r1 = requests.get(f"{BASE_URL}/api/advisor/session/{s1}").json()
    r2 = requests.get(f"{BASE_URL}/api/advisor/session/{s2}").json()
    assert r1["profile"]["business_type"] == "kirana"
    assert r2["profile"]["business_type"] == "clinic"
    assert r1["profile"]["employees"] == 3
    assert r2["profile"]["employees"] == 2
    print(" PASS: Session Isolation Verified (Sessions s1 and s2 maintained completely separate states).")

    print("\n" + "=" * 70)
    print("ALL 10 DISCOVERY SCENARIOS & SESSION ISOLATION PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()

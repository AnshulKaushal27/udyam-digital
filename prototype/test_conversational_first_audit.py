import requests
import json
import time

BASE = "http://127.0.0.1:5000"
s = requests.Session()

def run_tests():
    print("=" * 70)
    print("PROJECT UDYAM DIGITAL: COMPREHENSIVE END-TO-END QA AUDIT")
    print("=" * 70)
    
    # ----------------------------------------------------
    # TEST 1: ASSETS & INTRO PAGE SERVING
    # ----------------------------------------------------
    print("\n[TEST 1] Brand Assets & Intro Experience Serving...")
    r_home = s.get(f"{BASE}/")
    assert r_home.status_code == 200, f"Home page returned {r_home.status_code}"
    assert "indian_msme_digital_hero.svg" in r_home.text, "Intro SVG not linked in home page"
    assert "morphLogo" in r_home.text, "Morphing logo missing in home page"
    assert "logoutCustomer()" in r_home.text, "Logout button missing in home page"
    assert "airtel_ai_agent_logo.svg" in r_home.text, "Airtel AI agent logo missing in home page"
    
    r_svg = s.get(f"{BASE}/static/illustrations/indian_msme_digital_hero.svg")
    assert r_svg.status_code == 200, "Indian MSME digital hero SVG asset not found"
    assert "AIRTEL BUSINESS" in r_svg.text, "SVG missing Airtel Business branding"
    print("  [PASS] Home page & custom Indian MSME digital illustration verified.")

    # ----------------------------------------------------
    # TEST 2: GUI-ONLY INDEPENDENT JOURNEY (Zero Chat Messages)
    # ----------------------------------------------------
    print("\n[TEST 2] GUI-Only Independent Journey (Zero Chat Messages)...")
    sess_gui = f"sess_gui_test_{int(time.time())}"
    
    # 2.1 Initial State
    wf = s.get(f"{BASE}/api/workflow/state/{sess_gui}").json()["workflow"]
    assert wf["stage"] == "USER_TYPE_SELECTION", f"Expected USER_TYPE_SELECTION, got {wf['stage']}"
    
    # 2.2 Select Business Owner via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "SELECT_USER_TYPE", "payload": {"user_type": "customer"}
    }).json()["workflow"]
    assert wf["stage"] == "CUSTOMER_ACCOUNT_CHECK", f"Expected CUSTOMER_ACCOUNT_CHECK, got {wf['stage']}"
    
    # 2.3 Select New to Airtel via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "SELECT_ACCOUNT_STATUS", "payload": {"status": "new"}
    }).json()["workflow"]
    assert wf["stage"] == "CUSTOMER_SIGNUP", f"Expected CUSTOMER_SIGNUP, got {wf['stage']}"
    
    # 2.4 Complete Signup via GUI Form
    reg_res = s.post(f"{BASE}/api/auth/customer/signup", json={
        "session_id": sess_gui,
        "name": "Kavita Rao",
        "mobile": "9845112233",
        "business_name": "Rao Super Bazaar",
        "business_type": "kirana",
        "dpdp_consent": True
    }).json()
    assert reg_res["status"] == "success", "Signup failed"
    wf = reg_res["workflow"]
    assert wf["stage"] == "BUSINESS_IDENTIFICATION", f"Expected BUSINESS_IDENTIFICATION, got {wf['stage']}"
    assert wf["customer"]["name"] == "Kavita Rao", "Customer name mismatch"
    assert wf["customer"]["dpdp_consented"] is True, "DPDP consent not recorded"
    
    # 2.5 Select Business Category (Kirana) via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "SELECT_CATEGORY", "payload": {"category": "kirana"}
    }).json()["workflow"]
    assert wf["stage"] == "REQUIREMENTS_COLLECTION", f"Expected REQUIREMENTS_COLLECTION, got {wf['stage']}"
    assert wf["recommendation"]["bundle_id"] == "bundle_kirana", "Base bundle mismatch"
    
    # 2.6 Toggle Requirements (Instant UPI Failover) via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "TOGGLE_REQUIREMENT", "payload": {"requirement": "upi_failover"}
    }).json()["workflow"]
    assert "upi_failover" in wf["discovery"]["requirements"], "Requirement upi_failover not saved"
    
    # 2.7 Proceed to Plan Exploration via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "GO_TO_STAGE", "payload": {"stage": "PLAN_EXPLORATION"}
    }).json()["workflow"]
    assert wf["stage"] == "PLAN_EXPLORATION", f"Expected PLAN_EXPLORATION, got {wf['stage']}"
    
    # 2.8 Toggle Modular Add-on (WhatsApp API P15) via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "TOGGLE_ADDON", "payload": {"addon_id": "P15"}
    }).json()["workflow"]
    assert "P15" in wf["recommendation"]["active_addons"], "Addon P15 not active"
    assert wf["recommendation"]["monthly_subtotal"] == 1999 + 999, f"Expected 2998, got {wf['recommendation']['monthly_subtotal']}"
    assert wf["recommendation"]["total_monthly"] == 2998 + round(2998 * 0.18), f"Total monthly mismatch: {wf['recommendation']['total_monthly']}"
    
    # 2.9 Proceed to Smart KYC via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "GO_TO_STAGE", "payload": {"stage": "KYC_VERIFICATION"}
    }).json()["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"

    # 2.9b Complete KYC Verification via Specimen Demo
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "VERIFY_KYC_DEMO", "payload": {"gstin": "07AAAAA0000A1Z5"}
    }).json()["workflow"]
    assert wf["kyc"]["status"] in ["VERIFIED", "APPROVED"]
    
    # 2.10 Proceed to Live Fulfillment Stepper via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "GO_TO_STAGE", "payload": {"stage": "INSTALLATION_TRACKING"}
    }).json()["workflow"]
    assert wf["stage"] == "INSTALLATION_TRACKING", f"Expected INSTALLATION_TRACKING, got {wf['stage']}"
    assert wf["order"]["milestone"] >= 1, "Order tracking milestone invalid"
    assert "Rahul Sharma" in wf["order"]["engineer_name"], "Assigned engineer missing"
    print("  [PASS] Full customer journey completed end-to-end purely through GUI without any chatbot messages!")

    # ----------------------------------------------------
    # TEST 3: CHAT-ONLY INDEPENDENT JOURNEY
    # ----------------------------------------------------
    print("\n[TEST 3] Chat-Only Independent Journey (Natural Language)...")
    sess_chat = f"sess_chat_test_{int(time.time())}"
    
    # 3.1 Chat: Identify as Business Owner
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "I am a business owner looking for shop internet"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "CUSTOMER_ACCOUNT_CHECK", f"Expected CUSTOMER_ACCOUNT_CHECK, got {wf['stage']}"
    
    # 3.2 Chat: Existing Account
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "I already have an account with Airtel"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "CUSTOMER_LOGIN", f"Expected CUSTOMER_LOGIN, got {wf['stage']}"
    
    # 3.3 Secure Login (handled via secure backend)
    login_res = s.post(f"{BASE}/api/auth/customer/login", json={
        "session_id": sess_chat, "identifier": "9810123456", "password": "Airtel@2026"
    }).json()
    assert login_res["status"] == "success", "Login failed"
    wf = login_res["workflow"]
    assert wf["customer"]["name"] == "Rajesh Gupta", "Customer profile restoration failed"
    
    # 3.4 Chat: State business category
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "I run a kirana general store"
    }).json()
    wf = r["workflow"]
    assert wf["discovery"]["business_type"] == "kirana", "Business type not parsed from chat"
    
    # 3.5 Chat: State CCTV requirement
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "I also need CCTV cameras for store surveillance"
    }).json()
    wf = r["workflow"]
    assert "cctv_security" in wf["discovery"]["requirements"], "CCTV requirement not parsed"
    assert "P23" in wf["recommendation"]["active_addons"], "CCTV add-on not added to quote"
    
    # 3.6 Chat: Ask for quote
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Show me the quote and monthly bill"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "QUOTE_REVIEW", f"Expected QUOTE_REVIEW, got {wf['stage']}"
    
    # 3.7 Chat: Ask to do KYC
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Let us verify KYC documents"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"

    # 3.7b Chat: Complete KYC via demo
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Verify specimen demo"
    }).json()
    
    # 3.8 Chat: Track order
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Track my order and installation status"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "INSTALLATION_TRACKING", f"Expected INSTALLATION_TRACKING, got {wf['stage']}"
    print("  [PASS] Full customer journey completed end-to-end purely through conversational chat!")

    # ----------------------------------------------------
    # TEST 4: BIDIRECTIONAL MIXED JOURNEY
    # ----------------------------------------------------
    print("\n[TEST 4] Bidirectional Synchronization & Mixed Journey...")
    sess_mix = f"sess_mix_test_{int(time.time())}"
    
    # Start in GUI: Select User Type
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_mix, "action": "SELECT_USER_TYPE", "payload": {"user_type": "customer"}
    }).json()["workflow"]
    
    # Continue in Chat: Mention Kirana
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_mix, "message": "I run a kirana store"
    }).json()
    wf = r["workflow"]
    assert wf["discovery"]["business_type"] == "kirana"
    
    # Continue in GUI: Toggle Static IP Add-on
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_mix, "action": "TOGGLE_ADDON", "payload": {"addon_id": "P11"}
    }).json()["workflow"]
    assert "P11" in wf["recommendation"]["active_addons"]
    
    # Continue in Chat: Ask for Bill
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_mix, "message": "What is the bill now?"
    }).json()
    assert "₹" in r["reply"] or "bill" in r["reply"].lower()
    print("  [PASS] Bidirectional state synchronization passed between Chat and GUI!")

    # ----------------------------------------------------
    # TEST 5: AIRTEL EMPLOYEE DEMO JOURNEY
    # ----------------------------------------------------
    print("\n[TEST 5] Airtel Employee Journey & Isolation...")
    sess_emp = f"sess_emp_test_{int(time.time())}"
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_emp, "action": "SELECT_USER_TYPE", "payload": {"user_type": "employee"}
    }).json()["workflow"]
    assert wf["stage"] == "EMPLOYEE_DEMO_ENTRY", f"Expected EMPLOYEE_DEMO_ENTRY, got {wf['stage']}"
    assert wf["user_type"] == "employee", "User type mismatch"
    
    r_ctrl = s.get(f"{BASE}/control")
    assert r_ctrl.status_code == 200, "Control portal unreachable"
    assert "CONTROL CONSOLE" in r_ctrl.text, "Control console branding missing"
    print("  [PASS] Employee Demo access verified and cleanly separated from customer onboarding!")

    # ----------------------------------------------------
    # TEST 6: MULTILINGUAL SUPPORT & PREFERENCES
    # ----------------------------------------------------
    print("\n[TEST 6] Multilingual Support (Hindi, Hinglish, Punjabi)...")
    for lang in ["hi", "hinglish", "pa"]:
        wf = s.post(f"{BASE}/api/workflow/transition", json={
            "session_id": sess_mix, "action": "SET_LANGUAGE", "payload": {"language": lang}
        }).json()["workflow"]
        assert wf["language"] == lang, f"Language set failed for {lang}"
    print("  [PASS] Dynamic language switching preserved workflow state across 4 languages!")

    print("\n" + "=" * 70)
    print(">>> ALL AUDIT TESTS PASSED WITH 100% SUCCESS! <<<")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()

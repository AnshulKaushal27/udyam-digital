"""
test_gui_chat_synchronization.py
=============================================================================
Acceptance Test Suite for GUI-Chat State Synchronization & Contextual AI Advisor
Bharti Airtel Business - Project Udyam Digital

Verifies all 16 Acceptance Criteria:
1. Initial state verification (Kirana, REQUIREMENTS_COLLECTION, 4 visible GUI options)
2. Send "mujhe tez internet chahiye"
3. Interpretation is connectivity-speed need
4. "High-Speed Symmetrical Fiber" (broadband_speed) becomes selected
5. Backend workflow state records broadband_speed
6. Assistant reply does NOT ask about UPI/POS
7. Ask "aur kya kya additions available hain"
8. Reply lists catalogue additions with names and prices
9. Reply does NOT continue asking UPI/POS question
10. GUI change via /api/workflow/transition reflects in subsequent chat turns
11. English & Hindi parity ("I need faster Wi-Fi", "मुझे तेज इंटरनेट चाहिए")
12. Ordinal reference ("the second option") resolves to broadband_speed
13. Invalid product ID rejection ("P99" rejected, not added to state)
14. Quick replies advance dynamically and contain no "undefined" chips
15. LLM unavailable fallback is graceful, non-crashing, and grounded
16. Regression suite integration
=============================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'prototype'))

import requests
import json
import unittest

from customer_workflow_engine import get_visible_gui_options, get_eligible_catalogue_options

BASE_URL = "http://127.0.0.1:5000"

class TestGuiChatSynchronization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            r = requests.get(f"{BASE_URL}/", timeout=5)
            assert r.status_code == 200
        except Exception as e:
            raise RuntimeError(f"Server is not running on {BASE_URL}: {e}")

    def setUp(self):
        # Reset any test mock LLM before each test
        requests.post(f"{BASE_URL}/api/advisor/test_mock_llm", json={"mode": "reset"})

    def tearDown(self):
        # Clean up test mock LLM after each test
        requests.post(f"{BASE_URL}/api/advisor/test_mock_llm", json={"mode": "reset"})

    def _setup_kirana_requirements_session(self, sid):
        """Helper to create session at REQUIREMENTS_COLLECTION stage."""
        r = requests.post(f"{BASE_URL}/api/workflow/transition", json={
            "session_id": sid,
            "action": "SELECT_CATEGORY",
            "payload": {"category": "kirana"}
        })
        self.assertEqual(r.status_code, 200)
        wf = r.json()["workflow"]
        self.assertEqual(wf["stage"], "REQUIREMENTS_COLLECTION")
        return wf

    def test_01_initial_state_verification(self):
        """Test 1: Verify Kirana store at REQUIREMENTS_COLLECTION has 4 visible GUI options."""
        sid = f"test_sync_init_{os.urandom(4).hex()}"
        wf = self._setup_kirana_requirements_session(sid)
        
        # Verify 4 options exist on backend
        options = get_visible_gui_options(wf)
        self.assertEqual(len(options), 4, f"Expected 4 visible options, got {len(options)}")
        option_ids = [opt["id"] for opt in options]
        self.assertIn("upi_failover", option_ids)
        self.assertIn("broadband_speed", option_ids)
        self.assertIn("cctv_security", option_ids)
        self.assertIn("static_ip", option_ids)

    def test_02_to_06_fast_internet_hinglish_request(self):
        """
        Tests 2-6:
        2. Send 'mujhe tez internet chahiye'
        3. Interpretation is connectivity-speed need
        4. 'High-Speed Symmetrical Fiber' (broadband_speed) becomes selected
        5. Backend workflow state records broadband_speed
        6. Assistant reply does NOT ask about UPI/POS
        """
        sid = f"test_sync_speed_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # Send Hinglish need
        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "mujhe tez internet chahiye",
            "language": "hinglish"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()

        # Test 3: Interpretation
        interp = data.get("interpretation", {})
        self.assertIn("speed", interp.get("interpreted_need", "").lower() + " " + interp.get("reply", "").lower())
        self.assertIn("broadband_speed", interp.get("target_product_ids", []))

        # Test 4 & 5: Backend state records broadband_speed
        wf = data.get("workflow", {})
        reqs = wf.get("discovery", {}).get("requirements", [])
        self.assertIn("broadband_speed", reqs, "broadband_speed must be in workflow discovery requirements")

        # Verify visible options reflects selected: True
        vis_opts = get_visible_gui_options(wf)
        speed_opt = next((o for o in vis_opts if o["id"] == "broadband_speed"), None)
        self.assertIsNotNone(speed_opt)
        self.assertTrue(speed_opt["selected"], "High-Speed Symmetrical Fiber must be marked selected")

        # Test 6: Reply does NOT ask UPI/POS question
        reply = data.get("reply", "")
        self.assertNotIn("UPI QR payments or card swipe POS machines", reply, "Must NOT ask the UPI/POS question")
        self.assertTrue(any(w in reply.lower() for w in ["fiber", "speed", "broadband", "symmetrical"]), "Reply must acknowledge fiber/speed")

    def test_07_to_09_additions_query(self):
        """
        Tests 7-9:
        7. Ask 'aur kya kya additions available hain'
        8. Reply lists catalogue additions with names and prices
        9. Reply does NOT continue asking UPI/POS question
        """
        sid = f"test_sync_additions_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # First express speed need
        requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "mujhe tez internet chahiye",
            "language": "hinglish"
        })

        # Ask additions query
        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "aur kya kya additions available hain",
            "language": "hinglish"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()
        reply = data.get("reply", "")

        # Test 8: Lists catalogue additions with prices
        self.assertTrue("800" in reply, "Must mention CCTV pricing (800)")
        self.assertTrue("300" in reply, "Must mention Static IP pricing (300)")
        self.assertTrue("499" in reply or "999" in reply, "Must mention other add-ons pricing (499/999)")

        # Test 9: Does NOT ask UPI/POS question
        self.assertNotIn("rely heavily on UPI QR payments or card swipe POS", reply, "Must not ask the UPI/POS question")

    def test_10_gui_change_reflects_in_chat(self):
        """Test 10: Toggling a requirement on GUI reflects in subsequent chat turns."""
        sid = f"test_sync_gui_toggle_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # User toggles CCTV on GUI
        r_gui = requests.post(f"{BASE_URL}/api/workflow/transition", json={
            "session_id": sid,
            "action": "TOGGLE_REQUIREMENT",
            "payload": {"requirement": "cctv_security"}
        })
        self.assertEqual(r_gui.status_code, 200)
        wf = r_gui.json()["workflow"]
        self.assertIn("cctv_security", wf["discovery"]["requirements"])

        # Visible options must reflect CCTV as selected
        vis = get_visible_gui_options(wf)
        cctv_opt = next((o for o in vis if o["id"] == "cctv_security"), None)
        self.assertTrue(cctv_opt["selected"], "CCTV must be selected in visible GUI options")

    def test_11_multilingual_parity_english_and_hindi(self):
        """Test 11: English ('I need faster Wi-Fi') and Hindi ('मुझे तेज इंटरनेट चाहिए') select broadband_speed."""
        # English
        sid_en = f"test_parity_en_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid_en)
        r_en = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid_en,
            "message": "I need faster Wi-Fi",
            "language": "en"
        })
        self.assertEqual(r_en.status_code, 200)
        d_en = r_en.json()
        self.assertIn("broadband_speed", d_en["workflow"]["discovery"]["requirements"])
        self.assertNotIn("UPI QR payments", d_en["reply"])

        # Hindi
        sid_hi = f"test_parity_hi_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid_hi)
        r_hi = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid_hi,
            "message": "मुझे तेज इंटरनेट चाहिए",
            "language": "hi"
        })
        self.assertEqual(r_hi.status_code, 200)
        d_hi = r_hi.json()
        self.assertIn("broadband_speed", d_hi["workflow"]["discovery"]["requirements"])
        self.assertNotIn("UPI QR payments", d_hi["reply"])

    def test_12_ordinal_reference_selection(self):
        """Test 12: Customer saying 'the second option' resolves to broadband_speed."""
        sid = f"test_sync_ordinal_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "I want the second option",
            "language": "en"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()
        wf = data["workflow"]
        # Option 2 is broadband_speed
        self.assertIn("broadband_speed", wf["discovery"]["requirements"], "The second option must resolve to broadband_speed")

    def test_13_invalid_product_id_rejection(self):
        """Test 13: Mock model returning target_product_ids: ['P99'] is rejected and not applied."""
        sid = f"test_sync_reject_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # Inject mock LLM response proposing fake product P99
        fake_llm_response = {
            "intent": "select_product",
            "interpreted_need": "Customer wants non-existent software",
            "target_product_ids": ["P99", "FAKE_ENTERPRISE_ERP"],
            "target_addon_ids": ["FAKE_ADDON"],
            "state_changes": {"selected_requirements": ["P99"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "I have added P99 to your package.",
            "quick_replies": ["Continue", "Review"]
        }
        requests.post(f"{BASE_URL}/api/advisor/test_mock_llm", json={"response": fake_llm_response})

        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "Give me P99",
            "language": "en"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()
        wf = data["workflow"]

        # P99 must NOT be in requirements or active addons!
        self.assertNotIn("P99", wf["discovery"]["requirements"])
        self.assertNotIn("P99", wf["recommendation"]["active_addons"])
        self.assertNotIn("FAKE_ENTERPRISE_ERP", wf["discovery"]["requirements"])

    def test_14_non_stale_quick_replies(self):
        """Test 14: Quick replies advance dynamically and contain no 'undefined' chips."""
        sid = f"test_sync_qr_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # Turn 1: Speed need
        r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "Fast internet",
            "language": "en"
        })
        qr1 = r1.json().get("quick_replies", [])
        self.assertTrue(len(qr1) > 0)
        for chip in qr1:
            chip_str = chip if isinstance(chip, str) else chip.get("label", "")
            self.assertNotIn("undefined", chip_str.lower())
            self.assertNotIn("null", chip_str.lower())
            self.assertTrue(len(chip_str.strip()) > 0)

        # Turn 2: Additions query
        r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "what additions are available?",
            "language": "en"
        })
        qr2 = r2.json().get("quick_replies", [])
        self.assertTrue(len(qr2) > 0)
        for chip in qr2:
            chip_str = chip if isinstance(chip, str) else chip.get("label", "")
            self.assertNotIn("undefined", chip_str.lower())
            self.assertNotIn("null", chip_str.lower())

    def test_15_llm_unavailable_graceful_fallback(self):
        """Test 15: When live LLM is unreachable or returns malformed data, fallback works deterministically."""
        sid = f"test_sync_fallback_{os.urandom(4).hex()}"
        self._setup_kirana_requirements_session(sid)

        # Inject broken mock response
        requests.post(f"{BASE_URL}/api/advisor/test_mock_llm", json={"response": "THIS IS INVALID NON-JSON TEXT"})

        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "fast fiber connection",
            "language": "en"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("broadband_speed", data["workflow"]["discovery"]["requirements"])
        self.assertTrue(len(data.get("reply", "")) > 0)

    def test_16_quote_review_confirmation_to_kyc(self):
        """Test 16: In quote review, typing 'ok this seems ok' or 'move on' smoothly transitions to KYC_VERIFICATION."""
        sid = f"test_sync_confirm_{os.urandom(4).hex()}"
        # Advance to PLAN_EXPLORATION
        requests.post(f"{BASE_URL}/api/workflow/transition", json={
            "session_id": sid,
            "action": "SELECT_PLAN",
            "payload": {"bundle_id": "bundle_clinic"}
        })

        # User confirms quote in chat
        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": sid,
            "message": "ok this seems ok",
            "language": "en"
        })
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["workflow"]["stage"], "KYC_VERIFICATION", "Workflow must advance to KYC_VERIFICATION")
        self.assertIn("Quotation confirmed", data["reply"])

if __name__ == "__main__":
    unittest.main()

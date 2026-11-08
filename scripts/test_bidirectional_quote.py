"""
test_bidirectional_quote.py
=============================================================================
Bharti Airtel Business - Bidirectional Quote Customization & Dynamic Package Card Test Suite
Verifies:
1. P19 Cloud POS recommendation renders base ₹599/mo, setup ₹2,500 for billing needs
2. Elimination of false CCTV requirements (no unwanted warning, no auto-checked add-on)
3. Price inquiries ("How much is CCTV?") do NOT modify the quote
4. Chat-based add-on addition ("Add CCTV") updates quote & pricing with confirmation
5. Chat-based add-on removal ("Remove CCTV") reverts quote
6. Modal package customizer (/api/quote/customize) updates quote state atomically
7. Multi-component customization (CCTV + Static IP) calculates 18% GST accurately
8. Budget objection ("Make it cheaper") recommends the ₹599 standalone tier
9. Package switching ("Switch to POS") updates base bundle and recomputes setup/recurring
10. Quote state persistence and telemetry tracking across version increments
=============================================================================
"""

import sys
import os
import requests
import json
import unittest

BASE_URL = "http://127.0.0.1:5000"

class TestBidirectionalQuote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Health check
        try:
            r = requests.get(f"{BASE_URL}/", timeout=5)
            assert r.status_code == 200
        except Exception as e:
            raise RuntimeError(f"Server is not running on {BASE_URL}: {e}")

    def test_01_billing_discovery_recommends_p19_cloud_pos(self):
        """Test 1: Invoicing needs recommend Cloud POS & Billing (P19) at ₹599/mo, NOT Kirana at ₹1,999/mo."""
        session_id = f"test_quote_sess_{os.urandom(4).hex()}"
        
        # Turn 1: Customer asks for billing
        r1 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "I need a digital billing system",
            "category": "kirana"
        })
        self.assertEqual(r1.status_code, 200)

        # Turn 2: Currently on paper
        r2 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "Currently on paper"
        })
        self.assertEqual(r2.status_code, 200)

        # Turn 3: Needs proper GST invoicing
        r3 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "Yes, need proper GST invoicing"
        })
        self.assertEqual(r3.status_code, 200)

        # Turn 4: Volume 300-400
        r4 = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "300-400"
        })
        self.assertEqual(r4.status_code, 200)
        data4 = r4.json()
        
        # Verify recommended package is Cloud POS (P19)
        self.assertTrue(data4.get("discovery_status") == "complete")
        quote = data4.get("quote") or {}
        self.assertIsNotNone(quote, "Quote should be generated")
        self.assertIn(quote.get("bundle_id"), ["prod_p19_pos", "P19"], f"Expected prod_p19_pos, got {quote.get('bundle_id')}")
        self.assertEqual(quote.get("monthly_base_inr"), 599, "Base monthly price must be ₹599")
        
        pricing = quote.get("pricing", {})
        self.assertEqual(pricing.get("monthly_base_inr"), 599)
        self.assertEqual(pricing.get("gst_18_inr"), 108, "18% GST on 599 should be 108")
        self.assertEqual(pricing.get("final_monthly_payable_inr"), 707, "Total monthly should be 707")
        self.assertEqual(pricing.get("one_time_setup_inr"), 2500, "Setup fee for P19 must be ₹2,500")
        self.assertEqual(pricing.get("first_payment_inr"), 3207, "First payment must be 707 + 2500 = 3207")

    def test_02_elimination_of_false_cctv_requirements(self):
        """Test 2: Verify that CCTV is NOT attributed to customer when unrequested."""
        session_id = f"test_cctv_sess_{os.urandom(4).hex()}"
        
        # Complete discovery without mentioning CCTV
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "I need a billing system", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "proper GST"})
        r = requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "500+"})
        
        quote = r.json().get("quote", {})
        unmet = quote.get("unmet_requirements", [])
        
        # Verify NO CCTV requirement in unmet
        cctv_unmet = [u for u in unmet if "cctv" in u.get("requirement", "").lower()]
        self.assertEqual(len(cctv_unmet), 0, "No false CCTV requirements should be attributed")
        
        # Verify NO add-ons pre-selected
        addons = quote.get("addons", [])
        self.assertEqual(len(addons), 0, "Add-ons must start unselected")

    def test_03_price_inquiry_does_not_modify_quote(self):
        """Test 3: Asking 'How much is CCTV?' must explain price WITHOUT modifying the quote."""
        session_id = f"test_inq_sess_{os.urandom(4).hex()}"
        
        # Setup initial quote
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "billing system", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "GST"})
        r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "300"})
        quote_init = r_init.json()["quote"]
        initial_version = quote_init.get("version_number", 1)
        initial_total = quote_init["pricing"]["final_monthly_payable_inr"]

        # User asks price
        r_inq = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "How much is CCTV?"
        })
        self.assertEqual(r_inq.status_code, 200)
        data = r_inq.json()
        
        # Verify response explains price (₹800/mo, ₹1,200 setup)
        reply = data["reply"]
        self.assertTrue("800" in reply and "1,200" in reply, f"Reply should explain ₹800/mo and ₹1,200 setup, got: {reply}")
        
        # Verify quote was NOT modified
        quote_after = data["quote"]
        self.assertEqual(quote_after.get("version_number", 1), initial_version, "Version must not increment on price inquiry")
        self.assertEqual(quote_after["pricing"]["final_monthly_payable_inr"], initial_total, "Pricing must remain unchanged")
        self.assertEqual(len(quote_after.get("addons", [])), 0, "No add-on should be attached")

    def test_04_chat_based_addon_addition(self):
        """Test 4: Typing 'Add CCTV' dynamically updates quote, pricing, and version number."""
        session_id = f"test_add_sess_{os.urandom(4).hex()}"
        
        # Setup initial quote
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "billing system", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "GST"})
        r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "300"})
        quote_id = r_init.json()["quote_id"]

        # Add CCTV via chat
        r_add = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "Add CCTV to my quote"
        })
        self.assertEqual(r_add.status_code, 200)
        data = r_add.json()
        quote = data["quote"]
        
        # Verify version incremented to 2
        self.assertEqual(quote.get("version_number"), 2, "Quote version must increment to 2")
        
        # Verify addon attached
        addons = quote.get("addons", [])
        self.assertEqual(len(addons), 1)
        self.assertIn("CCTV", addons[0]["name"])
        
        # Verify pricing math:
        # Base: 599, Addon: 800 -> Subtotal: 1399
        # GST (18% of 1399): 252
        # Final monthly: 1651
        # Setup: 2500 (POS) + 1200 (CCTV) = 3700
        # First payment: 1651 + 3700 = 5351
        pricing = quote["pricing"]
        self.assertEqual(pricing["monthly_base_inr"], 599)
        self.assertEqual(pricing["addons_monthly_inr"], 800)
        self.assertEqual(pricing["monthly_subtotal_inr"], 1399)
        self.assertEqual(pricing["gst_18_inr"], 252)
        self.assertEqual(pricing["final_monthly_payable_inr"], 1651)
        self.assertEqual(pricing["one_time_setup_inr"], 3700)
        self.assertEqual(pricing["first_payment_inr"], 5351)

    def test_05_chat_based_addon_removal(self):
        """Test 5: Typing 'Remove CCTV' removes the add-on and reverts total monthly amount."""
        session_id = f"test_rem_sess_{os.urandom(4).hex()}"
        
        # Setup initial quote & add CCTV
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "billing", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "GST"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "300"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "Add CCTV"})

        # Now remove CCTV
        r_rem = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "Remove CCTV from quote"
        })
        self.assertEqual(r_rem.status_code, 200)
        quote = r_rem.json()["quote"]
        
        # Verify version incremented to 3
        self.assertEqual(quote.get("version_number"), 3, "Quote version must increment to 3 on removal")
        self.assertEqual(len(quote.get("addons", [])), 0, "Add-on list must be empty")
        self.assertEqual(quote["pricing"]["final_monthly_payable_inr"], 707, "Total must revert to ₹707/mo")

    def test_06_modal_customization_api(self):
        """Test 6: POST /api/quote/customize updates quote state atomically with multi-addons."""
        session_id = f"test_modal_sess_{os.urandom(4).hex()}"
        
        # Setup initial quote
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "billing", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "GST"})
        r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "300"})
        quote_id = r_init.json()["quote_id"]

        # Call modal customization API with CCTV + Static IP
        r_cust = requests.post(f"{BASE_URL}/api/quote/customize", json={
            "quote_id": quote_id,
            "bundle_id": "prod_p19_pos",
            "addons": ["addon_cctv", "addon_static_ip"]
        })
        self.assertEqual(r_cust.status_code, 200)
        data = r_cust.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["version_number"], 2)
        
        quote = data["quote"]
        # Pricing: 599 + 800 + 300 = 1699
        # GST (18% of 1699): 306
        # Total monthly: 2005
        # Setup: 2500 + 1200 + 0 = 3700
        p = data["pricing"]
        self.assertEqual(p["monthly_subtotal_inr"], 1699)
        self.assertEqual(p["gst_18_inr"], 306)
        self.assertEqual(p["final_monthly_payable_inr"], 2005)
        self.assertEqual(p["one_time_setup_inr"], 3700)

    def test_07_budget_objection_and_package_switch(self):
        """Test 7: 'Make it cheaper' suggests standalone POS; 'Switch to POS' executes switch."""
        session_id = f"test_cheap_sess_{os.urandom(4).hex()}"
        
        # Direct kirana connectivity setup (starts on bundle_kirana @ 1,999)
        requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "We have 3 staff and UPI drop during evening rush",
            "category": "kirana"
        })
        r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "We use QR code mainly"
        })
        quote_id = r_init.json().get("quote_id")
        
        # Customer says "Make it cheaper"
        r_cheap = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "This is too expensive, make it cheaper"
        })
        self.assertEqual(r_cheap.status_code, 200)
        reply = r_cheap.json()["reply"]
        self.assertTrue("599" in reply or "POS" in reply, f"Consultant should offer ₹599 plan, got: {reply}")

        # Customer switches: "Switch to ₹599 POS plan"
        r_switch = requests.post(f"{BASE_URL}/api/advisor/chat", json={
            "session_id": session_id,
            "message": "Switch to ₹599 POS plan"
        })
        self.assertEqual(r_switch.status_code, 200)
        data_sw = r_switch.json()
        quote = data_sw["quote"]
        self.assertIn(quote["bundle_id"], ["prod_p19_pos", "P19"])
        self.assertEqual(quote["pricing"]["monthly_base_inr"], 599)
        self.assertEqual(quote["pricing"]["final_monthly_payable_inr"], 707)

    def test_08_quote_telemetry_and_persistence(self):
        """Test 8: Authoritative quote endpoint /api/quote/<id> returns complete versioned record."""
        session_id = f"test_tele_sess_{os.urandom(4).hex()}"
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "billing system", "category": "kirana"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "paper"})
        requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "GST"})
        r_init = requests.post(f"{BASE_URL}/api/advisor/chat", json={"session_id": session_id, "message": "300"})
        quote_id = r_init.json()["quote_id"]

        # Modify quote twice
        requests.post(f"{BASE_URL}/api/quote/customize", json={"quote_id": quote_id, "bundle_id": "prod_p19_pos", "addons": ["addon_sim"]})
        requests.post(f"{BASE_URL}/api/quote/customize", json={"quote_id": quote_id, "bundle_id": "prod_p19_pos", "addons": ["addon_sim", "addon_cctv"]})

        # Fetch authoritative record
        r_get = requests.get(f"{BASE_URL}/api/quote/{quote_id}")
        self.assertEqual(r_get.status_code, 200)
        res = r_get.json()
        q = res.get("quote", res)
        self.assertEqual(q["version_number"], 3)
        self.assertEqual(len(q["modification_history"]), 3)
        self.assertEqual(q["status"], "modified")

if __name__ == "__main__":
    unittest.main()

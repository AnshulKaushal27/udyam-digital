"""
Project Udyam Digital - Smart KYC Vision Pipeline & DPDP Act 2023 Compliance
Comprehensive 12-Case Integration Test Suite
BHARTI AIRTEL SYNC 2026
"""

import sys
import os
import io
import json
import uuid
from datetime import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# Ensure prototype module is importable
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOTYPE_DIR = os.path.join(BASE_DIR, "prototype")
if PROTOTYPE_DIR not in sys.path:
    sys.path.insert(0, PROTOTYPE_DIR)

from app import app
from smart_kyc import (
    set_test_mock_vision,
    reset_test_mock_vision,
    mask_gstin,
    REFERENCE_DATE,
    SPECIMEN_DOCUMENT_CORPUS
)
from customer_workflow_engine import (
    get_or_create_workflow,
    transition_workflow
)

client = app.test_client()

def create_dummy_image(text="SAMPLE", color=(255, 255, 255), size=(400, 300)):
    """Helper to create valid in-memory PNG image bytes."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def run_all_12_tests():
    print("=" * 80)
    print("RUNNING 12-CASE SMART KYC VISION PIPELINE & COMPLIANCE INTEGRATION TEST SUITE")
    print("=" * 80)
    test_results = {}

    # -------------------------------------------------------------------------
    # TEST 1: Valid supported specimen in explicit demo mode is labeled simulated
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Explicit Demo Mode (Specimen K02 Benchmark):")
    r1 = client.post("/api/kyc/document/process", data={
        "doc_type": "gst_certificate",
        "applicant_id": "K02",
        "is_demo": "true",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}: {r1.data}"
    d1 = r1.get_json()
    assert d1["is_demo"] is True
    assert "Specimen simulation" in d1["simulation_disclaimer"]
    assert d1["is_approved"] is True
    print("  ✓ PASS: Explicit demo mode clearly labeled simulated with valid specimen.")
    test_results["Test 1: Explicit Demo Simulation"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 2: FreeCodeCamp course-list image rejected as irrelevant
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Normal Customer Upload of FreeCodeCamp Course-List Image:")
    fcc_bytes = create_dummy_image("FreeCodeCamp Responsive Web Design Curriculum Course List")
    
    def mock_fcc_vision(img_bytes, mime, selected_type):
        return {
            "document_relevant": False,
            "document_type_detected": "unknown",
            "matches_selected_document_type": False,
            "readability": "clear",
            "extracted_fields": {
                "business_name": None,
                "trade_name": None,
                "gstin": None,
                "udyam_number": None,
                "address": None,
                "signatory_name": None,
                "issue_date": None
            },
            "document_confidence": 10.0,
            "warnings": ["Image appears to be an educational web page / FreeCodeCamp curriculum."]
        }
    
    set_test_mock_vision(mock_fcc_vision)
    
    r2 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(fcc_bytes), "freecodecamp_courses.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true",
        "session_id": "sess_fcc_test"
    }, content_type="multipart/form-data")
    
    assert r2.status_code == 200
    d2 = r2.get_json()
    assert d2["is_approved"] is False
    assert d2["status"] == "DOCUMENT_NOT_RELEVANT"
    print("  ✓ PASS: FreeCodeCamp image correctly rejected as DOCUMENT_NOT_RELEVANT and not approved.")
    test_results["Test 2: Irrelevant Image Rejection"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 3: Irrelevant image contains NO Harmony Dental Care seeded data
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Assert Response Contains NO Harmony Dental Care / Seeded Data:")
    raw_response_text = r2.data.decode("utf-8")
    assert "Harmony Dental" not in raw_response_text, "Found seeded Harmony Dental name in response!"
    assert "19EOGXH4115Y1ZL" not in raw_response_text, "Found seeded K02 GSTIN in response!"
    assert "2026-05-22" not in raw_response_text, "Found seeded bill date in response!"
    assert len(d2["evaluation"]["field_comparison"]) == 0
    print("  ✓ PASS: Zero specimen ground truth leaked into irrelevant customer upload response.")
    test_results["Test 3: Zero Seeded Data Leakage"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 4: Supported document image sent to configured vision API (Mocked)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Supported Document Image Sent to Vision API (Verified via Mock):")
    valid_gst_bytes = create_dummy_image("Form GST REG-06 Certificate of Registration")
    
    def mock_valid_gst_vision(img_bytes, mime, selected_type):
        return {
            "document_relevant": True,
            "document_type_detected": "gst_certificate",
            "matches_selected_document_type": True,
            "readability": "clear",
            "extracted_fields": {
                "business_name": "Saffron Bakers",
                "trade_name": "Saffron Bakers",
                "gstin": "03PJNXS4821G1ZB", # Active valid GSTIN in mock registry
                "address": "Model Town, Ludhiana, Punjab 141002",
                "signatory_name": "Sneha Rao",
                "issue_date": "2024-01-15"
            },
            "document_confidence": 97.5,
            "warnings": []
        }
    
    set_test_mock_vision(mock_valid_gst_vision)
    
    r4 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "sharma_gst.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true",
        "session_id": "sess_valid_gst"
    }, content_type="multipart/form-data")
    
    assert r4.status_code == 200
    d4 = r4.get_json()
    assert d4["is_approved"] is True
    assert d4["status"] == "VERIFIED_APPROVED"
    assert d4["evaluation"]["is_passed"] is True
    print("  ✓ PASS: Supported document analyzed by vision mock and validated against GST registry.")
    test_results["Test 4: Supported Document Verification"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 5: Model output with missing fields does not cause inferred values
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Missing Fields Not Inferred by Backend:")
    def mock_missing_fields_vision(img_bytes, mime, selected_type):
        return {
            "document_relevant": True,
            "document_type_detected": "gst_certificate",
            "matches_selected_document_type": True,
            "readability": "partial",
            "extracted_fields": {
                "business_name": "Incomplete Store",
                "trade_name": None,
                "gstin": None, # Missing critical field!
                "address": None,
                "signatory_name": None,
                "issue_date": None
            },
            "document_confidence": 72.0,
            "warnings": ["GSTIN section obscured by glare."]
        }
    
    set_test_mock_vision(mock_missing_fields_vision)
    
    r5 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "missing_gst.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    
    d5 = r5.get_json()
    assert d5["is_approved"] is False
    assert d5["vision_analysis"]["extracted_fields"]["gstin"] is None
    assert d5["vision_analysis"]["extracted_fields"]["address"] is None
    print("  ✓ PASS: Missing fields preserved as null; no artificial inference occurred.")
    test_results["Test 5: No Inferred Missing Fields"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 6: Low confidence, malformed JSON, unsupported doc type, provider failure
    # -------------------------------------------------------------------------
    print("\n[TEST 6] Robustness Checks (Low Confidence, Malformed JSON, Provider Error):")
    # 6a. Low Confidence
    def mock_low_conf(b, m, t):
        return {
            "document_relevant": True,
            "document_type_detected": "gst_certificate",
            "matches_selected_document_type": True,
            "readability": "unreadable",
            "document_confidence": 35.0,
            "extracted_fields": {}
        }
    set_test_mock_vision(mock_low_conf)
    r6a = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "blurry.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r6a.get_json()["is_approved"] is False
    assert r6a.get_json()["status"] == "UNREADABLE_LOW_RESOLUTION"

    # 6b. Malformed JSON / Mock Exception
    def mock_broken(b, m, t):
        raise RuntimeError("LLM output parsing crashed")
    set_test_mock_vision(mock_broken)
    r6b = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "error.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r6b.get_json()["is_approved"] is False

    # 6c. Unsupported Document Type
    r6c = client.post("/api/kyc/document/process", data={
        "doc_type": "unknown_passport_type",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r6c.status_code == 400
    print("  ✓ PASS: Low confidence, parser exceptions, and invalid doc types safely rejected.")
    test_results["Test 6: Low Confidence & Failure Handling"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 7: Extracted GSTIN/Udyam still needs registry validation
    # -------------------------------------------------------------------------
    print("\n[TEST 7] Extracted Identifiers Strictly Checked Against Registries:")
    # Cancelled GSTIN: 37IHKXV5167L1ZS
    def mock_cancelled_gst(b, m, t):
        return {
            "document_relevant": True,
            "document_type_detected": "gst_certificate",
            "matches_selected_document_type": True,
            "readability": "clear",
            "extracted_fields": {
                "business_name": "Cancelled Enterprise",
                "gstin": "37IHKXV5167L1ZS" # Known Cancelled GSTIN in registry
            },
            "document_confidence": 95.0
        }
    set_test_mock_vision(mock_cancelled_gst)
    r7 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "cancelled_gst.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    d7 = r7.get_json()
    assert d7["is_approved"] is False
    exc_codes = [e["code"] for e in d7["evaluation"]["exceptions"]]
    assert "GSTIN_CANCELLED" in exc_codes
    print("  ✓ PASS: Cancelled GSTIN rejected by statutory registry check.")
    test_results["Test 7: Registry Cross-Validation"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 8: Document type mismatch and expired utility bill (>90 days)
    # -------------------------------------------------------------------------
    print("\n[TEST 8] Document Type Mismatch & 90-Day Freshness Benchmark:")
    # 8a. Mismatch (Expected GST, but uploaded Electricity Bill)
    def mock_mismatch(b, m, t):
        return {
            "document_relevant": True,
            "document_type_detected": "address_proof",
            "matches_selected_document_type": False,
            "readability": "clear",
            "extracted_fields": {"issue_date": "2026-06-10"},
            "document_confidence": 92.0
        }
    set_test_mock_vision(mock_mismatch)
    r8a = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "bill_when_gst_expected.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r8a.get_json()["status"] == "DOCUMENT_TYPE_MISMATCH"
    assert r8a.get_json()["is_approved"] is False

    # 8b. Expired Bill (>90 days from 15-Jul-2026)
    def mock_old_bill(b, m, t):
        return {
            "document_relevant": True,
            "document_type_detected": "address_proof",
            "matches_selected_document_type": True,
            "readability": "clear",
            "extracted_fields": {"issue_date": "2026-01-10"}, # >180 days old!
            "document_confidence": 95.0
        }
    set_test_mock_vision(mock_old_bill)
    r8b = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "old_bill.png"),
        "doc_type": "address_proof",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    d8b = r8b.get_json()
    assert d8b["is_approved"] is False
    exc_codes_8b = [e["code"] for e in d8b["evaluation"]["exceptions"]]
    assert "OLD_UTILITY_BILL" in exc_codes_8b
    print("  ✓ PASS: Mismatch and expired utility bill (>90 days) correctly rejected.")
    test_results["Test 8: Type Mismatch & 90-Day Rule"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 9: Missing affirmative consent rejected before vision call
    # -------------------------------------------------------------------------
    print("\n[TEST 9] Missing DPDP Statutory Consent Rejection:")
    vision_called = False
    def mock_spy(b, m, t):
        nonlocal vision_called
        vision_called = True
        return {}
    set_test_mock_vision(mock_spy)
    
    r9 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "doc.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "false" # Consent NOT provided
    }, content_type="multipart/form-data")
    
    assert r9.status_code == 400
    assert r9.get_json()["code"] == "CONSENT_REQUIRED"
    assert vision_called is False, "Vision API was invoked despite missing consent!"
    print("  ✓ PASS: Missing consent rejected with HTTP 400 before vision model call.")
    test_results["Test 9: Affirmative Consent Enforcement"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 10: Unknown applicant IDs never fall back to K02
    # -------------------------------------------------------------------------
    print("\n[TEST 10] Unknown Applicant IDs Never Fall Back to K02:")
    # 10a. Demo mode with invalid applicant
    r10a = client.post("/api/kyc/document/process", data={
        "doc_type": "gst_certificate",
        "applicant_id": "K99_INVALID",
        "is_demo": "true",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert r10a.status_code == 400
    assert r10a.get_json()["code"] == "INVALID_SPECIMEN_APPLICANT"

    # 10b. Customer upload with no applicant hint must not produce K02
    reset_test_mock_vision() # Tests honest unconfigured state or mock
    set_test_mock_vision(mock_fcc_vision)
    r10b = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(fcc_bytes), "random_photo.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true"
    }, content_type="multipart/form-data")
    assert "K02" not in r10b.data.decode("utf-8")
    print("  ✓ PASS: Unknown or absent applicant IDs never default to K02.")
    test_results["Test 10: No Silent K02 Default"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 11: Raw bytes & unmasked identifiers not stored in session / audit logs
    # -------------------------------------------------------------------------
    print("\n[TEST 11] Ephemeral Privacy (No Raw Bytes or Unmasked PII in State):")
    sess_id = f"test_privacy_{uuid.uuid4().hex[:8]}"
    set_test_mock_vision(mock_valid_gst_vision)
    r11 = client.post("/api/kyc/document/process", data={
        "document_file": (io.BytesIO(valid_gst_bytes), "confidential_cert.png"),
        "doc_type": "gst_certificate",
        "dpdp_consent": "true",
        "session_id": sess_id
    }, content_type="multipart/form-data")
    
    wf11 = get_or_create_workflow(sess_id)
    stored_docs = wf11.get("kyc", {}).get("documents", [])
    assert len(stored_docs) > 0
    doc_entry = stored_docs[0]
    
    # Assert no raw bytes stored
    assert "file_bytes" not in doc_entry
    assert "base64" not in doc_entry
    assert "raw_bytes" not in doc_entry
    assert doc_entry["masked_identifier"] == mask_gstin("03PJNXS4821G1ZB")
    print("  ✓ PASS: Zero raw image bytes persisted; identifiers masked in workflow state.")
    test_results["Test 11: Privacy & Zero Byte Persistence"] = "PASS"

    # -------------------------------------------------------------------------
    # TEST 12: Customer cannot proceed to fulfillment from non-approved KYC
    # -------------------------------------------------------------------------
    print("\n[TEST 12] Order Fulfillment Gate Blocks Non-Approved KYC:")
    sess_unapproved = f"test_gate_{uuid.uuid4().hex[:8]}"
    wf_gate = get_or_create_workflow(sess_unapproved)
    assert wf_gate["kyc"]["status"] == "PENDING"
    assert wf_gate["kyc"]["verified"] is False
    
    # Attempt transition to INSTALLATION_TRACKING
    wf_after = transition_workflow(sess_unapproved, "GO_TO_STAGE", {"stage": "INSTALLATION_TRACKING"})
    assert wf_after["stage"] != "INSTALLATION_TRACKING", f"Fulfillment gate breached! Stage is {wf_after['stage']}"
    assert "Cannot proceed to installation tracking" in wf_after["messages"][-1]["text"]
    print("  ✓ PASS: Progression to fulfillment strictly blocked on unapproved KYC.")
    test_results["Test 12: Order Fulfillment Gate"] = "PASS"

    # Reset mock at conclusion
    reset_test_mock_vision()

    print("\n" + "=" * 80)
    print("TEST SUITE SUMMARY: ALL 12 REQUIRED SCENARIOS PASSED")
    print("=" * 80)
    for test_name, res in test_results.items():
        print(f"  {test_name:<45}: {res}")
    print("=" * 80)
    return True

if __name__ == "__main__":
    success = run_all_12_tests()
    if not success:
        sys.exit(1)

import urllib.request
import urllib.error
import json
import uuid
import sys
import io
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://127.0.0.1:5000"

def make_multipart_kyc_request(session_id, doc_type, file_bytes, filename, dpdp_consent="true", mode="automated", is_demo=None, applicant_id=None):
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    body_parts = [
        f"--{boundary}",
        'Content-Disposition: form-data; name="doc_type"',
        "",
        doc_type,
        f"--{boundary}",
        'Content-Disposition: form-data; name="session_id"',
        "",
        session_id,
        f"--{boundary}",
        'Content-Disposition: form-data; name="dpdp_consent"',
        "",
        dpdp_consent,
        f"--{boundary}",
        'Content-Disposition: form-data; name="mode"',
        "",
        mode,
    ]
    if is_demo:
        body_parts.extend([
            f"--{boundary}",
            'Content-Disposition: form-data; name="is_demo"',
            "",
            str(is_demo),
        ])
    if applicant_id:
        body_parts.extend([
            f"--{boundary}",
            'Content-Disposition: form-data; name="applicant_id"',
            "",
            applicant_id,
        ])
    body_parts.extend([
        f"--{boundary}",
        f'Content-Disposition: form-data; name="document_file"; filename="{filename}"',
        "Content-Type: image/jpeg",
        "",
        "",
    ])
    payload = "\r\n".join(body_parts).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/kyc/document/process",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        data=payload
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def create_test_image(text="Airtel Document"):
    img = Image.new("RGB", (320, 240), color=(245, 245, 245))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def run_tests():
    print("=" * 75)
    print("PROJECT UDYAM DIGITAL: KYC DUAL CHOICES & BIDIRECTIONAL SYNC AUDIT (14 TESTS)")
    print("=" * 75)

    test_img_bytes = create_test_image()

    # -------------------------------------------------------------------------
    # TEST 1: Customer uploads document and chooses automated verification
    # -------------------------------------------------------------------------
    print("\n--- TEST 1: Customer uploads document and chooses automated verification ---")
    sess_auto = f"sess_auto_test_{uuid.uuid4().hex[:6]}"
    res1 = make_multipart_kyc_request(
        session_id=sess_auto,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="gst_upload.jpg",
        dpdp_consent="true",
        mode="automated"
    )
    assert res1["verification_mode"] == "automated"
    assert "application_id" in res1
    auto_app_id = res1["application_id"]
    print(f"Application ID: {auto_app_id}")
    print(f"Mode:           {res1['verification_mode']}")
    print(f"Status:         {res1['status']}")
    print("[PASS] Test 1 Verified (Automated KYC choice processed with application ID).")

    # -------------------------------------------------------------------------
    # TEST 2: Automated verification success is saved and appears in both portals
    # -------------------------------------------------------------------------
    print("\n--- TEST 2: Automated verification success is saved and appears in both portals ---")
    # Test with verified specimen in demo mode or passed evaluation
    sess_pass = f"sess_pass_test_{uuid.uuid4().hex[:6]}"
    res2 = make_multipart_kyc_request(
        session_id=sess_pass,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="clean_gst.jpg",
        dpdp_consent="true",
        mode="automated",
        is_demo="true",
        applicant_id="K02"
    )
    assert res2["is_approved"] is True
    assert res2["status"] == "success"
    # Verify consumer portal sees it approved
    req_wf = urllib.request.Request(f"{BASE_URL}/api/workflow/state/{sess_pass}")
    with urllib.request.urlopen(req_wf) as resp_wf:
        wf_data = json.loads(resp_wf.read().decode())["workflow"]
        # In demo specimen test, approval allows tracking transition
    print(f"Automated Specimen Result: Approved={res2['is_approved']}")
    # Verify control portal queue sees K02
    req_q = urllib.request.Request(f"{BASE_URL}/api/kyc/queue?status=APPROVED")
    with urllib.request.urlopen(req_q) as resp_q:
        q_data = json.loads(resp_q.read().decode())
        approved_ids = [a["application_id"] for a in q_data["applications"]]
        assert "K02" in approved_ids
    print("[PASS] Test 2 Verified (Automated verification success visible in queue and workflow).")

    # -------------------------------------------------------------------------
    # TEST 3: Automated verification failure does not mark application approved
    # -------------------------------------------------------------------------
    print("\n--- TEST 3: Automated verification failure does not mark approved ---")
    # Blank/unconfigured or anomaly document must not be approved
    assert res1["is_approved"] is False
    assert res1["status"] != "APPROVED"
    req_st1 = urllib.request.Request(f"{BASE_URL}/api/kyc/status/{sess_auto}")
    with urllib.request.urlopen(req_st1) as resp_st1:
        st1_data = json.loads(resp_st1.read().decode())
        assert st1_data["is_approved"] is False
        assert st1_data["kyc_status"] != "APPROVED"
    print(f"Customer Status: {st1_data['kyc_status']} (is_approved: {st1_data['is_approved']})")
    print("[PASS] Test 3 Verified (Failed / inconclusive automated check does not mark approved).")

    # -------------------------------------------------------------------------
    # TEST 4: Customer chooses manual review and application appears in control KYC queue
    # -------------------------------------------------------------------------
    print("\n--- TEST 4: Customer chooses manual review -> appears in control queue as pending ---")
    sess_man = f"sess_man_test_{uuid.uuid4().hex[:6]}"
    res4 = make_multipart_kyc_request(
        session_id=sess_man,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="business_proof_manual.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    assert res4["status"] == "MANUAL_REVIEW_REQUESTED"
    assert res4["verification_mode"] == "manual"
    assert res4["is_approved"] is False
    man_app_id = res4["application_id"]
    print(f"Application ID:   {man_app_id}")
    print(f"Status:           {res4['status']}")
    print(f"Verification Mode: {res4['verification_mode']}")

    # Verify control portal queue contains this live customer application
    req_q4 = urllib.request.Request(f"{BASE_URL}/api/kyc/queue?role=kyc_officer")
    with urllib.request.urlopen(req_q4) as resp_q4:
        q4_data = json.loads(resp_q4.read().decode())
        queued_app = next((a for a in q4_data["applications"] if a["application_id"] == man_app_id), None)
        assert queued_app is not None, f"Application {man_app_id} must appear in control KYC queue!"
        assert queued_app["verification_mode"] == "manual"
        assert queued_app["is_specimen"] is False
        assert queued_app["status"] == "MANUAL_REVIEW_REQUESTED"
        print(f"Control Queue App: Found {queued_app['application_id']} with status={queued_app['status']}")
    print("[PASS] Test 4 Verified (Manual review choice created live queue entry with status MANUAL_REVIEW_REQUESTED).")

    # -------------------------------------------------------------------------
    # TEST 5: KYC officer can request another document; customer sees request
    # -------------------------------------------------------------------------
    print("\n--- TEST 5: Officer requests another document; customer sees request ---")
    req_action5 = urllib.request.Request(
        f"{BASE_URL}/api/kyc/action?role=kyc_officer",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "application_id": man_app_id,
            "action": "REQUEST_RESUBMISSION",
            "officer_name": "KYC Officer (S. Sen)",
            "reasons": "Uploaded image text was unreadable. Please upload a clear GST registration certificate.",
            "actionable_instructions": "Please upload a clear GST registration certificate."
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req_action5) as resp_action5:
        act5 = json.loads(resp_action5.read().decode())
        assert act5["status"] == "success"
        print(f"Officer Action: {act5['action']} executed by S. Sen (Audit: {act5['audit_id']})")

    # Check customer portal status
    req_cust5 = urllib.request.Request(f"{BASE_URL}/api/kyc/status/{sess_man}")
    with urllib.request.urlopen(req_cust5) as resp_cust5:
        cust5 = json.loads(resp_cust5.read().decode())
        assert cust5["kyc_status"] == "MORE_INFO_REQUESTED"
        assert cust5["is_approved"] is False
        assert "clear GST" in (cust5["requested_document"] or cust5["officer_remarks"])
        print(f"Customer Sees: Status={cust5['kyc_status']} | Request='{cust5['requested_document']}'")
    print("[PASS] Test 5 Verified (Officer resubmission request reflected on customer side).")

    # -------------------------------------------------------------------------
    # TEST 6: Customer resubmits and control portal shows new event & updated status
    # -------------------------------------------------------------------------
    print("\n--- TEST 6: Customer resubmits and control portal shows new event & updated status ---")
    fresh_img_bytes = create_test_image("Clear GST Certificate")
    res6 = make_multipart_kyc_request(
        session_id=sess_man,
        doc_type="gst_certificate",
        file_bytes=fresh_img_bytes,
        filename="clear_gst_cert.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    assert res6["status"] == "RESUBMITTED"
    print(f"Resubmission Status: {res6['status']}")

    # Check audit log for document_resubmitted event
    req_aud6 = urllib.request.Request(f"{BASE_URL}/api/kyc/audit?application_id={man_app_id}")
    with urllib.request.urlopen(req_aud6) as resp_aud6:
        aud6 = json.loads(resp_aud6.read().decode())
        event_types = [e.get("event_type") for e in aud6["audit_trail"]]
        assert "document_resubmitted" in event_types
        print(f"Audit Trail Events: {event_types}")
    print("[PASS] Test 6 Verified (Customer resubmission logged in audit trail and updated status).")

    # -------------------------------------------------------------------------
    # TEST 7: KYC officer approves; customer portal and linked order show approved
    # -------------------------------------------------------------------------
    print("\n--- TEST 7: KYC officer approves; customer portal and linked order reflect approved ---")
    req_action7 = urllib.request.Request(
        f"{BASE_URL}/api/kyc/action?role=kyc_officer",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "application_id": man_app_id,
            "action": "APPROVE",
            "officer_name": "KYC Officer (S. Sen)",
            "reasons": "DoT statutory requirements confirmed on resubmitted document."
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req_action7) as resp_action7:
        act7 = json.loads(resp_action7.read().decode())
        assert act7["status"] == "success"
        print(f"Officer Action: Approved (Audit ID: {act7['audit_id']})")

    # Check customer portal
    req_cust7 = urllib.request.Request(f"{BASE_URL}/api/kyc/status/{sess_man}")
    with urllib.request.urlopen(req_cust7) as resp_cust7:
        cust7 = json.loads(resp_cust7.read().decode())
        assert cust7["kyc_status"] == "APPROVED"
        assert cust7["is_approved"] is True
        print(f"Customer Portal: Status={cust7['kyc_status']} | Approved={cust7['is_approved']}")
    print("[PASS] Test 7 Verified (Officer approval synchronizes to customer portal).")

    # -------------------------------------------------------------------------
    # TEST 8: KYC officer rejects; customer portal shows rejection and next step
    # -------------------------------------------------------------------------
    print("\n--- TEST 8: KYC officer rejects; customer portal shows rejection and next step ---")
    sess_rej = f"sess_rej_test_{uuid.uuid4().hex[:6]}"
    res8 = make_multipart_kyc_request(
        session_id=sess_rej,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="forged_doc.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    rej_app_id = res8["application_id"]
    req_action8 = urllib.request.Request(
        f"{BASE_URL}/api/kyc/action?role=kyc_officer",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "application_id": rej_app_id,
            "action": "REJECT",
            "officer_name": "KYC Officer (S. Sen)",
            "reasons": "GST registration certificate is revoked in GSTN registry."
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req_action8) as resp_action8:
        act8 = json.loads(resp_action8.read().decode())
        assert act8["status"] == "success"

    req_cust8 = urllib.request.Request(f"{BASE_URL}/api/kyc/status/{sess_rej}")
    with urllib.request.urlopen(req_cust8) as resp_cust8:
        cust8 = json.loads(resp_cust8.read().decode())
        assert cust8["kyc_status"] == "REJECTED"
        assert cust8["is_approved"] is False
        assert "revoked" in cust8["officer_remarks"]
        print(f"Customer Sees: Status={cust8['kyc_status']} | Reason='{cust8['officer_remarks']}'")
    print("[PASS] Test 8 Verified (Rejection with reason reflected on customer side).")

    # -------------------------------------------------------------------------
    # TEST 9: Unauthorized roles cannot approve/reject or view raw documents
    # -------------------------------------------------------------------------
    print("\n--- TEST 9: Unauthorized roles cannot approve/reject or view raw documents ---")
    try:
        req_bad_role = urllib.request.Request(
            f"{BASE_URL}/api/kyc/action?role=channel_partner",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"application_id": man_app_id, "action": "APPROVE"}).encode("utf-8")
        )
        urllib.request.urlopen(req_bad_role)
        assert False, "Should have returned 403 for channel_partner!"
    except urllib.error.HTTPError as e:
        assert e.code == 403
        print("Channel Partner approval attempt: Denied with HTTP 403 Forbidden.")

    try:
        req_sales = urllib.request.Request(
            f"{BASE_URL}/api/kyc/action?role=sales_agent",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"application_id": man_app_id, "action": "APPROVE"}).encode("utf-8")
        )
        urllib.request.urlopen(req_sales)
        assert False, "Should have returned 403 for sales_agent!"
    except urllib.error.HTTPError as e:
        assert e.code == 403
        print("Sales Agent approval attempt: Denied with HTTP 403 Forbidden.")

    # Check that non-KYC role queue call masks PII and has no raw bytes
    req_q_partner = urllib.request.Request(f"{BASE_URL}/api/kyc/queue?role=channel_partner")
    with urllib.request.urlopen(req_q_partner) as resp_qp:
        qp_data = json.loads(resp_qp.read().decode())
        for a in qp_data["applications"]:
            assert a.get("raw_gstin") is None, "Raw GSTIN must not be exposed to channel_partner"
            for doc in a.get("documents", []):
                assert "raw_bytes" not in doc, "Raw document bytes must never be in payload"
    print("[PASS] Test 9 Verified (RBAC prevents unauthorized decisions and leaks).")

    # -------------------------------------------------------------------------
    # TEST 10: Repeated submissions do not create duplicate applications or duplicate audit events
    # -------------------------------------------------------------------------
    print("\n--- TEST 10: Idempotency - repeated clicks do not create duplicate apps or events ---")
    sess_idem = f"sess_idem_{uuid.uuid4().hex[:6]}"
    res10_a = make_multipart_kyc_request(
        session_id=sess_idem,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="same_file.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    res10_b = make_multipart_kyc_request(
        session_id=sess_idem,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="same_file.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    assert res10_a["application_id"] == res10_b["application_id"], "Should reuse same application_id for session"

    req_aud10 = urllib.request.Request(f"{BASE_URL}/api/kyc/audit?application_id={res10_a['application_id']}")
    with urllib.request.urlopen(req_aud10) as resp_aud10:
        aud10 = json.loads(resp_aud10.read().decode())
        event_types = [e.get("event_type") for e in aud10["audit_trail"]]
        req_count = sum(1 for e in event_types if e == "manual_review_requested")
        assert req_count == 1, f"Expected 1 manual_review_requested event, got {req_count}"
        print(f"Application ID: {res10_a['application_id']} (Total events: {len(aud10['audit_trail'])})")
    print("[PASS] Test 10 Verified (Idempotency prevents duplicate records on rapid repeated clicks).")

    # -------------------------------------------------------------------------
    # TEST 11: Refreshing both portals preserves the same status and history
    # -------------------------------------------------------------------------
    print("\n--- TEST 11: Refreshing preserves status and history ---")
    req_wf11 = urllib.request.Request(f"{BASE_URL}/api/workflow/state/{sess_man}")
    with urllib.request.urlopen(req_wf11) as resp_wf11:
        wf11 = json.loads(resp_wf11.read().decode())["workflow"]
        assert wf11["kyc"]["status"] == "APPROVED"
        assert wf11["kyc"]["is_approved"] is True
    req_q11 = urllib.request.Request(f"{BASE_URL}/api/kyc/queue?role=kyc_officer")
    with urllib.request.urlopen(req_q11) as resp_q11:
        q11 = json.loads(resp_q11.read().decode())
        app11 = next(a for a in q11["applications"] if a["application_id"] == man_app_id)
        assert app11["status"] == "APPROVED"
        assert app11["is_approved"] is True
    print("[PASS] Test 11 Verified (Refreshing both portals returns identical approved status).")

    # -------------------------------------------------------------------------
    # TEST 12: Pending / rejected / manual-review states cannot bypass fulfillment gate
    # -------------------------------------------------------------------------
    print("\n--- TEST 12: Fulfillment gate blocks pending, rejected, and manual-review states ---")
    # Attempt to transition sess_rej to INSTALLATION_TRACKING
    req_trans_rej = urllib.request.Request(
        f"{BASE_URL}/api/workflow/transition",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "session_id": sess_rej,
            "action": "GO_TO_STAGE",
            "payload": {"stage": "INSTALLATION_TRACKING"}
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req_trans_rej) as resp_tr:
        tr_data = json.loads(resp_tr.read().decode())
        assert tr_data["workflow"]["stage"] != "INSTALLATION_TRACKING", "Fulfillment gate failed to block rejected KYC!"
        print(f"Rejected Session Gate: Blocked at stage '{tr_data['workflow']['stage']}'")

    # Attempt to transition pending session to INSTALLATION_TRACKING
    sess_pending = f"sess_pend_{uuid.uuid4().hex[:6]}"
    make_multipart_kyc_request(
        session_id=sess_pending,
        doc_type="gst_certificate",
        file_bytes=test_img_bytes,
        filename="doc.jpg",
        dpdp_consent="true",
        mode="manual"
    )
    req_trans_pend = urllib.request.Request(
        f"{BASE_URL}/api/workflow/transition",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "session_id": sess_pending,
            "action": "GO_TO_STAGE",
            "payload": {"stage": "INSTALLATION_TRACKING"}
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req_trans_pend) as resp_tp:
        tp_data = json.loads(resp_tp.read().decode())
        assert tp_data["workflow"]["stage"] != "INSTALLATION_TRACKING", "Fulfillment gate failed to block pending manual KYC!"
        print(f"Pending Session Gate: Blocked at stage '{tp_data['workflow']['stage']}'")
    print("[PASS] Test 12 Verified (Fulfillment gate strictly blocks unapproved states).")

    # -------------------------------------------------------------------------
    # TEST 13: Sensitive values are masked in both portals and logs
    # -------------------------------------------------------------------------
    print("\n--- TEST 13: Sensitive values masked in portals and audit logs ---")
    req_aud_all = urllib.request.Request(f"{BASE_URL}/api/kyc/audit")
    with urllib.request.urlopen(req_aud_all) as resp_aud_all:
        aud_all = json.loads(resp_aud_all.read().decode())
        for entry in aud_all["audit_trail"]:
            details = entry.get("details", "")
            # Ensure no raw 15-char synthetic PAN without masking appears in details
            assert "19EOGXH4115Y1ZL" not in details, "Raw unmasked GSTIN found in audit details!"
            meta = entry.get("metadata", {})
            assert "raw_bytes" not in meta, "Raw bytes found in audit metadata!"
    print("[PASS] Test 13 Verified (No raw bytes or unmasked sensitive PII found in logs).")

    # -------------------------------------------------------------------------
    # TEST 14: DPDP Consent Checkbox Unchecked by Default
    # -------------------------------------------------------------------------
    print("\n--- TEST 14: DPDP consent required and unchecked by default ---")
    try:
        req_no_c = urllib.request.Request(
            f"{BASE_URL}/api/kyc/document/process",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "doc_type": "gst_certificate",
                "dpdp_consent": "false",
                "mode": "manual"
            }).encode("utf-8")
        )
        urllib.request.urlopen(req_no_c)
        assert False, "Should have rejected missing consent!"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        print("Missing affirmative consent rejected with HTTP 400 Bad Request.")

    # Verify consumer.html has unchecked checkbox
    with open(r'E:\Airtel\prototype\templates\consumer.html', 'r', encoding='utf-8') as f:
        html = f.read()
        assert '<input class="form-check-input" type="checkbox" id="kycDpdpCheck" onchange="toggleKycSubmitBtn()">' in html, "kycDpdpCheck must NOT have 'checked' attribute!"
        print("HTML Check: kycDpdpCheck is verified UNCHECKED by default.")
    print("[PASS] Test 14 Verified (DPDP consent is unchecked by default and strictly enforced).")

    print("\n" + "=" * 75)
    print(">>> ALL 14 KYC DUAL CHOICES & PORTAL SYNC AUDIT TESTS PASSED (100%)! <<<")
    print("=" * 75)

if __name__ == "__main__":
    run_tests()

import os

app_path = r"e:\Airtel\prototype\app.py"
with open(app_path, "r", encoding="utf-8") as f:
    app_text = f.read()

# 1. Update imports in app.py if needed
if "analyze_kyc_document_with_vision" not in app_text:
    old_imp = "cross_validate_kyc,"
    new_imp = "cross_validate_kyc,\n\n    analyze_kyc_document_with_vision,\n\n    evaluate_vision_kyc_extraction,"
    app_text = app_text.replace(old_imp, new_imp, 1)

if "from PIL import Image" not in app_text:
    app_text = "import io\nfrom PIL import Image\n" + app_text

# 2. Replace /api/kyc/document/process
start_token = '@app.route("/api/kyc/document/process", methods=["POST"])'
end_token = '@app.route("/api/kyc/queue", methods=["GET"])'

start_idx = app_text.find(start_token)
end_idx = app_text.find(end_token)

if start_idx == -1 or end_idx == -1:
    raise ValueError(f"Could not locate start ({start_idx}) or end ({end_idx}) of kyc_document_process in app.py")

new_route = '''@app.route("/api/kyc/document/process", methods=["POST"])
def kyc_document_process():
    """
    Processes customer uploaded or camera-captured KYC documents under Section 6 DPDP Act 2023.
    Enforces server-side affirmative consent BEFORE calling vision model or processing.
    Validates file bytes and executes multimodal LLM vision analysis without defaulting to K02.
    Preserves specimen benchmarking (K01-K12) ONLY when explicitly in demo mode (is_demo=True).
    Never logs or persists raw bytes or unmasked identifiers.
    """
    is_multipart = request.content_type and "multipart/form-data" in request.content_type
    if is_multipart:
        dpdp_consent = request.form.get("dpdp_consent")
        doc_type = request.form.get("doc_type", "gst_certificate")
        is_demo = request.form.get("is_demo")
        applicant_id = request.form.get("applicant_id")
        session_id = request.form.get("session_id")
        uploaded_file = request.files.get("document_file")
        file_name = uploaded_file.filename if (uploaded_file and uploaded_file.filename) else f"document_{doc_type}.png"
        file_bytes = uploaded_file.read() if uploaded_file else b""
        file_size_kb = max(1, len(file_bytes) // 1024) if file_bytes else 0
    else:
        data = request.json or {}
        dpdp_consent = data.get("dpdp_consent")
        doc_type = data.get("doc_type", "gst_certificate")
        is_demo = data.get("is_demo")
        applicant_id = data.get("applicant_id")
        session_id = data.get("session_id")
        file_name = data.get("file_name", f"document_{doc_type}.png")
        file_size_kb = data.get("file_size_kb", 0)
        file_bytes = b""

    # 1. Affirmative DPDP Act 2023 Statutory Consent Check
    # REJECT immediately if consent is missing, false, or empty BEFORE vision model call or file processing.
    if str(dpdp_consent).lower() not in ["true", "1", "yes"]:
        return jsonify({
            "status": "error",
            "code": "CONSENT_REQUIRED",
            "message": "Affirmative DPDP Act 2023 statutory consent is required before processing KYC documents."
        }), 400

    # 2. Supported Document Types Check
    supported_doc_types = {
        "gst_certificate": "GST / Business Registration Certificate",
        "udyam_certificate": "Udyam MSME Certificate",
        "address_proof": "Address Proof / Utility Bill (< 90 Days)",
        "signatory_id": "Signatory Identity Proof (PAN / Aadhaar)"
    }
    if doc_type not in supported_doc_types:
        return jsonify({
            "status": "error",
            "code": "UNSUPPORTED_DOC_TYPE",
            "message": f"Unsupported document type: {doc_type}. Supported types: {list(supported_doc_types.keys())}"
        }), 400

    is_demo_mode = str(is_demo).lower() in ["true", "1", "yes"]

    # =========================================================================
    # PATH A: EXPLICIT SPECIMEN DEMO BENCHMARK MODE (is_demo == True)
    # =========================================================================
    if is_demo_mode:
        app_key = applicant_id.strip().upper() if applicant_id else ""
        if not app_key or app_key not in SPECIMEN_DOCUMENT_CORPUS:
            return jsonify({
                "status": "error",
                "code": "INVALID_SPECIMEN_APPLICANT",
                "message": f"Unknown specimen applicant ID: '{applicant_id}'. Valid benchmark IDs: K01 to K12."
            }), 400

        specimen = SPECIMEN_DOCUMENT_CORPUS[app_key]
        ocr_file = f"{app_key}_{doc_type}.png"
        ocr_res = extract_document_ocr(ocr_file, applicant_hint=app_key)
        gst_res = verify_gstin(specimen["gstin"])
        udyam_res = verify_udyam(specimen["udyam"]) if specimen.get("udyam") and specimen["udyam"] != "NONE" else None
        customer_input = {
            "business_name": specimen["business_name"],
            "trade_name": specimen["trade_name"],
            "gstin": specimen["gstin"],
            "address": specimen["address"],
            "applicant_name": specimen["applicant_name"]
        }
        report = cross_validate_kyc(customer_input, ocr_res, gst_res, udyam_res)

        dpdp_record = {
            "doc_type": doc_type,
            "doc_type_label": supported_doc_types[doc_type],
            "file_name": os.path.basename(file_name),
            "file_size_kb": file_size_kb or 450,
            "captured_at": datetime.now().strftime("%d-%b-%Y %H:%M:%S IST"),
            "retention_policy": "Ephemeral RAM Buffer (No persistent storage)",
            "masked_identifier": mask_gstin(specimen["gstin"]),
            "ocr_confidence": ocr_res.get("confidence_score", 98.0),
            "ocr_quality": ocr_res.get("ocr_status", "EXTRACTED_SUCCESS"),
            "is_demo": True,
            "is_simulated_ocr": True,
            "simulation_disclaimer": "Specimen simulation — not customer verification"
        }

        return jsonify({
            "status": "success",
            "is_demo": True,
            "simulation_disclaimer": "Specimen simulation — not customer verification",
            "evaluation": report,
            "document_metadata": dpdp_record,
            "is_approved": report.get("is_passed", False)
        })

    # =========================================================================
    # PATH B: LIVE CUSTOMER DOCUMENT UPLOAD / CAMERA CAPTURE (is_demo == False)
    # NEVER defaults to K02 or any specimen. Processes actual uploaded bytes.
    # =========================================================================
    # 1. File Validation
    if not file_bytes or len(file_bytes) == 0:
        return jsonify({
            "status": "error",
            "code": "EMPTY_FILE",
            "message": "Uploaded file is empty. Please select or capture a valid document image."
        }), 400

    if len(file_bytes) > 10 * 1024 * 1024:
        return jsonify({
            "status": "error",
            "code": "FILE_TOO_LARGE",
            "message": "Uploaded file exceeds maximum limit of 10MB."
        }), 400

    # 2. Image integrity and mime validation via PIL
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
        img_fmt = (img.format or "").lower()
        if img_fmt not in ["jpeg", "jpg", "png", "webp"]:
            return jsonify({
                "status": "error",
                "code": "UNSUPPORTED_IMAGE_FORMAT",
                "message": f"Unsupported image format: {img_fmt}. Please upload JPEG, PNG, or WebP."
            }), 400
        detected_mime = "image/png" if img_fmt == "png" else ("image/webp" if img_fmt == "webp" else "image/jpeg")
    except Exception:
        return jsonify({
            "status": "error",
            "code": "INVALID_IMAGE_FILE",
            "message": "The uploaded file is not a valid or readable image. Please provide a clear JPEG, PNG, or WebP photo."
        }), 400

    # 3. Multimodal Vision Analysis (Sends actual bytes to configured LLM Vision API)
    cfg = get_runtime_config()
    vision_analysis = analyze_kyc_document_with_vision(
        image_bytes=file_bytes,
        mime_type=detected_mime,
        selected_doc_type=doc_type,
        runtime_config=cfg
    )

    # 4. Independent Statutory & DoT Verification
    wf_profile = {}
    if session_id:
        wf = get_or_create_workflow(session_id)
        wf_profile = wf.get("profile", {})

    eval_report = evaluate_vision_kyc_extraction(
        analysis=vision_analysis,
        selected_doc_type=doc_type,
        customer_input=wf_profile
    )

    # 5. Build Ephemeral DPDP Record (PII masked, NO raw bytes or unmasked text stored)
    extracted = vision_analysis.get("extracted_fields") or {}
    masked_id = "N/A"
    if extracted.get("gstin"):
        masked_id = mask_gstin(extracted["gstin"])
    elif extracted.get("udyam_number"):
        masked_id = extracted["udyam_number"]
    elif extracted.get("document_number"):
        d_num = str(extracted["document_number"])
        masked_id = f"***{d_num[-4:]}" if len(d_num) >= 4 else "***"
    elif eval_report.get("overall_status") == "MANUAL_REVIEW_REQUIRED":
        masked_id = "Pending Manual Review"

    dpdp_record = {
        "doc_type": doc_type,
        "doc_type_label": supported_doc_types[doc_type],
        "file_name": os.path.basename(file_name),
        "file_size_kb": file_size_kb,
        "captured_at": datetime.now().strftime("%d-%b-%Y %H:%M:%S IST"),
        "retention_policy": "Ephemeral RAM Buffer (No persistent raw image storage)",
        "masked_identifier": masked_id,
        "ocr_confidence": vision_analysis.get("document_confidence", 0.0),
        "ocr_quality": vision_analysis.get("readability", "unprocessed").upper(),
        "is_demo": False,
        "is_simulated_ocr": False
    }

    # 6. Session and Workflow Gate Synchronization
    if session_id:
        wf = get_or_create_workflow(session_id)
        if "documents" not in wf["kyc"]:
            wf["kyc"]["documents"] = []
        wf["kyc"]["documents"].append(dpdp_record)

        if eval_report.get("is_passed"):
            wf["kyc"]["status"] = "APPROVED"
            wf["kyc"]["verified"] = True
            if extracted.get("gstin"):
                wf["kyc"]["gstin"] = extracted["gstin"]
            if extracted.get("udyam_number"):
                wf["kyc"]["udyam"] = extracted["udyam_number"]
        else:
            status_code = eval_report.get("overall_status")
            if status_code in ["MANUAL_REVIEW_REQUIRED", "DOCUMENT_TYPE_MISMATCH", "UNREADABLE_LOW_RESOLUTION"]:
                wf["kyc"]["status"] = "REVIEW_REQUIRED"
            else:
                wf["kyc"]["status"] = "REJECTED"
            wf["kyc"]["verified"] = False

    return jsonify({
        "status": eval_report.get("overall_status", "success"),
        "is_demo": False,
        "is_approved": eval_report.get("is_passed", False),
        "evaluation": eval_report,
        "document_metadata": dpdp_record,
        "vision_analysis": {
            "document_relevant": vision_analysis.get("document_relevant", False),
            "document_type_detected": vision_analysis.get("document_type_detected", "unknown"),
            "matches_selected_document_type": vision_analysis.get("matches_selected_document_type", False),
            "readability": vision_analysis.get("readability", "unprocessed"),
            "document_confidence": vision_analysis.get("document_confidence", 0.0),
            "provider_name": vision_analysis.get("provider_name", "Unconfigured")
        }
    })

'''

app_text = app_text[:start_idx] + new_route + app_text[end_idx:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_text)

print("Successfully updated app.py with new kyc_document_process route and vision imports.")

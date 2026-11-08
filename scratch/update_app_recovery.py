with open(r'e:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None

for i, l in enumerate(lines):
    if '@app.route("/api/control/recovery/queue", methods=["GET"])' in l:
        start_idx = i
    if start_idx is not None and 'action = data.get("action", "").lower()' in l:
        end_idx = i + 1
        break

print(f"start: {start_idx}, end: {end_idx}")
assert start_idx is not None and end_idx is not None

new_block = '''@app.route("/api/control/recovery/queue", methods=["GET"])
def control_recovery_queue():
    """Lists all recovery records for the Airtel Control Portal with filtering, search, and RBAC masking."""
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_decision_roles = ["super_admin", "ops_manager", "sales_executive"]

    filter_type = request.args.get("filter", "all").lower()
    search = request.args.get("search", "").strip().lower()

    records = list(RECOVERY_RECORDS.values())

    # Filter logic
    if filter_type == "high_priority":
        records = [r for r in records if r.get("priority_score", 0) >= 70]
    elif filter_type == "price_too_high":
        records = [r for r in records if r.get("detected_objection") == "price_too_high"]
    elif filter_type == "technical_complexity":
        records = [r for r in records if r.get("detected_objection") == "technical_complexity"]
    elif filter_type == "draft_ready":
        records = [r for r in records if r.get("recovery_status") == "draft_ready"]
    elif filter_type == "contacted":
        records = [r for r in records if r.get("recovery_status") == "contacted"]
    elif filter_type == "recovered":
        records = [r for r in records if r.get("recovery_status") == "recovered"]

    # Search filter
    if search:
        records = [
            r for r in records
            if search in r.get("business_name", "").lower()
            or search in r.get("recovery_id", "").lower()
            or search in r.get("quote_id", "").lower()
            or search in r.get("assigned_agent", "").lower()
            or search in r.get("supporting_evidence", "").lower()
        ]

    # Sort: highest priority score first, then newest
    records.sort(key=lambda x: (x.get("priority_score", 0), x.get("created_at", "")), reverse=True)

    # RBAC Data Masking for unauthorized roles (e.g. channel_partner viewing global queue)
    out_records = []
    for r in records:
        r_copy = dict(r)
        if role not in allowed_decision_roles:
            phone = str(r_copy.get("contact_phone", ""))
            r_copy["contact_phone"] = phone[:6] + "****" if len(phone) >= 6 else "+91 98*** ****"
            cperson = str(r_copy.get("contact_person", ""))
            r_copy["contact_person"] = (cperson[:3] + "..." if len(cperson) > 3 else "Contact")
        out_records.append(r_copy)

    return jsonify({
        "status": "success",
        "count": len(out_records),
        "records": out_records,
        "role_authorized": role in allowed_decision_roles
    })

@app.route("/api/control/recovery/analytics", methods=["GET"])
def control_recovery_analytics():
    """Returns real-time recovery metrics, funnel rates, and historical baseline comparison."""
    analytics = get_recovery_analytics()
    return jsonify(analytics)

@app.route("/api/control/recovery/<recovery_id>", methods=["GET"])
def control_recovery_detail(recovery_id):
    """Retrieves full details of a specific recovery record with RBAC protection."""
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_decision_roles = ["super_admin", "ops_manager", "sales_executive"]

    rec = RECOVERY_RECORDS.get(recovery_id)
    if not rec:
        return jsonify({"status": "error", "message": f"Recovery record {recovery_id} not found."}), 404

    r_copy = dict(rec)
    if role not in allowed_decision_roles:
        phone = str(r_copy.get("contact_phone", ""))
        r_copy["contact_phone"] = phone[:6] + "****" if len(phone) >= 6 else "+91 98*** ****"
        cperson = str(r_copy.get("contact_person", ""))
        r_copy["contact_person"] = (cperson[:3] + "..." if len(cperson) > 3 else "Contact")

    return jsonify({"status": "success", "record": r_copy, "role_authorized": role in allowed_decision_roles})

@app.route("/api/control/recovery/<recovery_id>/action", methods=["POST"])
def control_recovery_action(recovery_id):
    """Executes actions on a recovery record: assign, update draft, contact, recover, close lost, opt out."""
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_action_roles = ["super_admin", "ops_manager", "sales_executive"]
    if role not in allowed_action_roles:
        return jsonify({"status": "error", "message": f"Access Denied: Role '{role}' is not authorized to execute recovery actions."}), 403

    rec = RECOVERY_RECORDS.get(recovery_id)
    if not rec:
        return jsonify({"status": "error", "message": f"Recovery record {recovery_id} not found."}), 404

    data = request.json or {}
    action = data.get("action", "").lower()
'''

lines[start_idx:end_idx] = [new_block + "\n"]

with open(r'e:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated app.py recovery endpoints with RBAC & PII masking successfully!")

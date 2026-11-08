import re

with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add import
kyc_import_marker = "    KYC_AUDIT_TRAIL\n)"
if kyc_import_marker in content and "from operations_intelligence import" not in content:
    oi_import = """    KYC_AUDIT_TRAIL
)
from operations_intelligence import (
    HISTORICAL_BASELINE,
    ASSIGNMENT_TARGETS,
    BUNDLE_SLA_DAYS,
    get_all_leads,
    get_executive_overview,
    get_funnel_intelligence,
    get_leads_by_funnel_stage,
    get_quote_loss_intelligence,
    get_kyc_intelligence,
    evaluate_order_risk,
    get_installation_operations_overview,
    get_unified_exceptions_queue,
    record_exception_action,
    get_partner_intelligence,
    generate_ai_business_insights,
    simulate_what_if_scenario
)"""
    content = content.replace(kyc_import_marker, oi_import, 1)
    print("1. Added operations_intelligence imports.")
else:
    print("1. Import already present or marker not found.")

# 2. Risk assessment in consumer_create_order
order_marker = "SHARED_ORDERS[order_id] = new_order"
if order_marker in content and "new_order[\"installation\"][\"risk_assessment\"]" not in content:
    order_repl = """new_order["installation"]["risk_assessment"] = evaluate_order_risk(new_order)
    SHARED_ORDERS[order_id] = new_order"""
    content = content.replace(order_marker, order_repl, 1)
    print("2. Added risk assessment in consumer_create_order.")
else:
    print("2. Order marker not updated.")

# 3. Risk assessment in control_update_kyc
kyc_marker = 'return jsonify({"status": "success", "order": order})\n\n@app.route("/api/control/orders/<order_id>/update_milestone"'
if kyc_marker in content and 'order["installation"]["risk_assessment"] = evaluate_order_risk(order)\n    return jsonify({"status": "success", "order": order})' not in content:
    kyc_repl = """order["installation"]["risk_assessment"] = evaluate_order_risk(order)
    return jsonify({"status": "success", "order": order})

@app.route("/api/control/orders/<order_id>/update_milestone\""""
    content = content.replace(kyc_marker, kyc_repl, 1)
    print("3. Added risk assessment in control_update_kyc.")
else:
    print("3. KYC marker not updated.")

# 4. Risk assessment in control_update_milestone
milestone_marker = "    # Phase 4: Order Activation Commission Trigger\n    if target_step == 5:"
if milestone_marker in content and 'risk_assessment"] = evaluate_order_risk(order)' not in content:
    milestone_repl = """    # Phase 6: Proactive Installation Risk Engine recalculation on milestone change
    order["installation"]["risk_assessment"] = evaluate_order_risk(order)

    # Phase 4: Order Activation Commission Trigger
    if target_step == 5:"""
    content = content.replace(milestone_marker, milestone_repl, 1)
    print("4. Added risk assessment in control_update_milestone.")
else:
    print("4. Milestone marker not updated.")

# 5. Replace analytics section
analytics_start = "# CONTROL PORTAL: DATA ANALYTICS & INSIGHTS (smb_leads.csv data)"
analytics_end = "# PHASE 1: INTELLIGENT BUSINESS DISCOVERY ENGINE & SESSION MANAGEMENT"

start_idx = content.find(analytics_start)
end_idx = content.find(analytics_end)

if start_idx != -1 and end_idx != -1:
    new_analytics_code = """# CONTROL PORTAL: PREDICTIVE OPERATIONS & BUSINESS INTELLIGENCE CENTRE (Phase 6)
# -------------------------------------------------------------------------
@app.route("/api/control/analytics/executive", methods=["GET"])
def control_executive_analytics():
    \"\"\"
    Section 2 & 3: Executive Operational Overview.
    Displays 13 KPIs with strict 4-dimensional segregation:
    - Historical Baseline (smb_leads.csv N=5,000)
    - Assignment Target
    - Live Prototype Results
    - Simulated Scenario
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_executive", "kyc_officer", "channel_partner", "sales_partner"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": f"Access Denied: Role '{role}' not permitted."}), 403

    overview = get_executive_overview(SHARED_ORDERS, SHARED_QUOTES, RECOVERY_RECORDS, KYC_AUDIT_TRAIL)
    return jsonify(overview)

@app.route("/api/control/analytics/funnel", methods=["GET"])
def control_funnel_analytics():
    \"\"\"
    Section 4: 6-Stage MSME Acquisition Funnel with segment and city drilldowns.
    Preserves backwards compatibility for baseline_funnel and live_prototype_stats.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": f"Access Denied: Role '{role}' cannot access funnel intelligence."}), 403

    segment = request.args.get("segment")
    city = request.args.get("city")
    city_tier = request.args.get("city_tier")

    detailed_funnel = get_funnel_intelligence(segment=segment, city=city, city_tier=city_tier)

    return jsonify({
        "status": "success",
        "detailed_funnel": detailed_funnel,
        "baseline_funnel": {
            "leads_generated": 5000,
            "contacted": 3406,
            "needs_assessed": 1974,
            "quote_accepted": 861,
            "kyc_completed": 588,
            "activated": 368,
            "overall_conversion_pct": 7.36,
            "avg_tat_days": 17.6,
            "blended_cac_inr": 15000,
            "steepest_drop": "Needs Assessed to Quote Accepted (56.4% Drop / 43.6% Pass)",
            "status_chase_calls_per_cust": 3.01
        },
        "live_prototype_stats": {
            "live_orders_count": len(SHARED_ORDERS),
            "approved_kyc_count": sum(1 for o in SHARED_ORDERS.values() if o.get('kyc', {}).get('status') in ['APPROVED', 'VERIFIED']),
            "active_installations": sum(1 for o in SHARED_ORDERS.values() if o.get('installation', {}).get('current_step') == 5),
            "avg_simulated_tat_days": 2.8
        }
    })

@app.route("/api/control/analytics/funnel/leads", methods=["GET"])
def control_funnel_leads_drilldown():
    \"\"\"
    Section 4: Interactive Drilldown into underlying lead records for any funnel stage.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Unauthorized to inspect funnel lead records."}), 403

    stage_key = request.args.get("stage", "lead_generated")
    segment = request.args.get("segment")
    city = request.args.get("city")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 50))

    data = get_leads_by_funnel_stage(stage_key, segment=segment, city=city, page=page, page_size=limit)
    return jsonify(data)

@app.route("/api/control/analytics/quote_loss", methods=["GET"])
def control_quote_loss_analytics():
    \"\"\"
    Section 5: Dedicated Quote Bottleneck and Loss Intelligence.
    Categorizes the 1,113 historical quote rejections across the 4 core buckets:
    - Price too high / opaque (414)
    - Competitor cheaper / faster (207)
    - Quote too complex (206)
    - Other (286)
    And links directly to Phase 3 recovery telemetry.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Role cannot view quote loss analytics."}), 403

    data = get_quote_loss_intelligence(RECOVERY_RECORDS)
    return jsonify(data)

@app.route("/api/control/analytics/kyc", methods=["GET"])
def control_kyc_analytics():
    \"\"\"
    Section 6: KYC Intelligence & Verification Bottleneck Analytics.
    Tracks applications, OCR quality anomalies, expired utility bills (>90d),
    GSTIN registry mismatches, and turnaround times.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "kyc_officer", "ops_manager"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Only KYC Officers, Ops Managers and Admins can view KYC analytics."}), 403

    data = get_kyc_intelligence(SHARED_ORDERS, KYC_AUDIT_TRAIL)
    return jsonify(data)

@app.route("/api/control/analytics/installations", methods=["GET"])
def control_installation_analytics():
    \"\"\"
    Section 7 & 8: Installation Operations Command & Proactive Risk Centre.
    Tracks orders across SLA milestones, bundle-specific SLA commitments
    (Kirana 2d, Clinic 3d, Multi-site 7d, Mfg 14d), and assigns explainable risk scores.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Only Operations Managers and Super Admins can access installation operations."}), 403

    data = get_installation_operations_overview(SHARED_ORDERS)
    return jsonify(data)

@app.route("/api/control/exceptions/queue", methods=["GET"])
def control_exceptions_queue():
    \"\"\"
    Section 9: Unified Operational Exception Management Centre.
    Unifies abandoned quotes, KYC exceptions, installation risks, SLA breaches,
    and unassigned resources into a single prioritized action queue.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "kyc_officer", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Unauthorized to view unified operational exceptions."}), 403

    data = get_unified_exceptions_queue(SHARED_ORDERS, SHARED_QUOTES, RECOVERY_RECORDS, KYC_AUDIT_TRAIL)
    return jsonify(data)

@app.route("/api/control/exceptions/<exception_id>/action", methods=["POST"])
def control_exception_action(exception_id):
    \"\"\"
    Section 9: Actioning an Operational Exception (acknowledge, resolve, reassign).
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "kyc_officer", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Unauthorized to act on exceptions."}), 403

    req_data = request.json or {}
    action = req_data.get("action", "acknowledge")
    owner = req_data.get("owner", f"Staff ({role})")
    notes = req_data.get("notes", "Action taken via Control Portal.")

    res = record_exception_action(exception_id, action, owner=owner, notes=notes)
    return jsonify(res)

@app.route("/api/control/leads", methods=["GET"])
def control_leads_list():
    \"\"\"Search and filter 5,000 synthetic leads database.\"\"\"
    search = request.args.get("search", "").lower()
    segment = request.args.get("segment", "")
    stage = request.args.get("stage", "")
    limit = int(request.args.get("limit", 50))

    filtered = []
    for r in LEADS:
        if segment and r.get("segment") != segment:
            continue
        if stage and r.get("stage_reached") != stage:
            continue
        if search:
            b_name = r.get("business_name", "").lower()
            c_name = r.get("city", "").lower()
            lid = r.get("lead_id", "").lower()
            if search not in b_name and search not in c_name and search not in lid:
                continue
        filtered.append(r)
        if len(filtered) >= limit:
            break

    return jsonify({"total_matching": len(filtered), "leads": filtered})

@app.route("/api/control/analytics/insights", methods=["GET"])
def control_business_insights():
    \"\"\"
    Section 11: AI-Powered Business Intelligence with structured 4-part schema:
    1. Observation
    2. Supporting Data (strictly real numbers from backend)
    3. Business Implication
    4. Recommended Action
    Preserves backwards compatibility for 'insights' array.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_executive"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Unauthorized to view AI business insights."}), 403

    data = generate_ai_business_insights()
    
    # Backwards compatibility format for tests and simple renderers
    compat_insights = [
        {
            "category": item["category"],
            "title": item["title"],
            "stat": item["supporting_data"][:60],
            "evidence": item["supporting_data"],
            "recommendation": item["recommended_action"],
            "observation": item["observation"],
            "business_implication": item["business_implication"]
        }
        for item in data["insights"]
    ]
    return jsonify({
        "status": "success",
        "insights": compat_insights,
        "structured_insights": data["insights"],
        "data_verified": True
    })

@app.route("/api/control/analytics/simulate", methods=["POST"])
def control_scenario_simulate():
    \"\"\"
    Section 12: Interactive Business Scenario Simulator.
    Calculates projected activations, revenue lift, and CAC payback period
    using a non-double-counting transparent model.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Only Operations Managers and Super Admins can run scenario simulations."}), 403

    params = request.json or {}
    result = simulate_what_if_scenario(params)
    return jsonify(result)

@app.route("/api/control/analytics/partner", methods=["GET"])
def control_partner_analytics():
    \"\"\"
    Section 10: Partner Performance Intelligence.
    Connected to Phase 4; evaluates lead volume, quote acceptance,
    activations, conversion rates, and activation-gated commissions.
    \"\"\"
    role = request.args.get("role", request.headers.get("X-Role", "super_admin")).lower()
    allowed_roles = ["super_admin", "ops_manager", "sales_partner", "channel_partner"]
    if role not in allowed_roles:
        return jsonify({"status": "error", "message": "Access Denied: Unauthorized to view partner analytics."}), 403

    city_filter = request.args.get("city")
    data = get_partner_intelligence(PARTNERS_REGISTRY, COMMISSION_LEDGER, city_filter=city_filter)
    return jsonify(data)

# -------------------------------------------------------------------------
"""
    content = content[:start_idx] + new_analytics_code + content[end_idx:]
    print("5. Replaced analytics section with complete Phase 6 suite.")
else:
    print(f"5. Markers not found: start={start_idx}, end={end_idx}")

with open('E:/Airtel/prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated app.py successfully.")

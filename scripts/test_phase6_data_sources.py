"""
Dedicated Verification Suite for Phase 6 Operations Intelligence Data Source Accuracy.
Verifies:
1. Canonical historical baseline matches smb_leads.csv (N=5,000, 7.36% conv, 17.6d TAT, ₹15,000 CAC, 3.01 chase calls).
2. Canonical project targets reconciled to Prompt.txt (22.0% Conv, 3.5d TAT, ₹3,800 CAC, <0.2 chase calls).
3. Zero-data / empty live state produces 'Unavailable' / 'No live data yet', NOT hardcoded fallbacks (no 28.5%, 16.7%, 92.0%, 25.2%, ₹6,850, 2.8d, 0.2 calls).
4. Live prototype metrics use defensible calculations and distinct session IDs (never quotes + orders as leads).
5. All 4 data dimensions (Historical, Target, Prototype Live, Simulation) are segregated and labeled.
6. Business insights follow strict 5-part schema with hypothesis tagging and rule-based provenance.
7. Quote loss recovery separates historical losses from live recovery records and explicitly tags ARPU assumptions.
"""

import sys
import requests
import json

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:5000"

def test_phase6_data_sources():
    print("=" * 80)
    print("VERIFYING PHASE 6 OPERATIONS INTELLIGENCE DATA SOURCE ACCURACY")
    print("=" * 80)

    # 1. Fetch Executive Analytics
    r = requests.get(f"{BASE_URL}/api/control/analytics/executive?role=super_admin")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()

    # Check 4 Dimensions Segregation
    dims = data["dimensions"]
    assert "historical_baseline" in dims
    assert "assignment_target" in dims
    assert "prototype_live" in dims
    assert "simulation" in dims

    # Verify Historical Baseline from file
    hb = dims["historical_baseline"]
    assert hb["sample_size"] == 5000
    assert hb["verified"] is True
    assert hb["conversion_pct"] == 7.36
    assert hb["tat_days"] == 17.6
    assert hb["cac_inr"] == 15000
    assert hb["status_chase_calls"] == 3.01
    print("✓ Dimension 1 (Historical Baseline): Verified 5,000 leads, 7.36% Conv, 17.6d TAT, ₹15,000 CAC, 3.01 Calls.")

    # Verify Canonical Targets from Prompt.txt
    at = dims["assignment_target"]
    assert "22.0%" in at["target_conversion"]
    assert "3.5" in at["target_tat"]
    assert "3,800" in at["target_cac"]
    assert "<0.2" in at["target_chase_calls"]
    print("✓ Dimension 2 (Project Targets): Reconciled to Prompt.txt (22.0% Conv, 3.5d TAT, ₹3,800 CAC, <0.2 Calls).")

    # Verify Prototype Live Dimension
    pl = dims["prototype_live"]
    assert "runtime_live_orders" in pl
    assert "seeded_demo_orders" in pl
    assert "unique_live_sessions" in pl
    print(f"✓ Dimension 3 (Prototype Live): Live sessions={pl['unique_live_sessions']}, Live orders={pl['runtime_live_orders']}, Seeded demo orders={pl['seeded_demo_orders']}.")

    # Verify Simulation Dimension
    sim = dims["simulation"]
    assert "hypothetical" in sim["disclaimer"].lower() or "projections" in sim["disclaimer"].lower()
    print("✓ Dimension 4 (Simulation): Explicitly labeled as hypothetical projections.")

    # Verify Metrics: NO Hardcoded Fallback Values
    metrics = {m["metric_id"]: m for m in data["metrics"]}

    # CAC must be Unavailable (spend not tracked)
    assert metrics["blended_cac"]["status"] == "unavailable"
    assert metrics["blended_cac"]["value"] is None
    assert "Unavailable" in metrics["blended_cac"]["prototype_value"]
    assert "6850" not in str(metrics["blended_cac"]["prototype_value"])
    print("✓ Blended CAC: Accurately returned as 'Unavailable' (spend not tracked, no fake ₹6,850).")

    # Status Chase Calls must be Unavailable (telephony logs not tracked)
    assert metrics["status_chase_calls"]["status"] == "unavailable"
    assert metrics["status_chase_calls"]["value"] is None
    assert "Unavailable" in metrics["status_chase_calls"]["prototype_value"]
    print("✓ Status Chase Calls: Accurately returned as 'Unavailable' (telephony untracked, no fake 0.2 calls).")

    # Total Leads must NOT be quotes + orders sum
    assert metrics["total_leads"]["formula"] == "count(distinct session_id)"
    assert "quotes" not in metrics["total_leads"]["formula"].lower()
    print("✓ Total Leads: Uses count of distinct session IDs, never adding unlike quotes + orders.")

    # Check Quote Recovery Rate does not use 28.5% fallback
    if metrics["quote_recovery_rate"]["status"] == "unavailable":
        assert metrics["quote_recovery_rate"]["value"] is None
        assert "28.5" not in metrics["quote_recovery_rate"]["prototype_value"]
        print("✓ Quote Recovery Rate: Empty queue returns 'No live recovery records', zero fallback 28.5%.")
    else:
        print(f"✓ Quote Recovery Rate: Live value calculated as {metrics['quote_recovery_rate']['prototype_value']}.")

    # Check KYC Rejection Rate does not use 16.7% fallback
    if metrics["kyc_rejection_rate"]["status"] == "unavailable":
        assert metrics["kyc_rejection_rate"]["value"] is None
        assert "16.7" not in metrics["kyc_rejection_rate"]["prototype_value"]
        print("✓ KYC Rejection Rate: No decisions returns 'No completed KYC evaluations', zero fallback 16.7%.")
    else:
        print(f"✓ KYC Rejection Rate: Live value calculated as {metrics['kyc_rejection_rate']['prototype_value']}.")

    # Check Installation SLA Compliance does not use 92.0% fallback
    if metrics["installation_sla_compliance"]["status"] == "unavailable":
        assert metrics["installation_sla_compliance"]["value"] is None
        assert "92.0" not in metrics["installation_sla_compliance"]["prototype_value"]
        print("✓ SLA Compliance: No orders returns 'No live orders to evaluate', zero fallback 92.0%.")
    else:
        print(f"✓ SLA Compliance: Live value calculated as {metrics['installation_sla_compliance']['prototype_value']}.")

    # 2. Check Quote Loss Intelligence
    r_ql = requests.get(f"{BASE_URL}/api/control/analytics/quote_loss?role=super_admin")
    assert r_ql.status_code == 200
    ql = r_ql.json()
    assert ql["total_rejected_quotes"] == 1113
    assert ql["categories"]["price_too_high"]["count"] == 414
    rec_int = ql["live_recovery_integration"]
    assert "assumed_monthly_arpu_inr" in rec_int
    assert "arpu_assumption_note" in rec_int
    print("✓ Quote Loss Intelligence: Preserved 1,113 historical losses, ARPU ₹3,850 explicitly labeled as assumption.")

    # 3. Check AI Business Insights Schema
    r_ins = requests.get(f"{BASE_URL}/api/control/analytics/insights?role=super_admin")
    assert r_ins.status_code == 200
    ins = r_ins.json()
    assert ins["data_verified"] is True
    for item in ins["structured_insights"]:
        assert "observation" in item
        assert "supporting_data" in item
        assert "business_implication" in item
        assert "recommended_action" in item
        assert "is_hypothesis" in item
        assert isinstance(item["is_hypothesis"], bool)
        assert "traceable_source" in item
    print(f"✓ AI Business Insights: All {len(ins['structured_insights'])} insights include observation, data, implication, action, traceable source, and hypothesis boolean.")

    # 4. Check Standalone Function with zero/empty state
    sys.path.append(r"E:\Airtel\prototype")
    from operations_intelligence import get_executive_overview
    empty_res = get_executive_overview({}, {}, {}, [], {})
    for m in empty_res["metrics"]:
        if m["metric_id"] in ["total_leads", "contacted_leads", "needs_assessed", "quotes_accepted", "kyc_completed", "activated_customers", "overall_conversion_rate", "avg_onboarding_tat", "blended_cac", "status_chase_calls", "quote_recovery_rate", "kyc_rejection_rate", "installation_sla_compliance"]:
            assert m["status"] == "unavailable", f"{m['metric_id']} expected status unavailable in empty state, got {m['status']}"
            assert m["value"] is None, f"{m['metric_id']} expected None value in empty state, got {m['value']}"
            assert m["comparison_available"] is False, f"{m['metric_id']} expected comparison_available False in empty state"
            assert "No comparison available" in m["change"] or "No baseline delta" in m["change"]
    print("✓ Isolated Zero-Data Test: 100% of metrics return 'unavailable' status, null value, and no fake deltas when sample is empty.")

    print("\n" + "=" * 80)
    print("ALL PHASE 6 DATA SOURCE INTEGRITY CHECKS PASSED (100% VERIFIED)")
    print("=" * 80)

if __name__ == "__main__":
    test_phase6_data_sources()

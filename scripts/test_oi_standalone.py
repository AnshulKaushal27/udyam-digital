import sys
sys.path.append('E:/Airtel/prototype')
import operations_intelligence as oi

print("Testing get_all_leads...")
leads = oi.get_all_leads()
print(f"Loaded {len(leads)} leads.")
assert len(leads) == 5000, f"Expected 5000, got {len(leads)}"

print("\nTesting get_executive_overview...")
shared_orders = {
    "ORD-TEST-1": {
        "order_id": "ORD-TEST-1",
        "bundle_id": "bundle_kirana",
        "created_at": "16-Jul-2026 10:00 IST",
        "kyc": {"status": "APPROVED", "audit_notes": "Auto-verified"},
        "installation": {"current_step": 4, "assigned_engineer": {"name": "Test Eng"}}
    }
}
shared_quotes = {
    "QTE-TEST-1": {"status": "ACCEPTED", "quote_id": "QTE-TEST-1"}
}
recovery_records = {
    "REC-TEST-1": {"status": "RECOVERED", "priority_score": 85, "business_name": "Test Kirana"}
}
kyc_audit = [{"is_passed": True, "ocr_quality_score": 0.95, "bill_age_days": 45}]

exec_view = oi.get_executive_overview(shared_orders, shared_quotes, recovery_records, kyc_audit)
print("Exec overview status:", exec_view["status"])
print(f"Total metrics in exec overview: {len(exec_view['metrics'])}")
assert len(exec_view["metrics"]) == 13, f"Expected 13 metrics, got {len(exec_view['metrics'])}"

print("\nTesting get_funnel_intelligence...")
funnel = oi.get_funnel_intelligence()
print("Funnel stages:", len(funnel["stages"]))
assert len(funnel["stages"]) == 6, f"Expected 6 stages, got {len(funnel['stages'])}"
print("Funnel stage 1 count:", funnel["stages"][0]["count"])
print("Funnel stage 6 count:", funnel["stages"][5]["count"])
assert funnel["stages"][0]["count"] == 5000
assert funnel["stages"][5]["count"] == 368

print("\nTesting get_quote_loss_intelligence...")
ql = oi.get_quote_loss_intelligence(recovery_records)
print("Quote losses total:", ql["total_rejected_quotes"])
assert ql["total_rejected_quotes"] == 1113
assert ql["categories"]["price_too_high"]["count"] == 414
assert ql["categories"]["competitor_cheaper"]["count"] == 207
assert ql["categories"]["quote_too_complex"]["count"] == 206
assert ql["categories"]["other"]["count"] == 286

print("\nTesting get_kyc_intelligence...")
kyc_intel = oi.get_kyc_intelligence(shared_orders, kyc_audit)
print("KYC intelligence status:", kyc_intel["status"])
assert kyc_intel["historical_baseline_comparison"]["total_historical_kyc_dropouts"] == 273

print("\nTesting evaluate_order_risk...")
risk = oi.evaluate_order_risk(shared_orders["ORD-TEST-1"])
print("Risk evaluation:", risk["risk_level"], "Score:", risk["risk_score"])

print("\nTesting get_unified_exceptions_queue...")
exc_queue = oi.get_unified_exceptions_queue(shared_orders, shared_quotes, recovery_records, kyc_audit)
print("Exceptions queue counts:", exc_queue["counts"])

print("\nTesting generate_ai_business_insights...")
insights = oi.generate_ai_business_insights()
print("Insights count:", insights["total_insights"])
assert insights["total_insights"] == 4

print("\nTesting simulate_what_if_scenario...")
sim = oi.simulate_what_if_scenario({"quote_acceptance_pct": 60, "kyc_completion_pct": 80, "activation_pct": 85, "cac_spend_inr": 8000})
print("Projected activations:", sim["funnel_projections"]["projected_activations"])
print("Incremental ARR:", sim["financial_impact"]["incremental_annual_revenue_inr"])

print("\nALL OPERATIONS INTELLIGENCE UNIT TESTS PASSED!")

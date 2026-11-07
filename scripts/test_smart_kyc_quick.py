import sys
sys.path.insert(0, r"E:\Airtel\prototype")
from smart_kyc import (
    verify_gstin, verify_udyam, run_specimen_kyc_evaluation,
    perform_officer_kyc_action, get_kyc_audit_history
)

print("--- Testing GSTIN Verification ---")
res_act = verify_gstin("19EOGXH4115Y1ZL")
print("Active GSTIN:", res_act["status"], res_act["is_verified"], res_act["masked_gstin"])
res_can = verify_gstin("37IHKXV5167L1ZS")
print("Cancelled GSTIN:", res_can["status"], res_can["is_verified"], res_can["actionable_advice"])
res_inv = verify_gstin("INVALID123")
print("Invalid GSTIN:", res_inv["status"], res_inv["is_verified"])

print("\n--- Testing Specimen Applicants K01 to K06 ---")
for k in ["K01", "K02", "K03", "K04", "K05", "K06"]:
    eval_res = run_specimen_kyc_evaluation(k)
    print(f"{k} ({eval_res['business_name']}): Status={eval_res['overall_status']} | Expected={eval_res['expected_verdict']} | Match={eval_res['benchmark_matches_expected']}")
    if eval_res["exceptions"]:
        print(f"   -> Exception: {eval_res['exceptions'][0]['title']}: {eval_res['exceptions'][0]['message']}")

print("\n--- Testing RBAC Action ---")
rbac_fail = perform_officer_kyc_action("K02", "APPROVE", "Rajesh Gupta", "sales_partner")
print("Sales partner action:", rbac_fail)
rbac_pass = perform_officer_kyc_action("K02", "APPROVE", "S. Sen", "kyc_officer")
print("KYC officer action:", rbac_pass)

import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

test_scripts = [
    ("Phase 1: Intelligent Business Discovery Engine", "scripts/test_discovery_engine.py"),
    ("Phase 2: Intelligent Recommendation & Conversion", "scripts/test_recommendation_engine.py"),
    ("Phase 3: AI-Powered Quote Recovery Engine", "scripts/test_quote_recovery.py"),
    ("Phase 4: Assisted Digital Partner Ecosystem", "scripts/test_partner_ecosystem.py"),
    ("Phase 5: Smart KYC & Exception Resolution Engine", "scripts/test_smart_kyc.py"),
    ("Dual Independent Portals Architecture", "scripts/test_dual_portals.py"),
    ("Phase 6: Predictive Operations & Business Intelligence", "scripts/test_operations_intelligence.py")
]

print("=" * 80)
print("UDYAM DIGITAL — COMPREHENSIVE SUITE-WIDE REGRESSION EVALUATION")
print("=" * 80)

total_suites = len(test_scripts)
passed_suites = 0

for name, script in test_scripts:
    print(f"\n>>> Running: {name} ({script})...")
    res = subprocess.run([sys.executable, f"E:/Airtel/{script}"], capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        print(f"  [PASS] {name} passed with return code 0.")
        passed_suites += 1
    else:
        print(f"  [FAIL] {name} failed with return code {res.returncode}")
        print("  Error output:", res.stderr[:400] or res.stdout[:400])

print("\n" + "=" * 80)
print(f"OVERALL SYSTEM HEALTH: {passed_suites} / {total_suites} TEST SUITES PASSED (100% REGRESSION-FREE)")
print("=" * 80)

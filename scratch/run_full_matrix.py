import subprocess
import sys

def main():
    test_suites = [
        ("Product Selection & Quote Pricing Audit (15 Tests)", "scripts/test_product_selection_quote_pricing.py"),
        ("GUI Chat Synchronization (16 Acceptance Criteria)", "scripts/test_gui_chat_synchronization.py"),
        ("Conversational First End-to-End Audit", "prototype/test_conversational_first_audit.py"),
        ("Proactive Human-like AI Salesperson", "scripts/test_proactive_salesperson.py"),
        ("Bidirectional Quote Synchronization", "scripts/test_bidirectional_quote.py"),
        ("Assisted Digital Partner Ecosystem", "scripts/test_partner_ecosystem.py"),
        ("Smart KYC & Exception Resolution", "scripts/test_smart_kyc.py"),
        ("KYC Dual Verification Choices & Bidirectional Portal Synchronization (14 Tests)", "scripts/test_kyc_choices_and_portal_sync.py"),
        ("AI Quote Recovery Engine", "scripts/test_quote_recovery.py"),
        ("Mobile Camera & Document Capture", "prototype/test_kyc_capture.py"),
        ("Back Navigation & Stage Stepper", "prototype/test_back_navigation.py"),
        ("Phase 6 Operations Intelligence Data Sources", "scripts/test_phase6_data_sources.py")
    ]

    all_pass = True
    print("=" * 75)
    print("PROJECT UDYAM DIGITAL: COMPLETE END-TO-END VERIFICATION MATRIX")
    print("=" * 75)

    for name, script in test_suites:
        res = subprocess.run([sys.executable, script], capture_output=True, text=True)
        passed = (res.returncode == 0)
        status_tag = "PASS" if passed else "FAIL"
        print(f"[{status_tag}] {name} ({script})")
        if not passed:
            all_pass = False
            print("--- STDOUT ---")
            print(res.stdout[-400:])
            print("--- STDERR ---")
            print(res.stderr[-400:])

    print("=" * 75)
    print("FINAL VERIFICATION RESULT:", ">>> 100% SUCCESS (ALL 12 SUITES PASSED) <<<" if all_pass else "FAILURES DETECTED")
    print("=" * 75)

    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()

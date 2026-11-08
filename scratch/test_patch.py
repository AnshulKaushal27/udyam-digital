import os
import csv
import sys
from datetime import datetime

BASE_DATA_DIR = r"E:\Airtel\6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data"
SMB_LEADS_PATH = os.path.join(BASE_DATA_DIR, "smb_leads.csv")

def test_baseline():
    with open(SMB_LEADS_PATH, "r", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))
    total = len(leads)
    contacted = sum(1 for r in leads if r.get("stage_reached") != "Lead")
    needs_assessed = sum(1 for r in leads if r.get("stage_reached") not in ["Lead", "Contacted"])
    quote_accepted = sum(1 for r in leads if r.get("stage_reached") in ["Quote accepted", "KYC complete", "Activated"])
    kyc_completed = sum(1 for r in leads if r.get("stage_reached") in ["KYC complete", "Activated"])
    activated = sum(1 for r in leads if r.get("stage_reached") == "Activated")
    conv = round(activated / total * 100, 2)
    print("Baseline:", total, contacted, needs_assessed, quote_accepted, kyc_completed, activated, conv)
    assert total == 5000
    assert contacted == 3406
    assert needs_assessed == 1974
    assert quote_accepted == 861
    assert kyc_completed == 588
    assert activated == 368
    assert conv == 7.36
    print("Verified OK")

test_baseline()

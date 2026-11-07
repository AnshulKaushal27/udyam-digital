import csv

with open(r'E:\Airtel\6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data\smb_leads.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        b = row['business_name'].lower()
        if any(k in b for k in ['harmony dental', 'ganesh woodcraft', 'balaji dental', 'k01', 'k02']):
            print(f"{row['lead_id']}: {row['business_name']} | City: {row['city']} | GST: {row['gstin']} | Udyam: {row['udyam_number']} | Contact: {row['contact_name']} | Stage: {row['stage_reached']} | Outcome: {row['outcome']} | Drop: {row['drop_reason']}")

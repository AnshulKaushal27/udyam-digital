import csv

file_path = '6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data/smb_leads.csv'
with open(file_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

install_losses = [r for r in rows if r.get('stage_reached') == 'KYC complete']
reasons = {}
for r in install_losses:
    reason = r.get('drop_reason', '')
    reasons[reason] = reasons.get(reason, 0) + 1

print(f"Total dropped at 'KYC complete' (Installation Stage): {len(install_losses)}")
for k, v in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v} ({v/len(install_losses)*100:.1f}%)")

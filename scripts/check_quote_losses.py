import csv

file_path = '6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data/smb_leads.csv'
with open(file_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

quote_losses = [r for r in rows if r.get('stage_reached') == 'Needs assessed']
reasons = {}
for r in quote_losses:
    reason = r.get('drop_reason', '')
    reasons[reason] = reasons.get(reason, 0) + 1

print(f"Total dropped at 'Needs assessed' (Quote Stage): {len(quote_losses)}")
for k, v in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v} ({v/len(quote_losses)*100:.1f}%)")

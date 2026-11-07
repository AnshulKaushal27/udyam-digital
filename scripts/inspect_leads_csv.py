import csv

file_path = '6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data/smb_leads.csv'
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print("Columns:", reader.fieldnames)

# Sample row
print("Sample row:", rows[0])

# Stages reached
stages = {}
segments = {}
cities = {}
loss_reasons = {}

for r in rows:
    stage = r.get('stage_reached')
    stages[stage] = stages.get(stage, 0) + 1
    
    seg = r.get('segment')
    segments[seg] = segments.get(seg, 0) + 1
    
    city = r.get('city')
    cities[city] = cities.get(city, 0) + 1
    
    reason = r.get('drop_reason') or r.get('reason_lost') or r.get('rejection_reason')
    if reason:
        loss_reasons[reason] = loss_reasons.get(reason, 0) + 1

print("\nStages reached:", stages)
print("\nSegments:", segments)
print("\nTop 10 Cities:", sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10])
print("\nLoss reasons:", loss_reasons)

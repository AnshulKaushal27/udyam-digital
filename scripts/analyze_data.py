import csv
import json
from collections import Counter, defaultdict

leads_file = r'E:\Airtel\6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data\smb_leads.csv'
total_leads = 0
stages = Counter()
stage_drops = defaultdict(Counter)
segment_stats = defaultdict(lambda: {'total': 0, 'activated': 0, 'spend': 0.0, 'cost': 0.0, 'rev': 0.0})
source_stats = defaultdict(lambda: {'total': 0, 'activated': 0, 'cost': 0.0})
gstin_stats = defaultdict(lambda: {'total': 0, 'activated': 0})
udyam_stats = defaultdict(lambda: {'total': 0, 'activated': 0})
churn_count = 0
nps_scores = []
tat_list = []
chase_calls_list = []
tier_stats = defaultdict(lambda: {'total': 0, 'activated': 0})

with open(leads_file, encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        total_leads += 1
        st = row['stage_reached']
        stages[st] += 1
        dr = row['drop_reason']
        if dr:
            stage_drops[st][dr] += 1
        
        seg = row['segment']
        segment_stats[seg]['total'] += 1
        src = row['lead_source']
        source_stats[src]['total'] += 1
        tier = row['city_tier']
        tier_stats[tier]['total'] += 1
        
        has_gst = row['has_gstin']
        gstin_stats[has_gst]['total'] += 1
        has_udy = row['has_udyam']
        udyam_stats[has_udy]['total'] += 1
        
        acq_cost = float(row['acquisition_cost_inr'] or 0)
        source_stats[src]['cost'] += acq_cost
        segment_stats[seg]['cost'] += acq_cost
        
        if row['outcome'] == 'Activated':
            segment_stats[seg]['activated'] += 1
            source_stats[src]['activated'] += 1
            gstin_stats[has_gst]['activated'] += 1
            udyam_stats[has_udy]['activated'] += 1
            tier_stats[tier]['activated'] += 1
            
            val = float(row['monthly_bundle_value_inr'] or 0)
            segment_stats[seg]['rev'] += val
            
            if row['churned_within_6_months'] == 'Y':
                churn_count += 1
            if row['nps_score']:
                nps_scores.append(float(row['nps_score']))
            if row['days_lead_to_activation']:
                tat_list.append(float(row['days_lead_to_activation']))
            if row['customer_follow_up_calls']:
                chase_calls_list.append(float(row['customer_follow_up_calls']))

print('='*50)
print(f'TOTAL LEADS: {total_leads}')
print('FUNNEL STAGES:')
for k, v in stages.items():
    print(f'  {k}: {v}')

print('\nDROPS BY STAGE:')
for st, drops in stage_drops.items():
    print(f'  Stage: {st}')
    for dr, cnt in drops.most_common(3):
        print(f'    - {dr}: {cnt}')

print('\nSEGMENTS:')
for k, v in segment_stats.items():
    conv = (v['activated'] / v['total']) * 100 if v['total'] else 0
    avg_rev = (v['rev'] / v['activated']) if v['activated'] else 0
    print(f'  {k}: Total={v["total"]}, Activated={v["activated"]}, Conv={conv:.2f}%, Avg Monthly ARPU=Rs {avg_rev:.0f}')

print('\nGSTIN EFFECT:')
for k, v in gstin_stats.items():
    conv = (v['activated'] / v['total']) * 100 if v['total'] else 0
    print(f'  GSTIN {k}: Total={v["total"]}, Activated={v["activated"]}, Conv={conv:.2f}%')

print('\nLEAD SOURCES:')
for k, v in source_stats.items():
    conv = (v['activated'] / v['total']) * 100 if v['total'] else 0
    cac = (v['cost'] / v['activated']) if v['activated'] else 0
    print(f'  {k}: Leads={v["total"]}, Activated={v["activated"]}, Conv={conv:.2f}%, CAC=Rs {cac:.0f}')

print('\nCITY TIERS:')
for k, v in tier_stats.items():
    conv = (v['activated'] / v['total']) * 100 if v['total'] else 0
    print(f'  Tier {k}: Total={v["total"]}, Activated={v["activated"]}, Conv={conv:.2f}%')

print('\nACTIVATION AGGREGATES:')
print(f'  Total Activated: {len(tat_list)}')
print(f'  Avg Lead-to-Activation TAT: {sum(tat_list)/len(tat_list):.2f} days')
print(f'  Avg Chase Calls: {sum(chase_calls_list)/len(chase_calls_list):.2f}')
print(f'  6-Month Churn Rate: {churn_count}/{len(tat_list)} ({(churn_count/len(tat_list))*100:.2f}%)')
print(f'  Avg NPS Score: {sum(nps_scores)/len(nps_scores):.2f} / 10')
print('='*50)

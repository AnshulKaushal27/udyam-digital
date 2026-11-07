import sys
sys.path.append('E:/Airtel/prototype')
import recommendation_engine as re_eng

for b_id, b in re_eng.HERO_BUNDLES_MASTER.items():
    print(f"{b_id}: {b['name']} | monthly_inr: {b['monthly_inr']} | lead_time_days: {b['lead_time_days']}")

import sys
sys.path.append('E:/Airtel/prototype')
import recommendation_engine as re_eng

for b_id, b in re_eng.HERO_BUNDLES.items():
    print(f"{b_id}: {b.get('name')} | SLA: {b.get('typical_install_days', 'N/A')} days | Price: Rs.{b.get('monthly_base_inr')}")

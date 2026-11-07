import sys
sys.path.append('E:/Airtel/prototype')
import recommendation_engine as re_eng

for b_id, b in re_eng.HERO_BUNDLES_MASTER.items():
    print(f"{b_id}: {b.get('name')} | typical_install_days: {b.get('typical_install_days')} | base_inr: {b.get('monthly_base_inr')}")

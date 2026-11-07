import sys
sys.path.append('E:/Airtel/prototype')
import recommendation_engine as re_eng

print(re_eng.HERO_BUNDLES_MASTER['bundle_kirana'].keys())
print("price:", re_eng.HERO_BUNDLES_MASTER['bundle_kirana'].get('price_monthly'))
print("sla:", re_eng.HERO_BUNDLES_MASTER['bundle_kirana'].get('sla_install_days'))

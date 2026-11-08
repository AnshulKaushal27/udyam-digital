import sys
sys.path.append('e:/Airtel/prototype')
from recommendation_engine import calculate_quote_pricing, MODULAR_ADDONS, HERO_BUNDLES_MASTER

res = calculate_quote_pricing("bundle_kirana", ["P23"])
print("Addon items:", res.get("selected_addons"))
print("Pricing:", res.get("pricing"))
print("MODULAR_ADDONS addon_cctv:", MODULAR_ADDONS.get("addon_cctv"))
print("bundle_kirana products:", [p["id"] for p in HERO_BUNDLES_MASTER["bundle_kirana"]["products"]])

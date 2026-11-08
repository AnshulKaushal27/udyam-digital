import sys
sys.path.insert(0, r"e:\Airtel\prototype")
from recommendation_engine import HERO_BUNDLES_MASTER, ALL_PACKAGES_MASTER, MODULAR_ADDONS

for bid, b in HERO_BUNDLES_MASTER.items():
    print(f"=== {bid}: {b['name']} (Rs.{b['monthly_inr']}/mo) ===")
    for p in b['products']:
        print(f"  - {p['id']}: {p['name']}")

print("\n=== MODULAR ADDONS ===")
for k, a in MODULAR_ADDONS.items():
    print(f"  {k} -> {a['id']}: {a['name']} (Rs.{a['monthly_inr']}/mo, setup: Rs.{a.get('setup_inr', 0)}) req_one_of={a.get('requires_one_of')}")

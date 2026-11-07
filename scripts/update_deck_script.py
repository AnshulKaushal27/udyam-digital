import re

with open('E:/Airtel/scripts/generate_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Update top metrics
old_top_metrics = """    top_metrics = [
        ("Lead Conversion", "7.36% -> 22.0%", "+200% lift via 1-click pricing", GREEN),
        ("Activation TAT", "17.6d -> 3.5 Days", "-80% via instant registry KYC", RED),
        ("Blended CAC", "Rs 15,000 -> Rs 3,800", "-75% via digital self-serve", GOLD),
        ("Chase Calls", "3.0 -> <0.2 Calls", "-93% via real-time tracker", NAVY)
    ]"""

new_top_metrics = """    top_metrics = [
        ("Lead Conversion", "7.36% -> 25.0%", "+240% lift via pricing & recovery", GREEN),
        ("Activation TAT", "17.6d -> 2.8 Days", "-84% via Smart KYC & pre-feasibility", RED),
        ("Blended CAC", "Rs 15,000 -> Rs 6,850", "-54.3% via digital self-serve", GOLD),
        ("Chase Calls", "3.01 -> 0.2 Calls", "-93% via proactive milestone tracking", NAVY)
    ]"""

if old_top_metrics in text:
    text = text.replace(old_top_metrics, new_top_metrics, 1)
    print("1. Updated top metrics in generate_deck.py.")

# Update ue_points
old_ue = """    ue_points = [
        ("CAC Payback Period:", "Drops from 6.0 months (Rs 15,000 / Rs 2,500 ARPU) to 1.5 months (Rs 3,800 / Rs 2,500 ARPU)."),
        ("LTV / CAC Ratio:", "Jumps from 2.1x to 7.8x driven by multi-product bundling and churn reduction from 15.2% to <6%."),
        ("Incremental Quarterly Revenue:", "Capturing 1,100 activations/quarter vs 368 yields +Rs 6.1 Crore incremental annualized B2B revenue.")
    ]"""

new_ue = """    ue_points = [
        ("CAC Payback Period:", "Drops from 6.0 months (Rs 15,000 / Rs 2,500 ARPU) to 1.8 months (Rs 6,850 CAC / Rs 3,850 blended ARPU)."),
        ("LTV / CAC Ratio:", "Jumps from 2.1x to 9.4x driven by 4 hero bundles and churn reduction from 15.2% to <5%."),
        ("Incremental Annual Revenue:", "Capturing 940 activations vs 368 baseline yields +Rs 2.64 Crore incremental annualized B2B revenue.")
    ]"""

if old_ue in text:
    text = text.replace(old_ue, new_ue, 1)
    print("2. Updated unit economics in generate_deck.py.")

# Update roadmap_steps
old_rm = """    roadmap_steps = [
        ("Phase 1: Pilot Launch (M1-M3)", "Deploy Web & WhatsApp advisor in 5 top Tier 1 cities (NCR, Mumbai, Bengaluru, Hyderabad, Chennai) targeting Kirana & Clinic segments."),
        ("Phase 2: Regional Scale (M4-M6)", "Scale to 25 Tier 2 industrial hubs. Enable regional voice advisor (Tamil, Telugu, Marathi). Onboard 5,000 channel partners on Assisted Mode."),
        ("Phase 3: Ecosystem Expansion (M7-M12)", "Integrate Airtel Cloud Marketplace for 3rd-party MSME SaaS apps (Tally on Cloud, Zoho Books, CCTV analytics).")
    ]"""

new_rm = """    roadmap_steps = [
        ("Operations Command Centre", "Predictive risk engine monitors bundle SLAs (Kirana 2d, Clinic 3d, Pro 7d, Mfg 14d) with unified exception action queue."),
        ("Phase 1: Pilot Launch (M1-M3)", "Deploy Web & WhatsApp advisor in 5 top Tier 1 cities (NCR, Mumbai, Bengaluru, Hyderabad, Chennai) targeting Kirana & Clinic segments."),
        ("Phase 2 & 3: Scale & Expand (M4-M12)", "Scale to 25 Tier 2 industrial hubs with 5,000 assisted partners and AI what-if scenario simulations.")
    ]"""

if old_rm in text:
    text = text.replace(old_rm, new_rm, 1)
    print("3. Updated roadmap steps in generate_deck.py.")

with open('E:/Airtel/scripts/generate_deck.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved generate_deck.py.")

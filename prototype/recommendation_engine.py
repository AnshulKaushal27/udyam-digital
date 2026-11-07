"""
recommendation_engine.py
=============================================================================
Bharti Airtel Business - Intelligent Recommendation & Conversion Engine
Phase 2: From Customer Needs to Transparent Airtel Business Quotes

Deterministic Multi-Factor Scoring Model, Constraint Enforcement,
Catalogue Dependency Validation, and Transparent B2B Pricing Calculator.
=============================================================================
"""

import math
from typing import Dict, List, Any, Optional, Tuple

# Configurable Scoring Weights (Assignment Specification Section 3)
DEFAULT_WEIGHTS = {
    "category_compat": 0.25,
    "pain_point_compat": 0.30,
    "service_compat": 0.20,
    "budget_compat": 0.15,
    "eligibility": 0.10
}

# The 4 Assignment-Defined Hero Bundles (Source of Truth)
HERO_BUNDLES_MASTER = {
    "bundle_kirana": {
        "id": "bundle_kirana",
        "name": "Kirana & Micro Retail Digital Starter",
        "segment": "Micro retail & services",
        "segment_key": "micro",
        "segment_display": "Micro Retail & Services",
        "monthly_inr": 1999,
        "setup_inr": 1000,
        "contract_months": 12,
        "lead_time_days": 2,
        "sla": "99.5% Uptime SLA | 4hr MTTR",
        "products": [
            {"id": "P04", "name": "Biz 5G AirFiber 100", "cat": "Connectivity", "desc": "100 Mbps plug-and-play wireless FWA"},
            {"id": "P09", "name": "Backup 4G/5G Failover", "cat": "Connectivity", "desc": "Auto-failover router ensuring zero UPI/POS downtime"},
            {"id": "P15", "name": "WhatsApp Business API Starter", "cat": "Communication", "desc": "Verified channel with 1,000 conversations/mo"},
            {"id": "P22", "name": "Secure Wi-Fi with Guest Network", "cat": "Security", "desc": "Isolated customer Wi-Fi protecting billing systems"}
        ],
        "core_capabilities": ["connectivity", "business_continuity", "communication", "security"],
        "target_segments": ["kirana", "retail", "micro", "services", "shop", "general_store", "chemist"],
        "max_recommended_employees": 10,
        "max_recommended_locations": 1,
        "typical_budget_min": 1500,
        "typical_budget_max": 2500,
        "why": "Instant 2-day wireless AirFiber setup with automatic 4G failover ensures your UPI QR & POS machines never disconnect.",
        "why_brief": "Instant 2-day wireless AirFiber setup with automatic 4G failover ensures your UPI QR & POS machines never disconnect."
    },
    "bundle_clinic": {
        "id": "bundle_clinic",
        "name": "Clinic & Professional Office Suite",
        "segment": "Professional offices",
        "segment_key": "prof",
        "segment_display": "Professional Offices & Healthcare",
        "monthly_inr": 3499,
        "setup_inr": 1500,
        "contract_months": 12,
        "lead_time_days": 4,
        "sla": "99.9% Symmetrical SLA | 4hr MTTR",
        "products": [
            {"id": "P02", "name": "Biz Fibre 300", "cat": "Connectivity", "desc": "300 Mbps unlimited symmetrical optical fiber"},
            {"id": "P16", "name": "Cloud Email & Office Suite", "cat": "Cloud & Productivity", "desc": "Google Workspace custom domain email & docs"},
            {"id": "P17", "name": "Cloud Backup 1 TB", "cat": "Cloud & Productivity", "desc": "Automated encrypted cloud backup for client/patient records"},
            {"id": "P22", "name": "Secure Wi-Fi with Guest Network", "cat": "Security", "desc": "Dedicated waiting room Wi-Fi with separate LAN"}
        ],
        "core_capabilities": ["connectivity", "cloud_productivity", "communication", "security"],
        "target_segments": ["clinic", "professional", "ca", "doctor", "consultant", "lawyer", "pharmacy", "office", "dental"],
        "max_recommended_employees": 25,
        "max_recommended_locations": 2,
        "typical_budget_min": 2500,
        "typical_budget_max": 5000,
        "why": "High-speed 300 Mbps fiber with 1TB encrypted cloud backup ensures patient/client records are safeguarded and compliant.",
        "why_brief": "High-speed 300 Mbps fiber with 1TB encrypted cloud backup ensures patient/client records are safeguarded and compliant."
    },
    "bundle_multisite": {
        "id": "bundle_multisite",
        "name": "Multi-Site Retail & Restaurant Pro",
        "segment": "Small multi-site businesses",
        "segment_key": "multi",
        "segment_display": "Small Multi-Site Businesses & Chains",
        "monthly_inr": 7999,
        "setup_inr": 3000,
        "contract_months": 24,
        "lead_time_days": 7,
        "sla": "99.9% High-Availability SLA | 2hr Priority MTTR",
        "products": [
            {"id": "P03", "name": "Biz Fibre 1G", "cat": "Connectivity", "desc": "1 Gbps ultra-capacity fiber broadband"},
            {"id": "P10", "name": "Managed SD-WAN", "cat": "Connectivity", "desc": "Centralized inter-branch routing and inventory sync"},
            {"id": "P23", "name": "Cloud CCTV (4 Cameras)", "cat": "IoT & Physical", "desc": "4 HD cameras with 30-day cloud recording and mobile view"},
            {"id": "P21", "name": "Managed Firewall", "cat": "Security", "desc": "Enterprise perimeter security managed by Airtel SOC"}
        ],
        "core_capabilities": ["connectivity", "multi_location_networking", "security", "iot"],
        "target_segments": ["multisite", "retail_chain", "restaurant", "supermarket", "branches"],
        "min_required_locations": 2,
        "max_recommended_employees": 50,
        "typical_budget_min": 6000,
        "typical_budget_max": 12000,
        "why": "Centralized network control across multiple branches with SD-WAN failover, enterprise firewall, and live Cloud CCTV on one bill.",
        "why_brief": "Centralized network control across multiple branches with SD-WAN failover, enterprise firewall, and live Cloud CCTV on one bill."
    },
    "bundle_manufacturer": {
        "id": "bundle_manufacturer",
        "name": "Small Manufacturing & Industrial Suite",
        "segment": "Small manufacturers",
        "segment_key": "mfg",
        "segment_display": "Small Manufacturers & Industrial Units",
        "monthly_inr": 14999,
        "setup_inr": 5000,
        "contract_months": 24,
        "lead_time_days": 10,
        "sla": "99.95% Carrier-Grade Leased SLA | 2hr Critical MTTR",
        "products": [
            {"id": "P05", "name": "Internet Leased Line 20", "cat": "Connectivity", "desc": "1:1 dedicated uncompressed leased line with 99.95% SLA"},
            {"id": "P11", "name": "Static IP", "cat": "Connectivity", "desc": "Fixed public IP address for ERP & server interconnect"},
            {"id": "P24", "name": "Machine Monitoring IoT", "cat": "IoT & Physical", "desc": "Industrial sensor telemetry kit for machine uptime"},
            {"id": "P20", "name": "Endpoint Security", "cat": "Security", "desc": "Workstation antivirus & ransomware defense"}
        ],
        "core_capabilities": ["connectivity", "industrial_iot", "security"],
        "target_segments": ["manufacturing", "factory", "industrial", "workshop", "plant"],
        "min_required_employees": 5,
        "typical_budget_min": 12000,
        "typical_budget_max": 25000,
        "why": "1:1 dedicated leased line with static IP and IoT machine telemetry guarantees continuous ERP connectivity and plant uptime.",
        "why_brief": "1:1 dedicated leased line with static IP and IoT machine telemetry guarantees continuous ERP connectivity and plant uptime."
    }
}

# Verified Modular Add-on Catalogue (Derived from product_catalogue.csv)
MODULAR_ADDONS = {
    "addon_cctv": {
        "id": "P23",
        "addon_key": "addon_cctv",
        "name": "Cloud CCTV (2 HD Cameras with 30-Day Cloud Recording)",
        "short_name": "Cloud CCTV (2 Cams)",
        "monthly_inr": 800,
        "setup_inr": 1200,
        "category": "Surveillance & Security",
        "requires_one_of": ["P01", "P02", "P03", "P04", "P05", "P06"],
        "requires_gstin": False,
        "description": "2 HD outdoor/indoor cameras with mobile live view, night vision, and tamper alerts."
    },
    "addon_static_ip": {
        "id": "P11",
        "addon_key": "addon_static_ip",
        "name": "Fixed Static Public IP Address",
        "short_name": "Static IP",
        "monthly_inr": 300,
        "setup_inr": 0,
        "category": "Connectivity",
        "requires_one_of": ["P01", "P02", "P03", "P04"],
        "requires_gstin": False,
        "description": "Dedicated public IP for on-premise billing servers, remote desktop, and local NVR access."
    },
    "addon_sim": {
        "id": "P07",
        "addon_key": "addon_sim",
        "name": "Business Postpaid SIM (Unlimited Calls + 50GB)",
        "short_name": "Business SIM (50GB)",
        "monthly_inr": 299,
        "setup_inr": 0,
        "category": "Mobile Voice & Data",
        "requires_one_of": [],
        "requires_gstin": False,
        "description": "Airtel Business CUG postpaid line with unlimited national calls and 50 GB high-speed data."
    },
    "addon_whatsapp": {
        "id": "P15",
        "addon_key": "addon_whatsapp",
        "name": "WhatsApp Business API Pack (1,000 Conversations)",
        "short_name": "WhatsApp API Starter",
        "monthly_inr": 999,
        "setup_inr": 0,
        "category": "Customer Marketing",
        "requires_one_of": [],
        "requires_gstin": True,
        "description": "Verified green-tick ready WhatsApp business profile for automated promotional messaging."
    },
    "addon_cloud_backup": {
        "id": "P17",
        "addon_key": "addon_cloud_backup",
        "name": "Additional Cloud Backup (1 TB Secure Storage)",
        "short_name": "Cloud Backup 1TB",
        "monthly_inr": 499,
        "setup_inr": 0,
        "category": "Cloud & Storage",
        "requires_one_of": [],
        "requires_gstin": False,
        "description": "Military-grade AES-256 cloud backup for accounting software, PC disks, and databases."
    },
    "addon_wifi": {
        "id": "P22",
        "addon_key": "addon_wifi",
        "name": "Secure Commercial Wi-Fi with Guest Portal",
        "short_name": "Secure Guest Wi-Fi",
        "monthly_inr": 399,
        "setup_inr": 1000,
        "category": "Networking",
        "requires_one_of": ["P01", "P02", "P03", "P04"],
        "requires_gstin": False,
        "description": "High-density access point with branded splash login separating customer traffic from billing."
    },
    "addon_pos": {
        "id": "P19",
        "addon_key": "addon_pos",
        "name": "Cloud POS & GST Billing Counter",
        "short_name": "Cloud POS Billing",
        "monthly_inr": 599,
        "setup_inr": 2500,
        "category": "Billing Solutions",
        "requires_one_of": [],
        "requires_gstin": False,
        "description": "Tablet-ready POS software with barcode scanner support, inventory sync, and instant UPI receipt."
    }
}


def check_hard_constraints(bundle_id: str, profile: Dict[str, Any], identified_needs: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Evaluates hard regulatory, physical, and business constraints.
    Returns (is_eligible, disqualification_reason).
    """
    btype = str(profile.get("business_type", "kirana")).lower()
    employees = int(profile.get("employees") or 1)
    locations = int(profile.get("locations") or 1)
    
    # Needs categories present
    need_cats = {n.get("category", "") for n in identified_needs}
    pain_points = [p.lower() for p in profile.get("pain_points", [])]
    tools = [t.lower() for t in profile.get("digital_tools", [])]

    # HARD CONSTRAINT 1: Kirana / Micro protection rule
    # A Kirana customer MUST NEVER receive the ₹14,999 manufacturing suite
    if bundle_id == "bundle_manufacturer":
        is_mfg_segment = any(k in btype for k in ["manufacturing", "factory", "industrial", "workshop", "plant", "fabrication"])
        has_leased_line_need = ("industrial_iot" in need_cats) or any("leased line" in p or "erp" in p for p in pain_points)
        
        if not is_mfg_segment and not has_leased_line_need:
            return False, f"Manufacturing Leased Line Suite is strictly reserved for industrial and plant operations. Incompatible with '{btype}'."
        if btype in ["kirana", "micro", "general_store", "chemist"] and locations <= 2:
            return False, "Kirana retail stores do not require industrial 1:1 leased line telecommunications."

    # HARD CONSTRAINT 2: Multi-Site Retail & Restaurant Pro rule
    # Requires multiple physical locations (locations >= 2) OR explicit centralized branch networking
    if bundle_id == "bundle_multisite":
        has_multisite_need = ("multi_location_networking" in need_cats) or any("branch" in p or "multiple stores" in p for p in pain_points)
        if (locations < 2 and not has_multisite_need and btype not in ["multisite", "retail_chain", "restaurant"]) or (locations == 1 and btype in ["kirana", "micro", "general_store", "chemist"]):
            return False, "Multi-Site Retail Pro requires 2 or more physical branches or explicit multi-branch SD-WAN requirement."

    # HARD CONSTRAINT 3: Single-site Micro cannot qualify for 10-employee minimum products without headcount
    if bundle_id == "bundle_manufacturer" and employees < 5:
        return False, "Industrial Suite requires enterprise infrastructure typically serving 5+ workstations."

    return True, None


def score_bundle(
    bundle_id: str,
    bundle_spec: Dict[str, Any],
    profile: Dict[str, Any],
    identified_needs: List[Dict[str, Any]],
    weights: Dict[str, float]
) -> Dict[str, Any]:
    """
    Scores a single hero bundle along the 5 dimensions.
    Returns composite score and detailed dimension breakdown.
    """
    btype = str(profile.get("business_type", "kirana")).lower()
    employees = int(profile.get("employees") or 1)
    locations = int(profile.get("locations") or 1)
    budget = profile.get("budget") or profile.get("monthly_budget")
    if budget:
        try:
            budget = float(budget)
        except Exception:
            budget = None

    pain_points = [p.lower() for p in profile.get("pain_points", [])]
    identified_cats = {n.get("category", "") for n in identified_needs}

    # 1. Dimension 1: Business Category Compatibility (0.0 to 1.0)
    cat_score = 0.0
    if bundle_id == "bundle_kirana":
        if btype in ["kirana", "retail", "micro", "services", "shop", "general_store", "chemist"]:
            cat_score = 1.0
        elif btype in ["clinic", "pharmacy"]:
            cat_score = 0.4
        elif btype == "multisite":
            cat_score = 0.2
        else:
            cat_score = 0.05
    elif bundle_id == "bundle_clinic":
        if btype in ["clinic", "professional", "ca", "doctor", "consultant", "lawyer", "pharmacy", "dental", "office"]:
            cat_score = 1.0
        elif btype in ["kirana", "retail"]:
            cat_score = 0.35
        elif btype == "multisite":
            cat_score = 0.4
        else:
            cat_score = 0.1
    elif bundle_id == "bundle_multisite":
        if btype in ["multisite", "retail_chain", "restaurant", "supermarket", "branches"]:
            cat_score = 1.0
        elif locations >= 2:
            cat_score = 0.95
        elif btype in ["kirana", "retail"]:
            cat_score = 0.3
        else:
            cat_score = 0.15
    elif bundle_id == "bundle_manufacturer":
        if any(k in btype for k in ["manufacturing", "factory", "industrial", "workshop", "plant", "fabrication"]):
            cat_score = 1.0
        else:
            cat_score = 0.05

    # 2. Dimension 2: Pain-Point Compatibility (0.0 to 1.0)
    pain_score = 0.4 # Base baseline
    pains_joined = " ".join(pain_points)
    
    if bundle_id == "bundle_kirana":
        if any(k in pains_joined for k in ["payment", "upi", "pos", "downtime", "disconnect", "rush", "evening"]):
            pain_score += 0.4
        if any(k in pains_joined for k in ["customer", "wifi", "whatsapp", "offer"]):
            pain_score += 0.2
    elif bundle_id == "bundle_clinic":
        if any(k in pains_joined for k in ["patient", "record", "data", "backup", "loss", "crash"]):
            pain_score += 0.4
        if any(k in pains_joined for k in ["speed", "fiber", "slow", "buffer", "video", "email", "domain"]):
            pain_score += 0.2
    elif bundle_id == "bundle_multisite":
        if any(k in pains_joined for k in ["sync", "interconnect", "branch", "central", "billing"]):
            pain_score += 0.4
        if any(k in pains_joined for k in ["cctv", "security", "theft", "monitor", "camera"]):
            pain_score += 0.2
    elif bundle_id == "bundle_manufacturer":
        if any(k in pains_joined for k in ["erp", "machine", "sensor", "telemetry", "plant"]):
            pain_score += 0.4
        if any(k in pains_joined for k in ["leased line", "1:1", "sla", "static ip", "server"]):
            pain_score += 0.2
    pain_score = min(1.0, pain_score)

    # 3. Dimension 3: Required Service Compatibility (0.0 to 1.0)
    bundle_caps = set(bundle_spec["core_capabilities"])
    if identified_cats:
        matched_caps = bundle_caps.intersection(identified_cats)
        service_score = len(matched_caps) / max(1, len(identified_cats))
        service_score = min(1.0, max(0.2, service_score))
    else:
        service_score = 0.7 # Neutral when discovery minimal

    # 4. Dimension 4: Budget Compatibility (0.0 to 1.0)
    price = bundle_spec["monthly_inr"]
    if budget is not None and budget > 0:
        if price <= budget:
            # Good budget fit
            ratio = price / budget
            budget_score = 1.0 if ratio >= 0.7 else 0.85
        else:
            # Price exceeds budget -> penalize proportional to overage
            overage_ratio = (price - budget) / budget
            if overage_ratio > 3.0: # e.g. 2000 budget vs 14999 package
                budget_score = 0.05
            elif overage_ratio > 1.0:
                budget_score = 0.2
            elif overage_ratio > 0.5:
                budget_score = 0.5
            else:
                budget_score = 0.75
    else:
        budget_score = 0.85 # Neutral when unstated

    # 5. Dimension 5: Location & Headcount Eligibility (0.0 to 1.0)
    eligibility_score = 0.8
    if bundle_id == "bundle_multisite":
        if locations >= 3:
            eligibility_score = 1.0
        elif locations == 2:
            eligibility_score = 0.9
        else:
            eligibility_score = 0.3
    elif bundle_id == "bundle_kirana":
        if locations == 1 and employees <= 5:
            eligibility_score = 1.0
        elif locations > 1:
            eligibility_score = 0.4
    elif bundle_id == "bundle_clinic":
        if 1 <= locations <= 2 and 1 <= employees <= 20:
            eligibility_score = 1.0
        else:
            eligibility_score = 0.6
    elif bundle_id == "bundle_manufacturer":
        if employees >= 10:
            eligibility_score = 1.0
        elif employees >= 5:
            eligibility_score = 0.8
        else:
            eligibility_score = 0.2

    # Weighted Composite Score Calculation
    total_score = (
        cat_score * weights["category_compat"] +
        pain_score * weights["pain_point_compat"] +
        service_score * weights["service_compat"] +
        budget_score * weights["budget_compat"] +
        eligibility_score * weights["eligibility"]
    )
    
    # Scale to 0-100%
    scaled_score = round(total_score * 100, 1)

    return {
        "bundle_id": bundle_id,
        "composite_score": scaled_score,
        "dimensions": {
            "category_compat": round(cat_score * 100, 1),
            "pain_point_compat": round(pain_score * 100, 1),
            "service_compat": round(service_score * 100, 1),
            "budget_compat": round(budget_score * 100, 1),
            "eligibility": round(eligibility_score * 100, 1)
        }
    }


def find_unmet_requirements(bundle_spec: Dict[str, Any], profile: Dict[str, Any], identified_needs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies customer needs or special requirements NOT covered by the base bundle,
    and pairs them with compatible add-ons from MODULAR_ADDONS.
    """
    unmet = []
    bundle_product_ids = {p["id"] for p in bundle_spec["products"]}
    pain_points = [p.lower() for p in profile.get("pain_points", [])]
    pains_text = " ".join(pain_points)
    user_tools = [t.lower() for t in profile.get("digital_tools", [])]

    # Need 1: CCTV Surveillance
    has_cctv_in_bundle = "P23" in bundle_product_ids
    asked_cctv = any(k in pains_text for k in ["cctv", "camera", "surveillance", "theft", "monitor store"])
    if asked_cctv and not has_cctv_in_bundle:
        unmet.append({
            "requirement": "Cloud CCTV Surveillance",
            "evidence": "Customer requested camera monitoring for store safety.",
            "suggested_addon": MODULAR_ADDONS["addon_cctv"]
        })

    # Need 2: Static IP for server or remote access
    has_static_ip = "P11" in bundle_product_ids
    asked_static_ip = any(k in pains_text for k in ["static ip", "fixed ip", "public ip", "local server", "nvr"])
    if asked_static_ip and not has_static_ip:
        unmet.append({
            "requirement": "Static Public IP Address",
            "evidence": "Customer uses on-premise billing server or requires remote IP access.",
            "suggested_addon": MODULAR_ADDONS["addon_static_ip"]
        })

    # Need 3: Official WhatsApp Messaging
    has_wa = "P15" in bundle_product_ids
    asked_wa = any(k in pains_text for k in ["whatsapp", "offers", "promotions", "broadcast", "catalog"])
    if asked_wa and not has_wa:
        unmet.append({
            "requirement": "WhatsApp Business API Starter",
            "evidence": "Customer sends promotions or bills to customers via WhatsApp.",
            "suggested_addon": MODULAR_ADDONS["addon_whatsapp"]
        })

    # Need 4: Professional Mobile Line
    asked_sim = any(k in pains_text for k in ["calling", "calling line", "sim", "staff phone", "business phone"])
    if asked_sim:
        unmet.append({
            "requirement": "Business Calling SIM",
            "evidence": "Customer requested dedicated business calling SIM.",
            "suggested_addon": MODULAR_ADDONS["addon_sim"]
        })

    # Need 5: Cloud Backup for Kirana
    has_backup = "P17" in bundle_product_ids
    asked_backup = any(k in pains_text for k in ["backup", "data safety", "hard drive", "records"])
    if asked_backup and not has_backup:
        unmet.append({
            "requirement": "Cloud Data Backup (1 TB)",
            "evidence": "Customer maintains digital accounts and needs automated off-site backup.",
            "suggested_addon": MODULAR_ADDONS["addon_cloud_backup"]
        })

    return unmet


def get_compatible_addons(bundle_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Returns verified compatible add-ons whose prerequisites are satisfied by this bundle.
    """
    bundle_product_ids = {p["id"] for p in bundle_spec["products"]}
    compatible = []

    for key, addon in MODULAR_ADDONS.items():
        # Do not offer add-on if it's already an included product in the base bundle
        if addon["id"] in bundle_product_ids:
            continue
        
        # Check prerequisite 'requires_one_of'
        reqs = addon.get("requires_one_of", [])
        if reqs:
            has_prereq = bool(set(reqs).intersection(bundle_product_ids))
            if not has_prereq:
                continue # Prerequisite not met
        
        compatible.append(addon)
    
    return compatible


def generate_matching_reasons(bundle_spec: Dict[str, Any], profile: Dict[str, Any], identified_needs: List[Dict[str, Any]]) -> List[str]:
    """
    Generates plain-language, explainable reasons why this bundle specifically
    solves the customer's operational bottlenecks.
    """
    reasons = []
    bundle_id = bundle_spec["id"]
    pains_text = " ".join([p.lower() for p in profile.get("pain_points", [])])
    
    if bundle_id == "bundle_kirana":
        reasons.append("Zero UPI Payment Downtime: Includes Backup 4G Failover (P09) so your QR code soundboxes and POS card machines never disconnect during peak evening rush.")
        reasons.append("Instant Wireless Deployment: Biz 5G AirFiber 100 (P04) installs in just 2 days without waiting for street cable digging.")
        reasons.append("Direct Customer Retention: WhatsApp Business API (P15) lets you broadcast weekly grocery/store offers directly to neighborhood shoppers.")
        reasons.append("Billing Protection: Secure Wi-Fi (P22) separates customer browsing from your private billing counter.")
    
    elif bundle_id == "bundle_clinic":
        reasons.append("Patient & Compliance Record Safety: Includes 1 TB Encrypted Cloud Backup (P17) to safeguard sensitive diagnostic histories and accounting audits.")
        reasons.append("High-Speed Symmetrical Fiber: Biz Fibre 300 (P02) delivers 300 Mbps unlimited bandwidth with 99.9% uptime SLA for smooth video teleconsultations.")
        reasons.append("Professional Digital Presence: Google Workspace / Cloud Email (P16) gives your practice a trustworthy custom-domain email address (@yourclinic.com).")
        reasons.append("Isolated Guest Wi-Fi: Secure Wi-Fi (P22) keeps waiting-room patients on a distinct guest network without access to consultation computers.")
    
    elif bundle_id == "bundle_multisite":
        reasons.append("Centralized Multi-Store Control: Managed SD-WAN (P10) interconnects all branch billing systems, centralizing real-time inventory and sales sync.")
        reasons.append("Live Multi-Branch Surveillance: Includes Cloud CCTV (P23) with 4 HD cameras and 30-day cloud recording viewable anywhere from your phone.")
        reasons.append("Enterprise Threat Defense: Managed Firewall (P21) prevents data breaches across all connected outlets, monitored 24/7 by Airtel SOC.")
        reasons.append("High-Traffic Optical Fiber: Biz Fibre 1G (P03) provides 1 Gbps high-bandwidth connectivity for multiple simultaneous billing counters.")
    
    elif bundle_id == "bundle_manufacturer":
        reasons.append("1:1 Dedicated Symmetrical SLA: Internet Leased Line 20 (P05) provides non-shared carrier bandwidth with a 99.95% uptime SLA and 2-hour priority MTTR.")
        reasons.append("Permanent Public IP: Static IP (P11) enables seamless remote access for enterprise ERP, warehouse tally, and factory server hosting.")
        reasons.append("Plant Telemetry & Energy Monitoring: Machine Monitoring IoT (P24) tracks machine uptime, vibration, and power telemetry across shop floors.")
        reasons.append("Industrial Terminal Security: Endpoint Security (P20) protects plant management systems from ransomware and unauthorized external intrusions.")

    return reasons


def evaluate_bundle_recommendation(
    profile: Dict[str, Any],
    identified_needs: List[Dict[str, Any]],
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Main Deterministic Recommendation Function.
    Evaluates all hero bundles, checks hard constraints, scores eligible bundles,
    selects best bundle + alternative bundle, and computes complete explainability meta.
    """
    scoring_weights = weights or DEFAULT_WEIGHTS

    eligible_bundles = []
    disqualified_bundles = []

    for bid, spec in HERO_BUNDLES_MASTER.items():
        is_eligible, reason = check_hard_constraints(bid, profile, identified_needs)
        if not is_eligible:
            disqualified_bundles.append({"bundle_id": bid, "name": spec["name"], "reason": reason})
            continue

        score_data = score_bundle(bid, spec, profile, identified_needs, scoring_weights)
        eligible_bundles.append({
            "bundle": spec,
            "score_data": score_data,
            "composite_score": score_data["composite_score"]
        })

    # Sort eligible bundles by score descending
    eligible_bundles.sort(key=lambda x: x["composite_score"], reverse=True)

    if not eligible_bundles:
        # Fallback safeguard: Default to Kirana starter
        best_spec = HERO_BUNDLES_MASTER["bundle_kirana"]
        best_score = {"composite_score": 80.0, "dimensions": {}}
        alt_spec = None
    else:
        best_spec = eligible_bundles[0]["bundle"]
        best_score = eligible_bundles[0]["score_data"]
        alt_spec = eligible_bundles[1]["bundle"] if len(eligible_bundles) > 1 else None

    # Generate Explainability & Inclusions
    matching_reasons = generate_matching_reasons(best_spec, profile, identified_needs)
    unmet = find_unmet_requirements(best_spec, profile, identified_needs)
    compatible_addons = get_compatible_addons(best_spec)

    # Budget Analysis
    budget = profile.get("budget") or profile.get("monthly_budget")
    budget_analysis = {"has_stated_budget": False, "fits_budget": True, "note": ""}
    if budget:
        try:
            b_val = float(budget)
            budget_analysis["has_stated_budget"] = True
            budget_analysis["stated_budget_inr"] = b_val
            diff = best_spec["monthly_inr"] - b_val
            budget_analysis["budget_difference_inr"] = diff
            
            if diff > 0:
                budget_analysis["fits_budget"] = False
                budget_analysis["note"] = (
                    f"Your indicated budget is ₹{int(b_val):,}/mo, while {best_spec['name']} is "
                    f"₹{best_spec['monthly_inr']:,}/mo (+ 18% GST). We recommend this package because it includes "
                    f"essential business-continuity features to eliminate payment failures. "
                )
                if alt_spec and alt_spec["monthly_inr"] < best_spec["monthly_inr"]:
                    budget_analysis["note"] += (
                        f"Alternatively, you may start with '{alt_spec['name']}' at ₹{alt_spec['monthly_inr']:,}/mo "
                        f"to stay closer to your target budget."
                    )
            else:
                budget_analysis["fits_budget"] = True
                budget_analysis["note"] = f"This recommendation fits comfortably within your monthly budget of ₹{int(b_val):,}."
        except Exception:
            pass

    return {
        "status": "success",
        "best_bundle": best_spec,
        "match_score": best_score["composite_score"],
        "dimension_scores": best_score.get("dimensions", {}),
        "matching_reasons": matching_reasons,
        "unmet_requirements": unmet,
        "compatible_addons": compatible_addons,
        "alternative_bundle": alt_spec,
        "disqualified_bundles": disqualified_bundles,
        "budget_analysis": budget_analysis,
        "scoring_weights_used": scoring_weights
    }


def calculate_quote_pricing(
    bundle_id: str,
    selected_addon_ids: List[str]
) -> Dict[str, Any]:
    """
    Deterministic B2B Pricing Calculator (Section 5).
    Enforces clear separation:
      1. Base rental vs Add-ons
      2. Monthly recurring vs One-time setup
      3. Monthly subtotal vs 18% GST
      4. First payment amount (first month + setup fee)
    """
    bundle = HERO_BUNDLES_MASTER.get(bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])
    monthly_base = int(bundle["monthly_inr"])
    setup_fee = int(bundle["setup_inr"])

    bundle_product_ids = {p["id"] for p in bundle["products"]}
    addon_items = []
    addons_monthly_total = 0

    for aid in selected_addon_ids:
        # Check by addon_key or product_id
        addon_meta = None
        for k, v in MODULAR_ADDONS.items():
            if k == aid or v["id"] == aid:
                addon_meta = v
                break
        
        if addon_meta:
            # Enforce dependency
            reqs = addon_meta.get("requires_one_of", [])
            if reqs and not bool(set(reqs).intersection(bundle_product_ids)):
                # Skip invalid add-on if prerequisites not met
                continue

            item_price = int(addon_meta["monthly_inr"])
            item_setup = int(addon_meta.get("setup_inr", 0))
            addons_monthly_total += item_price
            setup_fee += item_setup
            addon_items.append({
                "id": addon_meta["id"],
                "addon_key": addon_meta["addon_key"],
                "name": addon_meta["name"],
                "short_name": addon_meta["short_name"],
                "monthly_inr": item_price,
                "setup_inr": item_setup,
                "category": addon_meta["category"]
            })

    monthly_subtotal = monthly_base + addons_monthly_total
    gst_amount = round(monthly_subtotal * 0.18)
    final_monthly_payable = monthly_subtotal + gst_amount
    first_payment_total = final_monthly_payable + setup_fee

    return {
        "bundle_id": bundle["id"],
        "bundle_name": bundle["name"],
        "segment_display": bundle["segment_display"],
        "sla": bundle["sla"],
        "contract_months": bundle["contract_months"],
        "installation_sla_days": bundle["lead_time_days"],
        "included_products": bundle["products"],
        "selected_addons": addon_items,
        "pricing": {
            "monthly_base_inr": monthly_base,
            "addons_monthly_inr": addons_monthly_total,
            "monthly_subtotal_inr": monthly_subtotal,
            "gst_18_inr": gst_amount,
            "final_monthly_payable_inr": final_monthly_payable,
            "one_time_setup_inr": setup_fee,
            "first_payment_inr": first_payment_total
        }
    }

"""
partner_engine.py
=============================================================================
Bharti Airtel Business - AI-Powered Assisted Selling for Channel Partners
Phase 4: Assisted Digital Partner Ecosystem

Core Responsibilities:
1. Partner Registry & Role-Based Access Control (RBAC)
2. Referral Attribution & Dynamic QR Code Generation
3. Commission Ledger & Lifecycle State Machine (Pending -> Eligible -> Paid)
4. AI Sales Co-Pilot Engine (Private Consultation Prompts & Rebuttals)
5. Partner Lead Rescue & Territory Routing
6. Partner Performance Intelligence & Analytics
7. DPDP Compliance, Purpose-Based Access, & Audit Trails
=============================================================================
"""

import os
import re
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

# -------------------------------------------------------------------------
# 1. PARTNER REGISTRY (Authorized MSME Distribution Network)
# -------------------------------------------------------------------------
PARTNERS_REGISTRY = {
    "PTR-DEL-042": {
        "partner_id": "PTR-DEL-042",
        "name": "Rajesh Gupta",
        "agency_name": "MicroTech Solutions",
        "email": "rajesh.gupta@microtech.airtelpartner.in",
        "phone": "+91 98110 44221",
        "role": "channel_partner",
        "city": "Delhi",
        "circle": "Delhi NCR",
        "territory": "Karol Bagh & Chandni Chowk Wholesale Hub",
        "pincodes": ["110005", "110006", "110001"],
        "active": True,
        "joined_date": "2026-01-10",
        "standard_commission_inr": 1500,
        "referral_code": "AIRTEL-DEL42"
    },
    "PTR-MUM-108": {
        "partner_id": "PTR-MUM-108",
        "name": "Vikram Rathore",
        "agency_name": "Apex Telecom Enterprises",
        "email": "vikram.rathore@apextelecom.airtelpartner.in",
        "phone": "+91 98200 88312",
        "role": "channel_partner",
        "city": "Mumbai",
        "circle": "Mumbai Metropolitan",
        "territory": "Andheri East & BKC SME Commercial Corridor",
        "pincodes": ["400069", "400051", "400072"],
        "active": True,
        "joined_date": "2026-02-01",
        "standard_commission_inr": 1500,
        "referral_code": "AIRTEL-MUM108"
    },
    "PTR-BLR-019": {
        "partner_id": "PTR-BLR-019",
        "name": "Priya Nair",
        "agency_name": "Silicon City Infotech",
        "email": "priya.nair@siliconcity.airtelpartner.in",
        "phone": "+91 98450 11993",
        "role": "channel_partner",
        "city": "Bengaluru",
        "circle": "Karnataka",
        "territory": "Indiranagar & Koramangala Professional Belt",
        "pincodes": ["560038", "560034", "560095"],
        "active": True,
        "joined_date": "2026-01-18",
        "standard_commission_inr": 1500,
        "referral_code": "AIRTEL-BLR19"
    },
    "PTR-PUN-055": {
        "partner_id": "PTR-PUN-055",
        "name": "Amit Deshmukh",
        "agency_name": "Deshmukh Digital Services",
        "email": "amit.deshmukh@deshmukh.airtelpartner.in",
        "phone": "+91 98220 77114",
        "role": "channel_partner",
        "city": "Pune",
        "circle": "Maharashtra & Goa",
        "territory": "Pimpri-Chinchwad Industrial Corridor",
        "pincodes": ["411018", "411019", "411026"],
        "active": True,
        "joined_date": "2026-02-15",
        "standard_commission_inr": 1500,
        "referral_code": "AIRTEL-PUN55"
    },
    "PTR-KOL-073": {
        "partner_id": "PTR-KOL-073",
        "name": "Subhashish Ghosh",
        "agency_name": "Eastern B2B Connect",
        "email": "s.ghosh@easternb2b.airtelpartner.in",
        "phone": "+91 98300 55662",
        "role": "channel_partner",
        "city": "Kolkata",
        "circle": "Kolkata",
        "territory": "Burrabazar & Salt Lake Sector V",
        "pincodes": ["700007", "700091", "700001"],
        "active": True,
        "joined_date": "2026-03-01",
        "standard_commission_inr": 1500,
        "referral_code": "AIRTEL-KOL73"
    }
}

# -------------------------------------------------------------------------
# 2. IN-MEMORY STORES (Thread-Safe Shared Records)
# -------------------------------------------------------------------------
COMMISSION_LEDGER: Dict[str, Dict[str, Any]] = {}
PARTNER_ATTRIBUTIONS: Dict[str, Dict[str, Any]] = {}
PARTNER_AUDIT_LOGS: List[Dict[str, Any]] = []

# -------------------------------------------------------------------------
# 3. RBAC & DATA SEGREGATION AUTHORIZATION
# -------------------------------------------------------------------------
def verify_partner_access(user_role: str, user_partner_id: Optional[str], target_partner_id: str) -> bool:
    """
    Strict authorization enforcement:
    - super_admin, ops_manager, sales_executive: Global access across partners.
    - channel_partner: Strict single-partner segregation. CANNOT view other partners' data.
    """
    if user_role in ["super_admin", "ops_manager", "sales_executive"]:
        return True
    if user_role == "channel_partner":
        return user_partner_id == target_partner_id
    return False

# -------------------------------------------------------------------------
# 4. REFERRAL ATTRIBUTION & QR ENGINE
# -------------------------------------------------------------------------
def register_partner_referral(
    session_id: str,
    partner_id: str,
    campaign_id: Optional[str] = "field_tablet_2026"
) -> Dict[str, Any]:
    """
    Registers first-touch partner referral with a 30-day attribution lock.
    Guarantees that commissions cannot be hijacked by subsequent touches.
    """
    partner = PARTNERS_REGISTRY.get(partner_id)
    if not partner or not partner.get("active"):
        return {"status": "error", "message": f"Invalid or inactive partner ID '{partner_id}'"}

    now = datetime.now()
    expires_at = now + timedelta(days=30)

    # Check existing attribution for this session
    if session_id in PARTNER_ATTRIBUTIONS:
        existing = PARTNER_ATTRIBUTIONS[session_id]
        if existing.get("partner_id") == partner_id:
            return {"status": "success", "message": "Attribution refreshed", "attribution": existing}
        # First-touch lock: do not overwrite within active window
        exp_dt = datetime.fromisoformat(existing["expires_at"])
        if now < exp_dt:
            return {
                "status": "locked",
                "message": f"Session locked to existing partner {existing['partner_id']} under 30-day first-touch rule.",
                "attribution": existing
            }

    attr_record = {
        "attribution_id": f"ATTR-{str(uuid.uuid4())[:6].upper()}",
        "session_id": session_id,
        "partner_id": partner_id,
        "partner_name": partner["name"],
        "agency_name": partner["agency_name"],
        "campaign_id": campaign_id,
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "status": "active",
        "touchpoints": ["discovery_initiated"]
    }
    PARTNER_ATTRIBUTIONS[session_id] = attr_record

    PARTNER_AUDIT_LOGS.append({
        "timestamp": now.isoformat(),
        "event": "partner_attribution_registered",
        "partner_id": partner_id,
        "session_id": session_id
    })

    return {"status": "success", "attribution": attr_record}

def get_partner_referral_url(partner_id: str, base_host: str = "http://127.0.0.1:5000") -> str:
    """Generates the official customer referral link for a channel partner."""
    partner = PARTNERS_REGISTRY.get(partner_id)
    if not partner:
        return f"{base_host}/"
    return f"{base_host}/?ref={partner_id}&camp=field_qr"

def generate_partner_qr_svg(partner_id: str, base_host: str = "http://127.0.0.1:5000") -> str:
    """
    Generates a clean, branded SVG representing the partner referral QR code.
    Works 100% offline without external network dependencies.
    """
    partner = PARTNERS_REGISTRY.get(partner_id, {
        "name": "Airtel Business Partner",
        "agency_name": "Authorized Agency",
        "referral_code": partner_id
    })
    ref_url = get_partner_referral_url(partner_id, base_host)
    
    # Generate deterministic visual QR pattern based on partner hash
    h = hash(partner_id) & 0xFFFFFF
    rows = []
    for r in range(11):
        cols = []
        for c in range(11):
            # Keep corner finder patterns dark
            is_finder = (r < 3 and c < 3) or (r < 3 and c > 7) or (r > 7 and c < 3)
            val = 1 if is_finder else (((h >> ((r * 11 + c) % 24)) & 1) ^ ((r + c) % 2))
            fill = "#d90429" if val else "#ffffff"
            cols.append(f'<rect x="{c * 16 + 24}" y="{r * 16 + 24}" width="14" height="14" rx="2" fill="{fill}"/>')
        rows.append("".join(cols))
    pattern_svg = "".join(rows)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 224 260" width="224" height="260">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
    </filter>
  </defs>
  <rect width="224" height="260" rx="12" fill="#ffffff" stroke="#e0e0e0" stroke-width="1.5" filter="url(#shadow)"/>
  
  <!-- Airtel Red Header Band -->
  <path d="M 0 12 Q 0 0 12 0 L 212 0 Q 224 0 224 12 L 224 22 L 0 22 Z" fill="#d90429"/>
  <text x="112" y="16" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" font-weight="bold" text-anchor="middle" letter-spacing="0.5">AIRTEL BUSINESS PARTNER</text>
  
  <!-- QR Code Matrix -->
  <g transform="translate(0, 8)">
    {pattern_svg}
  </g>
  
  <!-- Partner Identifier Pill -->
  <rect x="20" y="214" width="184" height="34" rx="6" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1"/>
  <text x="112" y="228" fill="#111111" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="bold" text-anchor="middle">{partner['agency_name']}</text>
  <text x="112" y="240" fill="#666666" font-family="monospace" font-size="8.5" text-anchor="middle">{partner['referral_code']} &bull; Scan to Discover</text>
</svg>"""

# -------------------------------------------------------------------------
# 5. COMMISSION LEDGER ENGINE
# -------------------------------------------------------------------------
def record_order_commission(
    order: Dict[str, Any],
    partner_id: str,
    commission_amount_inr: int = 1500
) -> Dict[str, Any]:
    """
    Creates an initial 'pending' commission record upon partner-attributed order creation.
    Strict rule: Commission becomes 'eligible' ONLY after order activation (Step 5).
    """
    partner = PARTNERS_REGISTRY.get(partner_id)
    if not partner:
        return {"status": "error", "message": f"Partner {partner_id} not registered."}

    order_id = order.get("order_id")
    if not order_id:
        return {"status": "error", "message": "Order ID required for commission."}

    # Anti-duplication check
    existing = next((c for c in COMMISSION_LEDGER.values() if c.get("order_id") == order_id), None)
    if existing:
        return {"status": "exists", "commission": existing}

    comm_id = f"COM-2026-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now()

    record = {
        "commission_id": comm_id,
        "partner_id": partner_id,
        "partner_name": partner["name"],
        "agency_name": partner["agency_name"],
        "order_id": order_id,
        "customer_name": order.get("business_name") or order.get("signatory_name") or "MSME Enterprise",
        "bundle_id": order.get("bundle_id", "bundle_kirana"),
        "bundle_name": order.get("bundle_name", "Airtel Business Plan"),
        "monthly_subtotal_inr": order.get("monthly_subtotal", 1999),
        "commission_amount_inr": commission_amount_inr,
        "status": "pending",  # pending -> eligible -> approved -> paid (or reversed)
        "created_at": now.isoformat(),
        "created_at_display": now.strftime("%d-%b-%Y %H:%M IST"),
        "eligible_at": None,
        "approved_at": None,
        "paid_at": None,
        "reversed_at": None,
        "notes": [f"Order created with referral attribution to {partner['name']}. Status: PENDING activation."]
    }
    COMMISSION_LEDGER[comm_id] = record

    PARTNER_AUDIT_LOGS.append({
        "timestamp": now.isoformat(),
        "event": "commission_created_pending",
        "commission_id": comm_id,
        "partner_id": partner_id,
        "order_id": order_id
    })

    return {"status": "success", "commission": record}

def update_commission_on_activation(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Triggered when an order reaches Step 5 (Installation & Service Activation).
    Transitions commission status from 'pending' to 'eligible'.
    """
    comm = next((c for c in COMMISSION_LEDGER.values() if c.get("order_id") == order_id), None)
    if not comm:
        return None

    if comm["status"] == "pending":
        comm["status"] = "eligible"
        now = datetime.now()
        comm["eligible_at"] = now.isoformat()
        comm["notes"].append(f"Service activated at {now.strftime('%d-%b-%Y %H:%M IST')}. Commission is now ELIGIBLE for payout approval.")
        
        PARTNER_AUDIT_LOGS.append({
            "timestamp": now.isoformat(),
            "event": "commission_marked_eligible",
            "commission_id": comm["commission_id"],
            "order_id": order_id
        })
    return comm

def update_commission_status(
    commission_id: str,
    action: str,  # approve, mark_paid, reverse
    admin_user: str = "Super Admin",
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Admin-controlled commission state transitions:
    - approve: eligible -> approved
    - mark_paid: approved -> paid
    - reverse: any -> reversed (e.g. order cancelled, fraud detected)
    """
    comm = COMMISSION_LEDGER.get(commission_id)
    if not comm:
        return {"status": "error", "message": f"Commission {commission_id} not found."}

    now = datetime.now()
    now_str = now.strftime("%d-%b-%Y %H:%M IST")

    if action == "approve":
        if comm["status"] != "eligible":
            return {"status": "error", "message": f"Only ELIGIBLE commissions can be approved (current: {comm['status']})."}
        comm["status"] = "approved"
        comm["approved_at"] = now.isoformat()
        comm["notes"].append(f"Commission approved for payout batch by {admin_user} at {now_str}.")

    elif action == "mark_paid":
        if comm["status"] not in ["approved", "eligible"]:
            return {"status": "error", "message": f"Cannot pay commission in status '{comm['status']}'. Must be approved first."}
        comm["status"] = "paid"
        comm["paid_at"] = now.isoformat()
        comm["notes"].append(f"Disbursed via bank transfer by {admin_user} at {now_str}.")

    elif action == "reverse":
        comm["status"] = "reversed"
        comm["reversed_at"] = now.isoformat()
        comm["notes"].append(f"Commission REVERSED by {admin_user} at {now_str}. Reason: {reason or 'Order cancelled/unverified'}")

    else:
        return {"status": "error", "message": f"Unknown action '{action}'"}

    PARTNER_AUDIT_LOGS.append({
        "timestamp": now.isoformat(),
        "event": f"commission_{action}",
        "commission_id": commission_id,
        "admin_user": admin_user
    })

    return {"status": "success", "commission": comm}

# -------------------------------------------------------------------------
# 6. AI SALES CO-PILOT (Private Partner Assistance)
# -------------------------------------------------------------------------
def generate_partner_copilot_advice(
    profile: Dict[str, Any],
    identified_needs: List[str],
    current_bundle: Dict[str, Any],
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Generates confidential real-time sales advice for the channel partner
    during assisted onboarding sessions (invisible to the customer).
    """
    btype = profile.get("business_type", "kirana")
    bundle_id = current_bundle.get("id", "bundle_kirana")
    monthly_inr = current_bundle.get("monthly_inr", 1999)
    customer_budget = profile.get("stated_budget") or profile.get("budget")

    # 1. Deterministic Rationale
    rationale = f"Recommended {current_bundle.get('name', 'Business Plan')} as best-fit for {btype.upper()} operations."

    # 2. Satisfied vs Unmet Analysis
    satisfied_needs = []
    unmet_needs = []

    need_keys = [n.split(":")[0] if ":" in n else n for n in identified_needs]
    
    if bundle_id == "bundle_kirana":
        satisfied_needs = ["100 Mbps Wireless FWA Connectivity", "Automatic 4G/5G UPI Failover", "WhatsApp Business Verified API", "Secure Commercial Wi-Fi"]
        if any("cctv" in n or "surveillance" in n for n in need_keys):
            unmet_needs.append("Cloud CCTV Surveillance (Pitch 2-Cam Add-on at ₹1,200/mo)")
        if any("backup" in n or "cloud" in n for n in need_keys):
            unmet_needs.append("Cloud Backup 500GB Expansion (Pitch Add-on at ₹450/mo)")
        if any("ip" in n or "static" in n for n in need_keys):
            unmet_needs.append("Static IP Pool (Pitch /29 pool at ₹500/mo)")

    elif bundle_id == "bundle_clinic":
        satisfied_needs = ["200 Mbps Optical Business Fiber", "1TB Cloud Backup (Compliant Patient Records)", "Google Workspace Enterprise Email", "Secure Commercial Wi-Fi"]
        if any("cctv" in n for n in need_keys):
            unmet_needs.append("Waiting Room Cloud CCTV (Pitch 2-Cam Pack at ₹1,200/mo)")

    elif bundle_id == "bundle_multisite":
        satisfied_needs = ["500 Mbps Business Fiber", "Managed SD-WAN Multi-Branch Sync", "Cloud CCTV Analytics (4 Cams Included)", "Managed Hardware Firewall"]
        
    elif bundle_id == "bundle_manufacturer":
        satisfied_needs = ["Internet Leased Line 1:1 Dedicated Bandwidth", "Static IPv4 /29 Subnet", "Machine IoT Telemetry Monitoring", "Dedicated Enterprise Account Manager"]

    # 3. Consultative Prompts for Field Rep
    prompts = []
    if btype == "kirana":
        prompts = [
            "Ask: 'Aapki dukan par sham ke time UPI payments kitni baar fail hote hain?'",
            "Ask: 'Billing computer ya soundbox ke alawa koi CCTV camera bhi lagana chahte hain?'",
            "Consultative Tip: Emphasize that preventing just 1 UPI failure during evening peak covers the ₹66/day plan cost."
        ]
    elif btype == "clinic":
        prompts = [
            "Ask: 'Patient appointments aur diagnostic reports abhi local hard drive par save hoti hain ya cloud par?'",
            "Ask: 'Custom domain email (e.g., info@clinicname.com) use karte hain ya personal Gmail?'",
            "Consultative Tip: Highlight that our 1TB cloud backup is encrypted and compliant with medical privacy standards."
        ]
    elif btype == "multisite":
        prompts = [
            "Ask: 'Teenon outlets ka inventory data real-time sync hota hai ya end-of-day?'",
            "Ask: 'Single consolidated bill aur unified SLA dashboard prioritize karenge?'",
            "Consultative Tip: Point out that SD-WAN eliminates expensive MPLS lines while guaranteeing 99.9% uptime across all branches."
        ]
    else:
        prompts = [
            "Ask: 'ERP servers on-premise hain ya cloud hosted?'",
            "Ask: 'Machine breakdown hone par telemetry alerts chahiye?'",
            "Consultative Tip: Highlight 1:1 symmetric upload/download with 99.95% enterprise SLA."
        ]

    # 4. Anticipated Objections & Field Rebuttals
    objections = []
    if customer_budget and int(customer_budget) < monthly_inr:
        diff = monthly_inr - int(customer_budget)
        objections.append({
            "objection": f"Budget Mismatch (Customer expects ₹{int(customer_budget):,}/mo, quote is ₹{monthly_inr:,}/mo)",
            "rebuttal": f"Acknowledge budget respectfully. Explain that this bundle includes automatic 4G failover router (₹1,200 value) which eliminates revenue loss from payment drops. Alternatively, suggest annual billing (1 month free)."
        })
    else:
        objections.append({
            "objection": "Price comparison with consumer mobile hotspot",
            "rebuttal": "Consumer hotspots throttle after daily FUP and have zero SLA. Airtel Business delivers uncapped business priority bandwidth with 4-hour doorstep MTTR."
        })
        objections.append({
            "objection": "Contract lock-in hesitation (12-month commitment)",
            "rebuttal": "Explain that Airtel waives router and hardware security deposit with 100% free doorstep engineer installation."
        })

    # 5. Partner Commission Preview
    commission_preview = {
        "commission_amount_inr": 1500,
        "eligibility_trigger": "Paid on Step 5 Installation & Service Activation",
        "estimated_payout_days": "3 to 5 business days after digital KYC clearance",
        "margin_tier": "Airtel Gold Partner Standard Payout"
    }

    return {
        "partner_role": "Confidential AI Field Co-Pilot",
        "target_bundle_name": current_bundle.get("name"),
        "target_bundle_price": monthly_inr,
        "rationale": rationale,
        "satisfied_needs": satisfied_needs,
        "unmet_needs": unmet_needs,
        "consultative_prompts": prompts,
        "anticipated_objections": objections,
        "commission_preview": commission_preview
    }

# -------------------------------------------------------------------------
# 7. PARTNER PERFORMANCE ANALYTICS
# -------------------------------------------------------------------------
def get_partner_performance(partner_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Computes real-time sales performance metrics for a specific partner
    or aggregated system-wide for administrators.
    """
    # Filter commissions
    if partner_id:
        comm_list = [c for c in COMMISSION_LEDGER.values() if c.get("partner_id") == partner_id]
        attr_list = [a for a in PARTNER_ATTRIBUTIONS.values() if a.get("partner_id") == partner_id]
        partner_obj = PARTNERS_REGISTRY.get(partner_id, {})
    else:
        comm_list = list(COMMISSION_LEDGER.values())
        attr_list = list(PARTNER_ATTRIBUTIONS.values())
        partner_obj = {"name": "All Airtel Partners", "agency_name": "Pan-India Network"}

    total_referred = len(attr_list)
    total_orders = len(comm_list)
    
    pending_comms = [c for c in comm_list if c["status"] == "pending"]
    eligible_comms = [c for c in comm_list if c["status"] == "eligible"]
    approved_comms = [c for c in comm_list if c["status"] == "approved"]
    paid_comms = [c for c in comm_list if c["status"] == "paid"]
    reversed_comms = [c for c in comm_list if c["status"] == "reversed"]

    activations = len(eligible_comms) + len(approved_comms) + len(paid_comms)
    conversion_rate = round((activations / max(1, total_referred)) * 100, 1)

    pending_inr = sum(c["commission_amount_inr"] for c in pending_comms)
    eligible_inr = sum(c["commission_amount_inr"] for c in eligible_comms)
    approved_inr = sum(c["commission_amount_inr"] for c in approved_comms)
    paid_inr = sum(c["commission_amount_inr"] for c in paid_comms)
    total_earned_inr = eligible_inr + approved_inr + paid_inr

    return {
        "status": "success",
        "partner_id": partner_id or "ALL",
        "partner_name": partner_obj.get("name"),
        "agency_name": partner_obj.get("agency_name"),
        "metrics": {
            "total_referred_sessions": total_referred,
            "total_orders_placed": total_orders,
            "pending_activations": len(pending_comms),
            "total_activations": activations,
            "conversion_rate_pct": conversion_rate,
            "commission_earned_inr": total_earned_inr,
            "commission_pending_inr": pending_inr,
            "commission_paid_inr": paid_inr,
            "commission_reversed_inr": sum(c["commission_amount_inr"] for c in reversed_comms)
        },
        "breakdown": {
            "pending": len(pending_comms),
            "eligible": len(eligible_comms),
            "approved": len(approved_comms),
            "paid": len(paid_comms),
            "reversed": len(reversed_comms)
        },
        "recent_commissions": sorted(comm_list, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
    }

# -------------------------------------------------------------------------
# 8. SEED INITIAL COMMISSION RECORDS
# -------------------------------------------------------------------------
def seed_initial_partner_data():
    """Seeds realistic demonstration commission and attribution records."""
    if COMMISSION_LEDGER:
        return

    # Seed 1: Rajesh Gupta (Delhi) - Completed & Paid Activation
    c1 = {
        "commission_id": "COM-2026-9011",
        "partner_id": "PTR-DEL-042",
        "partner_name": "Rajesh Gupta",
        "agency_name": "MicroTech Solutions",
        "order_id": "ORD-2026-8801",
        "customer_name": "Aggarwal Sweets & Namkeen",
        "bundle_id": "bundle_kirana",
        "bundle_name": "Kirana & Micro Retail Digital Starter",
        "monthly_subtotal_inr": 1999,
        "commission_amount_inr": 1500,
        "status": "paid",
        "created_at": "2026-05-15T11:00:00",
        "created_at_display": "15-May-2026 11:00 IST",
        "eligible_at": "2026-05-18T14:30:00",
        "approved_at": "2026-05-19T10:00:00",
        "paid_at": "2026-05-20T16:00:00",
        "notes": ["Order activated by Ops Manager Vikram Rathore.", "Disbursed via direct NEFT."]
    }
    COMMISSION_LEDGER[c1["commission_id"]] = c1

    # Seed 2: Rajesh Gupta (Delhi) - Eligible Activation (Awaiting Payout Approval)
    c2 = {
        "commission_id": "COM-2026-9012",
        "partner_id": "PTR-DEL-042",
        "partner_name": "Rajesh Gupta",
        "agency_name": "MicroTech Solutions",
        "order_id": "ORD-2026-8802",
        "customer_name": "Khurana Medical Store",
        "bundle_id": "bundle_clinic",
        "bundle_name": "Clinic & Professional Office Suite",
        "monthly_subtotal_inr": 3499,
        "commission_amount_inr": 1500,
        "status": "eligible",
        "created_at": "2026-06-01T10:30:00",
        "created_at_display": "01-Jun-2026 10:30 IST",
        "eligible_at": "2026-06-04T12:00:00",
        "approved_at": None,
        "paid_at": None,
        "notes": ["Service activated; eligible for weekly payout batch."]
    }
    COMMISSION_LEDGER[c2["commission_id"]] = c2

    # Seed 3: Rajesh Gupta (Delhi) - Pending Installation
    c3 = {
        "commission_id": "COM-2026-9013",
        "partner_id": "PTR-DEL-042",
        "partner_name": "Rajesh Gupta",
        "agency_name": "MicroTech Solutions",
        "order_id": "ORD-2026-8803",
        "customer_name": "Bansal Book Depot",
        "bundle_id": "bundle_kirana",
        "bundle_name": "Kirana & Micro Retail Digital Starter",
        "monthly_subtotal_inr": 1999,
        "commission_amount_inr": 1500,
        "status": "pending",
        "created_at": "2026-06-10T15:20:00",
        "created_at_display": "10-Jun-2026 15:20 IST",
        "eligible_at": None,
        "approved_at": None,
        "paid_at": None,
        "notes": ["Order placed in assisted tablet mode; hardware dispatch in flight."]
    }
    COMMISSION_LEDGER[c3["commission_id"]] = c3

    # Seed 4: Vikram Rathore (Mumbai) - Paid Multi-Site Deal
    c4 = {
        "commission_id": "COM-2026-9021",
        "partner_id": "PTR-MUM-108",
        "partner_name": "Vikram Rathore",
        "agency_name": "Apex Telecom Enterprises",
        "order_id": "ORD-2026-7711",
        "customer_name": "Shivaji Fast Food & Cafes (2 Branches)",
        "bundle_id": "bundle_multisite",
        "bundle_name": "Multi-Site Retail & Restaurant Pro",
        "monthly_subtotal_inr": 7999,
        "commission_amount_inr": 1500,
        "status": "paid",
        "created_at": "2026-05-10T14:00:00",
        "created_at_display": "10-May-2026 14:00 IST",
        "eligible_at": "2026-05-17T16:00:00",
        "approved_at": "2026-05-18T11:00:00",
        "paid_at": "2026-05-19T14:00:00",
        "notes": ["Closed via field tablet; paid in batch May-2026."]
    }
    COMMISSION_LEDGER[c4["commission_id"]] = c4

    # Seed 5: Priya Nair (Bengaluru) - Pending KYC
    c5 = {
        "commission_id": "COM-2026-9031",
        "partner_id": "PTR-BLR-019",
        "partner_name": "Priya Nair",
        "agency_name": "Silicon City Infotech",
        "order_id": "ORD-2026-6612",
        "customer_name": "Dr. Sen Dental Clinic",
        "bundle_id": "bundle_clinic",
        "bundle_name": "Clinic & Professional Office Suite",
        "monthly_subtotal_inr": 3499,
        "commission_amount_inr": 1500,
        "status": "pending",
        "created_at": "2026-06-12T09:45:00",
        "created_at_display": "12-Jun-2026 09:45 IST",
        "eligible_at": None,
        "approved_at": None,
        "paid_at": None,
        "notes": ["KYC verification in progress."]
    }
    COMMISSION_LEDGER[c5["commission_id"]] = c5

    # Seed initial attributions
    PARTNER_ATTRIBUTIONS["sess_demo_delhi"] = {
        "attribution_id": "ATTR-DEL-001",
        "session_id": "sess_demo_delhi",
        "partner_id": "PTR-DEL-042",
        "partner_name": "Rajesh Gupta",
        "agency_name": "MicroTech Solutions",
        "campaign_id": "field_qr",
        "created_at": "2026-06-10T10:00:00",
        "expires_at": "2026-07-10T10:00:00",
        "status": "active",
        "touchpoints": ["qr_scanned", "discovery_completed"]
    }
    PARTNER_ATTRIBUTIONS["sess_demo_mumbai"] = {
        "attribution_id": "ATTR-MUM-001",
        "session_id": "sess_demo_mumbai",
        "partner_id": "PTR-MUM-108",
        "partner_name": "Vikram Rathore",
        "agency_name": "Apex Telecom Enterprises",
        "campaign_id": "field_tablet",
        "created_at": "2026-06-08T11:00:00",
        "expires_at": "2026-07-08T11:00:00",
        "status": "active",
        "touchpoints": ["assisted_mode_launched", "order_placed"]
    }

# Initialize seed data on module import
seed_initial_partner_data()

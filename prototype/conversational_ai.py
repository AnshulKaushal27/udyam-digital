"""
Project Udyam Digital — Proactive Conversational AI & Indecision Engine
Bharti Airtel SYNC 2026 Innovation Challenge
Team: Halo · Thapar Institute of Engineering & Technology

Features:
1. Intelligent Indecision & Delegation Handler (English, Hindi, Punjabi, Hinglish)
2. Response Classification Framework (7 categories)
3. Preference State Tracking & Non-Assumed Verification Boundaries
4. Intent Recognition (Digital Invoicing, GST Billing, POS, Inventory, CCTV, IoT, etc.)
5. Product Catalogue Validation (P01-P25 with P19 Cloud POS & Billing enforcement)
6. Dynamic Multilingual Synchronization (en, hi, pa, hinglish)
7. Recommendation Lifecycle State Management (not_ready, draft, generated, viewed, modified, accepted, rejected, superseded)
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple

# -------------------------------------------------------------------------
# 1. MULTILINGUAL INDECISION & DELEGATION DICTIONARY
# -------------------------------------------------------------------------
INDECISION_PATTERNS = {
    "en": [
        r"\bwhatever is fine\b", r"\banything works\b", r"\byou decide\b",
        r"\bi don'?t know\b", r"\bwhatever you recommend\b", r"\bdoesn'?t matter\b",
        r"\bi'?m not sure\b", r"\bwhatever you want\b", r"\bup to you\b",
        r"\bany is fine\b", r"\beither works\b", r"\byou choose\b",
        r"\bno preference\b", r"\banything is good\b", r"\bwhatever\b"
    ],
    "hi": [
        r"\bjo marzi\b", r"\bkuch bhi chalega\b", r"\baap decide kar lo\b",
        r"\bmujhe nahi pata\b", r"\baap suggest kar do\b", r"\bjo sahi lage\b",
        r"\bkuch bhi\b", r"\baap dekh lo\b", r"\bjo behtar ho\b",
        r"\bmujhe idea nahi\b", r"\bjo apko theek lage\b"
    ],
    "pa": [
        r"\bjo marzi\b", r"\btusi hi dass do\b", r"\bmainu nahi pata\b",
        r"\bjehda theek hove\b", r"\bkoi vi chalega\b", r"\bkujh vi\b",
        r"\btusi dekh lo\b", r"\bmainu ki pata\b", r"\btusi dasso\b"
    ],
    "hinglish": [
        r"\baap hi decide kar lo\b", r"\bjo best hai woh de do\b",
        r"\bmujhe technical details nahi pata\b", r"\baap batao\b",
        r"\bjo aapko theek lage\b", r"\bkuch bhi chalega\b",
        r"\byou decide yaar\b", r"\bjo marzi yaar\b", r"\bno idea\b"
    ]
}

# Compile patterns
COMPILED_INDECISION = {
    lang: [re.compile(p, re.IGNORECASE) for p in patterns]
    for lang, patterns in INDECISION_PATTERNS.items()
}

# Natural Language Switching Requests
LANG_SWITCH_PATTERNS = {
    "hi": [
        r"\b(?:speak|talk|continue|reply|chat)\s+(?:in\s+)?hindi\b",
        r"\bhindi\s+(?:me|mein|vich|please|plz)\b",
        r"\bhindi\s+me\s+baat\s+karo\b",
        r"\bhindi\s+bolo\b",
        r"\bcan\s+you\s+speak\s+hindi\b"
    ],
    "en": [
        r"\b(?:speak|talk|continue|reply|chat)\s+(?:in\s+)?english\b",
        r"\benglish\s+(?:please|plz|only)\b",
        r"\benglish\s+me\s+bolo\b",
        r"\bcan\s+you\s+speak\s+english\b",
        r"\bswitch\s+to\s+english\b"
    ],
    "pa": [
        r"\b(?:speak|talk|continue|reply|chat)\s+(?:in\s+)?punjabi\b",
        r"\bpunjabi\s+(?:ch|vich|please|plz)\b",
        r"\bpunjabi\s+ch\s+gall\s+karo\b",
        r"\bpunjabi\s+vich\s+bolo\b",
        r"\bcan\s+you\s+speak\s+punjabi\b",
        r"\btusi\s+punjabi\s+ch\s+gall\s+kar\s+sakde\s+o\b"
    ],
    "hinglish": [
        r"\b(?:speak|talk|continue|reply|chat)\s+(?:in\s+)?hinglish\b",
        r"\bhinglish\s+(?:me|mein|please|plz)\b",
        r"\bhinglish\s+bolo\b",
        r"\bmixed\s+hindi\s+english\b"
    ]
}

COMPILED_LANG_SWITCH = {
    lang: [re.compile(p, re.IGNORECASE) for p in patterns]
    for lang, patterns in LANG_SWITCH_PATTERNS.items()
}

# -------------------------------------------------------------------------
# 2. PRODUCT CATALOGUE TRUTH TABLE (Validating Against product_catalogue.csv)
# -------------------------------------------------------------------------
OFFICIAL_CATALOGUE = {
    "P01": {"name": "Biz Fibre 100", "cat": "Connectivity", "price_min": 999, "price_max": 1199, "speed": "100 Mbps"},
    "P02": {"name": "Biz Fibre 300", "cat": "Connectivity", "price_min": 1499, "price_max": 1799, "speed": "300 Mbps"},
    "P03": {"name": "Biz Fibre 1G", "cat": "Connectivity", "price_min": 3999, "price_max": 4499, "speed": "1 Gbps"},
    "P04": {"name": "Biz 5G AirFiber 100", "cat": "Connectivity", "price_min": 899, "price_max": 1099, "speed": "100 Mbps FWA"},
    "P05": {"name": "Internet Leased Line 20", "cat": "Connectivity", "price_min": 8000, "price_max": 12000, "speed": "20 Mbps 1:1 CIR"},
    "P06": {"name": "Internet Leased Line 100", "cat": "Connectivity", "price_min": 25000, "price_max": 35000, "speed": "100 Mbps 1:1 CIR"},
    "P09": {"name": "Backup 4G/5G Failover", "cat": "Connectivity", "price_min": 499, "price_max": 599, "type": "POS Failover"},
    "P10": {"name": "Managed SD-WAN", "cat": "Connectivity", "price_min": 2500, "price_max": 3500, "type": "Multi-site Router"},
    "P11": {"name": "Static IP", "cat": "Connectivity", "price_min": 200, "price_max": 300, "type": "Fixed Public IP"},
    "P12": {"name": "Cloud Telephony / SIP", "cat": "Communication", "price_min": 1000, "price_max": 1500, "type": "IVR Lines"},
    "P15": {"name": "WhatsApp Business API Starter", "cat": "Communication", "price_min": 999, "price_max": 1499, "type": "Verified Channel"},
    "P16": {"name": "Cloud Email & Office Suite", "cat": "Cloud & Productivity", "price_min": 125, "price_max": 150, "type": "Domain Email"},
    "P17": {"name": "Cloud Backup 1 TB", "cat": "Cloud & Productivity", "price_min": 499, "price_max": 699, "type": "Encrypted Offsite Backup"},
    "P18": {"name": "Website + Domain Starter", "cat": "Cloud & Productivity", "price_min": 299, "price_max": 499, "type": "5-page Builder"},
    "P19": {
        "name": "Cloud POS & Billing",
        "cat": "Cloud & Productivity",
        "price_min": 599,
        "price_max": 899,
        "setup_inr": 2500,
        "type": "GST Invoicing & Billing Software",
        "description": "GST-ready billing, inventory sync, UPI/card acceptance on tablet and phone.",
        "monthly_inr": 599
    },
    "P20": {"name": "Endpoint Security", "cat": "Security", "price_min": 99, "price_max": 149, "type": "Device Antivirus"},
    "P21": {"name": "Managed Firewall", "cat": "Security", "price_min": 1999, "price_max": 2999, "type": "Perimeter Security"},
    "P22": {"name": "Secure Wi-Fi with Guest Network", "cat": "Security", "price_min": 399, "price_max": 599, "type": "Isolated Guest Wi-Fi"},
    "P23": {"name": "Cloud CCTV", "cat": "IoT & Physical", "price_min": 199, "price_max": 299, "type": "HD Security Camera"},
    "P24": {"name": "Machine Monitoring IoT", "cat": "IoT & Physical", "price_min": 149, "price_max": 249, "type": "Factory Sensor Telemetry"},
    "P25": {"name": "Fleet Tracker", "cat": "IoT & Physical", "price_min": 199, "price_max": 299, "type": "GPS Vehicle Tracker"}
}

# -------------------------------------------------------------------------
# 3. LANGUAGE SWITCH DETECTION
# -------------------------------------------------------------------------
def detect_natural_language_switch(text: str) -> Optional[str]:
    """
    Detects if the user requested to change the conversation language.
    Returns: 'en', 'hi', 'pa', 'hinglish', or None.
    """
    if not text:
        return None
    for lang, patterns in COMPILED_LANG_SWITCH.items():
        for pat in patterns:
            if pat.search(text):
                return lang
    return None

# -------------------------------------------------------------------------
# 4. RESPONSE CLASSIFICATION FRAMEWORK (7 Categories)
# -------------------------------------------------------------------------
def classify_user_response(text: str, session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classifies customer message into 1 of 7 categories:
    1. explicit_answer
    2. delegated_decision
    3. uncertainty
    4. refusal
    5. clarification_request
    6. change_of_requirement
    7. unrelated_query
    """
    text_clean = text.strip()
    text_low = text_clean.lower()

    # 1. Delegated Decision Check
    for lang, patterns in COMPILED_INDECISION.items():
        for pat in patterns:
            if pat.search(text_low):
                if any(w in text_low for w in ["don't know", "dont know", "nahi pata", "ki pata", "not sure", "no idea"]):
                    return {
                        "category": "uncertainty",
                        "raw_text": text,
                        "confidence": 0.95,
                        "delegated": False
                    }
                return {
                    "category": "delegated_decision",
                    "raw_text": text,
                    "confidence": 0.96,
                    "delegated": True
                }

    # 2. Refusal Check
    refusal_words = ["don't want", "dont want", "no need", "nahi chahiye", "nahi lagwana", "skip", "reject", "not interested", "nahi"]
    if any(w == text_low or f" {w} " in f" {text_low} " for w in refusal_words) and len(text_low.split()) <= 4:
        # Avoid treating "No, we are 5 people" as pure refusal
        if not any(k in text_low for k in ["staff", "people", "log", "bills", "invoices", "stores"]):
            return {
                "category": "refusal",
                "raw_text": text,
                "confidence": 0.92,
                "delegated": False
            }

    # 3. Clarification Request Check
    if any(k in text_low for k in ["what is the difference", "difference between", "kya farak hai", "kya difference", "explain", "samjhao", "meaning", "matlab"]):
        return {
            "category": "clarification_request",
            "raw_text": text,
            "confidence": 0.94,
            "delegated": False
        }

    # 4. Change of Requirement Check
    change_markers = [
        "actually i", "actually we", "change", "badal", "nahi ab", "instead",
        "we also have", "now we have", "opening new branch", "switch to", "not a shop", "not manufacturing"
    ]
    if any(k in text_low for k in change_markers):
        return {
            "category": "change_of_requirement",
            "raw_text": text,
            "confidence": 0.91,
            "delegated": False
        }

    # 5. Unrelated Query Check
    unrelated_markers = ["weather", "who made you", "cricket", "ipl", "joke", "capital of", "president", "ceo of airtel", "song"]
    if any(k in text_low for k in unrelated_markers) and not any(biz in text_low for biz in ["bill", "net", "wifi", "shop", "gst", "pos", "fiber"]):
        return {
            "category": "unrelated_query",
            "raw_text": text,
            "confidence": 0.88,
            "delegated": False
        }

    # 6. Explicit Answer Check (default for substantive business input)
    return {
        "category": "explicit_answer",
        "raw_text": text,
        "confidence": 0.95,
        "delegated": False
    }

# -------------------------------------------------------------------------
# 5. INTELLIGENT INDECISION & PREFERENCE STATE TRACKER
# -------------------------------------------------------------------------
def get_or_create_preference_state(session: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieves or initializes the preference tracking state on session."""
    if "preference_tracking" not in session:
        session["preference_tracking"] = {}
    return session["preference_tracking"]

def handle_indecision_policy(
    session: Dict[str, Any],
    question_id: str,
    classification: Dict[str, Any],
    recommended_default: str,
    default_reason: str,
    contrast_summary: Dict[str, str],
    lang: str = "en"
) -> Tuple[str, Dict[str, Any]]:
    """
    Implements the 2-step Indecision Policy:
    First occurrence:
      - Acknowledge
      - Explain the two choices briefly if distinction matters
      - Give the customer an easy recommendation
    Second occurrence:
      - Stop asking about that preference
      - Make sensible default decision
      - Continue conversation

    NEVER asks the same question a third time.
    """
    pref_state = get_or_create_preference_state(session)
    q_state = pref_state.get(question_id, {
        "question_id": question_id,
        "status": "unanswered",
        "clarification_attempts": 0,
        "customer_delegated": False,
        "selected_value": None,
        "selection_reason": ""
    })

    q_state["clarification_attempts"] += 1

    if classification["category"] == "delegated_decision" or q_state["clarification_attempts"] >= 2:
        # Second occurrence OR direct delegation ("You decide" / "Jo marzi"):
        # Make the sensible default decision immediately and proceed!
        q_state["status"] = "delegated"
        q_state["customer_delegated"] = True
        q_state["selected_value"] = recommended_default
        q_state["selection_reason"] = default_reason
        pref_state[question_id] = q_state

        if lang == "hi":
            ack = f"बिल्कुल! मैं आपके लिए {contrast_summary.get('short_hi', recommended_default)} सेलेक्ट कर रहा हूँ, ताकि आप भविष्य में कहीं से भी एक्सेस कर सकें।"
        elif lang == "pa":
            ack = f"ਬਿਲਕੁਲ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ {contrast_summary.get('short_pa', recommended_default)} ਆਪਸ਼ਨ ਚੁਣ ਰਿਹਾ ਹਾਂ, ਤਾਂ ਜੋ ਤੁਹਾਨੂੰ ਕੋਈ ਦਿੱਕਤ ਨਾ ਆਵੇ।"
        elif lang == "hinglish":
            ack = f"Theek hai! Main aapke liye {contrast_summary.get('short_hinglish', recommended_default)} prefer karunga, taaki aap easily access kar sakein."
        else:
            ack = f"Understood! I'll select the {recommended_default} option for you so you can access it easily."

        return ack, q_state

    else:
        # First occurrence of uncertainty ("I don't know" / "Not sure"):
        # Explain briefly and provide an easy recommendation
        q_state["status"] = "uncertain"
        q_state["customer_delegated"] = False
        pref_state[question_id] = q_state

        if lang == "hi":
            ack = (
                f"{contrast_summary.get('desc_hi', 'क्लाउड-बेस्ड बिलिंग में आप कहीं से भी बिल बना सकते हैं, जबकि डेस्कटॉप सिर्फ एक कंप्यूटर पर चलता है।')} "
                f"आपके सेटअप के लिए क्लाउड-बेस्ड सबसे सही रहेगा। क्या आप इससे सहमत हैं?"
            )
        elif lang == "pa":
            ack = (
                f"{contrast_summary.get('desc_pa', 'ਕਲਾਊਡ ਬਿਲਿੰਗ ਨਾਲ ਤੁਸੀਂ ਫੋਨ ਜਾਂ ਟੈਬਲੇਟ ਤੋਂ ਵੀ ਇਨਵੌਇਸ ਬਣਾ ਸਕਦੇ ਹੋ।')} "
                f"ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਕਲਾਊਡ ਆਪਸ਼ਨ ਰਿਕਮੈਂਡ ਕਰਾਂਗਾ। ਕੀ ਇਹ ਠੀਕ ਹੈ?"
            )
        elif lang == "hinglish":
            ack = (
                f"{contrast_summary.get('desc_hinglish', 'Cloud-based billing aapko kahin se bhi bills manage karne deta hai, jabki desktop software local PC par depend karta hai.')} "
                f"Aapke liye cloud-based best rahega. Shall we go with that?"
            )
        else:
            ack = (
                f"{contrast_summary.get('desc_en', 'Cloud-based invoicing allows you to create bills from anywhere, whereas desktop software is tied to one PC.')} "
                f"I recommend cloud-based for your workflow. Does that work for you?"
            )

        return ack, q_state

# -------------------------------------------------------------------------
# 6. DIGITAL BILLING & INVOICING INTENT RECOGNITION
# -------------------------------------------------------------------------
def detect_billing_and_invoicing_intent(text: str, session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detects if customer specifically requested digital billing, GST invoicing, POS, or inventory.
    Initializes or updates session['billing_intent'].
    """
    text_low = text.lower()
    
    if "billing_intent" not in session:
        session["billing_intent"] = {
            "active": False,
            "requested_feature": None,
            "current_method": None, # "paper" | "software" | "spreadsheet"
            "gst_required": None,
            "monthly_invoices": None,
            "deployment_preference": None, # "cloud" | "desktop"
            "inventory_needed": None,
            "catalogue_product_id": "P19",
            "catalogue_product_name": "Cloud POS & Billing",
            "catalogue_price_inr": 599
        }

    b_intent = session["billing_intent"]

    # 1. Billing / Invoicing keywords
    if any(k in text_low for k in ["billing", "invoice", "invoicing", "pos", "bills", "parcha", "bahi khata", "bill book", "bill system"]):
        b_intent["active"] = True
        if "gst" in text_low:
            b_intent["gst_required"] = True
        if "pos" in text_low:
            b_intent["requested_feature"] = "POS Billing"
        elif "invoice" in text_low or "invoicing" in text_low:
            b_intent["requested_feature"] = "GST Invoicing Software"
        else:
            b_intent["requested_feature"] = "Digital Billing System"

    # 2. Current Method Extraction
    if any(k in text_low for k in ["paper", "manual", "kacha bill", "haath se", "khata", "diary"]):
        b_intent["current_method"] = "paper"
    elif any(k in text_low for k in ["software", "tally", "busy", "computerized"]):
        b_intent["current_method"] = "software"
    elif any(k in text_low for k in ["excel", "spreadsheet", "sheet"]):
        b_intent["current_method"] = "spreadsheet"

    # 3. GST Requirement
    if any(k in text_low for k in ["gst invoice", "gst bill", "proper gst", "yes", "haan", "zaroor", "proper invoicing"]) and b_intent["active"]:
        if "gst" in text_low or b_intent["current_method"] == "paper":
            b_intent["gst_required"] = True

    # 4. Invoice Volume Extraction
    m_range = re.search(r'(\d+)\s*(?:-|to|–)\s*(\d+)', text_low)
    if m_range and b_intent["active"]:
        b_intent["monthly_invoices"] = f"{m_range.group(1)}–{m_range.group(2)}"
    else:
        m_num = re.search(r'\b(\d{2,4})\b', text_low)
        if m_num and b_intent["active"] and not any(w in text_low for w in ["staff", "people", "log", "stores", "locations"]):
            b_intent["monthly_invoices"] = int(m_num.group(1))

    # 5. Cloud vs Desktop Preference
    if any(k in text_low for k in ["cloud", "online", "phone pe", "mobile pe", "tablet"]):
        b_intent["deployment_preference"] = "cloud"
    elif any(k in text_low for k in ["offline", "desktop", "pc only", "bina internet"]):
        b_intent["deployment_preference"] = "offline"

    # 6. Inventory Mention
    if any(k in text_low for k in ["inventory", "stock", "maal", "godown", "item list"]):
        b_intent["inventory_needed"] = True

    return b_intent

# -------------------------------------------------------------------------
# 7. PRODUCT CATALOGUE VALIDATION (Prevent Hallucinations)
# -------------------------------------------------------------------------
def validate_catalogue_eligibility(service_request: str) -> Dict[str, Any]:
    """
    Strictly verifies whether a requested business solution is present in Airtel's catalogue.
    Does NOT hallucinate unlisted Airtel products or invent prices.
    """
    req_low = service_request.lower()

    # Invoicing & POS Software -> P19 Cloud POS & Billing
    if any(k in req_low for k in ["billing", "invoice", "pos", "gst software"]):
        p19 = OFFICIAL_CATALOGUE["P19"]
        return {
            "is_offered": True,
            "product_id": "P19",
            "product_name": p19["name"],
            "monthly_inr": p19["monthly_inr"],
            "setup_inr": p19["setup_inr"],
            "description": p19["description"],
            "complementary_connectivity": "P04 (Biz 5G AirFiber 100) or P01 (Biz Fibre 100)",
            "flag_human_rep": False
        }

    # Cloud Backup -> P17
    if any(k in req_low for k in ["backup", "patient record", "cloud storage"]):
        p17 = OFFICIAL_CATALOGUE["P17"]
        return {
            "is_offered": True,
            "product_id": "P17",
            "product_name": p17["name"],
            "monthly_inr": p17["price_min"],
            "setup_inr": 0,
            "description": p17["type"],
            "complementary_connectivity": "P02 (Biz Fibre 300)",
            "flag_human_rep": False
        }

    # Cloud CCTV -> P23
    if any(k in req_low for k in ["cctv", "camera", "surveillance"]):
        p23 = OFFICIAL_CATALOGUE["P23"]
        return {
            "is_offered": True,
            "product_id": "P23",
            "product_name": p23["name"],
            "monthly_inr": p23["price_min"],
            "setup_inr": 1800,
            "description": p23["type"],
            "complementary_connectivity": "P01 (Biz Fibre 100)",
            "flag_human_rep": False
        }

    # Heavy Custom ERP (SAP / Salesforce / CAD) -> NOT in catalogue
    if any(k in req_low for k in ["sap", "oracle erp", "salesforce", "cad software", "heavy manufacturing erp"]):
        return {
            "is_offered": False,
            "product_id": None,
            "product_name": None,
            "monthly_inr": 0,
            "setup_inr": 0,
            "description": "Specialized enterprise software is not packaged directly in Airtel's SMB catalogue.",
            "complementary_connectivity": "P05 (Internet Leased Line 20) with Static IP (P11)",
            "flag_human_rep": True,
            "explanation": "Airtel provides the carrier-grade connectivity, static IP and cloud infrastructure for specialized ERPs, while the ERP license is maintained by the client."
        }

    # Default connectivity
    return {
        "is_offered": True,
        "product_id": "P04",
        "product_name": "Biz 5G AirFiber 100",
        "monthly_inr": 899,
        "setup_inr": 0,
        "description": "Plug-and-play wireless business broadband",
        "complementary_connectivity": None,
        "flag_human_rep": False
    }

# -------------------------------------------------------------------------
# 8. DYNAMIC SYSTEM PROMPT BUILDER WITH MULTILINGUAL INJECTION
# -------------------------------------------------------------------------
def build_proactive_sales_prompt(session: Dict[str, Any], lang: str) -> str:
    """
    Builds the dynamic system prompt enforcing:
    - Consultative salesperson personality
    - Strict native language consistency (English, Devanagari Hindi, Gurmukhi Punjabi, Hinglish)
    - Proactive handling of customer indecision (no endless loops)
    - Accurate product catalogue pricing (P19 Cloud POS @ ₹599/mo)
    - Single question at a time
    """
    profile = session.get("profile", {})
    btype = profile.get("business_type", "kirana")
    b_intent = session.get("billing_intent", {})
    pref_state = session.get("preference_tracking", {})

    # Language Directives
    if lang == "hi":
        lang_directive = (
            "LANGUAGE DIRECTIVE: Respond entirely in natural conversational Hindi using Devanagari script (देवनागरी). "
            "Maintain the tone of a friendly and knowledgeable Airtel Business salesperson. "
            "Common technology terms like GST, UPI, POS, billing, software, cloud, and fiber should be kept in natural English where common."
        )
    elif lang == "pa":
        lang_directive = (
            "LANGUAGE DIRECTIVE: Respond in natural conversational Punjabi using Gurmukhi script (ਪੰਜਾਬੀ). "
            "Maintain a friendly, respectful and consultative tone. "
            "Common business and technology terminology (GST, UPI, POS, billing, internet) may remain in English where natural."
        )
    elif lang == "hinglish":
        lang_directive = (
            "LANGUAGE DIRECTIVE: Respond in natural Indian Hinglish using a comfortable, polite mixture of Hindi and English. "
            "Do not force formal Hindi translations of commonly used business and technology terms. Sound like a knowledgeable local Airtel manager."
        )
    else: # English
        lang_directive = (
            "LANGUAGE DIRECTIVE: Respond entirely in natural, simple English. "
            "Maintain the tone of a friendly, knowledgeable Airtel Business sales consultant."
        )

    # Indecision Instructions
    indecision_directive = (
        "CRITICAL INDECISION & DELEGATION POLICY:\n"
        "1. If customer says 'Whatever is fine', 'You decide', 'I don't know', 'Jo marzi', 'Tusi hi dass do', or 'Kuch bhi chalega':\n"
        "   - DO NOT ASK THE SAME PREFERENCE QUESTION AGAIN.\n"
        "   - TAKE OWNERSHIP: Make a sensible, recommended business decision on their behalf (e.g. choose Cloud POS billing because it allows mobile/anywhere access).\n"
        "   - Briefly state why, and move the conversation forward.\n"
        "2. When customer needs digital billing/invoicing: Confirm manual vs software -> GST needs -> approximate monthly volume. "
        "   Once volume (~300-400 bills) is established, RECOMMEND Cloud-based billing immediately. DO NOT interrogate about cloud vs desktop.\n"
        "3. NEVER ask the same question more than once if customer delegates or indicates indifference."
    )

    # Catalogue & Pricing Directive
    catalogue_directive = (
        "PRODUCT CATALOGUE & PRICING CONSTRAINTS:\n"
        "- Invoicing / Billing software is genuinely offered as: 'Cloud POS & Billing (P19)' at ₹599/month (setup ₹2,500). "
        "  Features: GST-ready invoicing, barcode scanner support, inventory sync, and instant UPI payment receipts.\n"
        "- Connectivity: Biz 5G AirFiber 100 (P04) at ₹899–₹1,099/mo or Biz Fibre 100 (P01) at ₹999/mo.\n"
        "- Complete Kirana Starter Bundle is ₹1,999/mo (includes AirFiber 100 + 4G Backup Failover + WhatsApp API + Guest Wi-Fi).\n"
        "- NEVER hallucinate unlisted products or invent fake prices. NEVER recommend a ₹14,999 industrial package to a retail/billing customer!"
    )

    prompt = (
        f"You are an experienced, empathetic, and proactive Airtel Business sales consultant in India helping an MSME owner.\n\n"
        f"{lang_directive}\n\n"
        f"{indecision_directive}\n\n"
        f"{catalogue_directive}\n\n"
        "CONVERSATION RULES:\n"
        "1. ASK EXACTLY ONE QUESTION AT A TIME. Keep normal responses strictly between 10 and 35 words.\n"
        "2. Always acknowledge what the customer just shared with natural empathy (e.g., 'Samajh gaya.', 'Bilkul!', 'Understood.').\n"
        "3. Do not ask for information already known.\n"
        "4. Transition towards recommendation once requirements are sufficient (usually after 2–3 key inputs).\n\n"
        f"CURRENT CUSTOMER PROFILE: {json.dumps(profile, ensure_ascii=False)}\n"
        f"BILLING INTENT STATUS: {json.dumps(b_intent, ensure_ascii=False)}\n"
        f"PREFERENCE TRACKING: {json.dumps(pref_state, ensure_ascii=False)}\n\n"
        "STREAMING OUTPUT FORMAT:\n"
        "Output your conversational message to the user directly.\n"
        "Then, on a new line, output the exact marker ||META|| followed by a single-line JSON object:\n"
        '{"profile_updates": {...}, "quick_replies": ["option 1", "option 2"], '
        '"recommend_bundle": "<bundle_id or null>", "discovery_complete": <true or false>, "why_brief": "<short summary>"}\n'
    )

    return prompt

# -------------------------------------------------------------------------
# 9. DETERMINISTIC CONVERSATIONAL FALLBACK GENERATOR (Zero-Failure Execution)
# -------------------------------------------------------------------------
def generate_deterministic_consultant_reply(
    session: Dict[str, Any],
    last_user_text: str,
    lang: str = "en"
) -> Tuple[str, List[str], Optional[str], bool, str]:
    """
    Deterministic rule-based conversational consultant.
    Guarantees that even without LLM connectivity, the exact regression conversation:
    'I need a digital billing system' -> 'Paper' -> 'Yes' -> '300-400'
    proceeds smoothly to recommendation without looping on 'cloud vs desktop'!
    """
    text_clean = last_user_text.strip()
    text_low = text_clean.lower()
    
    # 1. Update billing intent
    b_intent = detect_billing_and_invoicing_intent(text_clean, session)
    profile = session.get("profile", {})
    btype = profile.get("business_type", "kirana")
    msg_count = len(session.get("messages", [])) + 1

    # 2. Check for Indecision / Delegation in current input
    classification = classify_user_response(text_clean, session)

    # ---------------------------------------------------------
    # SCENARIO A: DIGITAL BILLING & INVOICING WORKFLOW
    # ---------------------------------------------------------
    if b_intent["active"]:
        # Step 1: Customer asks for billing system
        if b_intent["current_method"] is None and not any(k in text_low for k in ["paper", "software", "spreadsheet"]):
            if lang == "hi":
                reply = "बिल्कुल! अभी आप कागज़ (paper) पर बिलिंग करते हैं या कोई सॉफ्टवेयर इस्तेमाल कर रहे हैं?"
                quick = ["कागज़ पर (Paper)", "सॉफ्टवेयर पर (Software)", "एक्सेल स्प्रेडशीट"]
            elif lang == "pa":
                reply = "ਬਿਲਕੁਲ! ਹੁਣ ਤੁਸੀਂ ਕਾਗਜ਼ (paper) 'ਤੇ ਬਿਲਿੰਗ ਕਰਦੇ ਹੋ ਜਾਂ ਕੋਈ ਸਾਫਟਵੇਅਰ ਵਰਤ ਰਹੇ ਹੋ?"
                quick = ["ਕਾਗਜ਼ 'ਤੇ (Paper)", "ਕੰਪਿਊਟਰ ਸਾਫਟਵੇਅਰ", "ਐਕਸਲ ਸ਼ੀਟ"]
            elif lang == "hinglish":
                reply = "Bilkul! Abhi aap paper par billing karte hain ya koi software use kar rahe hain?"
                quick = ["Currently on paper", "Using software", "Simple spreadsheet"]
            else:
                reply = "Understood! Are you currently doing manual paper billing or using any software?"
                quick = ["Currently on paper", "Using software", "Simple spreadsheet"]
            return reply, quick, None, False, ""

        # Step 2: Customer said paper, check GST invoicing
        if b_intent["current_method"] == "paper" and b_intent["gst_required"] is None and not any(w in text_low for w in ["yes", "haan", "proper", "gst"]):
            if lang == "hi":
                reply = "समझ गया। क्या आपको प्रॉपर GST इनवॉइसिंग और बिलिंग सॉफ्टवेयर चाहिए?"
                quick = ["हाँ, GST इनवॉइसिंग चाहिए", "नहीं, साधारण बिल काफी है"]
            elif lang == "pa":
                reply = "ਸਮਝ ਗਿਆ। ਕੀ ਤੁਹਾਨੂੰ ਪ੍ਰੋਪਰ GST ਇਨਵੌਇਸਿੰਗ ਅਤੇ ਬਿਲਿੰਗ ਸਾਫਟਵੇਅਰ ਚਾਹੀਦਾ ਹੈ?"
                quick = ["ਹਾਂ, GST ਬਿਲਿੰਗ ਚਾਹੀਦੀ ਹੈ", "ਨਹੀਂ, ਸਿੰਪਲ ਬਿੱਲ ਕਾਫੀ ਹੈ"]
            elif lang == "hinglish":
                reply = "Samajh gaya. Aapko proper GST invoicing aur billing software chahiye?"
                quick = ["Yes, need proper GST invoicing", "Simple non-GST bill is fine"]
            else:
                reply = "Understood. Do you need proper GST-compliant invoicing software?"
                quick = ["Yes, need proper GST invoicing", "Simple non-GST bill is fine"]
            return reply, quick, None, False, ""

        # Step 3: GST confirmed, check invoice volume
        if b_intent["monthly_invoices"] is None:
            if lang == "hi":
                reply = "महीने में लगभग कितने बिल या इनवॉइस बनते हैं?"
                quick = ["100–200", "300–400", "500 से अधिक"]
            elif lang == "pa":
                reply = "ਮਹੀਨੇ ਵਿੱਚ ਲਗਭਗ ਕਿੰਨੇ ਬਿੱਲ ਬਣਦੇ ਹਨ?"
                quick = ["100–200", "300–400", "500 ਤੋਂ ਵੱਧ"]
            elif lang == "hinglish":
                reply = "Mahine mein approximately kitne bills banate hain?"
                quick = ["100–200", "300–400", "500+ bills"]
            else:
                reply = "Approximately how many invoices do you generate monthly?"
                quick = ["100–200", "300–400", "500+ bills"]
            return reply, quick, None, False, ""

        # Step 4: Volume established (e.g. 300-400)!
        # PROACTIVE SALES CONSULTANT ACTION:
        # Instead of asking cloud vs desktop repeatedly, make the decision and recommend Cloud POS Billing (P19)!
        b_intent["deployment_preference"] = "cloud"
        session["identified_needs"].append({
            "category": "cloud_productivity",
            "customer_statement": last_user_text,
            "classified_requirement": "Cloud POS & GST Billing Counter (P19)",
            "type": "explicit",
            "importance": "critical",
            "evidence": f"Customer generates {b_intent['monthly_invoices']} monthly invoices and requires GST-ready digital billing.",
            "confidence": 0.98
        })

        target_bundle = "bundle_kirana"
        if lang == "hi":
            reply = (
                "अच्छा! आपके लिए क्लाउड-बेस्ड बिलिंग सिस्टम सबसे सही रहेगा। इसमें आप टैबलेट या फोन से कहीं भी इनवॉइस बना सकते हैं "
                "और बारकोड/UPI पेमेंट तुरंत ले सकते हैं। मैंने आपके लिए उपयुक्त प्लान तैयार कर दिया है।"
            )
            why = "एयरटेल क्लाउड POS और बिलिंग (P19) के साथ 2-दिन का एयरफाइबर सेटअप आपके बिलिंग काउंटर को 100% अपटाइम देता है।"
            quick = ["प्लान डिटेल्स देखें", "इंस्टॉलेशन समय चेक करें", "कॉल बैक बुक करें"]
        elif lang == "pa":
            reply = (
                "ਵਧੀਆ! ਤੁਹਾਡੇ ਲਈ ਕਲਾਊਡ-ਬੇਸਡ ਬਿਲਿੰਗ ਸਿਸਟਮ ਸਭ ਤੋਂ ਵਧੀਆ ਰਹੇਗਾ। ਇਸ ਨਾਲ ਤੁਸੀਂ ਮੋਬਾਈਲ ਜਾਂ ਟੈਬਲੇਟ ਤੋਂ ਸਿੱਧਾ ਇਨਵੌਇਸ ਬਣਾ ਸਕਦੇ ਹੋ। "
                "ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਏਅਰਟੈਲ ਦਾ ਢੁਕਵਾਂ ਬੰਡਲ ਤਿਆਰ ਕਰ ਦਿੱਤਾ ਹੈ।"
            )
            why = "ਏਅਰਟੈਲ ਕਲਾਊਡ POS ਬਿਲਿੰਗ (P19) ਅਤੇ ਹਾਈ-ਸਪੀਡ ਇੰਟਰਨੈਟ ਤੁਹਾਡੇ ਕਾਰੋਬਾਰ ਨੂੰ ਤੇਜ਼ ਅਤੇ ਭਰੋਸੇਮੰਦ ਬਣਾਉਂਦਾ ਹੈ।"
            quick = ["ਪੈਕੇਜ ਵੇਖੋ", "ਇੰਸਟਾਲੇਸ਼ਨ ਸਮਾਂ", "ਕਾਲ ਬੁੱਕ ਕਰੋ"]
        elif lang == "hinglish":
            reply = (
                "Achha! Aapke liye cloud-based billing system suitable rahega. Ismein aap phone ya tablet se kahin se bhi invoices manage kar sakte hain "
                "aur instant UPI payments le sakte hain. Main aapke liye best option recommend kar raha hoon."
            )
            why = "Airtel Cloud POS Billing (P19) aur reliable AirFiber internet aapke counter par kabhi billing rukne nahi dega."
            quick = ["View Package Details", "Check Installation SLA", "Request Call Back"]
        else:
            reply = (
                "Cloud-based billing would be a sensible option for your requirements. It allows you to create GST invoices from tablet or phone with instant UPI acceptance. "
                "I have prepared the matching Airtel Business recommendation for you."
            )
            why = "Airtel Cloud POS Billing (P19) combined with plug-and-play AirFiber ensures fast invoicing and uninterrupted UPI payments."
            quick = ["View Package Details", "Check Installation SLA", "Request Call Back"]

        return reply, quick, target_bundle, True, why

    # ---------------------------------------------------------
    # SCENARIO B: INDECISION OR DELEGATION IN GENERAL DISCOVERY
    # ---------------------------------------------------------
    if classification["category"] in ["delegated_decision", "uncertainty"]:
        ack, q_state = handle_indecision_policy(
            session=session,
            question_id="general_preference",
            classification=classification,
            recommended_default="AirFiber with automatic 4G backup",
            default_reason="Customer delegated; wireless 5G FWA with auto 4G failover ensures zero payment downtime.",
            contrast_summary={
                "short_hi": "एयरफाइबर और 4G बैकअप",
                "short_pa": "ਏਅਰਫਾਈਬਰ ਅਤੇ 4G ਬੈਕਅੱਪ",
                "short_hinglish": "AirFiber with 4G backup",
                "desc_en": "AirFiber installs in 48 hours without trenching, while traditional wired fiber takes 5–7 days.",
                "desc_hi": "एयरफाइबर बिना तार खोदे 48 घंटे में एक्टिव हो जाता है, जबकि वायर्ड फाइबर में 5-7 दिन लगते हैं।",
                "desc_pa": "ਏਅਰਫਾਈਬਰ ਬਿਨਾਂ ਤਾਰ ਖੋਦੇ 48 ਘੰਟਿਆਂ ਵਿੱਚ ਚਾਲੂ ਹੋ ਜਾਂਦਾ ਹੈ।",
                "desc_hinglish": "AirFiber bina wiring ke 48 hours me activate ho jata hai, jabki traditional fiber me 5-7 din lagte hain."
            },
            lang=lang
        )
        return ack, ["Proceed with recommendation", "Explain other options"], "bundle_kirana", True, "Wireless plug-and-play AirFiber ensures zero disruption."

    # ---------------------------------------------------------
    # SCENARIO C: REGULAR DISCOVERY FLOW BY BUSINESS CATEGORY
    # ---------------------------------------------------------
    if btype == "clinic":
        if msg_count <= 2:
            if lang == "hi":
                reply = "नमस्ते डॉक्टर साहब! क्या आपके क्लीनिक पर पेशेंट रिकॉर्ड्स और बिलिंग के लिए 1TB सुरक्षित क्लाउड बैकअप आवश्यक है?"
                quick = ["हाँ, 1TB बैकअप चाहिए", "सिर्फ फ़ास्ट Wi-Fi", "मरीज़ों के लिए गेस्ट Wi-Fi"]
            elif lang == "pa":
                reply = "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਡਾਕਟਰ ਸਾਹਿਬ! ਕੀ ਮਰੀਜ਼ਾਂ ਦੇ ਰਿਕਾਰਡ ਸੁਰੱਖਿਅਤ ਰੱਖਣ ਲਈ ਕਲਾਊਡ ਬੈਕਅੱਪ ਚਾਹੀਦਾ ਹੈ?"
                quick = ["ਹਾਂ, ਕਲਾਊਡ ਬੈਕਅੱਪ ਚਾਹੀਦਾ ਹੈ", "ਸਿਰਫ਼ ਤੇਜ਼ ਇੰਟਰਨੈਟ", "ਦੋਵੇਂ ਚਾਹੀਦੇ ਹਨ"]
            elif lang == "hinglish":
                reply = "Samajh gaya doctor saab. Patient files aur medical records ka secure cloud backup zaroori hai?"
                quick = ["Yes, 1TB backup needed", "Only fast Wi-Fi", "Need guest Wi-Fi too"]
            else:
                reply = "Understood. For your clinic, do you require automated 1TB encrypted cloud backup for patient records and billing?"
                quick = ["Yes, 1TB cloud backup", "Only high-speed Wi-Fi", "Both needed"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "bundle_clinic"
            reply = "Understood! Clinic Suite with 300 Mbps symmetrical fiber and 1TB encrypted cloud backup is ideal for your practice."
            quick = ["View Package Details", "Check Installation SLA", "Book Appointment"]
            return reply, quick, target_bundle, True, "High-speed 300 Mbps fiber with 1TB encrypted backup keeps patient records safe and compliant."

    elif btype == "multisite":
        if msg_count <= 2:
            reply = "Got it. Do you need centralized CCTV monitoring and SD-WAN failover across your branches on a single bill?"
            quick = ["Yes, CCTV & SD-WAN both", "Single bill is critical", "Need CCTV mainly", "Just fast internet"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "bundle_multisite"
            reply = "Understood! Multi-Site Retail Pro links all branches with 1 Gbps fiber, SD-WAN, and 4x Cloud CCTV on one unified bill."
            quick = ["View Package Details", "Check Installation SLA", "Request Survey"]
            return reply, quick, target_bundle, True, "Centralized SD-WAN inter-branch sync and cloud surveillance on a single monthly invoice."

    elif btype == "manufacturer":
        if msg_count <= 2:
            reply = "Understood. Do you require dedicated uncompressed leased line bandwidth with static IP for ERP?"
            quick = ["Yes, 1:1 Leased Line", "Static IP for ERP", "Machine IoT sensors", "All of these"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "bundle_manufacturer"
            reply = "Understood. The Small Manufacturing Suite with uncompressed leased line and machine IoT telemetry is the right fit."
            quick = ["View Package Details", "Check Installation SLA", "Talk to Enterprise Team"]
            return reply, quick, target_bundle, True, "Dedicated 1:1 CIR leased line with static IP ensures 99.95% ERP uptime."

    else: # Kirana / Micro
        if msg_count <= 2:
            if lang == "hi":
                reply = "नमस्ते! आपकी दुकान पर UPI पेमेंट्स और POS मशीन का उपयोग होता है?"
                quick = ["हाँ, UPI और POS दोनों", "सिर्फ QR कोड", "कैश मुख्य रूप से"]
            elif lang == "pa":
                reply = "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਕੀ ਤੁਹਾਡੀ ਦੁਕਾਨ 'ਤੇ UPI ਅਤੇ POS ਮਸ਼ੀਨ ਵਰਤੀ ਜਾਂਦੀ ਹੈ?"
                quick = ["ਹਾਂ, ਦੋਵੇਂ ਵਰਤੇ ਜਾਂਦੇ ਹਨ", "ਸਿਰਫ਼ QR ਕੋਡ", "ਸਿਰਫ਼ ਕੈਸ਼"]
            elif lang == "hinglish":
                reply = "Samajh gaya. Aapki dukaan par UPI payments aur POS machine use karte hain?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            else:
                reply = "Understood! Does your shop rely heavily on UPI QR payments or card swipe POS machines?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "bundle_kirana"
            reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."

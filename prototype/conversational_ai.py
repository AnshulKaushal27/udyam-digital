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
        b_intent["active"] = True
    elif any(k in text_low for k in ["software", "tally", "busy", "computerized"]):
        b_intent["current_method"] = "software"
        b_intent["active"] = True
    elif any(k in text_low for k in ["excel", "spreadsheet", "sheet"]):
        b_intent["current_method"] = "spreadsheet"
        b_intent["active"] = True

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

    # Strict Turn & Indecision Directives
    indecision_directive = (
        "CRITICAL CONVERSATIONAL RULES (ABSOLUTE NON-NEGOTIABLE):\n"
        "1. You are speaking in REAL-TIME with an MSME customer. Output ONLY YOUR NEXT SINGLE MESSAGE (15 to 30 words maximum).\n"
        "2. NEVER simulate the customer's responses. NEVER generate both sides of the conversation. Output ONLY what YOU say next!\n"
        "3. ASK AT MOST ONE SINGLE QUESTION AT A TIME. Never ask multiple questions. Never concatenate questions.\n"
        "4. DO NOT loop or repeat questions. Do not jump ahead into future steps.\n"
        "5. If customer is on paper billing: acknowledge and ask ONLY whether they need GST-compliant invoices. Stop!\n"
        "6. If customer already confirmed GST: ask ONLY approximately how many invoices they generate monthly. Stop!\n"
        "7. If customer volume is known (~300-500 bills): recommend Cloud POS & Billing (P19) at ₹599/month (setup ₹2,500).\n"
        "8. If customer expresses indecision ('Whatever is fine', 'You decide', 'Jo marzi', 'Tusi hi dass do'):\n"
        "   - DO NOT ASK THE SAME PREFERENCE QUESTION AGAIN.\n"
        "   - TAKE OWNERSHIP: Make a sensible recommendation on their behalf and advance.\n"
        "9. NEVER ask the same question twice. NEVER repeat sentences."
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

        target_bundle = "prod_p19_pos"
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
        # 1. Check if user asked about connectivity speed or fast internet
        is_speed_need = any(k in text_low for k in ["tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi", "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber", "fibre", "symmetrical", "buffering", "speed chahiye", "तेज इंटरनेट", "इंटरनेट", "हाई स्पीड", "स्पीड", "वाईफाई", "फास्ट इंटरनेट", "ਤੇਜ਼ ਇੰਟਰਨੈੱਟ", "ਇੰਟਰਨੈੱਟ", "ਹਾਈ ਸਪੀਡ", "ਸਪੀਡ", "ਵਾਈ-ਫਾਈ"])
        if is_speed_need:
            if lang == "hi":
                reply = "समझ गया! मैंने आपके लिए High-Speed Symmetrical Fiber विकल्प चुन लिया है ताकि आपको हाई-स्पीड और बफरिंग-फ्री इंटरनेट मिले। इसके अलावा क्या आपको CCTV या Static IP की आवश्यकता है?"
                quick = ["24/7 Cloud CCTV जोड़ें", "Static IP जोड़ें", "डिजिटल बंडल तैयार करें"]
            elif lang == "pa":
                reply = "ਸਮਝ ਗਿਆ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ High-Speed Symmetrical Fiber ਚੁਣ ਲਿਆ ਹੈ ਤਾਂ ਜੋ ਤੁਹਾਨੂੰ ਤੇਜ਼ ਅਤੇ ਬਿਨਾਂ ਰੁਕਾਵਟ ਇੰਟਰਨੈੱਟ ਮਿਲੇ। ਕੀ ਤੁਹਾਨੂੰ CCTV ਜਾਂ Static IP ਦੀ ਲੋੜ ਹੈ?"
                quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ", "Static IP ਸ਼ਾਮਲ ਕਰੋ", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
            elif lang == "hinglish":
                reply = "Samajh gaya! Maine aapke liye High-Speed Symmetrical Fiber select kar diya hai taaki aapko high speed aur zero buffering connectivity mile. Iske alawa kya aapko CCTV surveillance ya Static IP ki zaroorat hai?"
                quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            else:
                reply = "Understood! I have selected High-Speed Symmetrical Fiber for your setup to ensure consistent high-speed bandwidth with zero buffering. Would you also like to explore Cloud CCTV or Static IP?"
                quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            return reply, quick, "bundle_kirana", False, "High-speed symmetrical broadband selected for zero-buffering operations."

        # 2. Check if user asked what additions or options are available
        is_additions_query = any(k in text_low for k in ["aur kya", "what else", "additions", "available options", "kya kya add", "other options", "kya kya options", "what additions", "available additions", "add-ons available", "add ons available", "kya add kar sakte"])
        if is_additions_query:
            if lang == "hi":
                reply = "आपके सेटअप के लिए ये अतिरिक्त विकल्प उपलब्ध हैं:\n1. 24/7 Cloud CCTV (2 कैमरे, 30 दिन रिकॉर्डिंग) - ₹800/माह\n2. Fixed Static IP Address (सर्वर या NVR के लिए) - ₹300/माह\n3. Instant UPI & POS Failover (4G बैकअप सिम) - ₹499/माह\n4. WhatsApp Business API (कस्टमर मैसेजिंग) - ₹999/माह\nक्या आप इनमें से कोई जोड़ना चाहते हैं?"
                quick = ["Cloud CCTV जोड़ें (+₹800)", "Static IP जोड़ें (+₹300)", "डिजिटल बंडल तैयार करें"]
            elif lang == "pa":
                reply = "ਤੁਹਾਡੇ ਸੈੱਟਅੱਪ ਲਈ ਇਹ ਹੋਰ ਵਿਕਲਪ ਉਪਲਬਧ ਹਨ:\n1. 24/7 Cloud CCTV (2 ਕੈਮਰੇ) - ₹800/ਮਹੀਨਾ\n2. Fixed Static IP Address - ₹300/ਮਹੀਨਾ\n3. Instant UPI Failover (4G ਬੈਕਅੱਪ) - ₹499/ਮਹੀਨਾ\n4. WhatsApp Business API - ₹999/ਮਹੀਨਾ"
                quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ (+₹800)", "Static IP ਸ਼ਾਮਲ ਕਰੋ (+₹300)", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
            elif lang == "hinglish":
                reply = "Aapke setup ke liye ye catalogue-backed additions available hain:\n1. 24/7 Cloud CCTV (2 HD Cameras with 30-day cloud recording) - ₹800/mo\n2. Fixed Static IP Address (for servers or local NVR) - ₹300/mo\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\n4. WhatsApp Business API (automated customer updates) - ₹999/mo\nAap inme se kaunsa option add karna chahte hain?"
                quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            else:
                reply = "Here are the eligible catalogue-backed additions available for your business:\n1. 24/7 Cloud CCTV (2 HD Cameras, 30-day cloud recording) - ₹800/mo\n2. Fixed Static IP Address - ₹300/mo\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\n4. WhatsApp Business API - ₹999/mo\nWould you like to add any of these to your setup?"
                quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            return reply, quick, None, False, "Listing catalogue-backed eligible additions."

        # 3. Check for specific payment mentions
        has_payment_mentioned = any(k in text_low for k in ["upi", "pos", "qr", "cash", "payment", "card", "swipe", "scanner", "gpay", "phonepe", "paytm"])
        if has_payment_mentioned or msg_count > 2:
            target_bundle = "prod_p19_pos"
            if "cash" in text_low and not any(k in text_low for k in ["upi", "pos", "qr"]):
                reply = "Understood! For cash-centric retail, our high-speed Fiber ensures your store accounting and billing stay uninterrupted."
            else:
                reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI QR and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."
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
            target_bundle = "prod_p19_pos"
            reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."


# -------------------------------------------------------------------------
# 10. BIDIRECTIONAL QUOTE ACTION & CUSTOMIZATION RECOGNITION
# -------------------------------------------------------------------------
def parse_quote_action_intent(
    text: str,
    session: Dict[str, Any],
    current_quote: Optional[Dict[str, Any]] = None,
    lang: str = "en"
) -> Optional[Dict[str, Any]]:
    """
    Recognizes customer intent to inspect prices or modify the active quote via natural conversation:
    1. Inquire price without modifying quote ("How much is CCTV?")
    2. Add add-on ("Add CCTV", "Include static IP", "Yes add it")
    3. Remove add-on ("Remove CCTV", "Don't need cameras")
    4. Make it cheaper / Budget objections ("Make it cheaper", "Too expensive")
    5. Switch package ("Switch to ₹599 POS plan", "Switch to Kirana starter")
    """
    text_clean = text.strip()
    text_low = text_clean.lower()

    # 1. Price Inquiries (Must NOT modify quote)
    is_inquiry = any(k in text_low for k in ["how much", "kitna", "kitne", "price of", "cost of", "rate of", "kya charge"])
    
    if is_inquiry:
        if any(k in text_low for k in ["cctv", "camera", "surveillance"]):
            if lang == "hi":
                reply = "एयरटेल क्लाउड CCTV (2 HD कैमरे, 30-दिन का क्लाउड बैकअप) ₹800/महीना है और एक बार का इंस्टॉलेशन ₹1,200 है। क्या आप इसे अपने कोटेशन में जोड़ना चाहते हैं?"
            elif lang == "pa":
                reply = "ਏਅਰਟੈਲ ਕਲਾਊਡ CCTV (2 ਕੈਮਰੇ, 30 ਦਿਨ ਰਿਕਾਰਡਿੰਗ) ₹800/ਮਹੀਨਾ ਹੈ (+ ₹1,200 ਸੈੱਟਅੱਪ)। ਕੀ ਤੁਸੀਂ ਇਸਨੂੰ ਸ਼ਾਮਲ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?"
            elif lang == "hinglish":
                reply = "Cloud CCTV (2 HD Cameras, 30-day cloud recording) ₹800/month hai with ₹1,200 one-time setup. Kya aap ise apne quote me add karna chahte hain?"
            else:
                reply = "Cloud CCTV (2 HD Cameras with 30-day cloud recording & mobile live view) costs ₹800/month with a one-time setup of ₹1,200. Would you like me to add it to your quote?"
            return {
                "action": "inquire_price",
                "target_key": "addon_cctv",
                "reply_text": reply,
                "quick_replies": ["Yes, add CCTV to quote", "No, keep current quote"],
                "requires_quote_update": False
            }

        if any(k in text_low for k in ["static ip", "fixed ip", "public ip"]):
            if lang == "hi":
                reply = "फिक्स्ड स्टैटिक IP एड्रेस ₹300/महीना है (जीरो सेटअप चार्ज)। क्या मैं इसे आपके प्लान में जोड़ दूँ?"
            elif lang == "pa":
                reply = "ਸਟੈਟਿਕ ਪਬਲਿਕ IP ₹300/ਮਹੀਨਾ ਹੈ (ਜ਼ੀਰੋ ਸੈੱਟਅੱਪ ਫੀਸ)। ਕੀ ਤੁਸੀਂ ਇਸਨੂੰ ਸ਼ਾਮਲ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?"
            elif lang == "hinglish":
                reply = "Static Public IP address ₹300/month hai with ₹0 setup fee. Tally ya server ke liye use hota hai. Add kar doon?"
            else:
                reply = "A Fixed Static Public IP address is ₹300/month with zero setup fee. It provides a permanent IP for on-premise servers. Would you like to add it?"
            return {
                "action": "inquire_price",
                "target_key": "addon_static_ip",
                "reply_text": reply,
                "quick_replies": ["Yes, add Static IP", "No, keep current quote"],
                "requires_quote_update": False
            }

        if any(k in text_low for k in ["sim", "postpaid", "calling line"]):
            reply = "Airtel Business Postpaid SIM with unlimited national calling and 50 GB data is ₹299/month (zero setup fee). Would you like to add it to your quote?"
            return {
                "action": "inquire_price",
                "target_key": "addon_sim",
                "reply_text": reply,
                "quick_replies": ["Yes, add Business SIM", "No, keep current quote"],
                "requires_quote_update": False
            }

    # 2. Add Add-on Intent
    is_add = any(k in text_low for k in ["add ", "include ", "add kar", "daal do", "yes, add", "yes add", "please add"]) or any(k in text_low for k in ["cctv chahiye", "static ip chahiye", "sim chahiye"])
    if is_add or text_low in ["add cctv", "add static ip", "add sim", "add airfiber", "cctv chahiye", "static ip chahiye"]:
        if any(k in text_low for k in ["cctv", "camera"]):
            if lang == "hi":
                reply = "मैंने आपके कोटेशन में क्लाउड CCTV (+₹800/माह, ₹1,200 सेटअप) जोड़ दिया है। आपका पैकेज कार्ड अपडेट हो गया है।"
            elif lang == "pa":
                reply = "ਮੈਂ ਤੁਹਾਡੇ ਕੋਟੇਸ਼ਨ ਵਿੱਚ ਕਲਾਊਡ CCTV (+₹800/ਮਹੀਨਾ) ਜੋੜ ਦਿੱਤਾ ਹੈ। ਤੁਹਾਡਾ ਪੈਕੇਜ ਕਾਰਡ ਅਪਡੇਟ ਹੋ ਗਿਆ ਹੈ।"
            elif lang == "hinglish":
                reply = "Cloud CCTV (+₹800/mo, ₹1,200 setup) aapke quote mein add ho gaya hai. Package card update kar diya gaya hai."
            else:
                reply = "I have added Cloud CCTV (2 Cameras, +₹800/mo, ₹1,200 setup) to your quote. Your package card and pricing summary have been updated in real-time."
            return {
                "action": "add_addon",
                "target_key": "addon_cctv",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

        if any(k in text_low for k in ["static ip", "fixed ip"]):
            reply = "I have added a Fixed Static Public IP (+₹300/mo) to your quote. Your package card and pricing have been updated."
            return {
                "action": "add_addon",
                "target_key": "addon_static_ip",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

        if any(k in text_low for k in ["sim", "postpaid"]):
            reply = "I have added a Business Postpaid SIM (+₹299/mo) to your quote. Your package card has been updated."
            return {
                "action": "add_addon",
                "target_key": "addon_sim",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

        if any(k in text_low for k in ["airfiber", "air fiber", "add airfiber", "include airfiber"]):
            reply = "I have added Biz 5G AirFiber 100 (+₹899/mo) to your quote. Your package card has been updated."
            return {
                "action": "add_addon",
                "target_key": "addon_airfiber",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

    # 3. Remove Add-on Intent
    is_remove = any(k in text_low for k in ["remove", "hata", "cancel", "don't need", "dont need", "nahi chahiye", "drop", "delete"])
    if is_remove:
        active_addons_in_quote = []
        if current_quote:
            for a in current_quote.get("addons", []):
                if isinstance(a, dict):
                    active_addons_in_quote.append(a.get("addon_key") or a.get("id"))
                elif isinstance(a, str):
                    active_addons_in_quote.append(a)
            for sa in current_quote.get("selected_addons", []):
                if isinstance(sa, dict):
                    active_addons_in_quote.append(sa.get("addon_key") or sa.get("id"))
                elif isinstance(sa, str):
                    active_addons_in_quote.append(sa)
        if any(k in text_low for k in ["cctv", "camera"]):
            if not ("addon_cctv" in active_addons_in_quote or "P23" in active_addons_in_quote):
                return {
                    "action": "remove_addon",
                    "target_key": "addon_cctv",
                    "reply_text": "Cloud CCTV is not currently selected in your configuration. Your current quotation remains unchanged.",
                    "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                    "requires_quote_update": False
                }
            if lang == "hi":
                reply = "मैंने आपके कोटेशन से क्लाउड CCTV हटा दिया है। आपका मासिक किराया और पैकेज कार्ड अपडेट हो गया है।"
            elif lang == "pa":
                reply = "ਮੈਂ ਤੁਹਾਡੇ ਕੋਟੇਸ਼ਨ ਤੋਂ ਕਲਾਊਡ CCTV ਹਟਾ ਦਿੱਤਾ ਹੈ। ਤੁਹਾਡਾ ਪੈਕੇਜ ਕਾਰਡ ਅਪਡੇਟ ਹੋ ਗਿਆ ਹੈ।"
            elif lang == "hinglish":
                reply = "Cloud CCTV quote se remove kar diya gaya hai. Aapka monthly total update ho gaya hai."
            else:
                reply = "I have removed Cloud CCTV from your quote. Your package card and monthly total have been updated in real-time."
            return {
                "action": "remove_addon",
                "target_key": "addon_cctv",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

        if any(k in text_low for k in ["static ip", "fixed ip"]):
            if not ("addon_static_ip" in active_addons_in_quote or "P11" in active_addons_in_quote):
                return {
                    "action": "remove_addon",
                    "target_key": "addon_static_ip",
                    "reply_text": "Fixed Static IP Address is not currently selected in your configuration. Your current quotation remains unchanged.",
                    "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                    "requires_quote_update": False
                }
            reply = "I have removed Static Public IP from your quote. Your pricing has been updated."
            return {
                "action": "remove_addon",
                "target_key": "addon_static_ip",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

        if any(k in text_low for k in ["sim", "postpaid"]):
            reply = "I have removed the Business Postpaid SIM from your quote."
            return {
                "action": "remove_addon",
                "target_key": "addon_sim",
                "reply_text": reply,
                "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                "requires_quote_update": True
            }

    # 4. Budget Objections / Make It Cheaper
    is_cheaper = any(k in text_low for k in ["cheaper", "sasta", "expensive", "costly", "kam budget", "less budget", "lower cost", "reduce price", "make it cheaper"])
    if is_cheaper:
        current_bundle_id = current_quote.get("bundle_id") if current_quote else None
        current_addons = current_quote.get("addons", []) if current_quote else []
        
        if current_addons:
            reply = "We can reduce your monthly bill by removing optional add-ons like Cloud CCTV (+₹800/mo) or switching to standalone Cloud POS Billing at ₹599/mo. Would you like to remove add-ons or switch to the ₹599 plan?"
            quick = ["Remove All Add-ons", "Switch to ₹599 POS Plan", "Keep Current Quote"]
        elif current_bundle_id == "bundle_kirana":
            reply = "If you don't need the bundled AirFiber 5G broadband right now, you can start with standalone Cloud POS & GST Billing for just ₹599/month (+ ₹2,500 setup). Would you like me to switch your quote to the ₹599 plan?"
            quick = ["Switch to ₹599 POS Plan", "Keep Kirana Starter Plan", "Customize Package"]
        else:
            reply = "At ₹599/month, Cloud POS & Billing (P19) is our most affordable GST billing counter tier with inventory sync and UPI receipts. Would you like to review its itemized breakdown?"
            quick = ["Itemized Quote", "Accept Quote & Verify", "Customize Package"]
        
        return {
            "action": "make_cheaper",
            "target_key": None,
            "reply_text": reply,
            "quick_replies": quick,
            "requires_quote_update": False
        }

    # 5. Switch Base Package
    if any(k in text_low for k in ["switch to pos", "switch to 599", "switch to ₹599", "give me only billing", "only pos", "only billing"]):
        reply = "I have switched your package to Cloud POS & Billing (P19) at ₹599/month (+ ₹2,500 setup). Your package card and quote have been updated in real-time."
        return {
            "action": "switch_package",
            "target_key": "prod_p19_pos",
            "reply_text": reply,
            "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
            "requires_quote_update": True
        }

    if any(k in text_low for k in ["switch to kirana", "switch to starter", "switch to 1999", "full bundle"]):
        reply = "I have switched your package to Kirana & Micro Retail Digital Starter at ₹1,999/month (AirFiber 100 + 4G backup failover + WhatsApp API). Your package card has been updated."
        return {
            "action": "switch_package",
            "target_key": "bundle_kirana",
            "reply_text": reply,
            "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
            "requires_quote_update": True
        }

    return None


# -------------------------------------------------------------------------
# 11. UNIFIED CONTEXTUAL PROMPT & STRUCTURED INTERPRETATION ENGINE
# -------------------------------------------------------------------------
_GLOBAL_TEST_MOCK_LLM = None

def set_test_mock_llm(mock_fn):
    """Test hook to register a mock LLM function for deterministic integration testing."""
    global _GLOBAL_TEST_MOCK_LLM
    _GLOBAL_TEST_MOCK_LLM = mock_fn

def build_unified_advisor_prompt(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]]
) -> str:
    """
    Constructs a comprehensive system prompt grounding the model in:
    - Current workflow stage
    - Profile and identified needs
    - Numbered GUI options currently visible to the customer
    - Eligible catalogue products & add-ons with pricing
    - Conversation history
    - Structured JSON output format
    """
    stage = workflow.get("stage", "REQUIREMENTS_COLLECTION")
    profile = session.get("profile", {})
    btype = workflow.get("discovery", {}).get("business_type", profile.get("business_type", "kirana"))
    reqs = workflow.get("discovery", {}).get("requirements", [])
    rec = workflow.get("recommendation", {})
    cur_bundle = rec.get("bundle_id", "bundle_kirana")
    active_addons = rec.get("active_addons", [])
    
    # Format visible options for the prompt with clear 1-based indices
    options_summary = []
    for opt in visible_options:
        idx = opt.get("index")
        name = opt.get("name")
        oid = opt.get("id")
        desc = opt.get("description", "")
        sel = "[SELECTED]" if opt.get("selected") else "[UNSELECTED]"
        price = f" ({opt.get('price_inr')}/mo)" if "price_inr" in opt else ""
        options_summary.append(f"  Option {idx}: ID='{oid}' | Name='{name}'{price} | Status={sel} | Desc: {desc}")
    visible_str = "\n".join(options_summary) if options_summary else "  (None currently displayed)"

    # Format catalogue options
    cat_summary = []
    for item in eligible_catalogue:
        cid = item.get("id")
        cname = item.get("name")
        cprice = item.get("price")
        cdesc = item.get("description")
        cat_summary.append(f"  Item {cid}: '{cname}' | Price={cprice} | {cdesc}")
    catalogue_str = "\n".join(cat_summary)

    prompt = (
        "You are the Airtel Business GenAI Digital Advisor for 'Project Udyam Digital' (Bharti Airtel SYNC 2026 Innovation Challenge).\n"
        "Your role is to understand MSME business owners' needs and recommend appropriate Airtel Business solutions.\n\n"
        f"CURRENT WORKFLOW STAGE: {stage}\n"
        f"CUSTOMER PROFILE: Business Type='{btype}', Known Info={json.dumps(profile, ensure_ascii=False)}\n"
        f"CURRENT SELECTIONS: Requirements={json.dumps(reqs)}, Bundle='{cur_bundle}', Active Add-ons={json.dumps(active_addons)}\n\n"
        "CURRENTLY VISIBLE GUI OPTIONS ON CUSTOMER SCREEN (Ordered 1 to N):\n"
        f"{visible_str}\n\n"
        "ELIGIBLE AIRTEL PRODUCT CATALOGUE (Official items & pricing):\n"
        f"{catalogue_str}\n\n"
        f"PREFERRED LANGUAGE: {language} (Respond in English, Hindi Devanagari, Punjabi Gurmukhi, or conversational Hinglish based on user input).\n\n"
        "INTERPRETATION & CONVERSATIONAL RULES:\n"
        "1. INTERPRET MEANING over literal phrase matching. Do not rely on brittle word matches.\n"
        "   - 'mujhe tez internet chahiye', 'need faster Wi-Fi', 'internet slow hai', 'high speed connection chahiye' -> interpret as a connectivity speed need.\n"
        "     In REQUIREMENTS_COLLECTION, map this to visible Option 'broadband_speed' (High-Speed Symmetrical Fiber) and mark it for selection.\n"
        "   - 'aur kya kya additions available hain', 'what else is available', 'what add-ons can I get' -> interpret as 'list_available_options'.\n"
        "     Explain the visible/eligible catalogue additions (e.g. Cloud CCTV, Static IP, WhatsApp API, Cloud POS Billing, UPI failover) with names and pricing.\n"
        "     DO NOT continue asking unrelated payment/POS questions when the customer asked what is available!\n"
        "   - References like 'the second option', 'option 2', 'dusra option' MUST be resolved against the currently visible numbered options list above.\n"
        "2. GROUNDED REPLIES: Never invent non-existent products, fake discounts, or unverified prices. Keep pricing strictly grounded in the catalogue.\n"
        "3. SINGLE CONVERSATIONAL FOCUS: Do not repeat questions already answered. If the customer just expressed a need or asked a question, address it directly.\n"
        "4. OUTPUT FORMAT: You MUST return ONLY a valid JSON object matching the exact schema below:\n"
        "{\n"
        '  "intent": "select_product | add_need | list_available_options | ask_question | provide_information | change_profile | confirm | other",\n'
        '  "interpreted_need": "short plain-language description of customer need",\n'
        '  "target_product_ids": ["catalogue or GUI option ID, e.g. broadband_speed, P23, etc."],\n'
        '  "target_addon_ids": ["catalogue-backed addon ID if applicable, e.g. P23, P11"],\n'
        '  "state_changes": {\n'
        '    "selected_requirements": ["broadband_speed"],\n'
        '    "bundle_id": null,\n'
        '    "selected_addons": []\n'
        '  },\n'
        '  "needs_clarification": false,\n'
        '  "clarification_question": null,\n'
        '  "reply": "<friendly, professional natural language response in requested language>",\n'
        '  "quick_replies": ["option 1", "option 2"]\n'
        "}\n"
        "Output ONLY the JSON object. Do not wrap in extra markdown or commentary."
    )
    return prompt

def interpret_user_intent_fallback(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Deterministic contextual fallback when live LLM is unreachable or returns invalid format.
    Grounded strictly in visible GUI options and catalogue.
    """
    text_clean = user_message.strip()
    text_low = text_clean.lower()
    stage = workflow.get("stage", "REQUIREMENTS_COLLECTION")
    reqs = list(workflow.get("discovery", {}).get("requirements", []))
    
        # 0A. Check for Removal Intent ("remove cctv", "cctv nahi chahiye", "dont need static ip", "fiber hata do")
    is_remove = any(k in text_low for k in ["remove", "hata", "hatao", "hata do", "cancel", "don't need", "dont need", "nahi chahiye", "drop", "delete", "unselect"])
    if is_remove:
        active_addons = list(workflow.get("recommendation", {}).get("active_addons", []))
        rec = workflow.get("recommendation", {})
        
        target_r = None
        target_a = None
        disp_name = None
        
        if any(k in text_low for k in ["cctv", "camera"]):
            target_r = "cctv_security"
            target_a = "P23"
            disp_name = "24/7 Cloud CCTV Surveillance"
        elif any(k in text_low for k in ["static ip", "fixed ip"]):
            target_r = "static_ip"
            target_a = "P11"
            disp_name = "Fixed Static Public IP Address"
        elif any(k in text_low for k in ["speed", "fiber", "fibre", "broadband"]):
            target_r = "broadband_speed"
            target_a = "P01"
            disp_name = "High-Speed Symmetrical Fiber"
        elif any(k in text_low for k in ["upi", "failover", "backup"]):
            target_r = "upi_failover"
            target_a = "P09"
            disp_name = "Instant UPI & POS Failover"
        elif any(k in text_low for k in ["whatsapp"]):
            target_r = "whatsapp_api"
            target_a = "P15"
            disp_name = "WhatsApp Business API"
        elif any(k in text_low for k in ["pos", "billing"]):
            target_r = "pos_billing"
            target_a = "P19"
            disp_name = "Cloud POS & Billing Counter"

        if target_r or target_a:
            is_present = (target_r and target_r in reqs) or (target_a and target_a in active_addons)
            if is_present:
                remove_reqs = [target_r] if (target_r and target_r in reqs) else []
                remove_aids = [target_a] if (target_a and target_a in active_addons) else []
                reply = f"Removed {disp_name} from your configuration. Your quotation has been recalculated."
                return {
                    "intent": "remove_product",
                    "interpreted_need": f"Removed requirement: {disp_name}",
                    "target_product_ids": [],
                    "target_addon_ids": [],
                    "state_changes": {
                        "remove_requirements": remove_reqs,
                        "remove_addons": remove_aids
                    },
                    "needs_clarification": False,
                    "clarification_question": None,
                    "reply": reply,
                    "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
                }
            else:
                reply = f"{disp_name} is not currently selected in your configuration. Your quotation remains unchanged."
                return {
                    "intent": "remove_product",
                    "interpreted_need": f"{disp_name} was not selected",
                    "target_product_ids": [],
                    "target_addon_ids": [],
                    "state_changes": {},
                    "needs_clarification": False,
                    "clarification_question": None,
                    "reply": reply,
                    "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
                }

    # 0. Check for delegation / recommendation request (e.g. "you decide", "what is best", "what do you recommend", "aap decide karo")
    is_delegation = any(k in text_low for k in ["you decide", "what is best", "best for my", "recommend", "aap batao", "tum batao", "suggest", "which plan", "confused", "dont know", "don't know", "what should i choose"])
    if is_delegation:
        reply = "I recommend our Kirana Digital Starter with plug-and-play AirFiber and automatic 4G backup SIM. It is our most popular option engineered to ensure zero payment dropouts."
        return {
            "intent": "select_product",
            "interpreted_need": "Customer delegated package selection to advisor",
            "target_product_ids": ["broadband_speed", "upi_failover"],
            "target_addon_ids": [],
            "state_changes": {"selected_requirements": ["broadband_speed", "upi_failover"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": ["View Package Details", "View Available Add-ons", "Confirm Quote"]
        }

    # 1. Check for inquiries about available additions / options
    is_additions_query = any(k in text_low for k in [
        "aur kya", "what else", "additions", "available options", "kya kya add",
        "other options", "kya kya options", "what additions", "available additions",
        "add-ons available", "add ons available", "kya add kar sakte", "available items"
    ])
    if is_additions_query:
        if language == "hi":
            reply = "आपके सेटअप के लिए ये अतिरिक्त विकल्प उपलब्ध हैं:\n1. 24/7 Cloud CCTV (2 कैमरे, 30 दिन रिकॉर्डिंग) - ₹800/माह\n2. Fixed Static IP Address (सर्वर या NVR के लिए) - ₹300/माह\n3. Instant UPI & POS Failover (4G बैकअप सिम) - ₹499/माह\n4. WhatsApp Business API (कस्टमर मैसेजिंग) - ₹999/माह\nक्या आप इनमें से कोई जोड़ना चाहते हैं?"
            quick = ["Cloud CCTV जोड़ें (+₹800)", "Static IP जोड़ें (+₹300)", "डिजिटल बंडल तैयार करें"]
        elif language == "pa":
            reply = "ਤੁਹਾਡੇ ਸੈੱਟਅੱਪ ਲਈ ਇਹ ਹੋਰ ਵਿਕਲਪ ਉਪਲਬਧ ਹਨ:\n1. 24/7 Cloud CCTV (2 ਕੈਮਰੇ) - ₹800/ਮਹੀਨਾ\n2. Fixed Static IP Address - ₹300/ਮਹੀਨਾ\n3. Instant UPI Failover (4G ਬੈਕਅੱਪ) - ₹499/ਮਹੀਨਾ\n4. WhatsApp Business API - ₹999/ਮਹੀਨਾ"
            quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ (+₹800)", "Static IP ਸ਼ਾਮਲ ਕਰੋ (+₹300)", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
        elif language == "hinglish":
            reply = "Aapke setup ke liye ye catalogue-backed additions available hain:\n1. 24/7 Cloud CCTV (2 HD Cameras with 30-day cloud recording) - ₹800/mo\n2. Fixed Static IP Address (for servers or local NVR) - ₹300/mo\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\n4. WhatsApp Business API (automated customer updates) - ₹999/mo\nAap inme se kaunsa option add karna chahte hain?"
            quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
        else:
            reply = "Here are the eligible catalogue-backed additions available for your business:\n1. 24/7 Cloud CCTV (2 HD Cameras, 30-day cloud recording) - ₹800/mo\n2. Fixed Static IP Address - ₹300/mo\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\n4. WhatsApp Business API - ₹999/mo\nWould you like to add any of these to your setup?"
            quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            
        return {
            "intent": "list_available_options",
            "interpreted_need": "Customer inquired about available additions and add-ons",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": quick
        }

    # 1B. Check for Quote / Bill / Pricing request
    is_quote_query = (
        any(k in text_low for k in ["quote", "bill", "monthly bill", "pricing", "charges"])
        and not any(k in text_low for k in ["how much is", "cctv", "camera", "static ip", "whatsapp", "soundbox", "pos", "billing machine", "billing software", "billing system"])
    )
    if is_quote_query:
        total_m = workflow.get("recommendation", {}).get("total_monthly", 1999)
        return {
            "intent": "view_quote",
            "interpreted_need": "Review quotation and transparent monthly bill",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {"stage": "QUOTE_REVIEW"},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": f"Here is your transparent itemized quotation: ₹{total_m}/month (inclusive of 18% GST). Zero hidden fees.",
            "quick_replies": ["Confirm Quote & Start Smart KYC", "Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)"]
        }

    # 2. Check for Ordinal Reference (e.g. 'the second option', 'option 2', 'dusra option')
    ordinal_map = {
        "first": 1, "1st": 1, "pehla": 1, "option 1": 1,
        "second": 2, "2nd": 2, "dusra": 2, "option 2": 2,
        "third": 3, "3rd": 3, "teesra": 3, "option 3": 3,
        "fourth": 4, "4th": 4, "chautha": 4, "option 4": 4
    }
    target_idx = None
    for k, idx in ordinal_map.items():
        if k in text_low:
            target_idx = idx
            break
            
    if target_idx and visible_options and target_idx <= len(visible_options):
        selected_opt = visible_options[target_idx - 1]
        opt_id = selected_opt.get("id")
        opt_name = selected_opt.get("name")
        opt_type = selected_opt.get("type")
        
        reply = f"I have selected {opt_name} for you based on option {target_idx} from the screen."
        state_changes = {}
        target_pids = [opt_id]
        target_aids = []
        
        if opt_type == "requirement":
            state_changes["selected_requirements"] = [opt_id]
        elif opt_type == "addon":
            state_changes["selected_addons"] = [opt_id]
            target_aids = [opt_id]
        elif opt_type == "base_plan":
            state_changes["bundle_id"] = opt_id
            
        return {
            "intent": "select_product",
            "interpreted_need": f"Selected option {target_idx}: {opt_name}",
            "target_product_ids": target_pids,
            "target_addon_ids": target_aids,
            "state_changes": state_changes,
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 3. Check for Fast Internet / Broadband Speed / Fiber Need
    is_speed_need = any(k in text_low for k in [
        "tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi",
        "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber",
        "fibre", "symmetrical", "buffering", "speed chahiye",
        "तेज इंटरनेट", "इंटरनेट", "हाई स्पीड", "स्पीड", "वाईफाई", "फास्ट इंटरनेट",
        "ਤੇਜ਼ ਇੰਟਰਨੈੱਟ", "ਇੰਟਰਨੈੱਟ", "ਹਾਈ ਸਪੀਡ", "ਸਪੀਡ", "ਵਾਈ-ਫਾਈ"
    ])
    if is_speed_need:
        if language == "hi":
            reply = "समझ गया! मैंने आपके लिए High-Speed Symmetrical Fiber विकल्प चुन लिया है ताकि आपको हाई-स्पीड और बफरिंग-फ्री इंटरनेट मिले। इसके अलावा क्या आपको CCTV या Static IP की आवश्यकता है?"
            quick = ["24/7 Cloud CCTV जोड़ें", "Static IP जोड़ें", "डिजिटल बंडल तैयार करें"]
        elif language == "pa":
            reply = "ਸਮਝ ਗਿਆ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ High-Speed Symmetrical Fiber ਚੁਣ ਲਿਆ ਹੈ ਤਾਂ ਜੋ ਤੁਹਾਨੂੰ ਤੇਜ਼ ਅਤੇ ਬਿਨਾਂ ਰੁਕਾਵਟ ਇੰਟਰਨੈੱਟ ਮਿਲੇ। ਕੀ ਤੁਹਾਨੂੰ CCTV ਜਾਂ Static IP ਦੀ ਲੋੜ ਹੈ?"
            quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ", "Static IP ਸ਼ਾਮਲ ਕਰੋ", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
        elif language == "hinglish":
            reply = "Samajh gaya! Maine aapke liye High-Speed Symmetrical Fiber select kar diya hai taaki aapko high speed aur zero buffering connectivity mile. Iske alawa kya aapko CCTV surveillance ya Static IP ki zaroorat hai?"
            quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
        else:
            reply = "Understood! I have selected High-Speed Symmetrical Fiber for your setup to ensure consistent high-speed bandwidth with zero buffering. Would you also like to explore Cloud CCTV or Static IP?"
            quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            
        return {
            "intent": "add_need",
            "interpreted_need": "High-speed symmetrical internet connectivity",
            "target_product_ids": ["broadband_speed"],
            "target_addon_ids": [],
            "state_changes": {"selected_requirements": ["broadband_speed"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": quick
        }

    # 4. Check for CCTV / Cloud Surveillance
    is_cctv_need = any(k in text_low for k in ["cctv", "camera", "cameras", "surveillance", "security camera"])
    if is_cctv_need:
        return {
            "intent": "add_need",
            "interpreted_need": "24/7 Cloud CCTV camera security",
            "target_product_ids": ["cctv_security"],
            "target_addon_ids": ["P23"],
            "state_changes": {"selected_requirements": ["cctv_security"], "selected_addons": ["P23"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Added 24/7 Cloud CCTV Surveillance (+₹800/mo) with 2 HD cameras and 30-day cloud recording.",
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 5. Check for Static IP
    is_static_ip = any(k in text_low for k in ["static ip", "fixed ip", "public ip", "server", "nvr"])
    if is_static_ip:
        return {
            "intent": "add_need",
            "interpreted_need": "Fixed static public IP address",
            "target_product_ids": ["static_ip"],
            "target_addon_ids": ["P11"],
            "state_changes": {"selected_requirements": ["static_ip"], "selected_addons": ["P11"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Added Fixed Static IP Address (+₹300/mo) for your dedicated servers and secure remote access.",
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 6. Check for UPI / POS failover
    is_upi_need = any(k in text_low for k in ["upi", "pos failover", "payment fail", "qr code", "card swipe", "soundbox"])
    if is_upi_need:
        return {
            "intent": "add_need",
            "interpreted_need": "Instant UPI & POS failover connectivity",
            "target_product_ids": ["upi_failover"],
            "target_addon_ids": ["P09"],
            "state_changes": {"selected_requirements": ["upi_failover"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Selected Instant UPI & POS Failover to guarantee zero transaction dropouts during peak rush.",
            "quick_replies": ["High-Speed Symmetrical Fiber", "24/7 Cloud CCTV", "Generate Digital Bundle"]
        }

    # 7. Check for Confirm / Progression
    is_confirm = any(k in text_low for k in ["proceed", "move on", "continue", "next", "confirm", "generate", "start kyc", "looks good", "theek hai", "chalo", "done", "okay"])
    if is_confirm:
        next_stage = "PLAN_EXPLORATION" if stage == "REQUIREMENTS_COLLECTION" else "KYC_VERIFICATION"
        return {
            "intent": "confirm",
            "interpreted_need": f"Proceed to next stage ({next_stage})",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {"stage": next_stage},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": f"Proceeding to {next_stage.replace('_', ' ').title()}. Your selections have been saved.",
            "quick_replies": ["Continue", "Review Selections"]
        }

    # Default fallback: helpful, stage-aware, non-hijacking
    if stage == "REQUIREMENTS_COLLECTION":
        default_reply = "Could you tell me more about your setup? You can select any of the visible options on the left (High-Speed Fiber, CCTV, Static IP, UPI failover) or describe your needs here."
        default_qr = ["High-Speed Fiber", "24/7 Cloud CCTV", "Fixed Static IP", "Instant UPI Failover"]
    else:
        default_reply = "I am here to help you configure the right Airtel Business plan. You can ask about available add-ons, customize your quote, or proceed to Smart KYC."
        default_qr = ["View Available Add-ons", "Confirm Quote & KYC", "Compare Other Plans"]
        
    return {
        "intent": "ask_question",
        "interpreted_need": "General customer inquiry",
        "target_product_ids": [],
        "target_addon_ids": [],
        "state_changes": {},
        "needs_clarification": False,
        "clarification_question": None,
        "reply": default_reply,
        "quick_replies": default_qr
    }

def interpret_user_intent_with_context(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]],
    mock_fn=None,
    live_caller=None
) -> Dict[str, Any]:
    """
    Interprets customer turn using the configured LLM path (or mock), grounded dynamically in visible options and catalogue.
    Falls back gracefully to deterministic contextual fallback if LLM is unavailable or fails.
    """
    global _GLOBAL_TEST_MOCK_LLM
    active_mock = mock_fn or _GLOBAL_TEST_MOCK_LLM
    prompt = build_unified_advisor_prompt(workflow, session, user_message, language, visible_options, eligible_catalogue)
    
    # 1. If test mock is active, call mock function
    if active_mock:
        try:
            mock_res = active_mock(prompt, user_message)
            if isinstance(mock_res, dict):
                return mock_res
            if isinstance(mock_res, str):
                clean_json = mock_res.strip().replace("```json", "").replace("```", "")
                return json.loads(clean_json)
        except Exception:
            pass

    # 2. Try live LLM caller if provided or available
    if live_caller:
        try:
            raw_text, bundle_id, engine = live_caller(prompt, user_message)
            if raw_text:
                clean_json = raw_text.strip().replace("```json", "").replace("```", "")
                parsed = json.loads(clean_json)
                if isinstance(parsed, dict) and "reply" in parsed:
                    return parsed
        except Exception:
            pass

    # 3. Deterministic Contextual Fallback
    return interpret_user_intent_fallback(workflow, session, user_message, language, visible_options, eligible_catalogue)

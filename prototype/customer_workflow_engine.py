"""
Project Udyam Digital - Customer Workflow & Dual-Mode State Engine
Handles:
1. Customer Authentication (Login & Signup with DPDP 2023 Compliance)
2. Central Authoritative Workflow State across Chat and GUI
3. Bidirectional Synchronization & Intent Extraction
4. Multilingual Dictionary for Onboarding Journeys
"""

import uuid
import re
from datetime import datetime
from recommendation_engine import (
    calculate_quote_pricing,
    HERO_BUNDLES_MASTER,
    ALL_PACKAGES_MASTER,
    MODULAR_ADDONS
)

REQ_TO_PRODUCT_MAP = {
    "broadband_speed": "P01",      # High-Speed Symmetrical Fiber
    "upi_failover": "P09",         # Instant UPI & POS Failover (Backup 4G/5G)
    "cctv_security": "P23",        # 24/7 Cloud CCTV Surveillance
    "static_ip": "P11",            # Fixed Static IP Address
    "whatsapp_api": "P15",         # WhatsApp Business API Starter
    "cloud_backup": "P17",         # Cloud Backup 1 TB
    "pos_billing": "P19",          # Cloud POS & GST Billing Counter
    "sim_cards": "P07",            # Business Postpaid SIM 50GB
    "business_sim": "P07"
}

REQ_DISPLAY_NAMES = {
    "broadband_speed": "High-Speed Symmetrical Fiber",
    "upi_failover": "Instant UPI & POS Failover",
    "cctv_security": "24/7 Cloud CCTV Surveillance",
    "static_ip": "Fixed Static IP Address",
    "whatsapp_api": "WhatsApp Business API",
    "cloud_backup": "Cloud Backup 1 TB",
    "pos_billing": "Cloud POS & GST Billing Counter",
    "sim_cards": "Business Postpaid SIM",
    "business_sim": "Business Postpaid SIM"
}

# Pre-seeded Mock Customer Accounts for seamless testing and demonstration
MOCK_CUSTOMERS = {
    "9810123456": {
        "id": "CUST-DEL-101",
        "name": "Rajesh Gupta",
        "mobile": "9810123456",
        "email": "rajesh@guptakirana.in",
        "password": "Airtel@2026",
        "business_name": "Gupta Kirana & General Store",
        "business_type": "kirana",
        "city": "Delhi",
        "gstin": "19EOGXH4115Y1ZL",
        "udyam": "UDYAM-MH-00-9516696",
        "requirements": ["upi_failover", "broadband_speed"],
        "saved_quote_id": "QTE-2026-9812",
        "saved_bundle_id": "bundle_kirana",
        "saved_addons": ["P15", "P23"],
        "workflow_stage": "PLAN_EXPLORATION"
    },
    "9820011223": {
        "id": "CUST-MUM-204",
        "name": "Dr. Joseph Shah",
        "mobile": "9820011223",
        "email": "drshah@harmonydental.com",
        "password": "Airtel@2026",
        "business_name": "Harmony Dental Care",
        "business_type": "clinic",
        "city": "Mumbai",
        "gstin": "19EOGXH4115Y1ZL",
        "udyam": "UDYAM-MH-00-9516696",
        "requirements": ["cloud_backup", "broadband_speed", "static_ip"],
        "saved_quote_id": "QTE-2026-4410",
        "saved_bundle_id": "bundle_clinic",
        "saved_addons": ["P11"],
        "workflow_stage": "KYC_VERIFICATION"
    },
    "9876543210": {
        "id": "CUST-BLR-305",
        "name": "Priya Sharma",
        "mobile": "9876543210",
        "email": "priya@sharmaretail.com",
        "password": "Airtel@2026",
        "business_name": "Sharma Superstores Multi-Site",
        "business_type": "multisite",
        "city": "Bangalore",
        "gstin": "29AABCU9603R1ZM",
        "udyam": "UDYAM-KR-00-1122334",
        "requirements": ["sdwan_failover", "cctv_security", "multi_store_sync"],
        "saved_quote_id": "QTE-2026-7890",
        "saved_bundle_id": "bundle_multisite",
        "saved_addons": ["P23", "P15"],
        "workflow_stage": "INSTALLATION_TRACKING"
    }
}

# Central in-memory Workflow Sessions Store
WORKFLOW_SESSIONS = {}

# Workflow Stages
STAGES = [
    "WELCOME",
    "USER_TYPE_SELECTION",
    "CUSTOMER_ACCOUNT_CHECK",
    "CUSTOMER_LOGIN",
    "CUSTOMER_SIGNUP",
    "EMPLOYEE_DEMO_ENTRY",
    "BUSINESS_IDENTIFICATION",
    "REQUIREMENTS_COLLECTION",
    "PLAN_EXPLORATION",
    "QUOTE_REVIEW",
    "PACKAGE_CUSTOMIZATION",
    "KYC_VERIFICATION",
    "INSTALLATION_TRACKING",
    "ONBOARDING_COMPLETE"
]

# Multilingual Localized Strings for Chatbot and Guided Workspace
I18N = {
    "en": {
        "welcome": "Namaste! Welcome to Airtel Business Project Udyam Digital.\n\nAre you a business owner looking for digital solutions, or an Airtel employee assisting customers?",
        "ask_account": "Great! Welcome, Business Owner. Are you already an Airtel Business customer?",
        "login_prompt": "Welcome back! Please enter your registered mobile number and password in the secure login panel.",
        "signup_prompt": "No problem! Let's create your Airtel Business account.\n\n👈 You can fill your details in the registration panel on the left, or simply reply here with your name, mobile, and business name (e.g. 'Anshul Kaushal 9434134144 Kaushal Sweets') and I'll fill it in for you!",
        "employee_prompt": "Welcome, Airtel Team! You can explore the internal operations, KYC queue, and funnel intelligence directly in Employee Demo Mode.",
        "business_type_prompt": "Great! Let's understand your business so I can suggest the right digital solutions. What kind of business do you run?",
        "requirements_prompt": "What are the biggest challenges or digital tools you need for your operations?",
        "recommendation_prompt": "Based on your business needs, here is our recommended digital bundle tailored for maximum uptime and value.",
        "catalogue_prompt": "Here is the full catalogue of Airtel Business plans. You can compare and select the one that fits best.",
        "quote_prompt": "Review your single transparent monthly quotation. You can toggle optional compatible add-ons in 1 click.",
        "kyc_prompt": "Let's complete statutory DoT KYC verification with our Zero-Typing Smart Registry lookup.",
        "tracker_prompt": "Congratulations! Your order is active in our live milestone fulfillment engine. Here is your tracking status."
    },
    "hi": {
        "welcome": "नमस्ते! Airtel Business के Project Udyam Digital में आपका स्वागत है।\n\nक्या आप अपने व्यवसाय के लिए डिजिटल समाधान ढूँढ रहे हैं या Airtel के कर्मचारी हैं जो ग्राहकों की सहायता कर रहे हैं?",
        "ask_account": "बहुत बढ़िया! क्या आपका पहले से Airtel Business में अकाउंट है?",
        "login_prompt": "स्वागत है! कृपया सुरक्षित लॉगिन पैनल में अपना पंजीकृत मोबाइल नंबर और पासवर्ड दर्ज करें।",
        "signup_prompt": "कोई बात नहीं! आइए आपका नया Airtel Business खाता बनाएं।\n\n👈 आप बाईं ओर दिए गए रजिस्ट्रेशन पैनल में अपना विवरण भर सकते हैं, अथवा मुझे चैट में लिख सकते हैं (जैसे: 'Anshul Kaushal 9434134144 Kaushal Sweets') और मैं अपने आप भर दूँगा!",
        "employee_prompt": "नमस्ते Airtel टीम! आप डेमो मोड में हमारे ऑपरेशन्स, KYC क्यू और एनालिटिक्स कंसोल को देख सकते हैं।",
        "business_type_prompt": "आइए आपके व्यवसाय को समझें ताकि हम सही डिजिटल समाधान सुझा सकें। आप किस प्रकार का व्यवसाय चलाते हैं?",
        "requirements_prompt": "दुकान या ऑफिस चलाने में आपको किन चुनौतियों का सामना करना पड़ता है?",
        "recommendation_prompt": "आपकी आवश्यकताओं के अनुसार, हमने आपके लिए यह विशेष Airtel डिजिटल बंडल तैयार किया है।",
        "catalogue_prompt": "यह Airtel Business के सभी उपलब्ध प्लान्स की सूची है। आप किसी भी प्लान को चुन सकते हैं।",
        "quote_prompt": "यह आपका पारदर्शी बिल है। आप 1-क्लिक में ज़रूरत अनुसार एड-ऑन्स जोड़ सकते हैं।",
        "kyc_prompt": "आइए DoT नियमों के तहत त्वरित स्मार्ट KYC सत्यापन पूरा करें।",
        "tracker_prompt": "बधाई हो! आपका ऑर्डर प्रोसेस हो रहा है। यहाँ आपकी लाइव डिलीवरी स्थिति है।"
    },
    "hinglish": {
        "welcome": "Namaste! Airtel Business Project Udyam Digital mein aapka swagat hai.\n\nKya aap ek business owner hain ya Airtel employee hain jo customers ko assist kar rahe hain?",
        "ask_account": "Awesome! Kya aapka already Airtel Business ke saath account hai?",
        "login_prompt": "Welcome back! Login panel mein apna registered mobile number aur password enter karein.",
        "signup_prompt": "Koi baat nahi! Chaliye aapka new Airtel Business account create karte hain.\n\n👈 Aap left side registration panel fill kar sakte hain, ya yahin chat mein type karein (jaise: 'Anshul Kaushal 9434134144 Kaushal Sweets') aur main automatically details fill kar dunga!",
        "employee_prompt": "Welcome Airtel Team! Aap demo mode mein internal operations and KYC queue access kar sakte hain.",
        "business_type_prompt": "Chaliye aapke business ko samajhte hain. Aap kis category ka business run karte hain?",
        "requirements_prompt": "Aapke business mein internet ya digital payments mein kya challenges aate hain?",
        "recommendation_prompt": "Aapke requirements ke basis par ye best value digital bundle recommend kiya gaya hai.",
        "catalogue_prompt": "Aap yahan se Airtel Business ke sabhi plans explore kar sakte hain.",
        "quote_prompt": "Yeh aapka transparent monthly quotation hai with zero hidden fees.",
        "kyc_prompt": "Chaliye instant registry lookup ke saath Smart KYC verify karte hain.",
        "tracker_prompt": "Badhaai ho! Aapka order successfully place ho gaya hai. Track your live installation here."
    },
    "pa": {
        "welcome": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! Airtel Business Project Udyam Digital ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ।\n\nਕੀ ਤੁਸੀਂ ਇੱਕ ਕਾਰੋਬਾਰੀ ਮਾਲਕ ਹੋ ਜਾਂ Airtel ਦੇ ਕਰਮਚਾਰੀ ਹੋ?",
        "ask_account": "ਵਧੀਆ! ਕੀ ਤੁਹਾਡੇ ਕੋਲ ਪਹਿਲਾਂ ਹੀ Airtel Business ਖਾਤਾ ਹੈ?",
        "login_prompt": "ਸੁਆਗਤ ਹੈ! ਕਿਰਪਾ ਕਰਕੇ ਲੌਗਇਨ ਪੈਨਲ ਵਿੱਚ ਆਪਣਾ ਮੋਬਾਈਲ ਨੰਬਰ ਅਤੇ ਪਾਸਵਰਡ ਦਰਜ ਕਰੋ।",
        "signup_prompt": "ਕੋਈ ਗੱਲ ਨਹੀਂ! ਆਓ ਤੁਹਾਡਾ ਨਵਾਂ Airtel Business ਖਾਤਾ ਬਣਾਈਏ।\n\n👈 ਤੁਸੀਂ ਖੱਬੇ ਪਾਸੇ ਦਿੱਤੇ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਪੈਨਲ ਵਿੱਚ ਆਪਣੇ ਵੇਰਵੇ ਭਰ ਸਕਦੇ ਹੋ, ਜਾਂ ਸਿੱਧਾ ਚੈਟ ਵਿੱਚ ਲਿਖ ਸਕਦੇ ਹੋ (ਜਿਵੇਂ: 'Anshul Kaushal 9434134144 Kaushal Sweets') ਅਤੇ ਮੈਂ ਆਪਣੇ ਆਪ ਭਰ ਦੇਵਾਂਗਾ!",
        "employee_prompt": "Airtel ਟੀਮ ਦਾ ਸੁਆਗਤ ਹੈ! ਡੈਮੋ ਮੋਡ ਵਿੱਚ ਕਰਮਚਾਰੀ ਕੰਸੋਲ ਖੋਲ੍ਹੋ।",
        "business_type_prompt": "ਆਓ ਤੁਹਾਡੇ ਕਾਰੋਬਾਰ ਨੂੰ ਸਮਝੀਏ। ਤੁਸੀਂ ਕਿਸ ਤਰ੍ਹਾਂ ਦਾ ਕਾਰੋਬਾਰ ਚਲਾਉਂਦੇ ਹੋ?",
        "requirements_prompt": "ਤੁਹਾਡੇ ਕਾਰੋਬਾਰ ਵਿੱਚ ਕਿਹੜੀਆਂ ਚੁਣੌਤੀਆਂ ਹਨ?",
        "recommendation_prompt": "ਤੁਹਾਡੀਆਂ ਲੋੜਾਂ ਅਨੁਸਾਰ, ਇਹ ਢੁਕਵਾਂ Airtel ਡਿਜੀਟਲ ਪੈਕੇਜ ਹੈ।",
        "catalogue_prompt": "ਇਹ ਸਾਰੇ ਉਪਲਬਧ Airtel Business ਪਲਾਨ ਹਨ।",
        "quote_prompt": "ਆਪਣਾ ਪਾਰਦਰਸ਼ੀ ਮਹੀਨਾਵਾਰ ਬਿੱਲ ਦੇਖੋ।",
        "kyc_prompt": "ਆਓ DoT ਨਿਯਮਾਂ ਅਨੁਸਾਰ ਤੁਰੰਤ KYC ਪੂਰਾ ਕਰੀਏ।",
        "tracker_prompt": "ਵਧਾਈਆਂ! ਤੁਹਾਡਾ ਆਰਡਰ ਲਾਈਵ ਟਰੈਕਿੰਗ ਵਿੱਚ ਹੈ।"
    }
}

def get_i18n_text(key, lang="en"):
    """Fetch localized string with English fallback."""
    l = lang if lang in I18N else "en"
    return I18N[l].get(key, I18N["en"].get(key, ""))

def get_or_create_workflow(session_id=None, language="en"):
    """
    Retrieves or initializes a synchronized workflow state.
    """
    sid = (session_id or "").strip() or f"sess_{uuid.uuid4().hex[:12]}"
    
    if sid not in WORKFLOW_SESSIONS:
        WORKFLOW_SESSIONS[sid] = {
            "session_id": sid,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "stage": "USER_TYPE_SELECTION",
            "interaction_mode": "balanced", # "balanced" | "chat_first" | "gui_first"
            "language": language if language in I18N else "en",
            "user_type": None,              # "customer" | "employee"
            "account_status": None,         # "existing" | "new"
            "customer": {
                "authenticated": False,
                "id": None,
                "name": "",
                "mobile": "",
                "email": "",
                "business_name": "",
                "business_type": "kirana",  # kirana, clinic, multisite, manufacturer
                "city": "Delhi",
                "dpdp_consented": False,
                "dpdp_token": None
            },
            "discovery": {
                "business_type": "kirana",
                "requirements": [],
                "staff_count": "2-4",
                "notes": ""
            },
            "recommendation": {
                "bundle_id": "bundle_kirana",
                "bundle_name": "Kirana Digital Starter",
                "monthly_base": 1999,
                "monthly_subtotal": 1999,
                "gst_18": 360,
                "total_monthly": 2359,
                "setup_fee": 1000,
                "contract_months": 12,
                "match_score": 96,
                "why_narrative": "Engineered for high UPI transaction volume with zero dropouts and 4G/5G POS failover.",
                "active_addons": []
            },
            "kyc": {
                "gstin": "",
                "udyam": "",
                "applicant_id": None,
                "status": "PENDING",
                "verified": False,
                "signatory_name": "",
                "documents": []
            },
            "order": {
                "order_id": "ORD-2026-9812",
                "placed_at": "15-Jul-2026",
                "milestone": 4, # 1 to 5
                "milestone_text": "Step 4: Hardware Dispatched & Field Engineer Assigned",
                "sla_days": "3.5 Days",
                "engineer_name": "Rahul Sharma",
                "engineer_phone": "+91 98101 23456"
            },
            "messages": [
                {
                    "sender": "bot",
                    "text": get_i18n_text("welcome", language),
                    "quick_replies": [
                        {"label": "👤 I am a Business Owner", "action": "SELECT_USER_TYPE", "value": "customer"},
                        {"label": "👔 I am an Airtel Employee", "action": "SELECT_USER_TYPE", "value": "employee"}
                    ]
                }
            ],
            "stage_history": []
        }
    
    return WORKFLOW_SESSIONS[sid]

def authenticate_customer(identifier, password, session_id=None):
    """
    Secure backend authentication for existing customer.
    Does NOT log password or pass to LLM.
    """
    clean_id = (identifier or "").strip().lower()
    clean_pwd = (password or "").strip()
    
    matched_cust = None
    for mob, cdata in MOCK_CUSTOMERS.items():
        if mob == clean_id or cdata["email"].lower() == clean_id:
            if cdata["password"] == clean_pwd:
                matched_cust = cdata
                break
                
    # Also support demo instant bypass if password is demo password
    if not matched_cust and (clean_pwd == "Airtel@2026" or clean_pwd == "demo" or clean_pwd == "123456"):
        # Auto-create lightweight demo customer
        matched_cust = {
            "id": f"CUST-{uuid.uuid4().hex[:6].upper()}",
            "name": "Valued Business Owner",
            "mobile": clean_id if clean_id.isdigit() else "9810123456",
            "email": clean_id if "@" in clean_id else "merchant@airtel.in",
            "business_name": "Airtel Business Merchant",
            "business_type": "kirana",
            "city": "Delhi",
            "gstin": "19EOGXH4115Y1ZL",
            "udyam": "UDYAM-MH-00-9516696",
            "requirements": ["broadband_speed", "upi_failover"],
            "saved_quote_id": "QTE-2026-9812",
            "saved_bundle_id": "bundle_kirana",
            "saved_addons": ["P15"],
            "workflow_stage": "BUSINESS_IDENTIFICATION"
        }
        
    if not matched_cust:
        return {"status": "error", "message": "Invalid mobile/email or password. For demo, use '9810123456' / 'Airtel@2026'."}

    # Update workflow session
    wf = get_or_create_workflow(session_id)
    wf["customer"]["authenticated"] = True
    wf["customer"]["id"] = matched_cust["id"]
    wf["customer"]["name"] = matched_cust["name"]
    wf["customer"]["mobile"] = matched_cust["mobile"]
    wf["customer"]["email"] = matched_cust["email"]
    wf["customer"]["business_name"] = matched_cust["business_name"]
    wf["customer"]["business_type"] = matched_cust.get("business_type", "kirana")
    wf["customer"]["city"] = matched_cust.get("city", "Delhi")
    
    wf["discovery"]["business_type"] = matched_cust.get("business_type", "kirana")
    wf["discovery"]["requirements"] = matched_cust.get("requirements", ["broadband_speed"])
    
    # Restore saved quote & bundle
    b_id = matched_cust.get("saved_bundle_id", "bundle_kirana")
    wf["recommendation"]["bundle_id"] = b_id
    wf["recommendation"]["active_addons"] = matched_cust.get("saved_addons", [])
    
    # Transition stage
    wf["stage"] = matched_cust.get("workflow_stage", "BUSINESS_IDENTIFICATION")
    wf["user_type"] = "customer"
    wf["account_status"] = "existing"
    
    # Append confirmation message to chat
    lang = wf["language"]
    welcome_back_msg = f"Welcome back, {matched_cust['name']} ({matched_cust['business_name']})! Your account and previous preferences have been securely restored."
    wf["messages"].append({
        "sender": "bot",
        "text": welcome_back_msg,
        "quick_replies": [
            {"label": "Explore Recommended Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
            {"label": "Adjust Business Needs", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"},
            {"label": "Verify Smart KYC", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
        ]
    })
    
    return {
        "status": "success",
        "message": "Authenticated successfully",
        "customer": wf["customer"],
        "workflow": wf
    }

def register_customer(data, session_id=None):
    """
    Registers a new MSME customer account with statutory DPDP 2023 consent logging.
    """
    owner_name = (data.get("name") or data.get("owner_name") or "").strip()
    mobile = (data.get("mobile") or "").strip()
    email = (data.get("email") or "").strip()
    business_name = (data.get("business_name") or "").strip()
    business_type = (data.get("business_type") or "kirana").strip()
    dpdp_consent = bool(data.get("dpdp_consent", True))
    
    if not owner_name or not mobile:
        return {"status": "error", "message": "Owner name and mobile number are mandatory."}
        
    wf = get_or_create_workflow(session_id)
    cust_id = f"CUST-{uuid.uuid4().hex[:6].upper()}"
    
    wf["customer"] = {
        "authenticated": True,
        "id": cust_id,
        "name": owner_name,
        "mobile": mobile,
        "email": email or f"{mobile}@msme.airtel.in",
        "business_name": business_name or f"{owner_name} Enterprises",
        "business_type": business_type,
        "city": data.get("city", "Delhi"),
        "dpdp_consented": dpdp_consent,
        "dpdp_token": f"DPDP-SHA256-{uuid.uuid4().hex[:12].upper()}"
    }
    
    wf["user_type"] = "customer"
    wf["account_status"] = "new"
    wf["discovery"]["business_type"] = business_type
    wf["stage"] = "BUSINESS_IDENTIFICATION"
    
    # Store in memory customer registry (preserve seeded demo accounts)
    if mobile not in ["9810123456", "9820011223"]:
        MOCK_CUSTOMERS[mobile] = {
            **wf["customer"],
            "password": data.get("password", "Airtel@2026")
        }
    
    # Add chatbot welcome
    msg = f"Account created successfully for {owner_name}! DPDP Act 2023 consent logged under token {wf['customer']['dpdp_token']}.\n\nLet's configure the right digital package for {wf['customer']['business_name']}."
    wf["messages"].append({
        "sender": "bot",
        "text": msg,
        "quick_replies": [
            {"label": "🏪 Kirana & Retail", "action": "SELECT_CATEGORY", "value": "kirana"},
            {"label": "🏥 Clinic & Healthcare", "action": "SELECT_CATEGORY", "value": "clinic"},
            {"label": "🏬 Multi-Site Stores", "action": "SELECT_CATEGORY", "value": "multisite"},
            {"label": "🏭 Small Factory", "action": "SELECT_CATEGORY", "value": "manufacturer"}
        ]
    })
    
    return {
        "status": "success",
        "message": "Account created successfully",
        "customer": wf["customer"],
        "workflow": wf
    }

def transition_workflow(session_id, action, payload=None):
    """
    Central Authoritative State Transition Handler.
    Handles events from both GUI clicks and Chat natural language extractions.
    """
    wf = get_or_create_workflow(session_id)
    payload = payload or {}
    lang = wf.get("language", "en")
    old_stage = wf.get("stage", "USER_TYPE_SELECTION")
    
    if action == "SELECT_USER_TYPE":
        utype = payload.get("user_type", "customer")
        wf["user_type"] = utype
        if utype == "customer":
            wf.setdefault("stage_history", []).append(old_stage)
            wf["stage"] = "CUSTOMER_ACCOUNT_CHECK"
            wf["messages"].append({
                "sender": "bot",
                "text": get_i18n_text("ask_account", lang),
                "quick_replies": [
                    {"label": "Yes, I have an account", "action": "SELECT_ACCOUNT_STATUS", "value": "existing"},
                    {"label": "No, I am new to Airtel", "action": "SELECT_ACCOUNT_STATUS", "value": "new"}
                ]
            })
        else:
            wf["stage"] = "EMPLOYEE_DEMO_ENTRY"
            wf["messages"].append({
                "sender": "bot",
                "text": get_i18n_text("employee_prompt", lang),
                "quick_replies": [
                    {"label": "🚀 Launch Employee Control Portal", "action": "LAUNCH_EMPLOYEE_PORTAL", "value": "/control"}
                ]
            })

    elif action == "SELECT_ACCOUNT_STATUS":
        status = payload.get("status", "new")
        wf["account_status"] = status
        if status == "existing":
            wf.setdefault("stage_history", []).append(old_stage)
            wf["stage"] = "CUSTOMER_LOGIN"
            wf["messages"].append({
                "sender": "bot",
                "text": get_i18n_text("login_prompt", lang),
                "quick_replies": [
                    {"label": "Use Demo Account (Rajesh Gupta)", "action": "AUTOFILL_DEMO_LOGIN", "value": "9810123456"},
                    {"label": "Switch to New Account", "action": "SELECT_ACCOUNT_STATUS", "value": "new"}
                ]
            })
        else:
            wf.setdefault("stage_history", []).append(old_stage)
            wf["stage"] = "CUSTOMER_SIGNUP"
            wf["messages"].append({
                "sender": "bot",
                "text": get_i18n_text("signup_prompt", lang),
                "quick_replies": [
                    {"label": "Already have an account? Sign In", "action": "SELECT_ACCOUNT_STATUS", "value": "existing"}
                ]
            })

    elif action == "AUTOFILL_DEMO_LOGIN":
        auth_res = authenticate_customer("9810123456", "Airtel@2026", session_id)
        return auth_res.get("workflow", wf)

    elif action == "VERIFY_KYC_DEMO":
        wf["kyc"]["status"] = "VERIFIED"
        wf["kyc"]["verified"] = True
        wf["kyc"]["gstin"] = payload.get("gstin", "07AAAAA0000A1Z5")
        wf["stage"] = "INSTALLATION_TRACKING"
        wf["messages"].append({
            "sender": "bot",
            "text": "Smart KYC specimen demo verification PASSED! Specimen test cleared under simulated benchmark.",
            "quick_replies": [
                {"label": "Track Order Progress", "action": "GO_TO_STAGE", "value": "INSTALLATION_TRACKING"}
            ]
        })

    elif action == "SUBMIT_KYC":
        is_appr = payload.get("is_approved") or payload.get("status") in ["APPROVED", "VERIFIED"]
        if is_appr:
            wf["kyc"]["status"] = "VERIFIED"
            wf["kyc"]["verified"] = True
            if payload.get("gstin"):
                wf["kyc"]["gstin"] = payload.get("gstin")
            wf["stage"] = "INSTALLATION_TRACKING"
            wf["messages"].append({
                "sender": "bot",
                "text": "Smart KYC statutory verification PASSED! Field engineer Rahul Sharma is assigned to fulfill your order.",
                "quick_replies": [
                    {"label": "Track Order Progress", "action": "GO_TO_STAGE", "value": "INSTALLATION_TRACKING"}
                ]
            })
        else:
            wf["kyc"]["status"] = payload.get("status", "REVIEW_REQUIRED")
            wf["kyc"]["verified"] = False
            wf["messages"].append({
                "sender": "bot",
                "text": "KYC document submitted but requires review or re-upload. Cannot proceed to installation tracking yet.",
                "quick_replies": [
                    {"label": "📄 Review KYC Documents", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
                ]
            })

    elif action == "UPDATE_DISCOVERY":
        for k in ["employees", "cameras", "devices", "locations"]:
            if k in payload:
                try:
                    wf["discovery"][k] = int(payload[k])
                except (ValueError, TypeError):
                    pass
        _recalculate_workflow_quote(wf)

    elif action == "SELECT_CATEGORY":
        cat = payload.get("category", "kirana").lower()
        cat_map = {
            "kirana": ("bundle_kirana", "Kirana Digital Starter", 1999),
            "clinic": ("bundle_clinic", "Clinic & Professional Office Suite", 3499),
            "multisite": ("bundle_multisite", "Multi-Site Retail Pro", 7999),
            "manufacturer": ("bundle_manufacturer", "Small Manufacturing Suite", 14999)
        }
        bundle_id, bundle_name, base_price = cat_map.get(cat, ("bundle_kirana", "Kirana Digital Starter", 1999))
        
        wf["discovery"]["business_type"] = cat
        wf["recommendation"]["bundle_id"] = bundle_id
        wf["recommendation"]["bundle_name"] = bundle_name
        wf["recommendation"]["monthly_base"] = base_price
        _recalculate_workflow_quote(wf)
        if old_stage != "REQUIREMENTS_COLLECTION":
            wf.setdefault("stage_history", []).append(old_stage)
        wf["stage"] = "REQUIREMENTS_COLLECTION"
        wf["messages"].append({
            "sender": "bot",
            "text": f"Selected {bundle_name}. What challenges or digital requirements does your setup have?",
            "quick_replies": [
                {"label": "⚡ Instant UPI & POS Failover", "action": "TOGGLE_REQUIREMENT", "value": "upi_failover"},
                {"label": "🌐 Symmetrical High-Speed Fiber", "action": "TOGGLE_REQUIREMENT", "value": "broadband_speed"},
                {"label": "📹 24/7 Cloud CCTV", "action": "TOGGLE_REQUIREMENT", "value": "cctv_security"},
                {"label": "🔒 Fixed Static IP Address", "action": "TOGGLE_REQUIREMENT", "value": "static_ip"},
                {"label": "Done! Show Recommendation", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"}
            ]
        })

    elif action == "ADD_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            if req not in reqs:
                reqs.append(req)
                pid = REQ_TO_PRODUCT_MAP.get(req)
                bundle_id = wf["recommendation"].get("bundle_id") or "bundle_kirana"
                bundle = ALL_PACKAGES_MASTER.get(bundle_id) or HERO_BUNDLES_MASTER.get(bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])
                bundle_included_pids = {p["id"] for p in bundle.get("products", [])}
                if pid and pid not in bundle_included_pids and pid not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(pid)
                _recalculate_workflow_quote(wf)
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Added requirement: {display_name}.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })
            else:
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Requirement {display_name} is already selected in your configuration.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })

    elif action == "REMOVE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            if req in reqs:
                reqs.remove(req)
                pid = REQ_TO_PRODUCT_MAP.get(req)
                if pid and pid in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].remove(pid)
                _recalculate_workflow_quote(wf)
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Removed requirement: {display_name}.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })
            else:
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Requirement {display_name} was not in your selected list.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })

    elif action == "TOGGLE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            if req in reqs:
                reqs.remove(req)
                pid = REQ_TO_PRODUCT_MAP.get(req)
                if pid and pid in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].remove(pid)
                ack = f"Removed requirement: {display_name}."
            else:
                reqs.append(req)
                pid = REQ_TO_PRODUCT_MAP.get(req)
                bundle_id = wf["recommendation"].get("bundle_id") or "bundle_kirana"
                bundle = ALL_PACKAGES_MASTER.get(bundle_id) or HERO_BUNDLES_MASTER.get(bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])
                bundle_included_pids = {p["id"] for p in bundle.get("products", [])}
                if pid and pid not in bundle_included_pids and pid not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(pid)
                ack = f"Added requirement: {display_name}."
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": ack,
                "quick_replies": [
                    {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })

    elif action == "SELECT_PLAN":
        b_id = payload.get("bundle_id", "bundle_kirana")
        cat_map = {
            "bundle_kirana": ("Kirana Digital Starter", 1999, "kirana"),
            "bundle_clinic": ("Clinic & Professional Office Suite", 3499, "clinic"),
            "bundle_multisite": ("Multi-Site Retail Pro", 7999, "multisite"),
            "bundle_manufacturer": ("Small Manufacturing Suite", 14999, "manufacturer")
        }
        b_name, b_price, b_cat = cat_map.get(b_id, ("Kirana Digital Starter", 1999, "kirana"))
        wf["discovery"]["business_type"] = b_cat
        wf["recommendation"]["bundle_id"] = b_id
        wf["recommendation"]["bundle_name"] = b_name
        wf["recommendation"]["monthly_base"] = b_price
        _recalculate_workflow_quote(wf)
        if old_stage != "PLAN_EXPLORATION":
            wf.setdefault("stage_history", []).append(old_stage)
        wf["stage"] = "PLAN_EXPLORATION"
        wf["messages"].append({
            "sender": "bot",
            "text": f"Updated active plan to {b_name} (₹{b_price}/mo). You can review itemized billing or customize modular add-ons.",
            "quick_replies": [
                {"label": "Customize Add-ons", "action": "GO_TO_STAGE", "value": "PACKAGE_CUSTOMIZATION"},
                {"label": "Confirm Quote & Verify KYC", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
            ]
        })

    elif action == "TOGGLE_ADDON":
        addon_id = payload.get("addon_id")
        addons = wf["recommendation"]["active_addons"]
        if addon_id:
            if addon_id in addons:
                addons.remove(addon_id)
                ack = f"Removed add-on {addon_id} from your quotation."
            else:
                addons.append(addon_id)
                ack = f"Added add-on {addon_id} to your quotation."
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": f"{ack} Total monthly bill is now ₹{wf['recommendation']['total_monthly']}/mo.",
                "quick_replies": [
                    {"label": "Confirm & Start Smart KYC", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"},
                    {"label": "Review Itemized Bill", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"}
                ]
            })

    elif action == "GO_TO_STAGE":
        new_stage = payload.get("stage") or payload.get("value")
        if new_stage in ["INSTALLATION_TRACKING", "ONBOARDING_COMPLETE"]:
            kyc_status = wf.get("kyc", {}).get("status", "PENDING")
            is_approved = wf.get("kyc", {}).get("is_approved", False) or (kyc_status in ["APPROVED", "VERIFIED"])
            unapproved_statuses = [
                "PENDING", "NOT_SUBMITTED", "SUBMITTED", "MANUAL_REVIEW_REQUESTED",
                "MANUAL_REVIEW_IN_PROGRESS", "MORE_INFO_REQUESTED", "RESUBMISSION_REQUIRED",
                "REJECTED", "AUTOMATED_VERIFICATION_FAILED", "REVIEW_REQUIRED"
            ]
            if not is_approved or kyc_status in unapproved_statuses:
                wf["messages"].append({
                    "sender": "bot",
                    "text": "Cannot proceed to installation tracking. Statutory KYC verification has not been approved yet. Please complete document verification first.",
                    "quick_replies": [
                        {"label": "Review KYC Documents", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
                    ]
                })
                return wf
        if new_stage in STAGES:
            if old_stage != new_stage:
                sh = wf.setdefault("stage_history", [])
                if not sh or sh[-1] != old_stage:
                    sh.append(old_stage)
            wf["stage"] = new_stage

            if new_stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
                _recalculate_workflow_quote(wf)

            prompt_key = {
                "USER_TYPE_SELECTION": "welcome",
                "CUSTOMER_ACCOUNT_CHECK": "ask_account",
                "CUSTOMER_LOGIN": "login_prompt",
                "CUSTOMER_SIGNUP": "signup_prompt",
                "EMPLOYEE_DEMO_ENTRY": "employee_prompt",
                "BUSINESS_IDENTIFICATION": "business_type_prompt",
                "REQUIREMENTS_COLLECTION": "requirements_prompt",
                "PLAN_EXPLORATION": "recommendation_prompt",
                "QUOTE_REVIEW": "quote_prompt",
                "PACKAGE_CUSTOMIZATION": "quote_prompt",
                "KYC_VERIFICATION": "kyc_prompt",
                "INSTALLATION_TRACKING": "tracker_prompt"
            }.get(new_stage)
            
            qr = []
            if new_stage == "KYC_VERIFICATION":
                qr = [
                    {"label": "Instant Verify Specimen GSTIN", "action": "VERIFY_KYC_DEMO", "value": "07AAAAA0000A1Z5"},
                    {"label": "Review Quotation", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"}
                ]
            elif new_stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
                qr = [
                    {"label": "Confirm Quote & Start KYC", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"},
                    {"label": "Customize Add-ons", "action": "GO_TO_STAGE", "value": "PACKAGE_CUSTOMIZATION"}
                ]

            if prompt_key:
                msg_payload = {"sender": "bot", "text": get_i18n_text(prompt_key, lang)}
                if qr:
                    msg_payload["quick_replies"] = qr
                wf["messages"].append(msg_payload)

    elif action in ["PREVIOUS_STAGE", "GO_BACK"]:
        history = wf.setdefault("stage_history", [])
        prev_stage = None
        while history:
            cand = history.pop()
            if cand != old_stage and cand in STAGES:
                prev_stage = cand
                break
        
        if not prev_stage:
            prev_map = {
                "EMPLOYEE_DEMO_ENTRY": "USER_TYPE_SELECTION",
                "CUSTOMER_ACCOUNT_CHECK": "USER_TYPE_SELECTION",
                "CUSTOMER_LOGIN": "CUSTOMER_ACCOUNT_CHECK",
                "CUSTOMER_SIGNUP": "CUSTOMER_ACCOUNT_CHECK",
                "BUSINESS_IDENTIFICATION": "CUSTOMER_ACCOUNT_CHECK",
                "REQUIREMENTS_COLLECTION": "BUSINESS_IDENTIFICATION",
                "PLAN_EXPLORATION": "REQUIREMENTS_COLLECTION",
                "QUOTE_REVIEW": "REQUIREMENTS_COLLECTION",
                "PACKAGE_CUSTOMIZATION": "PLAN_EXPLORATION",
                "KYC_VERIFICATION": "PLAN_EXPLORATION",
                "INSTALLATION_TRACKING": "KYC_VERIFICATION",
                "ONBOARDING_COMPLETE": "INSTALLATION_TRACKING"
            }
            prev_stage = prev_map.get(old_stage, "USER_TYPE_SELECTION")

        wf["stage"] = prev_stage
        if prev_stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
            _recalculate_workflow_quote(wf)

        prompt_key = {
            "USER_TYPE_SELECTION": "welcome",
            "CUSTOMER_ACCOUNT_CHECK": "ask_account",
            "CUSTOMER_LOGIN": "login_prompt",
            "CUSTOMER_SIGNUP": "signup_prompt",
            "EMPLOYEE_DEMO_ENTRY": "employee_prompt",
            "BUSINESS_IDENTIFICATION": "business_type_prompt",
            "REQUIREMENTS_COLLECTION": "requirements_prompt",
            "PLAN_EXPLORATION": "recommendation_prompt",
            "QUOTE_REVIEW": "quote_prompt",
            "PACKAGE_CUSTOMIZATION": "quote_prompt",
            "KYC_VERIFICATION": "kyc_prompt",
            "INSTALLATION_TRACKING": "tracker_prompt"
        }.get(prev_stage)

        qr = []
        if prev_stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
            qr = [
                {"label": "Confirm Quote & Start KYC", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"},
                {"label": "Customize Add-ons", "action": "GO_TO_STAGE", "value": "PACKAGE_CUSTOMIZATION"}
            ]
        elif prev_stage == "REQUIREMENTS_COLLECTION":
            qr = [
                {"label": "Instant UPI & POS Failover", "action": "TOGGLE_REQUIREMENT", "value": "upi_failover"},
                {"label": "Symmetrical High-Speed Fiber", "action": "TOGGLE_REQUIREMENT", "value": "broadband_speed"},
                {"label": "24/7 Cloud CCTV", "action": "TOGGLE_REQUIREMENT", "value": "cctv_security"},
                {"label": "Fixed Static IP Address", "action": "TOGGLE_REQUIREMENT", "value": "static_ip"},
                {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"}
            ]

        msg = f"Navigated back to {prev_stage.replace('_', ' ').title()}."
        if prompt_key:
            msg += f" {get_i18n_text(prompt_key, lang)}"
        wf["messages"].append({
            "sender": "bot",
            "text": msg,
            "quick_replies": qr
        })

    elif action == "SET_LANGUAGE":
        lang = payload.get("language", "en")
        wf["language"] = lang

    # Record previous stage into stage history stack if we moved forward to a different stage
    if wf.get("stage") != old_stage and action not in ["PREVIOUS_STAGE", "GO_BACK"]:
        history = wf.setdefault("stage_history", [])
        if not history or history[-1] != old_stage:
            history.append(old_stage)

    wf["updated_at"] = datetime.now().isoformat()
    return wf

def _recalculate_workflow_quote(wf):
    """Authoritative recalculation of quotation, itemized line items, GST, and setup fees."""
    rec = wf.setdefault("recommendation", {})
    bundle_id = rec.get("bundle_id") or "bundle_kirana"
    bundle = ALL_PACKAGES_MASTER.get(bundle_id) or HERO_BUNDLES_MASTER.get(bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])
    bundle_included_pids = {p["id"] for p in bundle.get("products", [])}

    reqs = wf.get("discovery", {}).get("requirements", [])
    active_addons = list(rec.get("active_addons", []))

    # Synchronize requirements with active addons
    for req in reqs:
        pid = REQ_TO_PRODUCT_MAP.get(req)
        if pid:
            # If not in base bundle and not already in active addons, add it
            if pid not in bundle_included_pids and pid not in active_addons:
                active_addons.append(pid)

    rec["active_addons"] = active_addons

    pricing_data = calculate_quote_pricing(bundle_id, active_addons)
    p = pricing_data["pricing"]

    rec["bundle_id"] = bundle["id"]
    rec["bundle_name"] = bundle["name"]
    rec["monthly_base"] = p["monthly_base_inr"]
    rec["setup_fee"] = p["one_time_setup_inr"]
    rec["contract_months"] = pricing_data.get("contract_months", 12)
    rec["monthly_subtotal"] = p["monthly_subtotal_inr"]
    rec["gst_rate"] = 0.18
    rec["gst_18"] = p["gst_18_inr"]
    rec["total_monthly"] = p["final_monthly_payable_inr"]
    rec["first_payment_total"] = p["first_payment_inr"]
    rec["selected_addons"] = pricing_data.get("selected_addons", [])
    rec["line_items"] = pricing_data.get("line_items", [])
    rec["included_products"] = pricing_data.get("included_products", [])


def get_visible_gui_options(workflow):
    """
    Returns the exact ordered list of options currently displayed on the customer GUI.
    Each item contains stable 1-based index, stable id, display name, type, description, and selected state.
    """
    stage = workflow.get("stage", "USER_TYPE_SELECTION")
    
    if stage == "REQUIREMENTS_COLLECTION":
        reqs = workflow.get("discovery", {}).get("requirements", [])
        return [
            {
                "index": 1,
                "id": "upi_failover",
                "name": "Instant UPI & POS Failover",
                "type": "requirement",
                "description": "Guaranteed backup SIM so customer payments never drop during evening rush.",
                "selected": "upi_failover" in reqs,
                "linked_addon_id": "P09"
            },
            {
                "index": 2,
                "id": "broadband_speed",
                "name": "High-Speed Symmetrical Fiber",
                "type": "requirement",
                "description": "Consistent upload and download bandwidth with zero buffering.",
                "selected": "broadband_speed" in reqs,
                "linked_product_id": "P01"
            },
            {
                "index": 3,
                "id": "cctv_security",
                "name": "24/7 Cloud CCTV Surveillance",
                "type": "requirement",
                "description": "Remote store monitoring with 30-day encrypted cloud recording.",
                "selected": "cctv_security" in reqs,
                "linked_addon_id": "P23",
                "price_inr": 800
            },
            {
                "index": 4,
                "id": "static_ip",
                "name": "Fixed Static IP Address",
                "type": "requirement",
                "description": "Host local servers, biometric attendance, or remote CCTV securely.",
                "selected": "static_ip" in reqs,
                "linked_addon_id": "P11",
                "price_inr": 300
            }
        ]
        
    elif stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
        rec = workflow.get("recommendation", {})
        cur_bundle = rec.get("bundle_id", "bundle_kirana")
        active_addons = rec.get("active_addons", [])
        return [
            {"index": 1, "id": "bundle_kirana", "name": "Kirana Digital Starter", "type": "base_plan", "price_inr": 1999, "selected": cur_bundle == "bundle_kirana", "description": "100 Mbps AirFiber + 4G Failover + WhatsApp API"},
            {"index": 2, "id": "bundle_clinic", "name": "Clinic & Professional Office Suite", "type": "base_plan", "price_inr": 3499, "selected": cur_bundle == "bundle_clinic", "description": "300 Mbps Fiber + 1TB Cloud Backup + Google Workspace"},
            {"index": 3, "id": "bundle_multisite", "name": "Multi-Site Retail Pro", "type": "base_plan", "price_inr": 7999, "selected": cur_bundle == "bundle_multisite", "description": "1 Gbps Fiber + SD-WAN Failover + 4x CCTV"},
            {"index": 4, "id": "bundle_manufacturer", "name": "Small Manufacturing Suite", "type": "base_plan", "price_inr": 14999, "selected": cur_bundle == "bundle_manufacturer", "description": "20 Mbps 1:1 Leased Line + Static IP + IoT Telemetry"},
            {"index": 5, "id": "P15", "name": "WhatsApp Business API", "type": "addon", "price_inr": 999, "selected": "P15" in active_addons, "description": "1,000 verified promotional/order update conversations"},
            {"index": 6, "id": "P23", "name": "Cloud CCTV 2 Cameras", "type": "addon", "price_inr": 800, "selected": "P23" in active_addons, "description": "2 HD cameras with 30-day encrypted cloud recording"},
            {"index": 7, "id": "P11", "name": "Fixed Static Public IP Address", "type": "addon", "price_inr": 300, "selected": "P11" in active_addons, "description": "Public IP for local billing servers & NVR access"},
            {"index": 8, "id": "P07", "name": "Business Postpaid SIM (50GB)", "type": "addon", "price_inr": 299, "selected": "P07" in active_addons, "description": "Unlimited voice calls + 50 GB CUG data"},
            {"index": 9, "id": "P17", "name": "Additional Cloud Backup (1 TB)", "type": "addon", "price_inr": 499, "selected": "P17" in active_addons, "description": "AES-256 cloud backup for accounting software & files"},
            {"index": 10, "id": "P19", "name": "Cloud POS & GST Billing Counter", "type": "addon", "price_inr": 599, "selected": "P19" in active_addons, "description": "GST-ready invoicing, barcode scanner, inventory & UPI receipts"}
        ]
        
    elif stage == "BUSINESS_IDENTIFICATION":
        cur_type = workflow.get("discovery", {}).get("business_type", "kirana")
        return [
            {"index": 1, "id": "kirana", "name": "Kirana & Retail Store", "type": "category", "selected": cur_type == "kirana", "description": "AirFiber 5G, UPI Soundbox, Billing POS failover"},
            {"index": 2, "id": "clinic", "name": "Healthcare Clinic & Office", "type": "category", "selected": cur_type == "clinic", "description": "Symmetrical Fiber 300, Cloud Records Backup & Secure Wi-Fi"},
            {"index": 3, "id": "multisite", "name": "Multi-Site Retail Chain", "type": "category", "selected": cur_type == "multisite", "description": "SD-WAN Central Controller, Static IP & Multi-Branch CCTV"},
            {"index": 4, "id": "manufacturer", "name": "Small Factory", "type": "category", "selected": cur_type == "manufacturer", "description": "Dedicated leased line, Static IP & IoT telemetry"}
        ]
        
    return []

def get_eligible_catalogue_options(workflow):
    """
    Returns verified catalogue-backed products and add-ons eligible for the customer.
    """
    return [
        {"id": "P01", "name": "Biz Fibre 100 Mbps", "category": "Connectivity", "price": "₹999/mo", "description": "High-speed symmetrical broadband with zero buffering"},
        {"id": "P02", "name": "Biz Fibre 300 Mbps", "category": "Connectivity", "price": "₹1,499/mo", "description": "Ultra-fast symmetrical fiber for multi-device operations"},
        {"id": "P04", "name": "Biz 5G AirFiber 100 Mbps", "category": "Connectivity", "price": "₹899/mo", "description": "Instant wireless plug-and-play broadband"},
        {"id": "P09", "name": "Backup 4G/5G Failover", "category": "Connectivity", "price": "₹499/mo", "description": "Automatic 4G/5G failover for POS and UPI payment terminals"},
        {"id": "P11", "name": "Fixed Static Public IP Address", "category": "Connectivity", "price": "₹300/mo", "description": "Public IP for local billing servers, remote access & NVR"},
        {"id": "P15", "name": "WhatsApp Business API", "category": "Customer Marketing", "price": "₹999/mo", "description": "1,000 verified promotional and order messaging conversations"},
        {"id": "P17", "name": "Additional Cloud Backup (1 TB)", "category": "Cloud & Storage", "price": "₹499/mo", "description": "Encrypted offsite backup for accounting data and invoices"},
        {"id": "P19", "name": "Cloud POS & GST Billing Counter", "category": "Billing Solutions", "price": "₹599/mo", "description": "GST-ready invoicing, barcode scanner, inventory sync & instant UPI receipts"},
        {"id": "P23", "name": "Cloud CCTV (2 HD Cameras)", "category": "Surveillance & Security", "price": "₹800/mo", "description": "2 HD outdoor/indoor cameras with mobile live view & 30-day cloud recording"}
    ]

def extract_signup_details(raw_text):
    """
    Extracts name, mobile number, business name, and password
    from conversational unstructured text typed by MSME business owner.
    Examples:
      - 'anshul kaushal 9434134144 kaushal sweets 2323123'
      - 'Anshul Kaushal 9434134144 Kaushal Sweets'
      - 'My name is Ramesh, mobile 9811223344, store is Ramesh General Store'
      - '9434134144 Kaushal Sweets'
    """
    text = (raw_text or "").strip()
    if not text:
        return None

    # Check for 10-digit Indian mobile number (handles +91, 0, or plain 10 digits)
    mob_match = re.search(r'(?:\+91[\s-]?)?(?:0)?([6-9]\d{9})\b', text)
    if not mob_match:
        mob_match = re.search(r'\b(\d{10})\b', text)
    
    if not mob_match:
        return None

    mobile = mob_match.group(1)
    
    name = ""
    biz_name = ""
    pwd = ""
    
    # 1. Labeled pattern extraction (e.g. name: ..., biz: ..., password: ...)
    labeled_name = re.search(r'(?:my\s+name\s+is|name\s+is|name|owner|naam|i\s+am)\s*[:=,-]?\s*([a-zA-Z\s]+?)(?:,|\.|\band\b|mobile|phone|number|biz|business|store|shop|$)', text, re.I)
    labeled_biz = re.search(r'(?:biz|business|store|shop|trade|dukaan|firm)(?:\s+name)?\s*[:=,-]?\s*(?:is)?\s*([a-zA-Z0-9\s]+?)(?:,|\.|\band\b|password|pwd|pin|$)', text, re.I)
    labeled_pwd = re.search(r'(?:pwd|password|pin|code)\s*[:=,-]?\s*(?:is)?\s*(\S+)', text, re.I)
    
    if labeled_name and labeled_name.group(1).strip():
        name = labeled_name.group(1).strip()
    if labeled_biz and labeled_biz.group(1).strip():
        biz_name = labeled_biz.group(1).strip()
    if labeled_pwd and labeled_pwd.group(1).strip():
        pwd = labeled_pwd.group(1).strip()

    # 2. Positional extraction around the mobile number
    span = mob_match.span()
    before = text[:span[0]].strip(' ,;:-')
    after = text[span[1]:].strip(' ,;:-')

    if not name and before:
        cleaned = re.sub(r'^(i am|my name is|im|name is|name:?)\s+', '', before, flags=re.I).strip(' ,;:-')
        cleaned = re.sub(r'\s*(?:mobile|phone|number|num|ph)$', '', cleaned, flags=re.I).strip(' ,;:-')
        if cleaned:
            name = cleaned.title()

    if after:
        cleaned_after = re.sub(r'^(?:is|store|shop|business|biz|dukaan)\s*(?:is|:)?\s*', '', after, flags=re.I).strip(' ,;:-')
        tokens = cleaned_after.split()
        if len(tokens) > 1 and (tokens[-1].isdigit() or (len(tokens[-1]) >= 4 and any(c.isdigit() for c in tokens[-1]))):
            if not pwd:
                pwd = tokens[-1]
            if not biz_name:
                biz_name = ' '.join(tokens[:-1]).strip(' ,;:-')
        else:
            if not biz_name and cleaned_after:
                biz_name = cleaned_after.strip(' ,;:-')

    # If mobile was first: '9434134144 Anshul Kaushal Kaushal Sweets'
    if not name and after and not biz_name:
        parts = after.split()
        if len(parts) >= 4:
            name = ' '.join(parts[:2]).title()
            biz_name = ' '.join(parts[2:]).title()
        elif len(parts) >= 2:
            name = ' '.join(parts[:2]).title()
        else:
            name = after.title()

    if not name:
        name = "Valued Business Owner"
    if not biz_name:
        biz_name = f"{name} Enterprises" if name != "Valued Business Owner" else "Airtel Business MSME"
    if not pwd:
        pwd = "Airtel@2026"

    return {
        "name": name.title().strip(),
        "mobile": mobile.strip(),
        "business_name": biz_name.title().strip(),
        "password": pwd.strip(),
        "dpdp_consent": True
    }

def parse_chat_intents(session_id, user_text):
    """
    Extracts structured intents & entities from conversational text
    and applies them directly to the synchronized workflow state.
    Provides complete bidirectional synchronization from Chat to GUI.
    """
    wf = get_or_create_workflow(session_id)
    text = user_text.lower().strip()
    stage = wf.get("stage", "USER_TYPE_SELECTION")

    # Ensure user message is persisted into server-side workflow messages
    if not wf["messages"] or wf["messages"][-1].get("text") != user_text:
        wf["messages"].append({"sender": "user", "text": user_text})

    # ====================================================
    # 0. DIRECT CHAT REGISTRATION DETAILS AUTO-FILL & SUBMIT
    # ====================================================
    # If the user types their registration information (name, mobile, store name) in chat
    if stage in ["CUSTOMER_SIGNUP", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_LOGIN", "USER_TYPE_SELECTION"]:
        signup_data = extract_signup_details(user_text)
        if signup_data and (stage == "CUSTOMER_SIGNUP" or any(w in text for w in ["new", "register", "create", "signup", "sign up", "sweets", "store", "shop", "kirana", "enterprises", "traders", "retail", "provisions", "solutions"])):
            wf["user_type"] = "customer"
            reg_res = register_customer(signup_data, session_id)
            c = reg_res.get("customer", {})
            return (
                f"✨ Auto-filled and registered for {c.get('name')} ({c.get('business_name')}) with mobile {c.get('mobile')}!\n\n"
                f"I have automatically filled your details in the registration panel on the left and logged your DPDP Act 2023 consent.\n\n"
                f"What type of business digital solutions are you exploring today (Kirana & Retail, Clinic, Multi-Store, or Small Factory)?"
            )

    # ====================================================
    # 0B. UNIVERSAL BACK / PREVIOUS STEP INTENT
    # ====================================================
    if any(phrase in text for phrase in ["go back", "previous step", "back to previous", "take me back", "pichhe jao", "piche jao", "last step", "pichhe chalo", "piche chalo", "prev step"]) or text in ["back", "piche", "pichhe", "previous"]:
        wf = transition_workflow(session_id, "PREVIOUS_STAGE")
        return "I've navigated back to the previous step. You can review your options or make changes in the panel on the left."

    # ====================================================
    # 1. USER_TYPE_SELECTION
    # ====================================================
    if stage == "USER_TYPE_SELECTION":
        if any(k in text for k in ["you decide", "what is best", "best for my", "recommend", "aap batao", "tum batao", "suggest", "which plan", "confused", "dont know", "don't know", "what should i choose"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "I recommend our Kirana Digital Starter with plug-and-play AirFiber and automatic 4G backup SIM. It is our most popular option engineered to ensure zero payment dropouts."

        if any(k in text for k in ["business", "business owner", "customer", "merchant", "dukaan", "shop", "store", "grocery", "run a", "own a business", "store owner", "businessman", "entrepreneur", "retailer", "client", "msme", "smb", "1", "option 1"]) and not any(w in text for w in ["airtel employee", "internal staff", "airtel team"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "customer"})
            return "Noted! Welcome, business owner. Are you already an Airtel Business customer?"

        if any(k in text for k in ["airtel employee", "internal staff", "airtel team", "airtel staff", "employee portal", "control portal"]) or text in ["employee", "staff", "airtel", "2", "option 2"]:
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "employee"})
            return "Welcome Airtel Team! You can access the Operations Control Portal directly in Demo Mode."

    # ====================================================
    # 2. CUSTOMER_ACCOUNT_CHECK
    # ====================================================
    if stage == "CUSTOMER_ACCOUNT_CHECK":
        # Existing Account
        if any(k in text for k in ["yes", "haan", "1", "option 1", "existing", "already", "already have", "i have an account", "have an account", "sign in", "login", "log in", "registered", "old customer"]) or any(w in text.split() for w in ["ha", "haanji"]):
            transition_workflow(session_id, "SELECT_ACCOUNT_STATUS", {"status": "existing"})
            return "Welcome back! Please enter your registered credentials in the login panel (or click 'Use Demo Account')."

        # New Account
        if any(k in text for k in ["new", "i am new", "new here", "new to airtel", "new customer", "first time", "nayi dukaan", "no account", "dont have", "don't have", "sign up", "signup", "create account", "register", "option 2"]) or any(w in text.split() for w in ["no", "na", "nahi", "nahin", "2"]):
            transition_workflow(session_id, "SELECT_ACCOUNT_STATUS", {"status": "new"})
            return "No problem! Please fill in your basic details in the signup panel on the left, or simply reply here with your name, mobile, and business name!"

    # ====================================================
    # 3. CUSTOMER_LOGIN & SIGNUP
    # ====================================================
    if stage in ["CUSTOMER_LOGIN", "CUSTOMER_SIGNUP"]:
        if any(k in text for k in ["demo", "rajesh", "rajesh gupta", "use demo", "test account", "autofill", "9810123456", "login with demo", "log me in", "sign in with demo", "quick login", "auto login"]):
            auth_res = authenticate_customer("9810123456", "Airtel@2026", session_id)
            return "Logged in successfully as Rajesh Gupta (Gupta Kirana Store). What type of business digital solutions are you exploring?"

        if any(k in text for k in ["switch to new", "new account", "sign up", "signup", "register", "create"]):
            transition_workflow(session_id, "SELECT_ACCOUNT_STATUS", {"status": "new"})
            return "Switched to signup panel. Please fill your basic details in the left panel or reply here in chat."

        if any(k in text for k in ["already have", "switch to login", "sign in", "login"]):
            transition_workflow(session_id, "SELECT_ACCOUNT_STATUS", {"status": "existing"})
            return "Switched to login panel. Please enter your credentials or use demo login."

        # If in CUSTOMER_LOGIN and user provided a mobile number
        if stage == "CUSTOMER_LOGIN":
            mob_m = re.search(r'\b([6-9]\d{9})\b', text)
            if mob_m:
                mob = mob_m.group(1)
                auth_res = authenticate_customer(mob, "Airtel@2026", session_id)
                if auth_res.get("status") == "success":
                    c = auth_res.get("customer", {})
                    return f"Welcome back, {c.get('name')} ({c.get('business_name')})! Your account and saved preferences have been restored. What type of business digital solutions are you exploring?"

        # If in CUSTOMER_SIGNUP and user entered general text without mobile number
        if stage == "CUSTOMER_SIGNUP":
            return (
                "👈 Please enter your Name, Mobile, and Business Name in the registration panel on the left.\n\n"
                "Or simply reply here with: 'Name Mobile BusinessName' (e.g. 'Anshul Kaushal 9434134144 Kaushal Sweets') and I will automatically fill it in for you!"
            )

    # ====================================================
    # 4. BUSINESS_IDENTIFICATION
    # ====================================================
    if stage in ["BUSINESS_IDENTIFICATION", "USER_TYPE_SELECTION", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_SIGNUP", "CUSTOMER_LOGIN"]:
        if any(k in text for k in ["multisite", "multi site", "multi-store", "chain", "branches", "multiple outlets", "multiple stores", "expanded to"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "multisite"})
            return "Selected Multi-Site Retail Pro. SD-WAN failover and central CCTV are included."

        if any(k in text for k in ["clinic", "doctor", "dental", "dentist", "hospital", "pathology", "lab", "ca office", "consultant", "lawyer", "office", "swasthya"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "clinic"})
            return "Selected Clinic & Professional Office Suite. Do you require cloud records backup and high uptime Wi-Fi?"

        if any(k in text for k in ["kirana", "grocery", "general store", "provision", "dukaan", "supermarket", "retail store", "retail shop", "retail business"]) or text in ["retail", "kirana", "1", "option 1"]:
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "Selected Kirana & Retail. How many staff or devices do you have, and what challenges do you face with Wi-Fi, payments, or security?"

        if any(k in text for k in ["factory", "manufacturing", "manufacturer", "plant", "workshop", "industrial", "warehouse", "production", "udyog"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "manufacturer"})
            return "Selected Small Manufacturing Suite with leased line and IoT telemetry."

        # Numeric selections in stage BUSINESS_IDENTIFICATION
        if stage == "BUSINESS_IDENTIFICATION":
            if text in ["1", "option 1"]:
                transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
                return "Selected Kirana & Retail Store."
            if text in ["2", "option 2"]:
                transition_workflow(session_id, "SELECT_CATEGORY", {"category": "clinic"})
                return "Selected Healthcare Clinic & Professional Office Suite."
            if text in ["3", "option 3"]:
                transition_workflow(session_id, "SELECT_CATEGORY", {"category": "multisite"})
                return "Selected Multi-Site Retail Chain."
            if text in ["4", "option 4"]:
                transition_workflow(session_id, "SELECT_CATEGORY", {"category": "manufacturer"})
                return "Selected Small Factory & Manufacturing."

    # ====================================================
    # 5. REQUIREMENTS_COLLECTION & DISCOVERY ENTITIES
    # ====================================================
    # Extract staff / employee numbers
    staff_m = re.search(r'(\d+)\s*(staff|employees?|workers?|people|persons?|team)', text)
    if staff_m:
        count = int(staff_m.group(1))
        wf["discovery"]["employees"] = count
        _recalculate_workflow_quote(wf)

    # Extract camera numbers
    cam_m = re.search(r'(\d+)\s*(cctv|cameras?|security cameras?)', text)
    if cam_m:
        count = int(cam_m.group(1))
        wf["discovery"]["cameras"] = count
        if "cctv_security" not in wf["discovery"]["requirements"]:
            wf["discovery"]["requirements"].append("cctv_security")
        if "P23" not in wf["recommendation"]["active_addons"]:
            wf["recommendation"]["active_addons"].append("P23")
        _recalculate_workflow_quote(wf)

    # Extract devices / computers
    dev_m = re.search(r'(\d+)\s*(devices?|computers?|laptops?|phones?|mobiles?|terminals?|pos)', text)
    if dev_m:
        count = int(dev_m.group(1))
        wf["discovery"]["devices"] = count
        _recalculate_workflow_quote(wf)

    # Requirements toggle / add / remove
    req_updated = False
    if any(k in text for k in ["cctv", "camera", "security", "surveillance"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no cctv", "don't need", "without"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "cctv_security"})
        req_updated = True

    if any(k in text for k in ["static ip", "fixed ip", "server", "remote access"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no static", "don't need", "without"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "static_ip"})
        req_updated = True

    if any(k in text for k in ["whatsapp", "messaging", "whatsapp bot", "customer engagement"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no whatsapp", "don't need", "without"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "whatsapp_api"})
        req_updated = True

    if any(k in text for k in ["soundbox", "payment soundbox", "upi audio", "voice payment"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no soundbox", "don't need", "without"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "soundbox"})
        req_updated = True

    if any(k in text for k in ["backup", "failover", "dual sim", "4g backup", "upi", "pos", "qr payments", "both upi & pos", "qr code", "card swipe"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no backup", "don't need", "without", "cash mainly", "no upi", "no pos"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "upi_failover"})
        req_updated = True

    if req_updated and stage == "REQUIREMENTS_COLLECTION":
        return f"Updated your requirements: Staff ({wf['discovery']['employees']}), Cameras ({wf['discovery']['cameras']}). Quotation adjusted to ₹{wf['recommendation']['total_monthly']}/mo."

    # Progression from requirements to plan / recommendation
    if stage == "REQUIREMENTS_COLLECTION":
        if (any(k in text for k in ["quote", "monthly bill", "the bill", "pricing", "charges", "cost"]) or any(w in text.split() for w in ["bill", "quote"])) and not any(w in text for w in ["billing", "billing system", "billing software", "billing machine"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
            return f"Here is your single transparent bill: ₹{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."
        elif any(k in text for k in ["done", "show plan", "view plan", "proceed", "continue", "next", "plans", "recommend", "how much", "ready", "move on", "move ahead", "looks good", "all set", "all good", "fine", "theek hai", "chalo", "aage", "send", "go", "forward", "generate", "bundle"]) or any(w in text.split() for w in ["ok", "okay", "k"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "PLAN_EXPLORATION"})
            return f"Here is your recommended package: {wf['recommendation']['bundle_name']} at ₹{wf['recommendation']['total_monthly']}/mo. You can review the itemized breakdown on the GUI or proceed to KYC."

    # ====================================================
    # 6. PLAN_EXPLORATION & QUOTE_REVIEW
    # ====================================================
    if stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
        confirm_phrases = [
            "ok", "okay", "move on", "move ahead", "proceed", "continue", "next", "go ahead",
            "confirm", "book", "take this", "i want this", "buy", "order", "finalize",
            "looks good", "looks fine", "seems ok", "seems good", "all good", "all ok", "all set",
            "sounds good", "sounds great", "fine", "great", "perfect", "done", "deal", "agree",
            "start kyc", "kyc", "verify", "documents", "forward", "let's go", "lets go",
            "theek hai", "thik hai", "sahi hai", "chalo", "aage badho", "aage chalo", "aage"
        ]
        if any(k in text for k in confirm_phrases) or any(w in text.split() for w in ["ok", "k", "kk", "yes", "haan", "ha", "done", "fine"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "KYC_VERIFICATION"})
            return f"Quotation confirmed for {wf['recommendation']['bundle_name']} at ₹{wf['recommendation']['total_monthly']}/mo! Switched to Smart KYC on the left panel."

        if "kirana" in text:
            transition_workflow(session_id, "SELECT_PLAN", {"bundle_id": "bundle_kirana"})
            return "Switched active plan to Kirana Digital Starter (₹1,999/mo). Pricing updated on GUI."
        if "clinic" in text:
            transition_workflow(session_id, "SELECT_PLAN", {"bundle_id": "bundle_clinic"})
            return "Switched active plan to Clinic & Professional Office Suite (₹3,499/mo). Pricing updated on GUI."
        if "multisite" in text or "multi" in text or "chain" in text:
            transition_workflow(session_id, "SELECT_PLAN", {"bundle_id": "bundle_multisite"})
            return "Switched active plan to Multi-Site Retail Pro (₹7,999/mo). Pricing updated on GUI."
        if "factory" in text or "manufactur" in text:
            transition_workflow(session_id, "SELECT_PLAN", {"bundle_id": "bundle_manufacturer"})
            return "Switched active plan to Small Manufacturing Suite (₹14,999/mo). Pricing updated on GUI."

    # ====================================================
    # 7. KYC_VERIFICATION
    # ====================================================
    if stage == "KYC_VERIFICATION":
        if any(k in text for k in ["demo", "specimen", "07aaaaa"]):
            transition_workflow(session_id, "VERIFY_KYC_DEMO", {"gstin": "07AAAAA0000A1Z5"})
            return "Smart KYC Specimen Demo PASSED! Tested under simulated benchmark. Tracking is live on the left panel!"
        elif any(k in text for k in ["track", "status", "installation", "delivery", "order"]):
            if wf.get("kyc", {}).get("status") in ["APPROVED", "VERIFIED"]:
                transition_workflow(session_id, "GO_TO_STAGE", {"stage": "INSTALLATION_TRACKING"})
                return "Proceeding to installation tracking. Field engineer Rahul Sharma is on his way!"
            else:
                return "Cannot proceed to installation tracking yet. Please complete Smart KYC document verification first or test with specimen demo."
        else:
            return "Please upload or capture your KYC document on the left panel, and confirm DPDP statutory consent. Our Smart KYC engine will verify it in real-time."
    
    # ====================================================
    # 8. INSTALLATION_TRACKING
    # ====================================================
    if stage in ["INSTALLATION_TRACKING", "ONBOARDING_COMPLETE"]:
        if any(k in text for k in ["track", "status", "installation", "delivery", "engineer", "eta", "when", "time"]):
            return "Your field engineer Rahul Sharma is currently in transit (ETA: 45 mins). Order ID: " + wf["order"]["order_id"]

    # ====================================================
    # 9. General Global Navigation Fallbacks
    # ====================================================
    if any(k in text for k in ["show plans", "all plans", "catalogue", "cheaper plan", "options"]):
        transition_workflow(session_id, "GO_TO_STAGE", {"stage": "PLAN_EXPLORATION"})
        return "Switched to plan comparison view. You can review all Airtel Business packages."

    if (any(k in text for k in ["quote", "pricing", "cost", "how much", "charges", "monthly bill", "the bill"]) or any(w in text.split() for w in ["bill", "quote"])) and not any(w in text for w in ["billing", "billing software", "billing machine", "billing system"]):
        if not any(item in text for item in ["cctv", "camera", "cameras", "ip", "static", "whatsapp", "sim", "backup", "pos", "router", "fiber", "speed"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
        return f"Here is your single transparent bill: ₹{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."

    if any(k in text for k in ["kyc", "verify documents", "verify kyc"]):
        transition_workflow(session_id, "GO_TO_STAGE", {"stage": "KYC_VERIFICATION"})
        return "Switched to Smart KYC. You can lookup GSTIN or test specimen documents with zero typing."

    if any(k in text for k in ["track order", "track installation", "engineer status"]):
        transition_workflow(session_id, "GO_TO_STAGE", {"stage": "INSTALLATION_TRACKING"})
        return "Here is your live fulfillment progress stepper. Field engineer Rahul Sharma is assigned."

    return None

# Project Udyam Digital 🚀
### Making Small Businesses Go Digital in One Sitting
**Airtel SYNC 2026 · YTL Hackathon · Enterprise Track A**  
**Team:** Team Halo · **Institution:** Thapar Institute of Engineering & Technology

---

## 🌐 Live Prototype & Evaluation Links

| Resource | Link | Description |
| :--- | :--- | :--- |
| **Live Consumer Portal** | [udyam-digital-c126.onrender.com](https://udyam-digital-c126.onrender.com/) | Interactive customer journey with multilingual AI advisor & dynamic quote |
| **Airtel Control & Partner Portal** | [udyam-digital-c126.onrender.com/control](https://udyam-digital-c126.onrender.com/control) | Operations intelligence, KYC officer review queue & partner desk |
| **Demo Video Walkthrough** | [Halo_TIET.mp4](./Halo_TIET.mp4) | High-definition 1080p demo video walkthrough |
| **Business Case Deck (PDF)** | [Halo_TIET.pdf](./Halo_TIET.pdf) | Official presentation deck |
| **Business Case Deck (PPTX)** | [Halo_TIET.pptx](./Halo_TIET.pptx) | Editable PowerPoint presentation |
| **Architecture Specification** | [Solution Architecture PDF](./submission/Solution_Architecture_and_Data_Flows.pdf) | End-to-end data flows and component specifications |
| **DPDP Compliance Note** | [DPDP Act 2023 Note PDF](./submission/DPDP_Act_2023_Privacy_and_Security_Note.pdf) | Statutory data privacy and security architecture note |

---

## 📊 North-Star Business Impact

| Metric | Historical Baseline (Assignment Data) | Project Target | Impact / Improvement |
| :--- | :--- | :--- | :--- |
| **Funnel Conversion** | 7.36% (368 / 5,000 leads) | **22.0%** | **~3× expansion** |
| **Activation TAT** | 17.6 days average | **3.5 days** | **80% reduction** |
| **Acquisition Cost (CAC)** | ₹15,000 per activation | **₹3,800** | **~75% reduction** |
| **Customer Follow-up Calls** | 3+ calls per customer | **< 0.2 calls** | **Near-zero status chasing** |
| **Six-Month Churn** | 15.2% (smb_leads.csv) | **4.8%** (team model) | **~68% reduction** |

*Note: Targets and projections; not verified production results. Historical baseline drawn directly from 5,000 leads in `smb_leads.csv`.*

---

## 🛠️ Implemented Architecture & Team Innovations

1. **Conversational AI Advisor**:
   - Multilingual voice/text discovery in Hindi, Hinglish, and English mapping needs to `product_catalogue.csv`.
2. **Transparent 1-Click Quote & Modular Checkout**:
   - Real-time dynamic pricing with toggleable add-ons, 18% GST breakdown, eliminating 3-5 day PDF quote wait.
3. **Smart KYC & DPDP Act 2023 Compliance**:
   - Sub-second mock GSTIN & Udyam registry lookups, utility bill recency checks (<90 days), affirmative bilingual consent, and dual verification options (automated vision extraction vs manual KYC officer review).
4. **Self-Serve Visual Order Tracker**:
   - Real-time 5-stage milestone tracking (Order Created ➔ KYC Approved ➔ Equipment Dispatched ➔ Fiber Splicing ➔ Live Activation).
5. **AI Quote Recovery Engine**:
   - Explainable 8-class objection taxonomy & rules-based recoverability scoring analyzing 1,113 abandoned leads with actionable rescue scripts and 1-click quote-resume URLs.
6. **Partner Operations & Attribution**:
   - QR attribution desk with a verified **₹1,500 activation-gated commission ledger state machine** (`Pending ➔ Eligible on Activation ➔ Approved ➔ Paid`).

---

## 💻 Local Quickstart

```bash
# Clone the repository
git clone https://github.com/AnshulKaushal27/udyam-digital.git
cd udyam-digital

# Install dependencies
pip install -r requirements.txt

# Run the local server
python app.py
```

Open `http://localhost:5000` for the Consumer Portal and `http://localhost:5000/control` for the Airtel Staff & Partner Portal.

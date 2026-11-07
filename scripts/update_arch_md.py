import re

with open('E:/Airtel/submission/Solution_Architecture_and_Data_Flows.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace section 6 header with section 7 header
old_sec6 = "## 6. Key Performance Indicators & Target Impact"
new_sec6 = """## 6. Predictive Operations & Operations Intelligence Centre Architecture

```mermaid
flowchart TD
    subgraph DataSources["Heterogeneous Operational Data Sources"]
        HDS[("Historical smb_leads.csv<br/>(N=5,000 Baseline)")]
        LMS[("Live In-Memory State<br/>(Orders, Quotes, Audit)")]
        TGT[("Assignment Targets<br/>(25% Conv, <=3d TAT)")]
        SIM[("What-If Simulator<br/>(Non-Double-Counting Model)")]
    end

    subgraph OPEngine["Operations Intelligence Core Engine (operations_intelligence.py)"]
        DMS["Strict 4-Dimensional Metric Segregator<br/>(Anti-Hallucination Governance)"]
        FDS["6-Stage Funnel Diagnostics<br/>(56.4% Drop Isolation)"]
        QLS["Quote Loss Intelligence<br/>(Price 414, Competitor 207, Complex 206)"]
        KYC["KYC Bottleneck Engine<br/>(OCR Quality, 90d Freshness, GSTIN)"]
        PRIS["Proactive Installation Risk Engine<br/>(Kirana 2d, Clinic 3d, Pro 7d, Mfg 14d)"]
        UEQ["Unified Exception Action Centre<br/>(Abandoned Quotes, KYC, Risk, Breaches)"]
        PPerf["Partner Performance BI<br/>(Fair Conversion Metrics & Commissions)"]
        AIBI["Executive Insights Generator<br/>(Strict 4-Part Observation-Data-Action)"]
        WISS["What-If Scenario Simulator<br/>(Activations, ARR, Payback Projection)"]
    end

    subgraph ControlPortal["Airtel Control Portal Operational Command Surface"]
        ExecDash["13-KPI Executive Command Grid<br/>(Provenance-Tagged Metric Cards)"]
        FunnelView["Interactive 6-Stage Waterfall<br/>(Segment/Tier Filters & Lead Drilldown)"]
        ExcQueue["Unified Action Desk<br/>(1-Click Acknowledge, Resolve with Notes)"]
        OpsGrid["Live Orders Pipeline & Risk Badges<br/>(LOW, MED, HIGH, SLA BREACHED)"]
        SimDesk["Executive What-If Strategy Desk<br/>(Real-Time Sliders & Financial Impact)"]
    end

    DataSources --> DMS
    DMS --> FDS & QLS & KYC & PRIS & UEQ & PPerf & AIBI & WISS
    FDS & QLS & KYC & PRIS & UEQ & PPerf & AIBI & WISS --> ControlPortal
```

### Key Operations Intelligence Components:
1. **Strict 4-Dimensional Segregation:** Mandates absolute provenance separation between Historical Assignment Baseline (N=5,000), Assignment Targets, Live Prototype Transactions, and Simulated Scenarios. Every metric carries an explicit `data_source` tag.
2. **6-Stage Funnel Diagnostics:** Tracks the acquisition journey from Lead Generated (5,000) through Activated (368), mathematically isolating the 56.4% collapse point (1,113 drops) at Stage 3->4 (Needs Assessed to Quote Accepted).
3. **Quote Loss Intelligence:** Categorizes historical quote rejections into Price Too High (414 / 37.2%), Competitor Cheaper (207 / 18.6%), Quote Complex (206 / 18.5%), and Delivery Delays (286 / 25.7%), paired with actionable recommendations and Phase 3 recovery cross-links.
4. **Bundle-Specific Proactive Installation Risk Engine:** Evaluates orders against product-specific SLAs (Kirana 2 days, Clinic 3 days, Multi-site 7 days, Manufacturing 14 days), computing an explainable 0-100 risk score and assigning status (`LOW_RISK`, `MEDIUM_RISK`, `HIGH_RISK`, `SLA_BREACHED`) with root-cause explanations and operational directives.
5. **Unified Exception Management Centre:** Merges 4 distinct operational incident streams (abandoned high-priority quotes, KYC exceptions, installation risks, and unassigned resources) into a single prioritized queue supporting 1-click acknowledgment and resolution with auditable notes.
6. **Executive Business Insights (Strict 4-Part Schema):** Formulates verified insights containing (1) Empirical Observation, (2) Traceable Supporting Data, (3) Business Implication, and (4) Recommended Operational Action.
7. **Interactive What-If Scenario Simulator:** Features a transparent mathematical model without double-counting, projecting net activations, incremental ARR, CAC spend, and payback period from user-adjusted quote acceptance, KYC completion, activation, and recovery rates.

## 7. Key Performance Indicators & Target Impact"""

if old_sec6 in text:
    text = text.replace(old_sec6, new_sec6, 1)
    print("Updated Solution_Architecture_and_Data_Flows.md with Section 6.")
else:
    print("Section 6 header not found.")

with open('E:/Airtel/submission/Solution_Architecture_and_Data_Flows.md', 'w', encoding='utf-8') as f:
    f.write(text)

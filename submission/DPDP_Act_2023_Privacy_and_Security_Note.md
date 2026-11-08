# Project Udyam Digital: Data Privacy & Security Architecture Note
**Compliance Framework: Digital Personal Data Protection (DPDP) Act, 2023 & DoT Telecom KYC Mandates**  
<div class="meta">Airtel SYNC 2026 · Digital Track | Team Halo · Thapar | Version 1.0 (November 2026)</div>

---

### 1. Executive Summary & Philosophy
Project Udyam Digital re-engineers MSME onboarding for Accel Telecom / Airtel Business from a paper-intensive physical process into a digital-first, paperless experience. Because MSME onboarding intersects statutory telecom KYC requirements (under Department of Telecommunications / TRAI mandates) with personal and enterprise financial data, the system is designed strictly around the **Privacy-by-Design** principles of India's **Digital Personal Data Protection (DPDP) Act, 2023**.

---

### 2. Core DPDP Act 2023 Architectural Principles

#### Principle 1: Notice & Granular, Unbundled Consent (Section 6)
* **Pre-Capture Multilingual Notice:** Before requesting any document upload or registry query, the user is presented with a standalone, clear notice in their chosen language (English, Hindi, or regional languages).
* **Unchecked-by-Default Affirmative Consent:** In strict adherence to Section 6 of the DPDP Act 2023, the consent checkbox is unchecked by default, prohibiting pre-ticked opt-ins. Explicit affirmative opt-in is validated both client-side and server-side before any document analysis occurs.
* **Dual Choice of Verification Modes:** Customers are provided transparent, explicit choices between (a) Automated AI verification with statutory registry cross-referencing, and (b) Requesting manual KYC review by an authorized Airtel KYC compliance desk.
* **Unbundled Consent:** Telecommunications service activation consent is strictly segregated from marketing or third-party communications consent. Customers can opt out of promotional communications without blocking their service application.
* **Consent Artifact Logging:** Every consent event generates an immutable digital audit record containing: `Lead_ID`, `Timestamp_UTC`, `Language_Selected`, `Consent_Version`, and `IP_Hash`.

#### Principle 2: Purpose Limitation & Lawful Basis (Section 4 & 7)
* Data collected through Project Udyam Digital is restricted strictly to:
  1. Statutory telecom identity and address verification mandated by DoT.
  2. Telecom network feasibility and optical fiber/AirFiber hardware installation.
  3. Generating unified monthly B2B billing and tax invoices (GSTIN matching).
* No secondary monetization, unconsented behavioral profiling, or unauthorized third-party broker sharing is permitted.

#### Principle 3: Data Minimization (Section 6(1))
* **Zero Financial Hoarding:** The system does **not** collect bank statements, income tax returns, or private financial records. If a business verifies its active status via the GSTIN / Udyam registries, supplementary identity checks are restricted to authorized signatory verification.
* **Field-Level Selective OCR:** Document OCR pipelines only extract the specific fields required for compliance (e.g., Entity Name, Registration Date, Address, Signatory Name). Extraneous text, barcodes, or unrelated document artifacts are discarded from runtime memory.

---

### 3. Technical Security & PII Protection Controls

| Control Domain | Architectural Implementation | Standard / Protocol |
|---|---|---|
| **Encryption in Transit** | All client-server, LLM API, and registry integrations use TLS 1.3 with HSTS enabled. Plaintext HTTP is permanently disabled. | TLS 1.3 / Perfect Forward Secrecy |
| **Encryption at Rest** | Document repositories and databases are encrypted using FIPS 140-3 validated AES-256 keys managed via enterprise HSM/KMS. | AES-256-GCM / Cloud KMS |
| **PII & Identifier Masking** | Permanent runtime masking in application logs, customer support views, and partner portals: <br>• Aadhaar: `XXXX-XXXX-1234` (Strict UIDAI masking compliance) <br>• PAN: `XXXXX1234X` <br>• GSTIN: `27AAAAA****1ZX` | Automated RegEx Redaction Filter |
| **Data Retention & Ephemeral Cache** | Uploaded document images are processed purely in ephemeral in-memory RAM buffers during the request lifecycle. No raw image bytes or unmasked identity proofs are written to persistent disk storage, session states, or audit logs. Temporary memory buffers are immediately released upon completion of verification. | Zero-Disk Ephemeral Memory Buffer |
| **Access Control (RBAC)** | Strict principle of least privilege. Field partners and sales executives only view lead status and bundle details; they cannot view or download raw KYC identity proofs. | OAuth 2.0 / Fine-Grained RBAC |

---

### 4. Incident Response & Data Principal Rights (Section 11 & 12)
* **Right to Correction & Erasure:** Authorized signatories can update outdated contact credentials or request erasure of pre-activation draft leads that were not consummated into active telecom contracts.
* **Automated Data Breach Escalation:** In accordance with Section 8(6) of the DPDP Act, automated intrusion detection systems alert the Data Protection Officer (DPO) and the Data Protection Board of India (DPBI) within statutory notification windows.

*Submitted on behalf of Team Halo (Thapar) for Airtel SYNC 2026.*

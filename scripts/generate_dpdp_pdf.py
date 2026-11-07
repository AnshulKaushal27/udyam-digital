import os
import win32com.client

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {
    size: A4 portrait;
    margin: 1.5cm;
  }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.35;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }
  .header-table {
    width: 100%;
    border-bottom: 2px solid #e40000;
    padding-bottom: 6px;
    margin-bottom: 12px;
  }
  .title {
    font-size: 15pt;
    font-weight: bold;
    color: #0f172a;
    margin: 0;
  }
  .subtitle {
    font-size: 9.5pt;
    color: #e40000;
    font-weight: bold;
    margin-top: 2px;
  }
  .meta {
    font-size: 8pt;
    color: #64748b;
  }
  h2 {
    font-size: 10.5pt;
    color: #0f172a;
    border-left: 3px solid #e40000;
    padding-left: 6px;
    margin-top: 10px;
    margin-bottom: 4px;
    text-transform: uppercase;
  }
  p {
    margin: 0 0 6px 0;
  }
  ul {
    margin: 0 0 6px 0;
    padding-left: 18px;
  }
  li {
    margin-bottom: 3px;
  }
  b {
    color: #0f172a;
  }
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8.5pt;
  }
  table.data-table th {
    background-color: #0f172a;
    color: #ffffff;
    padding: 5px 8px;
    text-align: left;
    font-size: 8.5pt;
  }
  table.data-table td {
    padding: 4px 8px;
    border-bottom: 1px solid #e2e8f0;
  }
  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }
  .footer {
    border-top: 1px solid #cbd5e1;
    margin-top: 12px;
    padding-top: 6px;
    font-size: 7.5pt;
    color: #64748b;
    text-align: center;
  }
</style>
</head>
<body>

<div class="header-table">
  <div class="title">Project Udyam Digital: Data Privacy & Security Architecture Note</div>
  <div class="subtitle">Compliance Framework: Digital Personal Data Protection (DPDP) Act, 2023 & DoT Telecom KYC Mandates</div>
  <div class="meta">Airtel SYNC 2026 · Digital Track | Team Halo · Thapar Institute of Engineering & Technology | Version 1.0 (November 2026)</div>
</div>

<h2>1. Executive Summary & Design Philosophy</h2>
<p>Project Udyam Digital replaces the paper-heavy, multi-week physical sales journey for India's 6.3 Crore MSMEs with a 15-minute digital onboarding experience. Because telecom onboarding intersects statutory identity verification (under Department of Telecommunications mandates) with merchant identity, this platform implements strict <b>Privacy-by-Design</b> as established by India's <b>DPDP Act, 2023</b>.</p>

<h2>2. Core DPDP Act 2023 Architectural Principles</h2>
<ul>
  <li><b>Granular, Unbundled Consent (Section 6):</b> Prior to requesting camera capture or registry queries, the customer receives an explicit, standalone consent prompt in their selected regional language (Hindi, English, etc.). Telecom service activation is completely decoupled from promotional marketing opt-ins. Each consent event stores an immutable log (<code>Lead_ID</code>, <code>Timestamp_UTC</code>, <code>Language</code>, <code>IP_Hash</code>).</li>
  <li><b>Purpose Limitation (Section 4 & 7):</b> Customer and enterprise data is strictly restricted to: (1) Statutory DoT KYC verification, (2) Last-mile optical fiber/AirFiber hardware dispatch, and (3) Generating monthly unified tax invoices. Zero unauthorized data monetization or secondary broker sharing is permitted.</li>
  <li><b>Strict Data Minimization (Section 6(1)):</b> The platform eliminates unnecessary financial collection (no bank statements or balance sheets). If active status is verified via GSTIN/Udyam registries, supplementary checks are strictly limited to authorized signatory ID and utility bill address matching.</li>
</ul>

<h2>3. Technical Security & PII Protection Controls</h2>
<table class="data-table">
  <tr>
    <th style="width: 25%;">Control Domain</th>
    <th style="width: 50%;">Architectural Implementation</th>
    <th style="width: 25%;">Standard / Protocol</th>
  </tr>
  <tr>
    <td><b>Encryption in Transit</b></td>
    <td>All client, LLM Advisor, and registry API calls strictly enforce TLS 1.3 with Perfect Forward Secrecy. HTTP is disabled.</td>
    <td>TLS 1.3 / HSTS</td>
  </tr>
  <tr>
    <td><b>Encryption at Rest</b></td>
    <td>All databases, registry caches, and object storage buckets are encrypted using enterprise AES-256 keys via Cloud KMS.</td>
    <td>FIPS 140-3 / AES-256</td>
  </tr>
  <tr>
    <td><b>PII Identifier Masking</b></td>
    <td>Automated regex filters redact sensitive numbers in logs and UI: Aadhaar (<code>XXXX-XXXX-1234</code>), PAN (<code>XXXXX1234X</code>), GSTIN (<code>27AAAAA****1ZX</code>).</td>
    <td>Automated Data Masking</td>
  </tr>
  <tr>
    <td><b>Ephemeral Document Purge</b></td>
    <td>Uploaded identity photos are held in volatile RAM/ephemeral storage during OCR parsing and automatically purged post-validation.</td>
    <td>24-Hour Purge Lifecycle</td>
  </tr>
  <tr>
    <td><b>Role-Based Access (RBAC)</b></td>
    <td>Field partners and sales agents see lead progress and order status only; raw identity proofs are strictly inaccessible to third parties.</td>
    <td>OAuth 2.0 / Fine-Grained RBAC</td>
  </tr>
</table>

<h2>4. Data Principal Rights & Incident Response</h2>
<p>In accordance with Sections 11–13 of the DPDP Act, customers retain full rights to review, correct, or request deletion of pre-activation draft records. An automated security monitoring agent flags anomalous access patterns, ensuring compliance with statutory breach escalation protocols to the Data Protection Board of India.</p>

<div class="footer">
  Project Udyam Digital · Confidential & Proprietary · Prepared for Airtel SYNC 2026 by Team Halo (Thapar)
</div>

</body>
</html>
"""

def generate_pdf():
    html_file = os.path.abspath(r"E:\Airtel\submission\dpdp_note.html")
    pdf_file = os.path.abspath(r"E:\Airtel\submission\DPDP_Act_2023_Privacy_and_Security_Note.pdf")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Converting HTML to PDF via Word: {html_file} -> {pdf_file}")
    word = win32com.client.Dispatch("Word.Application")
    try:
        doc = word.Documents.Open(html_file)
        # wdFormatPDF = 17
        doc.SaveAs(pdf_file, 17)
        doc.Close()
        print("DPDP Note PDF generated successfully!")
    finally:
        word.Quit()

if __name__ == "__main__":
    generate_pdf()

# Privacy Policy

> **DRAFT — FOR REVIEW BY LEGAL COUNSEL**  
> This document is a working draft prepared for the IST Health platform launch. It does not constitute legal advice and must be reviewed and approved by qualified legal counsel before production use. Do not rely on this draft as a statement of regulatory compliance.

**Effective date:** 13 July 2026  
**Last updated:** 13 July 2026

---

## 1. Introduction

This Privacy Policy describes how **IRISSTAR Technologies** (“**IST**,” “**we**,” “**us**,” or “**our**”), operating the **IST Health** hospital and clinic management platform (the “**Platform**”), collects, uses, stores, and protects personal information.

The Platform is provided to healthcare facilities and authorized users in Qatar and may be accessed by staff, administrators, and—where enabled—patients. The application display name is **IST Technologies LLC / IST Health**.

By accessing or using the Platform, you acknowledge that you have read this Privacy Policy. Where required, separate consent may be obtained for specific processing activities.

---

## 2. Data Controller and Contact

**Data controller:** IRISSTAR Technologies  
**Product:** IST Health (GNU Health–based hospital/clinic management system)

**Primary office (Qatar):**  
Office 214/215, 2nd Floor, Regus D-Ring Building no 65, D-Ring Road, Old Airport, PO Box 32522, Doha, Qatar

**Additional offices:**  
- **UAE:** Level 20, 48, Burj Gate Tower, Downtown Dubai, PO Box 22061, Dubai, U.A.E.  
- **India:** Prestige Polygon, 3rd Floor, 471 Anna Salai, Teynampet, Chennai, Tamil Nadu 600 035, India

**Privacy inquiries:** info@isttechnologies.qa  
**General contact:** sahni.ps@gmail.com  
**Website:** https://www.isttechnologies.qa

---

## 3. Scope

This policy applies to personal information processed through the IST Health Platform, including:

- Web and application interfaces branded as IST Health
- Backend systems powered by GNU Health and related open-source components
- Demo, user-acceptance testing (UAT), and production environments operated by or on behalf of IST

This policy does not cover third-party websites linked from the Platform or services operated independently by a healthcare facility that uses IST Health, except where IST acts as a processor on that facility’s behalf under a separate agreement.

---

## 4. Information We Collect

We may collect and process the following categories of information, depending on your role and the features in use:

### 4.1 Patient and clinical data

- Identity and demographic details (name, date of birth, gender, nationality, contact information, identifiers)
- Medical history, diagnoses, clinical notes, and care plans
- Appointments, admissions, and visit records
- Laboratory orders, results, and related metadata
- Pharmacy prescriptions, dispensing records, and medication history
- Billing and insurance-related information where applicable
- Documents, images, or files uploaded to patient records

Patient data in demo/UAT environments may include **synthetic or anonymized test data** created for training and validation. Production environments process real patient information only where authorized by the healthcare facility and applicable law.

### 4.2 Healthcare staff and administrator data

- Name, professional credentials, role, department, and employment identifiers
- Account credentials (username, hashed passwords, authentication logs)
- Activity logs related to system access and record changes
- Contact details and institutional affiliation

### 4.3 Technical and usage data

- IP address, browser type, device information, and session identifiers
- Access timestamps, audit trails, and error/diagnostic logs
- Configuration and preference settings (e.g., language selection)

We do not intentionally collect information beyond what is necessary to operate, secure, and improve the Platform for healthcare delivery.

---

## 5. How We Use Information and Legal Basis

We process personal information for purposes that may include:

| Purpose | Examples |
|--------|----------|
| **Healthcare provision and administration** | Managing patient records, scheduling, clinical workflows, lab and pharmacy operations |
| **Account and access management** | Creating user accounts, authentication, role-based access control |
| **Security and integrity** | Audit logging, fraud prevention, incident detection, backups |
| **Platform operation and support** | Maintenance, troubleshooting, service notifications |
| **Legal and regulatory obligations** | Responding to lawful requests, record-keeping where required |
| **Consent-based activities** | Optional communications or features where explicit consent is obtained |

**Legal basis (general):** Processing is generally undertaken to deliver healthcare-related services at the direction of the healthcare facility, to perform contractual obligations with authorized users, to protect vital interests in emergency contexts, and—where applicable—based on consent or legitimate interests in securing and operating the Platform. The specific legal basis may vary by jurisdiction and by the role of IST (controller vs. processor). This draft does not assert compliance with any particular statute.

---

## 6. Qatar and GCC Context

IST Health is designed for use in Qatar and the wider Gulf Cooperation Council (GCC) region. We aim to align our data handling practices with generally recognized data protection principles, including:

- **Lawfulness, fairness, and transparency** in processing personal information
- **Purpose limitation** — using data for identified healthcare and operational purposes
- **Data minimization** — collecting only what is reasonably necessary
- **Accuracy** — supporting correction of inaccurate records through authorized users
- **Storage limitation** — retaining data only as long as needed for the stated purposes
- **Integrity and confidentiality** — implementing appropriate security measures
- **Accountability** — maintaining records of processing and access controls

Qatar’s personal data protection framework (including the Personal Data Privacy Protection Law, “PDPL”) and sector-specific healthcare regulations may apply to processing activities in Qatar. **This draft has not been verified for PDPL or other regulatory compliance.** Healthcare facilities using IST Health remain responsible for their own regulatory obligations, including patient notices, consent where required, and reporting to relevant authorities.

Where processing involves users or data subjects in the UAE, India, or other jurisdictions, additional local requirements may apply. IST will work with customers and counsel to address cross-border considerations as deployments expand.

---

## 7. Data Storage, Hosting, and Security

### 7.1 Hosting

Platform data is hosted on **Google Cloud Platform (GCP)** infrastructure. Primary compute resources are deployed in the **GCP `me-central1` region** (Middle East), subject to change with notice where appropriate for operational or contractual reasons.

### 7.2 Security measures

We implement administrative, technical, and organizational measures designed to protect personal information, which may include:

- Encrypted connections (TLS) for data in transit
- Access controls and role-based permissions aligned to clinical roles
- Authentication requirements for staff and administrator accounts
- Audit logging of significant system events
- Regular backups and recovery procedures
- Network segmentation and monitoring within the cloud environment

No method of transmission or storage is completely secure. We cannot guarantee absolute security but strive to apply measures appropriate to the sensitivity of health information.

---

## 8. Data Retention

Retention periods depend on:

- The healthcare facility’s clinical and legal record-keeping requirements
- Applicable laws and professional standards in Qatar and other relevant jurisdictions
- Whether the environment is production, demo, or UAT

**Demo/UAT data:** Synthetic or test patient data may be refreshed, anonymized, or deleted periodically as part of testing cycles.

**Production data:** Retained according to the healthcare facility’s policies and contractual terms with IST, unless a longer or shorter period is required by law or agreed in writing.

When data is no longer needed, we support secure deletion or anonymization in accordance with applicable procedures and agreements.

---

## 9. Sharing and Third Parties

We may share information with:

| Third party | Role |
|-------------|------|
| **Google Cloud Platform** | Cloud infrastructure and hosting provider |
| **GNU Health and open-source stack** | Core hospital information system software (see Section 10) |
| **Healthcare facility** | The clinic or hospital that owns or controls patient records |
| **Authorized subprocessors** | Vendors engaged for support, monitoring, or security, under contractual safeguards |
| **Legal authorities** | When required by applicable law or valid legal process |

We do not sell personal information. We require service providers that process data on our behalf to use it only for specified purposes and to apply appropriate security measures.

---

## 10. Open-Source Software (GNU Health)

The Platform is built on **GNU Health**, an open-source hospital and health information system licensed under the **GNU General Public License (GPL)**. GNU Health source code is publicly available under its license terms. IST’s proprietary branding, customizations, hosting environment, and operational layers may be subject to separate terms.

Use of GNU Health components does not by itself determine how IST processes personal data; our handling of personal information is governed by this Privacy Policy, customer agreements, and applicable law.

---

## 11. International Transfers

Where personal information is accessed from or transferred to countries outside Qatar (for example, support personnel in India or UAE offices, or GCP services with global operations), we aim to implement safeguards appropriate to the transfer, such as contractual clauses and access restrictions. Details of specific transfer mechanisms should be confirmed with legal counsel for each deployment.

---

## 12. Your Rights and Requests

Depending on your role, relationship with a healthcare facility, and applicable law, you may have rights to:

- **Access** personal information held about you
- **Request correction** of inaccurate or incomplete data
- **Request deletion** or restriction of processing, subject to clinical and legal retention requirements
- **Object** to certain processing or withdraw consent where processing is consent-based
- **Receive information** about how your data is used

**Patients** should generally direct requests regarding clinical records to their healthcare provider (the data controller for clinical care). IST will assist authorized facilities in responding where we act as a processor.

**Staff and administrators** may contact us at **info@isttechnologies.qa** for account-related privacy inquiries. We will respond within a reasonable timeframe, subject to identity verification and legal limitations.

We may decline requests that are manifestly unfounded, repetitive, or would impair the rights of others or our ability to meet legal or clinical obligations.

---

## 13. Children’s Data

The Platform may process information about pediatric patients as part of clinical care at a healthcare facility. Such processing is performed under the facility’s authority and applicable guardian consent requirements. The Platform is not intended for direct use by children without appropriate supervision and authorization.

---

## 14. Changes to This Policy

We may update this Privacy Policy from time to time. The “Last updated” date at the top will reflect material changes. Continued use of the Platform after updates constitutes acknowledgment of the revised policy, where permitted by law. Material changes affecting healthcare facilities may also be communicated through contractual channels.

---

## 15. Disclaimer

This Privacy Policy is provided as a **draft for internal review and legal counsel approval**. It is intended to describe IST’s intended practices in good faith but **does not constitute a warranty of compliance** with Qatar PDPL, GCC regulations, HIPAA, GDPR, or any other specific legal framework unless and until formally confirmed by qualified legal advisors and reflected in binding documentation.

---

**IRISSTAR Technologies** · IST Health  
info@isttechnologies.qa · https://www.isttechnologies.qa

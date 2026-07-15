# Upstream GNU Health HIS Image ↔ IST HIS Sync Review

**Date:** 2026-07-15  
**Upstream image root:** `docs/upstream/original/images/images/` (nested under `docs/upstream/original/images/`)  
**Deployment baseline:** GNU Health HIS **5.0.6**, Tryton/SAO **7.0.53**, **53** health modules activated, **React primary + SAO secondary**  
**Method:** Full filename inventory (119 files); visual content review of representative screenshots across all functional clusters (patients, appointments, lab, inpatient, surgery, ICU, genetics, OB/GYN, Orthanc, lifestyle, NTD, federation, finance, access control, ghcontrol, diagrams); RST citation map; comparison to React routes, Setup Hub, Help Centre, and `docs/ist-his/` stubs.

---

## Executive summary

| Sync bucket | Count | % of 119 | Meaning |
|-------------|------:|--------:|---------|
| **Aligned (feature available)** | 18 | **15%** | Concept matches something users can do in IST today (usually React list/create *or* SAO with same model), but **UI is still SAO/GTK in the screenshot** — not a visual match to React. |
| **Partial** | 62 | **52%** | Module is activated / flow exists, but React only covers a thin slice; screenshot shows deep SAO/GTK forms, wizards, or Orthanc admin that React does not expose. |
| **Gap / outdated / N/A for React UX** | 39 | **33%** | Specialty SAO-only with missing IST how-to docs, **ghcontrol** install TUI (not our Setup Hub), Evolution CalDAV client, old GH **4.x** module screenshots, or pure branding/architecture art. |

**Honest verdict:** These upstream images are **not visually synced** with IST’s React UI. Nearly all clinical/admin screenshots show **Tryton SAO or GTK** with GNU Solidario demo data and orange selection chrome. **Do not paste them into IST Help as “what the app looks like.”** They remain valuable as **backend/SAO how-to references** for activated modules.

| Docs coverage vs image topics | Count (approx.) | Notes |
|-------------------------------|----------------:|-------|
| **Same** (procedural depth ≈ screenshot) | **0** | No IST doc reproduces SAO screen walkthroughs at this fidelity. |
| **Partial** | **~55** | Help workflows (thin) + module README stubs + comparison matrix. |
| **Missing** | **~45** | ICU, genetics, OB/GYN, Orthanc, NTD, federation queue, surgery depth, lab create-test wizard, ID cards/wristbands. |
| **N/A** | **~19** | Branding banners, federation architecture art, HIS branching diagram, Evolution desktop calendar. |

**Branding:** Upstream images brand **GNU Health HMIS** / demo institution **GNU SOLIDARIO HOSPITAL**. IST uses separate naming/branding (`IST_HIS_Naming_and_Branding_Policy.md`). Screenshots are outdated vs IST chrome.

**Version drift in images:** Several module-admin shots show health packages at **4.2.x / 4.4.0** and Tryton **6.0.x**; ghcontrol banner shows **5.0.0b3**. Our pin is **5.0.6** / Tryton **7.0.53** — treat those frames as illustrative, not version-accurate.

---

## Inventory

| Metric | Value |
|--------|------:|
| Total image files (png/jpg/jpeg/svg/gif) | **119** |
| Layout | Flat directory `images/images/` (no further subdirs) |
| Formats | 116 PNG + 3 JPG |
| Referenced from `docs/upstream/original/rst/` | ~110 unique filenames (some reused across RST files) |
| Unreferenced / orphan in tree | ~5 (see notes column) |

---

## Setup Hub spot-check (install / company / patient / appointments)

| Upstream image topic | Upstream meaning | IST reality | Match? |
|----------------------|------------------|-------------|---------|
| **ghcontrol_*** (install, instance, packages, backup) | Terminal TUI **GNU Health Control Center** for HIS install & DB lifecycle | IST ops use container/admin paths; **Setup Hub `/setup`** is **post-deploy configuration**, not ghcontrol | **No** — different tool & phase |
| **Install_Modules_*.png** | SAO Administration → Modules → Mark for Activation → Perform Pending | React `/modules` lists/marks; real upgrade often SAO/`trytond-admin` | **Partial** — same model, SAO screenshot, older module versions in image |
| **Party / patient create** (`GNU_Health_party_*`, patient main) | SAO Party Health tab + Patient form (deep demographics, critical info, many specialty tabs) | React `/parties`, `/patients` — lite create/edit; deep tabs → SAO | **Partial** — fields overlap; **UI differs** |
| **Appointments** form/list | SAO Health/Appointments with CalDAV UUID, urgency, specialty, status tabs | React `/appointments` — create/list; deep CalDAV/specialty linking often SAO | **Partial** — flow exists; **UI differs** |
| **Setup Hub order 1–9** | *No upstream image* of an equivalent wizard | Coded order: Companies → Currency → Administration → Party → Product → Stock → Calendar → Financial → Health | **IST-only UX** — document via Help `setup-order`, not upstream images |

**Conclusion:** Upstream “first steps / install” images **do not** describe Setup Hub. Keep linking ghcontrol images only for operators who use vanilla GH control tooling; for IST, document Setup Hub + Help instead.

---

## Recommendation

1. **Keep linking upstream originals** (this tree + RST) for **SAO screenshots** and specialty how-tos (ICU, genetics, Orthanc, federation, OB/GYN, NTD).
2. **Adapt key clinical/admin flows into IST Help** with **React screenshots** (and SAO callouts where React is thin): register patient, book appointment, lab order, admit/bed, invoice/pay, Setup Hub 1–9, company create.
3. **Never** present SAO/GTK images as the IST React UI; label them “SAO (secondary client)” when reused.
4. **Priority doc gaps** below should be closed first — they are how-to images for flows we either expose partially in React or only in SAO without IST Help articles.

---

## Priority gaps

| Priority | Image cluster | Why it matters | Suggested IST action |
|----------|---------------|----------------|----------------------|
| P1 | Patient list / main / party-as-patient | Core onboarding; React UI ≠ screenshots | Capture React screens for Help `wf-register-patient`; keep SAO shots labeled secondary |
| P1 | Appointments form + list | Daily ops | React Help screenshots; note CalDAV/status tabs → SAO |
| P1 | Lab new order + “Create test” wizard + PDF report | React orders only; results/wizard SAO | Expand Help `wf-lab-order`; add SAO steps for create-test & results |
| P1 | Health services → invoice → pay | Billing path | Align Help invoice/payment with SAO wizards; React financial is stub |
| P1 | Groups / users / modules admin | Setup Hub step 3 | React `/groups` `/users` `/modules` screenshots; SAO for Perform Pending |
| P2 | Beds + hospitalization form | Inpatient | Help admit/transfer already thin; add SAO hospitalization form reference |
| P2 | Surgeries form / ICD10-PCS / RCRI | Module active; React `/procedures` list-only | Help article + SAO deep form |
| P2 | Orthanc integration set (11 images) | Imaging module active; React list only | SAO/Orthanc runbook in IST docs |
| P2 | Evaluations history/form | React `/evaluations` thin | Help `wf-consultation` + SAO depth |
| P3 | ICU APACHE / ECG / GCS | SAO-only | IST Help stubs pointing to upstream RST |
| P3 | Genetics / OB-GYN / lifestyle / pediatrics / NTD | SAO-only specialties | Module README + “Open in SAO” + upstream images |
| P3 | Federation architecture + queue | Activated but not UAE HIE | Architecture note; do not confuse with `uae-hie-readiness` Help |
| P3 | ghcontrol / Evolution calendar | Not IST primary UX | Mark N/A for end users; ops appendix only |

---

## Full image table

**Legend — IST implementation**

- **React (partial):** Dedicated React route exists; depth thinner than screenshot.
- **SAO-only:** Module typically activated; use SAO / Open-in-SAO.
- **Ops/TUI:** Server control center — not React/SAO clinical UI.
- **Report/output:** PDF/ID card/wristband sample, not interactive UI.
- **Diagram/branding:** Architecture or marketing art.
- **External client:** e.g. Evolution CalDAV desktop.

**Legend — IST docs:** Same / Partial / Missing / N/A (relative to *screenshot how-to depth*).

| Image path | Description | Upstream doc | IST implementation | IST docs | Notes |
|------------|-------------|--------------|--------------------|----------|-------|
| `images/images/APACHE_II_Score_form_in_the_ICU_module_of_GNU_Health.png` | SAO ICU APACHE II score form under Hospitalizations → Intensive Care | `rst/userguide/modules/icu.rst` | SAO-only (`health_icu`) | Missing | No React ICU route; Help gap |
| `images/images/Chagas_DU_Survey_form_in_GNU_Health.png` | SAO Chagas DU survey form (vectors, housing, prevention) | `rst/userguide/modules/neglectedtropicaldiseases.rst` | SAO-only (`health_ntd_chagas`) | Missing | Epidemiology; not React |
| `images/images/Create_Health_Service_Invoice_dialog.png` | SAO wizard dialog to create invoice from health service | `rst/userguide/healthcenter/products.rst` | SAO-only (React financial stub) | Partial | Help has invoice/payment topics (thin) |
| `images/images/Create_Lab_Request_in_toolbar.png` | SAO toolbar action to create lab request | *(orphan — not cited in RST scan)* | React (partial) `/laboratory` + SAO | Partial | Unreferenced asset; still useful for SAO how-to |
| `images/images/Create_Lab_Request_through_main_menu.png` | SAO main-menu path to create lab request | *(orphan)* | React (partial) + SAO | Partial | Unreferenced |
| `images/images/Creating_a_new_lab_order_from_the_patient_window_in_GNU_Health.png` | SAO patient-related action → new lab order | `rst/userguide/modules/laboratory.rst` | React (partial); deep via SAO | Partial | Help `wf-lab-order` |
| `images/images/Creation_of_the_test_from_the_wizard_in_the_lab_request_form.png` | SAO Actions → “Lab: Create test” on request form | `rst/userguide/modules/laboratory.rst` | SAO-only wizard | Missing | Critical lab ops gap in React/Help |
| `images/images/Dengue_DU_Survey_form_in_GNU_Health.png` | SAO Dengue DU survey form | `rst/userguide/modules/neglectedtropicaldiseases.rst` | SAO-only (`health_ntd_dengue`) | Missing | |
| `images/images/Detailed_form_view_of_the_liver_function_test_type.png` | SAO lab test type definition (LFT) form | `rst/userguide/modules/laboratory.rst` | SAO-only config | Missing | Master data |
| `images/images/Detailed_information_from_the_lab_test_report.png` | SAO detailed lab result/report view | `rst/userguide/modules/laboratory.rst` | SAO-only (results) | Partial | Help points to SAO for results |
| `images/images/ECG_form_of_GNU_Health.png` | SAO ICU ECG form with waveform image + intervals | `rst/userguide/modules/icu.rst` | SAO-only | Missing | |
| `images/images/federation_components.png` | Architecture diagram: Nodes → Thalamus → HIS | `rst/userguide/modules/federation/*.rst` | Diagram (module `health_federation` SAO) | Partial | Stub + UAE HIE Help is separate topic |
| `images/images/ghcontrol_add_health_package_entry.png` | ghcontrol TUI: add health package menu | `rst/techguide/installation/vanilla.rst`, `administration/controlcenter.rst` | Ops/TUI — not Setup Hub | N/A | Not IST primary install UX |
| `images/images/ghcontrol_backup_instance.png` | ghcontrol backup instance screen | *(orphan / near controlcenter)* | Ops/TUI | N/A | Sibling of documented example |
| `images/images/ghcontrol_backup_instance_example.png` | ghcontrol backup example | `rst/techguide/administration/controlcenter.rst` | Ops/TUI | N/A | |
| `images/images/ghcontrol_create_instance_log_window.png` | ghcontrol instance creation log | `rst/techguide/installation/vanilla.rst` | Ops/TUI | N/A | |
| `images/images/ghcontrol_health_package_installation_ok.png` | ghcontrol package install success | vanilla + controlcenter | Ops/TUI | N/A | |
| `images/images/ghcontrol_his_installation_section.png` | ghcontrol HIS installation section | vanilla.rst | Ops/TUI | N/A | Version banner older than 5.0.6 |
| `images/images/ghcontrol_initial_screen.png` | ghcontrol main menu (Install HIS, Create DB, …) v5.0.0b3 | vanilla.rst | Ops/TUI | N/A | **≠ Setup Hub** |
| `images/images/ghcontrol_instance_creation_parameters.png` | TUI new instance name/password/email | vanilla.rst | Ops/TUI | N/A | Sample password in screenshot — do not copy into IST runbooks |
| `images/images/ghcontrol_new_instance_menu_entry.png` | ghcontrol new instance menu | vanilla.rst | Ops/TUI | N/A | |
| `images/images/ghcontrol_refresh_instance_entry.png` | ghcontrol refresh DB instance | vanilla + controlcenter | Ops/TUI | N/A | |
| `images/images/ghcontrol_refresh_instance_result.png` | ghcontrol refresh result | vanilla + controlcenter | Ops/TUI | N/A | |
| `images/images/ghcontrol_selection_health_package_to_add.png` | ghcontrol select package to add | vanilla + controlcenter | Ops/TUI | N/A | |
| `images/images/ghcontrol_start_stop_server.png` | ghcontrol start/stop server | vanilla + controlcenter | Ops/TUI | N/A | |
| `images/images/ghcontrol_update_dependencies_process.png` | ghcontrol update dependencies progress | controlcenter.rst | Ops/TUI | N/A | |
| `images/images/ghcontrol_update_packages_dependencies.png` | ghcontrol update packages menu | controlcenter.rst | Ops/TUI | N/A | |
| `images/images/gnuhealth-his.png` | Branding banner “GH HMIS / Hospital Management System” | `rst/preface.rst` | Diagram/branding | N/A | Not IST branding |
| `images/images/gnuhealth_command_line.png` | SAO “GNU Health Command” box (shortcut e.g. PAT) on patient list | `rst/userguide/basics/commandline.rst` | SAO-only UX affordance | Missing | React has its own nav/search |
| `images/images/gnuhealth_genetics_ana_betz_family_history.png` | SAO patient family genetic history | `rst/userguide/modules/genetics.rst` | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_gene_cftr_detailed_view.png` | SAO CFTR gene detail | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_gene_filter_options.png` | SAO gene list filters | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_genes_list_view.png` | SAO HGNC genes list (large dataset) | genetics.rst | SAO-only | Missing | GTK/SAO chrome |
| `images/images/gnuhealth_genetics_genetic_and_protein_diseases.png` | SAO genetic/protein diseases list | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_genetic_and_protein_diseases_form_view.png` | SAO disease form view | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_gen_command.png` | SAO command shortcut for genetics | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_patient_medical_history_matt.png` | Patient medical/genetic history (Matt) | *(orphan)* | SAO-only | Missing | Not cited in RST |
| `images/images/gnuhealth_genetics_variants_phenotypes_cftr.png` | CFTR variants/phenotypes | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_genetics_variants_phenotypes_patient_information_matt.png` | Patient variant phenotype info | genetics.rst | SAO-only | Missing | |
| `images/images/gnuhealth_health_professional.png` | SAO health professional record | `rst/userguide/basics/coremodule/healthprofessionals.rst` | React (partial) `/staff` | Partial | Specialty O2M deeper in SAO |
| `images/images/gnuhealth_his_features.png` | Conceptual circle diagram (Hospital Mgmt / EMR / HIS / Epidemiology / Demographics); typo “MANAGMENT” | `rst/features.rst` | Diagram/branding | N/A | Marketing; not UI sync |
| `images/images/Gnuhealth_lab_test_units.png` | SAO lab units configuration | laboratory.rst | SAO-only config | Missing | |
| `images/images/gnuhealth_party_health_professional.png` | Party form with Health Prof role | healthprofessionals.rst | React (partial) `/parties` `/staff` | Partial | |
| `images/images/GNU_Health_Health_Services_form.png` | SAO Health Services draft with CBC/RFT lines | products.rst (healthcenter) | React (partial) + SAO | Partial | Links lab ↔ billing |
| `images/images/GNU_Health_Lifestyle_Addictions_Alcohol_tab.png` | Patient Lifestyle → Addictions → Alcohol | `rst/userguide/modules/lifestyle.rst` | SAO-only (patient tabs) | Missing | React patient form lacks these tabs |
| `images/images/GNU_Health_Lifestyle_Addictions_Main_tab.png` | Lifestyle Addictions main | lifestyle.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Lifestyle_Addictions_Recreational_Drugs_tab.png` | Lifestyle recreational drugs | lifestyle.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Lifestyle_Diet_and_Exercise_tab.png` | Lifestyle Diet and Exercise | lifestyle.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Lifestyle_Safety_tab.png` | Lifestyle Safety | lifestyle.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Lifestyle_Sexuality_tab.png` | Lifestyle Sexuality | lifestyle.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Full_Synchronization.png` | Orthanc full sync action/UI | `rst/userguide/modules/imaging.rst` | SAO-only (`health_orthanc`) | Missing | |
| `images/images/GNU_Health_Orthanc_Instance_Preview.png` | Orthanc DICOM instance preview | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Integration.png` | Sidebar: Medical Imaging + Orthanc tree | imaging.rst | SAO-only | Missing | React `/imaging` is list/requests only |
| `images/images/GNU_Health_Orthanc_Newly_Synchronization.png` | Orthanc newly-changed sync | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Patients.png` | Orthanc patients list in HIS | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Search_Patient.png` | Orthanc patient search | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Series_Detail.png` | Orthanc series detail | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Series_List.png` | Orthanc series list | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Studies.png` | Orthanc studies with OHIF/Stone viewer links | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Study_Content.png` | Orthanc study content | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_Orthanc_Uploaded_DICOM_File.png` | Uploaded DICOM in Orthanc integration | imaging.rst | SAO-only | Missing | |
| `images/images/GNU_Health_party_person.png` | Party People form — create person/patient roles, demographics, Federation ID | `rst/userguide/basics/configuration.rst` | React (partial) `/parties` | Partial | Setup Hub step 4; UI differs |
| `images/images/GNU_Health_party_person_internal_user.png` | Party linked to internal user | `rst/userguide/healthcenter/accessmanagement.rst` | React (partial) + SAO | Partial | Users/roles Help thin |
| `images/images/GNU_Health_party_with_patient_attribute_set.png` | Party Health tab with Patient role, IDs, insurance | `rst/userguide/patientmanagement/patientmanagement.rst` | React (partial) | Partial | Core registration path |
| `images/images/GNU_Health_patient_main_screen.png` | Full SAO patient form (critical info, conditions, many specialty tabs) | patientmanagement.rst | React (partial) `/patients/:id` | Partial | **React ≠ this UI**; depth is SAO |
| `images/images/GNU_Health_Pediatrics_Newborn.png` | Pediatrics Newborn form (APGAR, QR, sign) | `rst/userguide/modules/pediatrics.rst` | SAO-only | Missing | |
| `images/images/GNU_LIMS_barcode_standards_and_QR_for_samples.png` | Lab sample barcode/QR standards illustration | laboratory.rst | Report/output + SAO LIMS | Missing | |
| `images/images/Gnuhealth_Calendar_Creation.JPG` | SAO Calendar Access Permissions tab | `rst/userguide/modules/calendar.rst` | React (partial) `/calendar` | Partial | Setup Hub step 7 |
| `images/images/Gnuhealth_Calendar_Creation_of_Calendar_in_Evolution.JPG` | **Evolution** desktop CalDAV calendar UI | calendar.rst | External client | N/A | Not IST React/SAO |
| `images/images/Gnuhealth_Calendar_Event_creation.JPG` | Calendar event creation (client) | calendar.rst | External/SAO | N/A / Partial | |
| `images/images/Gynecology_information_in_the_Patient_form_General_tab.png` | Patient OB/GYN General tab | `rst/userguide/modules/gynecology.rst` | SAO-only (`health_gyneco`) | Missing | |
| `images/images/Gynecology_information_in_the_patient_form_Screening_tab.png` | Patient OB/GYN Screening tab | gynecology.rst | SAO-only | Missing | |
| `images/images/HIS_branching.drawio.png` | Git branching strategy diagram (tags through 5.0.0) | *(orphan in RST)* | Diagram/branding | N/A | Dev process; not clinical UI |
| `images/images/How_to_access_the_list_of_appointments_for_a_specific_patient.png` | SAO related-menu path to patient appointments | `rst/userguide/patientmanagement/patientappointment.rst` | React (partial) + SAO relate | Partial | |
| `images/images/How_to_find_all_PSC_records_for_a_patient.png` | SAO path to Pediatric Symptom Checklist | pediatrics.rst | SAO-only | Missing | |
| `images/images/How_to_open_the_list_of_evaluations_for_a_specific_patient.png` | Patient form + Related menu → Evaluations | `rst/userguide/patientmanagement/patientevaluations.rst` | React (partial) `/evaluations` | Partial | Related menu is SAO pattern |
| `images/images/How_to_print_a_wristband_for_a_newborn_in_GNU_Health.png` | SAO print newborn wristband action | pediatrics.rst | SAO-only (+ qrcodes module) | Missing | |
| `images/images/Install_Modules_1.png` | SAO Modules list; mark activation (shows **4.4.0** health pkgs) | `rst/techguide/development/modules.rst` | React (partial) `/modules` + SAO | Partial | **Version outdated** vs 5.0.6 |
| `images/images/Install_Modules_2.png` | SAO Action → Perform Pending Activation/Upgrade | modules.rst | SAO-only for real upgrade | Partial | Setup Hub admin step |
| `images/images/Invoice_record_in_GNU_Health.png` | SAO Customer Invoice draft from lab services | products.rst | SAO-only (deep); React financial stub | Partial | |
| `images/images/Lab_test_types_list.png` | SAO lab test types list | laboratory.rst | SAO-only config | Missing | |
| `images/images/Multiple_lab_tests_can_be_grouped_in_a_single_order.png` | Multi-test lab order grouping | laboratory.rst | React (partial) + SAO | Partial | |
| `images/images/New_lab_order.png` | SAO “Lab: New order” wizard (CBC/LFT/RFT) | laboratory.rst | React (partial) | Partial | Closest to React lab create |
| `images/images/Newborn_wristband_Identification_with_all_the_information_encoded_in_QR.png` | Sample newborn wristband with QR | pediatrics.rst | Report/output | Missing | |
| `images/images/Patient_ID_card_sample_with_QR_Code.png` | Sample patient ID card with photo + QR | patientmanagement.rst, pediatrics.rst | Report/output (qrcodes) | Missing | Not React screen |
| `images/images/Patient_lab_test_report_in_PDF_format.png` | PDF Laboratory Report (CBC with abnormal flags) | laboratory.rst | Report/output | Partial | Print path via SAO |
| `images/images/Patient_list_view.png` | SAO Health/Patients list (Age, PUID, Hospitalized) | patientmanagement.rst | React (partial) `/patients` | Partial | **UI not aligned** with React branding |
| `images/images/Perinatal_and_Intrapartum_Information_dialog_Additional_Info_tab.png` | Obstetrics perinatal dialog Additional Info | `rst/userguide/modules/obstetrics.rst` | SAO-only | Missing | |
| `images/images/Perinatal_and_Intrapartum_Information_dialog_Main_tab.png` | Perinatal Main tab | obstetrics.rst, pediatrics.rst | SAO-only | Missing | |
| `images/images/Perinatal_Monitor_dialog.png` | Perinatal monitor dialog | obstetrics.rst | SAO-only | Missing | |
| `images/images/Prenatal_Evaluation_dialog.png` | Prenatal evaluation dialog (biometry, placenta) | obstetrics.rst | SAO-only | Missing | |
| `images/images/Process_of_paying_an_invoice_in_GNU_Health.png` | SAO Pay Invoice wizard (cash/EUR) | products.rst | SAO-only | Partial | Help payment topic thin |
| `images/images/Puerperium_Monitor_dialog.png` | Puerperium monitor dialog | obstetrics.rst | SAO-only | Missing | |
| `images/images/Sample_of_GNU_Health_HIS_node_federation_queue.png` | Federation Queue list (Queued POST messages) | `rst/userguide/modules/federation/gnuhealthfederation.rst` | SAO-only | Missing | Not UAE HIE |
| `images/images/Scheduler.png` | SAO Administration → Scheduled Actions form | `rst/techguide/development/scheduler.rst` | SAO-only admin | Missing | Cron ops |
| `images/images/Selection_of_the_GNU_Health_Federation_module.png` | SAO Modules list highlighting `health_federation` (**4.2.3** in shot) | gnuhealthfederation.rst | React (partial) list + SAO activate | Partial | Version outdated |
| `images/images/The_Access_Permissions_tab_in_the_Groups_form.png` | Groups form Access Permissions tab | accessmanagement.rst | React (partial) `/groups` | Partial | |
| `images/images/The_appointments_form_in_GNU_Health.png` | SAO appointment form (CalDAV UUID, specialty, urgency) | patientappointment.rst | React (partial) `/appointments` | Partial | **UI differs** |
| `images/images/The_Beds_list_in_GNU_Health.png` | Beds list for institution (Free/Occupied) | `rst/userguide/modules/inpatientmanagement.rst` | React (partial) `/beds` | Partial | Setup Hub Health links beds |
| `images/images/The_dialog_box_to_confirm_the_assignment_of_a_patient_to_a_bed.png` | Bed assignment confirmation dialog | inpatientmanagement.rst | SAO-only wizard | Partial | Admit Help thin |
| `images/images/The_dialog_to_select_a_ICD10-PCS_code.png` | ICD-10-PCS procedure code picker | `rst/userguide/modules/surgery.rst` | SAO-only (+ coding modules) | Missing | React `/procedures` list |
| `images/images/The_Evaluations_Form_in_GNU_Health.png` | Evaluation form Main Info (chief complaint, discharge) | patientevaluations.rst | React (partial) | Partial | Help `wf-consultation` |
| `images/images/The_Evaluations_History_in_GNU_Health.png` | Evaluations list for a patient | patientevaluations.rst | React (partial) | Partial | |
| `images/images/The_Groups_list_in_GNU_Health.png` | Administration Users Groups list | accessmanagement.rst | React (partial) `/groups` | Partial | Setup Hub step 3 |
| `images/images/The_GSC_form_in_GNU_Health.png` | Glasgow Coma Scale form (Eyes/Verbal/Motor → 15) | icu.rst | SAO-only | Missing | Filename “GSC” = GCS |
| `images/images/The_health_professional_can_access_all_the_patient_lab_tests_from_the_main_screen.png` | Patient → related lab results access | laboratory.rst | React (partial) + SAO | Partial | |
| `images/images/The_Hospitalization_form_in_GNU_Health.png` | Hospitalization administrative form (bed, admit reason, discharge) | patientappointment.rst | React (partial) beds; form SAO | Partial | |
| `images/images/The_Hospitalizations_list_in_GNU_Health.png` | Hospitalizations list | patientappointment.rst | SAO-only / thin React | Partial | |
| `images/images/The_list_of_all_appointments_in_GNU_Health.png` | Appointments list with status tabs (Confirmed, Checked in, …) | patientappointment.rst | React (partial) | Partial | Status tabs may differ in React |
| `images/images/The_list_of_appointments_for_a_specific_patient.png` | Patient-scoped appointments list | patientappointment.rst | React (partial) | Partial | |
| `images/images/The_Members_tab_in_the_Groups_form.png` | Groups Members tab | accessmanagement.rst | React (partial) | Partial | |
| `images/images/The_Obstetric_History_stores_information_about_a_pregnancy.png` | Obstetric history pregnancy record | obstetrics.rst | SAO-only | Missing | |
| `images/images/The_PSC_form_in_GNU_Health.png` | Pediatric Symptom Checklist form | pediatrics.rst | SAO-only | Missing | |
| `images/images/The_Revised_Cardiac_Risk_Index_dialog_in_GNU_Health.png` | Surgery RCRI dialog | surgery.rst | SAO-only | Missing | |
| `images/images/The_socioeconomics_module_in_GNU_Health.png` | Patient Socioeconomics tab (SES, risk checkboxes) | `rst/userguide/modules/socioeconomics.rst` | SAO-only | Missing | Highlighted tab in screenshot |
| `images/images/The_Surgeries_form_in_GNU_Health.png` | Full surgery record (checklist, procedures, OR) | surgery.rst | React (partial) `/procedures` | Missing Help | Deep form SAO-only |
| `images/images/The_Surgeries_tab_in_the_Patients_form.png` | Patient Surgeries tab | surgery.rst | SAO-only tab | Missing | |
| `images/images/The_User_tab_in_the_Users_form.png` | Users form User tab | accessmanagement.rst | React (partial) `/users` | Partial | |
| `images/images/Update_the_service_document_with_a_new_lab_test.png` | Update health service from lab request | laboratory.rst | SAO-only action | Partial | Billing bridge |

*Paths in the table are relative to `docs/upstream/original/`.*

---

## Cluster rollup (for planning)

| Cluster | # images | Typical IST UI | Doc posture |
|---------|--------:|----------------|-------------|
| ghcontrol / install ops | 16 | Ops/TUI only | N/A for clinical Help |
| Laboratory (+ reports) | 14 | React order; SAO results/wizards | Partial → strengthen Help |
| Orthanc / imaging | 11 | SAO | Missing |
| Genetics | 10 | SAO | Missing |
| Patient / party / ID | 8 | React partial | Partial |
| Appointments / hospitalizations | 8 | React partial + SAO | Partial |
| Obstetrics / perinatal | 7 | SAO | Missing |
| Lifestyle | 6 | SAO patient tabs | Missing |
| Access management | 5 | React partial | Partial |
| Surgery | 4 | React list; SAO depth | Missing Help |
| ICU | 3 | SAO | Missing |
| Pediatrics / newborn | 4 | SAO | Missing |
| Federation | 3 | SAO + diagram | Partial/Missing |
| Health services / invoice / pay | 4 | SAO deep | Partial |
| Calendar | 3 | React list; Evolution N/A | Partial / N/A |
| Modules install (SAO) | 2 | React + SAO | Partial |
| Branding / features / branching | 4 | N/A | N/A |
| Other (scheduler, socioeconomics, NTD, HP, command) | ~11 | Mostly SAO | Missing/Partial |

---

## Cross-references

- Feature matrix: [`GNU_Health_vs_IST_HIS_comparison.md`](./GNU_Health_vs_IST_HIS_comparison.md)
- Docs depth: [`DOCUMENT_CONTENT_PARITY.md`](./DOCUMENT_CONTENT_PARITY.md)
- Branding: [`IST_HIS_Naming_and_Branding_Policy.md`](./IST_HIS_Naming_and_Branding_Policy.md)
- Setup Hub code: `frontend/src/pages/SetupHubPage.tsx` (order 1–9)
- Help Centre: `frontend/help-content/`
- Upstream RST: `docs/upstream/original/rst/`

---

## Appendix: Review coverage note

All **119** filenames were inventoried and mapped to RST (or marked orphan). Visual inspection was performed on **all major clusters** (≈45+ files opened with the image reader), including every high-impact how-to class (patient, appointment, lab wizards, beds/hospitalization, surgery, ICU trio, Orthanc, genetics sample, OB prenatal, lifestyle, finance pay, groups, modules, ghcontrol, federation diagram/queue, branding). Remaining files in the same cluster share the same SAO/GTK visual language and module context; descriptions for those are derived from filename + RST caption + sibling screenshots. **None** of the clinical screenshots depict the IST React SPA chrome.

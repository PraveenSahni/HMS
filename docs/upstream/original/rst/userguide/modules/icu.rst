.. _userguide-modules-icu:intensive_care_unit:

Intensive Care Unit
===================

.. _userguide-modules-icu:intensive_care_unit-introduction_to_the_icu_functionality:

Introduction to the ICU Functionality
-------------------------------------

The module :code:`health_icu` provides basic functionality for Intensive Care Units (ICU). It covers both Intensive Care medicine and the processes related to the Intensive Care Unit, such as procedures and stock management.

The functionality is divided into two major sections:

* Patient ICU Information
* Patient Roundings

.. _userguide-modules-icu:intensive_care_unit-patient_icu_information:

Patient ICU Information
-----------------------

All information about a patient that is related to the ICU is managed in the *Health → Hospitalization → Intensive Care → Patient ICU Info* section. Every *Patient ICU Info* record is linked to a *Hospitalizations* record (not to a *Patients* record directly).

The *Patient ICU Info* form allows you to have an idea of the patient status, days since admission at ICU and use of mechanical ventilation, among other functionalities.

By clicking the *Relate* button you can directly create and evaluate the following data for a given patient:

* Acute Physiology and Chronic Health Evaluation II (APACHE II)
* Electrocardiograms (ECG)
* Glasgow Coma Scale (GCS)

.. _userguide-modules-icu:intensive_care_unit-patient_icu_information-apache_ii:

APACHE II
^^^^^^^^^

The Acute Physiology and Chronic Health Evaluation II (APACHE II) is a classification system for the severity of disease. It is applied within 24 hours of admission of a patient to an ICU. A score between 0 and 71 is computed based on several measurements, where higher scores correspond to more severe disease and a higher risk of death. (Read more about :wikipedia:`APACHE II`.)

.. thumbnail:: ../../images/APACHE_II_Score_form_in_the_ICU_module_of_GNU_Health.png
    :title: APACHE II Score form in the ICU module of GNU Health
    :align: right
    :width: 30%

The APACHE II form in GNU Health contains the following information:

* *Registration Code:* Link to the inpatient record of the patient (mandatory).
* *Date*: Date and time of the evaluation (mandatory).
* *Age*
* *Temperature*
* *MAP*
* *Heart Rate*
* *Resporatory Rate*
* *FiO2*
* *PaO2*
* *PaCO2*
* *A-a DO2*
* *pH*
* *Sodium*
* *Potassium*
* *Creatinine*
* *Hematocrit*
* *WBC*
* *ARF:* Check if appropriate.
* *Chronic condition:* Check if appropriate.
* *Score:* The resulting APACHE II score (calculated automatically).

.. _userguide-modules-icu:intensive_care_unit-patient_icu_information-ecg:

ECG
^^^

In the *Health → Hospitalizations → Intensive Care → ECG* section of GNU Health you can document any electrocardiograms taken from a patient.

.. thumbnail:: ../../images/ECG_form_of_GNU_Health.png
    :title: ECG form of GNU Health
    :align: right
    :width: 30%

The *ECG* form provides the following information:

* *Registration Code:* Link to the inpatient record of the patient (mandatory).
* *Date:* Date and time when the ECG was taken (mandatory). **Please note: Currently you have not access to this field in the form view, only in the list view.**
* *Lead:* Choose between I, II, III, aVF, aVR, aVL, V1, V2, V3, V4, V5, or V6.
* *Axis:* Choose between "Normal axis", "Left deviation", "Right deviation", or "Extreme right deviation" (mandatory).
* *Rate:* (mandatory)
* *Pacemaker:* Choose between "Sinus node", "Atrioventricular", or "Purkinje" (mandatory).
* *Rhythm:* Choose between "Regular" or "Irregular" (mandatory).
* *PR*
* *QRS*
* *QT*
* *ST Segment:* Choose between "Normal", "Depressed", or "Elevated" (mandatory).
* *T Wave Inversion*
* *Interpretation:* (mandatory)

At the bottom of the form you can add an image of the electrocardiogram plot.

.. _userguide-modules-icu:intensive_care_unit-patient_icu_information-gcs:

GCS
^^^

The Glasgow Coma Scale (GCS) is a standard to evaluate the level of consciousness of neurological patients. Based on three factors - eye opening, verbal response, and motor response - an overall score between 3 and 15 is calculated. A higher value indicates a higher level of consciousness and a better chance to recover. (Read more about the :wikipedia:`Glasgow Coma Scale`.)

.. thumbnail:: ../../images/The_GSC_form_in_GNU_Health.png
    :title: The GSC form in GNU Health
    :align: right
    :width: 30%

The *GCS* form in GNU Health provides the following fields:

* *Registration Code:* Link to the inpatient record of the patient (mandatory).
* *Date:* Date and time when the GCS was evaluated (mandatory).
* *Eyes:* Choose between "1: Does not open eyes", "2: Opens eyes in response to painful stimuly", "3: Opens eyes in response to voice", or "4: Opens eyes spontanously" (mandatory).
* *Verbal:* Choose between "1: Makes no sounds", "2: Incomprehensible sounds", "3: Utters inappropriate words", "4: Confused, disoriented", "5: Oriented, converses normally" (mandatory).
* *Motor:* Choose between "1: Makes no movements", "2: Extension to painful stimuli (decerebrate response)", "3: Abnormal flexion to painful stimuli (decorticate response)", "4: Flexion / Withdrawal to painful stimuli", "5: Localizes painful stimuli", or "6: Obeys commands" (mandatory).
* *Glasgow:* The resuling score (calculated automatically).

.. _userguide-modules-icu:intensive_care_unit-patient_rounding:

Patient Rounding
----------------

The :code:`health_icu` module adds the *ICU* tab to the *Roundings* form (which can be found in the *Health → Nursing → Roundings* section).
In this assessment (that can have different frequencies, depending on the center policies), you should enter the basic information starting at the *Main* tab first; once you are done with this tab, switch to the *ICU* tab. The assessment is divided into the following sections:

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-neurologic:

Neurologic
^^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Neurologic

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-respiratory_(incl._x-ray):

Respiratory (incl. X-Ray)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Respiratory

The ICU rounding allows to place an X-ray (or other imaging diagnosis image). Unlike attachments related to the object, that you can also use, this image is even more contextual and graphic. Of course, this image should be very recent to the evaluation itself.

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-drainages:

Drainages
^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Drainages

Chest drainages are input from a One2Many widget. This permits to have as many as in the patient, and with their own characteristics.

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-cardiovascular:

Cardiovascular
^^^^^^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Cardiovascular

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-blood_and_skin:

Blood and Skin
^^^^^^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Blood and Skin

.. _userguide-modules-icu:intensive_care_unit-patient_rounding-digestive_and_abdomen:

Digestive and Abdomen
^^^^^^^^^^^^^^^^^^^^^

.. todo:: Fill Modules in Detail - ICU - Digestive and Abdomen

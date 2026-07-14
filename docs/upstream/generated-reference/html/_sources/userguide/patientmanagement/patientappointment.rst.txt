.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management:

Patient Appointment and Admission Management
============================================
.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments:

Appointments
------------

.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments-information_stored_per_appointment:

Information stored per appointment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. thumbnail:: ../../images/The_appointments_form_in_GNU_Health.png
    :title: The appointments form in GNU Health.

Each appointment can store the following information:

* *Appointment ID*
* *Patient*: Select the name of a registered patient.
* *Visit*: Type of Appointment
* *State*: The current state of the appointment. Can for example indicate that the patient has already checked in or that the appointment was cancelled.
* *Health Professional*: The name of the appointed health professional.
* *Institution*: The name of the institution. The institution is likely a health center.
* *Date*
* *Urgency*: Level of Emergency
* *CalDAV Event*:
* *Inpatient Registration*: Links a patient that currently inhabits the institution.
* *Type*: Inpatient vs. Outpatient. Inpatient indicates the patient currently inhabits the institution.
* *Specialty*: What the appointed health professional specializes in.
* *Additional Information*

.. todo:: Explain CalDAV Event

.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments-list_of_all_appointments:

List of all appointments
^^^^^^^^^^^^^^^^^^^^^^^^

.. thumbnail:: ../../images/The_list_of_all_appointments_in_GNU_Health.png
    :title: The list of all appointments in GNU Health.

From the main menu of Health you have the possibility to get into the *Appointments* section. Here you see the list of all the appointments stored in the system.

* *Confirmed* tab: This list reflects all existing appointments for which the state of the appointment is set to "confirmed".
* *Checked in* tab: This list reflects all existing appointments for which the state of the appointment is set to "Checked in".
* *Free* tab: This list reflects all available timeslots where you can create a new appointment.
* *No Shows* tab: This list reflects all existing appointments for which the state of the appointment is set to "No Show".
* *All* tab: This list combines all the other lists mentioned above.


.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments-list_of_all_appointments-appointments_calendar:

Appointments Calendar
"""""""""""""""""""""

The subsection *Appointments Calendar* allows you to display all appointments stored in the system in a calendar view.

.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments-list_of_all_appointments-appointments_report:

Appointments Report
"""""""""""""""""""

The subsection *Appointments Report* allows you to display all appointments of a certain health professional in a certain time period.

.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-appointments-list_of_appointments_for_a_specific_patient:

List of appointments for a specific patient
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. thumbnail:: ../../images/How_to_access_the_list_of_appointments_for_a_specific_patient.png
    :title: How to access the list of appointments for a specific patient.

To access the list of all appointments for a specific patient only you typically start from the patients record. Simply click the *Relate* button and choose *Appointments*.

.. thumbnail:: ../../images/The_list_of_appointments_for_a_specific_patient.png
    :title: The list of appointments for a specific patient.

.. _userguide-patientmanagement-patientappointment:patient_appointment_and_admission_management-hospitalizations:

Hospitalizations
----------------

.. thumbnail:: ../../images/The_Hospitalizations_list_in_GNU_Health.png
    :title: The Hospitalizations list in GNU Health.

From the main menu you will have access to the *Hospitalizations* area. From here you will manage any kind of action related to the patient’s admission to or discharge from the hospital.

.. thumbnail:: ../../images/The_Hospitalization_form_in_GNU_Health.png
    :title: The Hospitalization form in GNU Health.

When you create a new Hospitalization record there are different tabs that will help you gather more information:

* *Administrative Data*: In this section you can enter all the administrative information related to the patient admission.
* *Nutrition*: The information in this section helps the hospital center to know more about the patient’s diet, belief etc.
* *Medication Plan*: All the information entered here is related to medication during the admission (indication, treatment period, dosage etc.).
* *Care Plan*: Here you will input all the data about nursing plan and discharge plan.

For more information about hospitalizations please refer to the :ref:`userguide-modules-inpatientmanagement:inpatient_management` chapter.

.. _techguide-fhir-usage:usage:

Usage
=====
.. _techguide-fhir-usage:usage-fhir_overview:

FHIR Overview
-------------
**Fast Healthcare Interoperability Resources (FHIR)** is a standard for exchanging healthcare information electronically developed by HL7. The standard defines a common interface for medical software interoperability. For more reading, look at the `FHIR standard <https://www.hl7.org/implement/standards/fhir/>`_.

.. _techguide-fhir-usage:usage-url_structure:

URL Structure
-------------

The FHIR standard defines a REST API, a set of interactions with each resource. Each resource handles different types of information. Currently, the GNU Health FHIR server supports 12 resources:

* **Conformance**: Describes the server's FHIR capabilities.
* **Patient**: Patient information, like email, address, SSN, etc.
* **DiagnosticReport**: Completed lab tests, but not the data
* **Observation**: Lab data, like Uric Acid values
* **Practitioner**: Health professionals and their information
* **Procedure**: Surgeries/operations
* **Condition**: Diseases/diagnoses
* **FamilyHistory**: Family histories of patients
* **Medication**: Medications (not prescriptions!)
* **MedicationStatement**: Medications taken by a patient
* **Immunization**: Immunizations
* **Organization**: Institutions, departments, companies, etc.

Each resource has its own endpoint. For example, the **Patient** endpoint is found at :code:`/Patient`, the **DiagnosticReport** endpoint at :code:`DiagnosticReport`, and so on. The only exception to this naming schema is the **Conformance** endpoint which is found at :code:`/` and :code:`/metadata`.

The interactions use HTTP verbs. Simple read and search interactions with GET, and so on.

For further reading into the REST design, read the `documentation <https://www.hl7.org/implement/standards/fhir/http.html>`_

.. note::
        Currently, the GNU Health FHIR server has no write functionality.

.. _techguide-fhir-usage:usage-authentication:

Authentication
--------------

**All resources, except for Conformance, require authentication**. The server authenticates with the user credentials of the underlying GNU Health/Tryton server. Login with your user credentials at :code:`/auth/login`. Logout at :code:`/auth/logout`. There is a simple welcome page for logged-in users at :code:`/auth/home`.

.. _techguide-fhir-usage:usage-searching_/_listing:

Searching / Listing
-------------------

To search a resource, simply add arguments to the endpoint to refine the search. For example, :code:`/Patient`, will return all the patients on the server. :code:`/Patient?name=Matt` will return all the patients with 'Matt' in their name.

.. note::
        There are still search criteria for the GNU Health FHIR server to implement, as using more than one search argument

Refer to the FHIR documentation for more information.

.. _techguide-fhir-usage:usage-test_server_examples:

Test Server Examples
--------------------

Some examples with the community FHIR server (may need to sign in):

* `List all patients <https://federation.gnuhealth.org:8700/Patient>`_
* `Show info for patient id #1 <https://federation.gnuhealth.org:8700/Patient/1>`_
* `Show health professionals matching the name "Cameron" <https://federation.gnuhealth.org:8700/Practitioner?name=Cameron>`_
* `List all surgeries <https://federation.gnuhealth.org:8700/Procedure>`_
* `List Lab results <https://federation.gnuhealth.org:8700/Observation>`_

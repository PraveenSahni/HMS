.. _userguide-basics-coremodule-prescriptions:prescriptions:

Prescriptions
=============
.. _userguide-basics-coremodule-prescriptions:prescriptions-about_prescriptions:

About Prescriptions
-------------------

Prescriptons can be found in the *Health → Prescriptions* section of GNU Health. However, since in most cases you only need to see the prescriptions of a specific patient, the recommended way is to open a *Patient* record and to switch to *Prescriptions* using the *Relate* button.

.. _userguide-basics-coremodule-prescriptions:prescriptions-information_stored_in_prescriptions:

Information Stored in Prescriptions
-----------------------------------

Each *Prescriptions* record stores some general information:

* *Patient*: Link to a patient (mandatory)
* *Prescription ID*
* *Prescription Date*
* *Prescribed by*: Link to a health professional
* *Pharmacy*: Link to a pharmacy (i.e. a *Party* record with the *Pharmacy* flag set)
* *Pregnancy Warning*
* *Prescription Verified*

The information about the medicaments can be found in the *Presciption Lines* section. Each *Prescription Line* consists of the following fields:

* *Medicament*: Link to a :ref:`Medicament<userguide-basics-coremodule-medicaments:medicaments>`
* *Indication*: Link to a *Pathology Info* record
* *Allow Substitution*
* *Print*
* *Form*: Link to a *Drug Form* record
* *Administration Route*: Link to another *Drug Form* record
* *Start*: Date and time
* *End*: Date and time
* *Dose*
* *Dose Unit*: Select an existing dose unit or create a new one
* *Times*
* *Frequency*
* *Admin Hours*
* *Frequency*
* *Unit*: Choose from "Seconds", "Minutes", "Hours", "Days", "Weeks", or "When required"
* *PRN*: Short for pro re nata (= use it as needed)
* *Treatment Duration*
* *Treatment Period*: Choose from "Minutes", "Hours", "Days", "Weeks", "Months", "Years", or "Indefinite"
* *Review*: Date and time
* *Units*
* *Refills #*
* *Comment*

Note: Only a fraction of these fields are visible in the list view, so make sure to open a *Prescription Line* in the form you to have access to all fields.

.. _userguide-basics-coremodule-prescriptions:prescriptions-prescription_stock:

Prescription stock
------------------

Prescriptions can be tracked and inventoried by means of :ref:`userguide-modules-stockmanagement:stock_management`.

To quickly create a new stock move, right-click the prescription → *Actions* → *Create Prescription Stock Move*. To view previous stock moves, right click the prescription → *Relate* → ''Stock Moves [readonly]''.

Note: Do not create new *Stock Moves* from the Relate view.

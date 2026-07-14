.. _userguide-basics-coremodule-immunizations:immunizations:

Immunizations
=============
GNU Health includes immunization functionality in the core module. This includes immunization schedules per country and year, the vaccination process, and the person immunization history and status report, to name the main aspects.

.. _userguide-basics-coremodule-immunizations:immunizations-the_vaccine:

The Vaccine
-----------

In GNU Health, vaccines are part of the medicament model, those that have set the vaccine attribute. GNU Health includes as default the vaccines that are part of the WHO essential list of medicines module, but you can set up your own set.

.. _userguide-basics-coremodule-immunizations:immunizations-the_immunization_schedule:

The Immunization schedule
-------------------------

*Health → Configuration → Immunization Schedule*



After you have the list of vaccines, you can create different immunization schedules. Each immunization schedule has the following fields:

* *Code*: Unique identifier for the schedule
* *Country*: The name of the country for this schedule
* *Year*: The year of this immunization schedule
* *Active*: This field indicates whether this particular schedule is on use. Among other things, it's taken into account when checking the immunization status of the person.
* *Description*: Short description of the schedule
* *Vaccines*: This widget lists all the vaccines on the schedule, and the main attributes. The details for this model will be explained in the next section.

.. _userguide-basics-coremodule-immunizations:immunizations-the_immunization_schedule-immunization_schedule_line:

Immunization Schedule Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

As described above, each immunization schedule is composed of vaccines, which their own peculiarities. For each vaccine, the following attributes apply:

* *Vaccine*: The name of the vaccine
* *Scope*: Recommendation status level . It can be systematic, recommended or limited to risk groups
* *Remarks*: Additional information and for this vaccine
* *Dose*: Dose or booster number
* *Age*: Age of the person when should be applied
* *Time unit*: Days, weeks, months or years

.. _userguide-basics-coremodule-immunizations:immunizations-the_vaccination_process:

The Vaccination Process
-----------------------

The following patient shortcut will take you both to the vaccination history and to the vaccination process itself.

*Health → Patient → (relate action) Vaccinations*

The vaccination form to register the information associated to the immunization itself. The main sections are:

* *Header*: It contains the patient name and the vaccine to administer
* *Administration section*: The amount of vaccine and the administration site
* *Stock information*: The stock and lot associated to the vaccine. GNU Health also allows to enter the picture of the vaccine label. This is quite important, since it contains quite a bit of information that can be useful in the future. Please include it whenever is possible.
* *Notes*: Extra information associated to the immunization process itself. There is also a wizard that allows to create the stock move of the product related to the vaccine, once this has been used / discarded.
* *Administrative Information*: Information related to the date, institution and to the health professional who applied the vaccine. The Vaccination process has two states. Those are *In Progress* and *Signed*. Once the immunization process has been signed by the health professional, the record becomes read-only.

.. _userguide-basics-coremodule-immunizations:immunizations-immunization_status_report:

Immunization Status Report
--------------------------

We can check the Patient immunization status by executing the following report:

*Health → Patient → (report) Immunization Status Report*

The report will ask you for the specific schedule, and the result will show the person immunization status for that specific schedule. Along with the patient information and the print date, the  immunization report will show each vaccine for the chosen schedule, its doses, age when they should be applied and the current status. Always verify and double check the person immunization status against any other historical records the person may have.

.. _userguide-basics-coremodule-immunizations:immunizations-vaccine_stock:

Vaccine stock
-------------

Vaccines can be tracked and inventoried by means of :ref:`userguide-modules-stockmanagement:stock_management`.

To quickly create a new stock move, right-click the vaccine → *Actions* → *Create Vaccine Stock Move*. To view previous stock moves, right click the vaccine → *Relate* → ''Stock Moves [readonly]''.

Note: Do not create new *Stock Moves* from the Relate view.

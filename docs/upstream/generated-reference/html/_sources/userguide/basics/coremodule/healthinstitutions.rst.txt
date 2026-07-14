.. _userguide-basics-coremodule-healthinstitutions:health_institutions:

Health Institutions
===================

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-introduction_to_health_institutions:

Introduction to Health Institutions
-----------------------------------

The Health Institution plays a central role in GNU Health. As a matter of fact, is the first thing you will have to create in the installation.

The health institution is a model. It is linked to the party model, but it has many other attributes.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-creating_and_updating_health_institutions:

Creating and Updating Health Institutions
-----------------------------------------

The very first health institution that you create is special because it is also your **company**. Please refer to the :ref:`techguide-installation-vanilla:vanilla_installation-creating_a_company` chapter for more details.

Health institutions can be accessed in the *Health → Institutions* section.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities:

Health Institution Facilities
-----------------------------

A health institution can have multiple facilities and resources, such as buildings, wards, operating rooms, beds or units.

The best way to access the health institution facilities is by clicking on the *Relate* button in the *Institutions* form as shown in the screenshot. One of the benefits of using related records from the institution form is that the related facility will contain the parent center, optimizing data entry and minimizing human error.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-beds:

Beds
^^^^

Beds are the most basic facilities in a health institution. Creating a bed record for each physical bed available is important for capacity planning and for finding a patient. Each bed belongs to a ward.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-beds-configuring_beds:

Configuring Beds
""""""""""""""""

Bed records in GNU Health can be managed in the **Health → Configuration → Institutions → Beds** section. For each **Bed** record you need a corresponding **Product Variant** record (which stands for the individual bed) plus a **Product** record (which stands for the bed category and defines its price).

Note: If you are not familiar with products in Tryton, there is more information about this concept in the chapter :ref:`userguide-healthcenter-products:products_and_services_management`. But if you just want to configure some beds at this moment and don't care about the details, then simply read on.

Configuring beds in GNU Health is a three step process:

1. For every category of beds, create a product record and enter the price the patient will be charged. Example:

.. list-table::
        :widths: 25 25 25 25
        :header-rows: 1

        * -
          - **Standard Bed**
          - **Luxury Bed**
          - **ICU Bed**
        * - **Price per day**
          - USD 150
          - USD 250
          - USD 500


1. For every bed available in your health institution, create a product variant record and check the *Bed* checkbox. Every variant will need a code as an identifier, but you are free to use any combination of characters and numbers to match the numbering scheme in your institution. Example:

.. list-table::
        :widths: 25 25 25 25
        :header-rows: 1

        * -
          - **Standard Bed**
          - **Luxury Bed**
          - **ICU Bed**
        * - **Variants**
          - * M101
            * M102
            * M103
            * M105
          - * M201
            * M202
            * M203
          - * ICU10
            * ICU20
            * ICU30

3. For every bed available in your health institution, create a bed record and assign it to the corresponding product variant record. A bed record stores additional information about a bed like its status (free, reserved, occupied, ...) or the ward it belongs to. If you skip this step you will not be able to assign a patient to a bed in the hospitalization process!

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-buildings:

Buildings
^^^^^^^^^

Buildings simply have a name and a code. At the moment you can not enter more information.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-buildings-configuring_buildings:

Configuring Buildings
"""""""""""""""""""""

Creating and editing buildings is straight forward. The only thing to keep in mind is that both the name and the code of a building need to be unique within a given health institution.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-wards:

Wards
^^^^^

Each ward belongs to one building (the physical location) and one unit (the organisational entity).

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-wards-configuring_wards:

Configuring Wards
"""""""""""""""""

Configuring wards is straight forward. However, the *Wards* form allows you to enter a lot of details about a ward:

* *Name:* The ward name is mandatory and must be unique within a health institution.
* *Building:* Link to an existing building or create a new one.
* *Floor Number:* Indicate the floor within a building.
* *Unit:* Link to an existing unit or create a new one.
* *Number of beds:* This field is for information only. It does not reflect the number of beds you have configured for your health institution.
* *Gender:* Indicate if a ward is gender specific. (If not, set it to "Unisex" which is the default value.)
* *Status:* Indicate if a ward has capacity for more patients. (Choose between "Beds available", "Full", or "Not available".)

The wards form allows you to indicate some special features as well:

* Telephone access
* Air conditioning
* Private bathroom
* Guest sofa-bed
* Television
* Internet access
* Refrigerator
* Microwave

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-operating_rooms:

Operating Rooms
^^^^^^^^^^^^^^^

Each operating room belongs to one building (the physical location) and one unit (the organizational entity).

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-operating_rooms-configuring_operating_rooms:

Configuring Operating Rooms
"""""""""""""""""""""""""""
The configuration of operating rooms is straight forward. A name is mandatory and must be unique within a given health institution. Assigning an operation room to a building and/or a unit is optional. Further information about the operation room can be stored in the *Extra Info* field.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-units:

Units
^^^^^

Units simply have a name and a code. At the moment you can not enter more information.

.. _userguide-basics-coremodule-healthinstitutions:health_institutions-health_institution_facilities-units-configuring_units:

Configuring Units
"""""""""""""""""

Creating and editing units is straight forward. The only thing to keep in mind is that both the name and the code of a unit need to be unique within a given health institution.

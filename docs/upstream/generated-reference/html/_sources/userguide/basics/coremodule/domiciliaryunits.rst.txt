.. _userguide-basics-coremodule-domiciliaryunits:domiciliary_units:

Domiciliary Units
=================


A Domiciliary Unit (DU) represents a human dwelling. It is composed of intra (domiciliary) and extra (peridomiciliary) spaces. The DU is a physical entity that denotes the place where one or more people live regularly.

Since it is a physical location, it can always be geo-referenced by latitude and longitude, and many times it will have an associated address (street, ZIP code, city). This DU information should always be provided, since it is key determinant of health. Diseases like dengue fever and Chagas disease are intimately related to the DU condition (see :ref:`userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases` for details).

.. _userguide-basics-coremodule-domiciliaryunits:domiciliary_units-the_*domiciliary_units*_form:

The *Domiciliary Units* Form
----------------------------

The *Domiciliary Units* form can be found at *Health → Demographics → Domiciliary Units* in the main navigation of GNU Health.

A domiciliary unit can be described by the following information:

* *Code*: A unique identifier of the dwelling. This field is required.
* *Description*: Short description of the DU.
* *Address*: Street, number, and other subdivisions (province, city, municipality, district, ... )
* *Latitude* and *Longitude*
* *OSM Map URL*: The OpenStreetMap URL is created automatically from the coordinates or the DU address. (If latitude and longitude are not provided, then the OSM Map URL will be generated based on the address components. However, latitude and longitude will usually give you a more accurate reference.)
* *General Conditions*: A summary of the living conditions. This field should be filled in all the times, since it's one of the most descriptive about the DU.
* *Type of Dwelling*: Single house, apartment, townhouse, ...
* *Infrastructure*: Electricity, gas, potable water, sewers, ...
* *Operational Sector*: The area that this DU belongs. Very important to know which operational area is responsible to take different health care actions (health promotion, healthcare area, ambulace action region, ...)

* *Members*: In this section a list with all inhabitants of a DU is shown. They may be or may not be family members. Each person should be associated to a DU.

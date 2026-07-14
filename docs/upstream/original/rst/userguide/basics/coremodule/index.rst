.. _userguide-basics-coremodule-index:the_core_module:

The core module
===============
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   healthinstitutions
   domiciliaryunits
   individuals
   bookoflife
   families
   healthprofessionals
   medicaments
   prescriptions
   vitalrecords
   immunizations
   procedures

.. todo:: Take and add new screenshots like here: https://en.wikibooks.org/wiki/GNU_Health/The_core_module

As we have mentioned already in previous sections of the book, GNU Health is composed of different modules which will provide specific functionality to your health center.

The module **health** is at the center of GNU Health. This module contains the core models and classes, so the rest of the modules will just inherit them. This gives modularity and scalability, without leaving behind the most important building blocks in public health. Some of the models found in the core module are:

* Individuals
* Families
* Domiciliary Units
* Operational Sectors
* Health Centers
* Diseases
* Patient
* Patient Evaluation / Encounters
* Medicaments
* Prescriptions
* Procedures

There are many others models in the core module, but this subset will give you an idea of the concept. If you are not a programmer, you don't really have to worry much about how GNU Health deals internally with dependencies and inter-module communication. For example, if you want to install the pediatrics module **health_pediatrics**, it will automatically mark the core module **health** for installation, as a dependency.

To learn more about GNU Health modules, please refer to the :ref:`techguide-development-models:models` chapter.

In this documentation, we will cover the functionality of the core module first before exploring the possibilities of the other modules.

.. _userguide-basics-coremodule-index:the_core_module-people_before_patients:

People before Patients
^^^^^^^^^^^^^^^^^^^^^^

If we want to be good in a Public Health system, the first thing we need to do is knowing our population. As I say, *we need to deal with people before patients* . Whenever possible, the health center should have a census, and the list of *domiciliary units* (DU) and their conditions, at least of those habitants that are part of the *operational sector* covered by the health center.

From a functional and implementation point of view, we should see the GNU Health core module objects as the first ones to be assessed. The process of collecting this information will get our health center involved with the community. In the next chapters we will be covering how to setup a Domiciliary Unit (DU); an Individual; the habitants of a DU; Families ; Operational Areas and Operational Sectors.

Once you have that information in place, you will be able to give a new attribute to the individual when she or he first come to your office, the patient attribute. As you can see, there are precious information and actions that can be done in Public Health before dealing with a single patient.

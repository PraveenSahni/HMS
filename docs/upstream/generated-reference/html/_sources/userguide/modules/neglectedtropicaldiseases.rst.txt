.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases:

Neglected Tropical Diseases
===========================

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-introduction_to_neglected_tropical_diseases:

Introduction to Neglected Tropical Diseases
-------------------------------------------

Neglected tropical diseases (NTD) are a group of infections which are common in developing regions of Africa, Asia, and the Americas. They are medically diverse in terms of pathogens, prevention measures, and treatments. Compared to the big three diseases targeted by the `UN Millennium Development Goal No. 6 <https://www.un.org/millenniumgoals/aids.shtml>`_ (HIV/AIDS, tuberculosis, and malaria), NTDs get less funding for treatment and research. The World Health Organisation (WHO) has prioritized 17 neglected tropical diseases which are common in almost 150 countries, affecting more than 1.4 billion people. (Read more about :wikipedia:`neglected tropical diseases`.)

Note: To use the functionality described in this chapter you must have the modules :code:`health_ntd`, :code:`health_ntd_chagas`, and :code:`health_ntd_dengue` installed. (:ref:`techguide-development-modules:modules`)

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-chagas_disease:

Chagas Disease
--------------

The Chagas disease is caused by a protozoa and spread by contact with infected feces of the triatomine bug. The protozoan can enter the body via the bug's bite, skin breaks, or mucous membranes. Infection can result from eating infected food and coming into contact with contaminated bodily fluids. There are approximately 15 million people infected with Chagas disease. The chance of morbidity is higher for immuno-compromised individuals, children, and elderly, but very low if treated early. The Chagas disease can be diagnosed through a serological test (although the test is not very accurate) and treated etiologically or with drugs (although the drugs have severe side effects). (Read more about :wikipedia:`Chagas disease`.)

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-chagas_disease-chagas_related_surveys:

Chagas Related Surveys
^^^^^^^^^^^^^^^^^^^^^^

The module :code:`health_ntd_chagas` adds the *Chagas DU Survey* form to GNU Health. This allows you to evaluate a domiciliary unit for risks regarding the Chagas disease. You can find this survey by opening the *Domiciliary Units* form and choosing the *Chagas DU Survey* via the *Relate* button in the toolbar.

.. thumbnail:: ../../images/Chagas_DU_Survey_form_in_GNU_Health.png
    :title: Chagas DU Survey form in GNU Health
    :align: right
    :width: 30%

The *Chagas DU Survey* allows to store the following information about a domiciliary unit:

* *Survey Code:* A code to identify the survey (created automatically).
* *DU:* The domiciliary unit which was evaluated (set automatically).
* *Date:* The date of the evaluation.
* *Status:* Choose from "Initial", "Unchanged", "Improved", or "Worsen" to give a summary of your findings.

Presence of triatomines:

* *Triatomines:* Check if triatomines were found.
* *Nymphs:* Check if nymphs were found.
* *Domiciliary:* Check if triatomines were found in the house.
* *Peri-Domiciliary:* Check if triatomines were found around the house.
* *Vector:* Choose from "T. infestans", "T. brasiliensis", "R. prolixus", "T. dimidiata", or "P. megistus".

Areas to improve:

* *Roof:* Check if appropriate.
* *Walls:* Check if appropriate.
* *Floor:* Check if appropriate.
* *Peri-domiciliary:* Check if the situation around the house (rather than the house itself) needs improvement.

Preventive measures:

* *Bug Traps:* Check if bug traps are in place.
* *Fumigation:* Check if the domiciliary unit has been fumigated.
* *Insecticide Paint:* Check if the domiciliary unit has been treated with insecticide-containing paint.

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-chagas_disease-chagas_related_laboratory_tests:

Chagas Related Laboratory Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The module :code:`health_ntd_chagas` also adds some Chagas disease related tests to the list of available laboratory tests, including:

* CHAGAS BLOOD SMEAR
* CHAGAS ELISA
* CHAGAS INDIRECT IMMUNOFLUORESCENCE - IFA
* CHAGAS PCR
* CHAGAS STROUT
* CHAGAS XENODIAGNOSIS

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-dengue_fever:

Dengue Fever
------------

Dengue fever is caused by a virus transmitted via mosquito bites. The fever is usually not fatal, but infection with one of four serotypes can increase later susceptibility to other serotypes, resulting in a potentially fatal disease called severe Dengue. There are 50–100 million dengue fever infections annually in Asia, Latin America, and Northern Australia. No treatment for either Dengue or severe Dengue exists beyond palliative care. (Learn more about :wikipedia:`dengue fever`.)

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-dengue_fever-dengue_related_surveys:

Dengue Related Surveys
^^^^^^^^^^^^^^^^^^^^^^


The module :code:`health_ntd_degnue` adds the *Dengue DU Dengue* form to GNU Health. This allows you to evaluate a domiciliary unit for risks regarding dengue fever. You can find this survey by opening the *Domiciliary Units* form and choosing the *Dengue DU Survey* via the *Relate* button in the toolbar.

.. thumbnail:: ../../images/Dengue_DU_Survey_form_in_GNU_Health.png
    :title: Dengue DU Survey form in GNU Health
    :align: right
    :width: 30%

The *Dengue DU Survey* allows to store the following information about a domiciliary unit:

* *Survey Code:* A code to identify the survey (created automatically).
* *DU:* The domiciliary unit which was evaluated (set automatically).
* *Date:* The date of the evaluation.
* *Status:* Choose from "Initial", "Unchanged", "Improved", or "Worsen" to give a summary of your findings.

Presence of larvae:

* *Larvae:* Check if aedes aegypti larvae were found.
* *Domiciliary:* Check if larvae were found in the house.
* *Peri-Domiciliary:* Check if larvae were found around the house.

Areas to improve:

* *Tyres:* Check if appropriate.
* *Animal Water Containers:* Check if appropriate.
* *Flower Vase:* Check if appropriate.
* *Potted Plants:* Check if appropriate.
* *Tree Holes:* Check if appropriate.
* *Rock Holes:* Check if appropriate.

Preventive measures:

* *Ovitraps:* Check if ovitraps are in place.
* *Fumigation:* Check if the domiciliary unit has been fumigated.

General:

* *Notes*
* *Next survey:* The date of the next evaluation of this domiciliary unit.

.. _userguide-modules-neglectedtropicaldiseases:neglected_tropical_diseases-dengue_fever-dengue_related_laboratory_tests:

Dengue Related Laboratory Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The module :code:`health_ntd_dengue` also adds some dengue fever related test to the list of available laboratory tests, including:

* DENGUE ELISA
* DENGUE IgG
* DENGUE PCR
* DENGUE PRNT

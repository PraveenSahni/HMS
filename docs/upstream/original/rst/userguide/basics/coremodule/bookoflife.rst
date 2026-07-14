.. _userguide-basics-coremodule-bookoflife:book_of_life:

Book of Life
============

.. _userguide-basics-coremodule-bookoflife:book_of_life-book_of_life.:

Book of life.
-------------
Our health is much more than just cold medical records. Most of the time, our health is the result of many events related to the environment, decisions we make, and interactions with many actors, that shape our life as individuals.


.. _userguide-basics-coremodule-bookoflife:book_of_life-book_of_life.-pages_of_life:

Pages of Life
^^^^^^^^^^^^^

GNU Health command : **POL**

GNU Health has developed a way to record the relevant events on a person life. These events are not just medical, but also demographical, biographical and social. Each of those relevant events make a Page of Life of the individual.

Integration with GNU Health HIS node: From the Hospital Management System Node (HIS) of GNU Health, processes such as encounters, prescriptions, lab and diagnostic imaging are mapped to the book of life of the person.

In addition, the page of life allows the person to be in charge of their health information. The person will be able to read and post relevant information to be part of their Book of Life.

Components of the page of life: Currently the main page types are

* Demographical
* Biographical
* Medical
* Social

In addition, the medical and social categories have their context, to know:

**Medical page contexts**:  Health condition, encounter, procedure, immunization, prescription, surgery, hospitalization, lab, Dx Imaging, genetics, family history, birth and death, among others.

**Genetics**: If the medical context is genetics, three additional fields will be shown: Gene, Natural variant, Phenotype

**Social page contexts**: Equity / Social gradient, stress, social exclusion, working conditions, education, physical environment, unemployment, social support, food, addiction, transport, health services, family functionality, family violence, bullying, war.

.. _userguide-basics-coremodule-bookoflife:book_of_life-book_of_life.-pages_of_life-page_of_life_link_in_the_gnu_health_federation:

Page of Life link in the GNU Health Federation
""""""""""""""""""""""""""""""""""""""""""""""
Each page of life is unique. The GNU Health federation package includes the Page of Life model in the Federation. Any newly created page of life, and their modifications, can be then be shared across the federation Health Information System.

More information about the :ref:`userguide-modules-federation-gnuhealthfederation:federation`

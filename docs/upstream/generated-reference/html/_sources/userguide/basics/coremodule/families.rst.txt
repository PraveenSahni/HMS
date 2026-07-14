.. _userguide-basics-coremodule-families:families:

Families
========
.. _userguide-basics-coremodule-families:families-the_family_concept_in_gnu_health:

The Family Concept in GNU Health
--------------------------------

Since GNU Health 2.0, the family object is a model that holds all the individuals that compose a family, from the legal and/or genetic point of view. The family members don't necessarily share the same :ref:`userguide-basics-coremodule-domiciliaryunits:domiciliary_units`.

A person can be part of several families at the same time. Consider the following situation:

* Peter Stone is the son of Mattew Stone and Rosanna Pellegrino.
* Peter marries Sandra Miller and has two children with her.
* After being divorced, Peter marries Lucia Martinez, and they have another child.

So Peter Stone would be:

* a son in the Stone-Pellegrino family
* the husband in the Stone-Miller familiy
* the husband in the Stone-Martinez familiy

The family model should only be used for one couple and their children, since things can become confusing otherwise. However, the system does not prevent you from entering families with more than two generations.

.. _userguide-basics-coremodule-families:families-managing_families:

Managing Families
-----------------

Families are managed in the *GNU Health → Demographics → Families* section.

If you are creating a family, the first thing to do is to assign it a unique family name. In our demo database we use a combination of the two lastnames of husband and wife (e.g. "Zenon-Betz" for the familiy of John Zenon and Ana Betz). While this should work fine most of the time, you will run into problems when you have several families with the same combinations of lastnames. In this situation, adding the firstnames could help to make the familiy name unique (e.g. "Zenon-Betz, John & Ana").

Below the family name you will find a list of the family members, each consisting of the following fields:

* *Party*: Link to a person (or a *Party* record whith the *Person* flag set, to be technically correct).
* *Role*: The role of this person within the familiy (e.g. "Mother", "Son"). Please note that this is a simple text field where you can enter whatever you like. There are no predefined roles, and there is no validation (like a to make sure that a mother is female or that a son is younger than its father).

.. _userguide-basics-coremodule-families:families-searching_family_members:

Searching Family Members
------------------------

In the *GNU Health → Demographics → Family Members* section you can find a list of all family members. This list is read-only, but you can use it to search family members by family name, party (person) or role.

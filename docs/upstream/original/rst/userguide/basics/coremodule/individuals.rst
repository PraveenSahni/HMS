.. _userguide-basics-coremodule-individuals:individuals:

Individuals
===========
.. _userguide-basics-coremodule-individuals:individuals-the_individual:

The Individual
--------------

It's time to enter the essential unit of GNU Health, *the person*. We take the person as a unique individual, yet, somebody that is part of a family, interacts with the community and makes up our society. This entity is so important that it's impossible to achieve good public health programs without information about the individuals. This concept that might seem trivial, is very often overlooked.

.. _userguide-basics-coremodule-individuals:individuals-review_of_concepts:

Review of concepts
------------------

We mentioned in the :ref:`userguide-basics-firststeps:first_steps` the concept of *Party*. A party is an abstract entity, which attributes will differentiate a health center from a person, or a person that is a doctor, a patient or both. The concept of *party* is extremely simple, yet very powerful and versatile.

At this point is important to go back and refresh the :ref:`Terminology <userguide-basics-firststeps:first_steps-his_and_lims_nodes>` used in GNU Health.

.. _userguide-basics-coremodule-individuals:individuals-your_first_individual_in_gnu_health:

Your first Individual in GNU Health
-----------------------------------

Follow the menu : **Party → Parties**

You will be presented with a Tree view (listing) of the parties in the system. Take a look at the screen shown in this section. I have selected / Highlighted three parties. "Ana Betz", "Cameron Cordara" and "GNU Solidario Hospital". They are all parties (entities), but their attributes make *Ana* a patient, *Cameron* a doctor and *GNU Solidario Hospital* a Health Institution.

Of course, under this model, you can have, for instance, a health professional that is also a patients. Don't forget that doctors are people :-)

To create a new record, click on the **new record icon**, or type **Ctrl+N**. You will be presented with the new party form view.

In a multidisciplinary team, the following information is usually done by the administration office, the front desk or sometimes by the social workers.

In this example, we will focus on Ana Betz. Let's go over the main fields:

* **Name**: This is a required field, denoted by the blue background. Required fields must be entered otherwise you won't be able to save the record.
* **Lastname**: Enter the lastname as appears in the ID card. Some countries use only the father's name, other use a combination of the father and the mother.
* **Alias**: Nickname (if any) of the person. Surprisingly enough, in many places around the world, people use nicknames to refer a particular person, and sometimes they don't know the real name. If that person has an alias / nickname, you should enter it on the system. It might be key to know about a missing person.
* **Party Attributes**: At this point, set the *Person* checkbox. Just check this one. Don't enable any other at this point.

Before going into the patient demographics. **save your work**. As a general rule, is important so save your work while working on records, to avoid losing your unsaved data, specially in long records. To save the person, **click on the save this record icon** or type **Ctrl+S**.

.. _userguide-basics-coremodule-individuals:individuals-your_first_individual_in_gnu_health-demographics:

Demographics
^^^^^^^^^^^^

The information entered in this section is very important at both individual and population level. The health professionals and authorities will have precious information for them to make good health programs and to assess the social determinants of health.

Here you enter the person's **date of birth, Social Security Number, citizenship, sex, profession, the Domiciliary Unit, education level and marital status**, among others. Other models (eg, patient)  modules (eg, socioeconomics) will make extensive use of these field. Most of the fields are self-explanatory and don't need to get into details. We'll just make some tips about some of them.

* **PUID** : This is the Person Unique Identifier Number or equivalent issue by a **specific country of region**. It can be empty, but once is entered, is unique to the person. The PUID is a key identifier of the individual. If there is a person that does not have a local PUID, set the **Alternative ID** checkbox and enter the information there.
* **Alternative IDs** : When you enable this checkbox, you will be able to enter new IDs, such as Passports, other countries SSNs, etc... The person can have multiple IDs, and they should be registered whenever possible. For example, it will facilitate contacting this person if she or he is from another country.For clarity sake, the alternative IDs section is not shown unless the checkbox is set.
* **Unidentified** : Check this box if the person has no ID at the moment of registration. This can be the case of people that is brought to the health center in an accident settings. Once we gather the information at a later time, we unset the checkbox and enter the ID.
* **Domiciliary Unit** : This is a **relational field** that points to the place where the person lives. This is the main person address and should not be confused with the addresses of their relatives acquaintances that we will describe next.

.. _userguide-basics-coremodule-individuals:individuals-your_first_individual_in_gnu_health-contact_information:

Contact Information
^^^^^^^^^^^^^^^^^^^

Click on the next tab ("General") to enter the information this person contact information. The address can be associated to a person or an institution. For example, we are showing the address of "Caro Forte", she is Ana Betz Kenpo Karate teacher, with the address of the Kenpo Karate school. Since the contact is associated to a physical person (relational field), you could easily get her teacher information opening the resource. This section also contains the contact mechanisms of the person, such as **email** or **phone number**.

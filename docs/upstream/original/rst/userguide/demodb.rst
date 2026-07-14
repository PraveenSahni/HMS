.. _userguide-demodb:using_the_demo_database:

Using the Demo Database
=======================

.. _userguide-demodb:using_the_demo_database-introduction_to_the_demo_database:

Introduction to the Demo Database
---------------------------------

GNU Health default installation comes with no data. It's interesting, for academic and training purposes to have some demo data that exemplifies concepts and improves the learning curve.

The demo database is an ongoing project and it will be adapting to the each new GNU Health version. The clinical history will also grow with time.

For consistency sake, it's important to have the main characters information constant (family members name, birth dates and place, health centers, family doctors etc.). The information and characters are fictitious and we should try to make it valid for different cultures.

.. _userguide-demodb:using_the_demo_database-the_zenon-betz_family:

The Zenon-Betz Family
---------------------

The story goes around the Betz family, and the main character, Ana Betz, a primary school teacher.

* Health Center: GNU Solidario Hospital in Las Palmas, Spain
* Family Doctor: Cameron Cordara

    * ID: 765870
    * Speciality: Family Medicine
    * Institution: GNU Solidario Hospital
* Family: Zenon-Betz family

    * John Zenon (SSN: 40556644)
    * **Ana Betz (Fed ID: ESPGNU777ORG)** born October 4th, 1985, the main character
    * Matt (SSN: 97234436), born March 15th 2010, their son

.. _userguide-demodb:using_the_demo_database-the_zenon-betz_family-demographics_information:

Demographics Information
^^^^^^^^^^^^^^^^^^^^^^^^

* Sex: Female
* Marital Status: Married
* Profession: School teacher
* Education Level: University
* Domiciliary Unit

    * Housing Conditions: Comfortable and good sanitary conditions

.. _userguide-demodb:using_the_demo_database-the_zenon-betz_family-patient_information:

Patient Information
^^^^^^^^^^^^^^^^^^^

* Socio-Economic Status: Middle class
* Allergies: β-lactam hypersensitivity
* Diseases: Type 1 Diabetes diagnosed on November 10th 1993
* Medication: Insulin since November 10th 1993
* Genetic Information

    * Family history
    * Maternal Grandfather: Marfan's Syndrome (Q87.4)
    * Father: Essential (primary) hypertension (I10)
    * Disease Genes
    * BRCA1: breast cancer 1, early onset

* Obstetric Information: G1P1A0

    * Newborn: Matt, epidural, vaginal birth

* Lifestyle

    * Ex-smoker
    * Addictions: No recreational drugs
    * Sexuality: Heterosexual, monogamous, practices safe sex
    * Safety: Motorcycle rider, uses helmet

.. _userguide-demodb:using_the_demo_database-the_zenon-betz_family-other_information:

Other Information
^^^^^^^^^^^^^^^^^

* Family information (Family functionality level, members, operational sectors...)
* Medical Imaging (X-rays, CTs, MRIs...)
* Genetic info / risks
* Lab orders and results
* Clinical history of the family

.. _userguide-demodb:using_the_demo_database-online_community_servers:

Online Community Servers
------------------------

We have two main community servers available in the Internet so you can connect and try the latest GNU Health. This is probably the simplest way to check out GNU Health for the first time.

#. **federation.gnuhealth.org**: The GNU Health Federation community hub. Contains the latest stable version

.. _userguide-demodb:using_the_demo_database-online_community_servers-gnu_health_federation_community_hub:

GNU Health Federation Community Hub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**federation.gnuhealth.org**: The GNU Health Federation community hub. Contains the latest stable version of the following components :

* Thalamus message server
* Health Information System and Person Master Index
* GNU Health HIS and LIMS nodes
* GNU Health WebDAV server and calendaring system


The community Hospital Management demo server runs behind a web server (NGINX) and a WSGI server (UWSGI).

.. _userguide-demodb:using_the_demo_database-online_community_servers-gnu_health_federation_community_hub-connection_to_the_gnu_health_his_and_lims:

Connection to the GNU Health HIS and LIMS
""""""""""""""""""""""""""""""""""""""""""

#. Install the GNU Health client (GNU/Linux, FreeBSD or other *NIX*) Proceed as explained in the :ref:`GNU Health Client Installation section <techguide-installation-vanilla:vanilla_installation-installation_of_the_gnu_health_client>`
#. Use the following server and credentials . Please note that the Database name can change. You can use the "profile" to select the DB from the list

.. hint::
        * **Server**: federation.gnuhealth.org:443
        * **Database**: health50
        * **User name**: admin
        * **Password**: gnusolidario

        The community server uses SSL protocol with the port 443

.. note::
         The community server database resets regularly , so we have clean demo data. That means that you can also play and experiment with it without fear of "breaking" the DB : .

.. note::
         Please **do not** change the language of the admin account! Instead, copy the admin account to a new account, e.g. admin_fr, and set this accounts language to the desired language!


.. _userguide-demodb:using_the_demo_database-online_community_servers-gnu_health_federation_community_hub-connection_to_the_health_information_system_via_browser:

Connection to the Health Information System via Browser
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
You can connect to the community hub using the web interface.
Please note that this is alpha and not intended for production systems yet.

https://federation.gnuhealth.org

.. _userguide-demodb:using_the_demo_database-online_community_servers-development_server:


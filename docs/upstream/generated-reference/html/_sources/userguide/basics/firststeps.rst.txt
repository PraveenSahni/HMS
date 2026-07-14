.. _userguide-basics-firststeps:first_steps:

First Steps
===========
.. _userguide-basics-firststeps:first_steps-introduction:

Introduction
------------
Before we start the implementation process, it is important to get familiar with the terminology commonly used in the rest of this book. At the beginning some words might be a bit puzzling, but with a bit of practice, you will find this terminology quite logical.

Even if you are not a technical person, it might be helpful to understand that GNU Health is an ecosystem of heterogeneous platforms. GNU Health has the following main components and nodes:

* Hospital Management Information System (HIS) node
* Laboratory Information System (LIMS) node
* Person Master Index
* Message server (Thalamus)
* Health Information System


.. _userguide-basics-firststeps:first_steps-his_and_lims_nodes:

HIS and LIMS nodes
-------------------

.. todo:: Take and add new screenshots like here: https://en.wikibooks.org/wiki/GNU_Health/First_Steps

The following concepts are essential to understand how GNU Health HIS and LIMS nodes work.

* **Party**: In GNU Health, a party is an entity. An abstract concept to define someone or something that has legal status. It's the unit of the relationship in Tryton. Some examples of Parties are:

  * Patients
  * Companies
  * Health professionals
  * Health centers
* **Model**: The model defines each object in GNU Health. Models define the database objects (tables). :code:`gnuhealth.patient` is a model example.
* **Field**: The building blocks of the model. For example: age and sex are :code:`gnuhealth.patient` fields.
* **View**: Views are the representation of the model on the screen. Most models will have an individual form to accept data into the model and display data out from the model.

  * **Tree**: The list format of the model. The tree view allow us to search and select multiple records.
  * **Form**: The representation of the model on the screen that allows you to input data.
* **Table**: The model representation at the database server. The model :code:`gnuhealth.patient` is mapped in the table :code:`gnuhealth_patient` in PostgreSQL.
* **Record**: Each unique entry in a particular database table. For example *Ana Betz* is a record on the :code:`gnuhealth_patient` table in PostgreSQL.
* **Module**: Modules are programs that provide specific functionality. GNU Health provides different modules to meet your health center needs. Example of modules are *Socioeconomics*, *Genetics* and *Surgery*. You should only activate the modules that are actually needed for your center.
* **Report**: Reports allow you to dynamically print documents in Open Document / LibreOffice format (ODF), Portable Document Format (PDF) or even directly to the printer.
* **Action**: Actions are processes excecuted upon one or more selected records.
* **Notebook**: A tabbed group of forms designed to make navigation easier.

.. _userguide-basics-firststeps:first_steps-navigation_area:

Navigation Area
---------------
Now it is time to identify the components of the GNU Health Screen. In the following screenshot we have marked the main sections :

* **Main Menu** : We can navigate among the different functionalities. Configuration, Patients, Financial, ... You can deactivate the main menu (useful in low resolution devices) by pressing *'Ctrl+T'*
* **Tabs** : Tryton allows you to have multiple records open at the same time. The section "Tabs" of the screenshot shows the current form.
* **Actions** : Under the Tabs section you will find different icons that act upon the current record. You can, for instance, create a new record, generate a report, change the view, select related records associated to this patient (appointments, lab tests... ).
* **Record form** : This is where you see and input the information. Notice that you can have tabbed forms (notebooks) in the lower half of the form, which allows quick and easy navigation. In this example some of the tabs within the records are main, medication, diseases, surgeries, socioeconomics and gynecological information. The upper side of this form is static, so the health professional has the most relevant information about the patient always visible.
* **Status bar** : The lower side of the screen shows the status bar. From left to right, these are fields :

  * **User name** : In this case we logged in as *Administrator*
  * **Organization Name** : *GNU Solidario Hospital*
  * **Requests** : Tryton has an internal messaging system. You will get notifications in realtime.
  * **Server Information** : The lower right section gives you login and server information. In this example, it shows "admin@localhost:8000/demo". *admin* is the login name, *localhost'' the name of the GNU Health server, *8000* is the port where connects and *demo* is the database name.

.. _userguide-basics-firststeps:first_steps-form_fields_and_field_types:

Form fields and field types
---------------------------

Let's now go through the most relevant field types and how to properly use them. We will use the previous screenshot of the patient  as the example.

* **Text fields** : These type of fields allow us to enter a lot of information. You will see them normally like large boxes. In our example, the field under "Patient Allergies and Critical Information" is a text field.
* **Character fields** : These type of fields are similar to the Text fields, but with a limited size. There are few character fields and none in this example. The *diet type* in the lifestyle section or the Gene ID on genetics are example for character fields.
* **Date Fields** : These fields will open a calendar when clicked, so you can choose the date. Alternatively, you can enter the date manually. The *date of birth* is a Date field.
* **DateTime Fields** : Similar to the date fields, but with the addition of time. An example of this field is the *Date/time of birth* of the newborn, in the neonatology module.
* **Integer fields** : These fields allow only integer numbers. They show a "0" by default. An example is *Minutes of physical exercise per day*
* **Float fields** : You can enter decimal numbers. The *body temperature* is one example of a float field.
* **Function fields** : These are special fields, in the sense that they are calculated in real time, depending, most of the time, on the values of other fields. For example, the *Patient Age* is a function field. Notice that the field has a grey background, meaning that is *'read-only'*. It will calculate the current patient age in years/months/days depending on the patient date of birth. Another example of function field is the *Hospitalization Status* of the patient.
* **Selection fields** : These fields will let you choose from a list of options. For example, the patient *Sex* or the *blood type* are selection fields. This type of field minimizes typing error.
* | **Relational fields** : These fields retrieve information from a related model. They are of the form One2Many or Many2One. Relational fields are important to keep the uniqueness of data. By using this type of fields, you link the ID of an existing record, without duplicating information, to another record. The *patient* is a relational (One2Many) field. It relates to the *party* model, from where it gets all the administrative data (Social security number, address, etc... ).
  | Shortcuts : **[F2]** will open the related record and **[F3]** will create a new record
* **Required fields**: These fields are mandatory. You must enter information or else the record won't be saved. You can quickly identify the required fields because they have a blue background. The **Patient** field is a required field.

.. _userguide-basics-firststeps:first_steps-time_to_practice:

Time to Practice
----------------

**Important :** Make sure you are in your **demo database**. This demo database that you created has no important information. You can put anything you want. You can even delete it and recreate it. Just make sure you don't use a production database for your tests. One way to prevent accidentally entering the production database is to have a different password for your demo database, this way if you select the wrong database, you won't be able to login.

If you do not have a demo database yet, please refer to the chapter :ref:`techguide-demodb:local_demo_database` to learn how to create your own testing environment.

It's been a lot of information! Now is time to play around with all this information.

With the information try the following :

#. Navigate in the Main menu
#. Open the Configuration Submenu
#. Create a Physician with the Family Medicine Specialty.

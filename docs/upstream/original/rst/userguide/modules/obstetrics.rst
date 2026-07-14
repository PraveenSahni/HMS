.. _userguide-modules-obstetrics:obstetrics:

Obstetrics
==========

.. _userguide-modules-obstetrics:obstetrics-introduction_to_obstetrics:

Introduction to Obstetrics
--------------------------

All information related to pregnancy, childbirth and the postnatal period can be found in the *Obstetric History* which can be accessed via the *Related* button in the *Patient* form. Due to the complexity of this information, it is not a section within the *Patient* form; to view or edit the obstetric history of a patient, click the *Relate* button in the toolbar and select *Obstetric History* instead. This will present you a list of all pregnancies of that patient.

.. thumbnail:: ../../images/The_Obstetric_History_stores_information_about_a_pregnancy.png
    :title: The Obstetric History stores information about a pregnancy
    :align: right
    :width: 30%

The form for a single pregnancy has basically four sections:

* some general information (top and bottom of the form)
* a list with *Prenatal Evaluations*
* a list with * Perinatal and Intrapartum Information*
* a list with *Puerperium Monitor* records

.. _userguide-modules-obstetrics:obstetrics-general_pregnancy_information:

General Pregnancy Information
-----------------------------

The following fields allow you to store general information about a pregnancy:

* *Patient ID*: The name of the patient (link to a *Patient* record).
* *Health Prof*: The name of the doctor (link to a *Person* record).
* *Institution*: The health institution (link to a *Institution* record).
* *Pregnancy*: The number of the pregnancy for this patient. GNU Health will prevent you from using the same number twice; however, it will not force you to start with number 1 or to use consecutive numbers.
* *LMP*: The date of the last menstruation period.
* *Pregnancy Due Date*: The expected date of birth for the baby (automatically calculated based on the *LMP* date).
* *Current Pregnancy*: Check this box to indicate that this is the most recent pregnancy. GNU Heath will make sure that you have only one current pregnancy per patient. If you uncheck this box, the fields *End of Pregnancy* and *Result* must be filled in, because GNU Health assumes that this pregnancy has ended.
* *Fetuses*: The number of fetuses.
* *Monozygotic*: Check this box if a pregnancy consists of more than one fetus and they are monozygotic.
* *IUGR*: To indicate a intrauterine growth restriction. Choose between symmetric and asymmetric.
* *Warn*: Check this box if the pregancy is (or was) not normal.

The following fields are only available if the box *Current Pregnancy* has been unchecked:

* *Reverse*: Check this box if the patient does not know the date of her last menstruational period. This will make the field *Pr. Weeks* visible (see below).
* *End of Pregnancy*: The date when the pregnancy has ended.
* *Pr. Weeks*: The duration of the pregnancy in weeks. This field is only visible if you check the *Reverse* checkbox (see above). Entering a value in this field will delete the date in the *LMP* field (see above).
* *Result*: Choose between Live birth, Abortion, Stillbirth and Status unknown.
* *Home Birth*: Check to indicate if a patient gave birth at home.
* *BBA (Born Before Arrival)*: Check to indicate if a patient gave birth on her way to the health institution.

.. _userguide-modules-obstetrics:obstetrics-prenatal_evaluations:

Prenatal Evaluations
--------------------

In the *Prenatal Evaluations* section of the *Obstetrics History* you can store the results of all evaluations before birth. For each evaluation the following fields are available:

.. thumbnail:: ../../images/Prenatal_Evaluation_dialog.png
    :title: Prenatal Evaluation dialog
    :align: right
    :width: 30%

General information:

* *Date*: The date of the evaluation
* *Gestational Week*: Calculated automatically
* *Institution*: The health instituation where the evaluation took place
* *Health Prof*: The health professional responsible for the evaluation

Information about the mother:

* *Hypertension*: Check this box if the mother has hypertension.
* *Preeclampsia*: Check this box if the mother has pre-eclampsia.
* *Overweight*: Check this box if the mother has overweight or obesity.
* *Diabetes*: Check this box if the mother has glucose intolerance or diabetes.

Information about the placenta:

* *Placenta Previa*: Check if applicable
* *Placentation*: Choose between Normal decidua, Accreta, Increta, Percreta
* *Vasa Previa*: Check if applicable

Information about the fetus:

* *Fundal Height*
* *Fetus Heart Rate*
* *EFW* (Estimated Fetal Weight)
* *BPD* (Biparental Diameter)
* *HC* (Head Circumference)
* *AC* (Abdominal Circumference)
* *FL* (Femur Length)

.. _userguide-modules-obstetrics:obstetrics-perinatal_and_intrapartum_information:

Perinatal and Intrapartum Information
-------------------------------------

The *Perinatal Info* section documents everything that happens immediately before or after the birth of the baby, that is, from week 28 of gestation until about the first seven days after birth. Each *Perinatal and Intrapartum Information* record has a *Main* tab and a *Additional Info* tab.

.. _userguide-modules-obstetrics:obstetrics-perinatal_and_intrapartum_information-*main*_tab:

*Main* Tab
^^^^^^^^^^

.. thumbnail:: ../../images/Perinatal_and_Intrapartum_Information_dialog_Main_tab.png
    :title: Perinatal and Intrapartum Information dialog (Main tab)
    :align: right
    :width: 30%

* *Gestational Weeks*
* *Admission*: Date and time of admission
* *Code*
* *Delivery Mode*: Choose between "Vaginal – Spontaneous", "Vaginal - Vacuum Extraction", "Vaginal - Forceps Extraction", or "C-section".
* *Fetus Presentation*: Choose between "Cephalic", "Breech", or "Shoulder".
* *Monitors*: See "*Perinatal Monitor* Dialog" below
* *Notes*
* *Institution*
* *Health Professional*

.. _userguide-modules-obstetrics:obstetrics-perinatal_and_intrapartum_information-*main*_tab-*perinatal_monitor*_dialog:

*Perinatal Monitor* Dialog
""""""""""""""""""""""""""

.. thumbnail:: ../../images/Perinatal_Monitor_dialog.png
    :title: Perinatal Monitor dialog
    :align: right
    :width: 30%

The *Monitors* section allows you to record all vital signs of both mother and fetus. Each *Perinatal Monitor* record provides the following values:

Mother:

* *Date and Time*
* *Systolic Pressure* and *Diastolic Pressure*
* *Mother's Heart Frequency* (as opposed to *Fetus Heart Frequency* - see below)
* *Contractions*
* *Cervix Dilation*
* *Fundal Height*

Fetus:

* *Fetus Position*: Choose between "Occiput / Cephalic Posterior", "Frank Breech", "Complete Breech", "Transverse Lie", or "Footling Breech".
* *Fetus Heart Frequency* (as opposed to *Mother's Heart Frequency* - see above)

Complications:

* *Bleeding*: Check if appropriate
* *Meconium*: Check if appropriate

.. _userguide-modules-obstetrics:obstetrics-perinatal_and_intrapartum_information-*additional_info*_tab:

*Additional Info* Tab
^^^^^^^^^^^^^^^^^^^^^

.. thumbnail:: ../../images/Perinatal_and_Intrapartum_Information_dialog_Additional_Info_tab.png
    :title: Perinatal and Intrapartum Information dialog (Additional Info tab)
    :align: right
    :width: 30%

The *Additional Info* tab provides the following fields:

* *Dystocia*
* *Episiotomy*
* *Lacerations*: Choose between "Perineal", "Vaginal", "Cervial", "Broad Ligament", "Vulvar", "Rectal", "Bladder", or "Urethral".
* *Hematoma*: Choose between "Vaginal", "Vulvar", or "Retroperitoneal".
* *Placenta Anomalies*: Check the *Incomplete*, *Retained*, and *Abruptio Placentae* boxes if appropriate.

.. _userguide-modules-obstetrics:obstetrics-puerperium_monitor:

Puerperium Monitor
------------------

The Puerperium is the period beginning immediately after the birth of a child and extending for about six weeks. It is a time in wich the mother's body, including hormone levels and uterus size, returns to a non-pregnant state.

.. thumbnail:: ../../images/Puerperium_Monitor_dialog.png
    :title: Puerperium Monitor dialog
    :align: right
    :width: 30%

The *Puerperium Monitor* section allows you to document this phase. Each record provides the following data:

* *Institution*
* *Health Professional*
* *Date and Time*
* *Fundal Height*
* *Lochia Amount*: Choose between "normal", "abundant", or "hemorrhage".
* *Lochia Color*: Choose between "rubra", "serosa", or "alba".
* *Lochia Odor*: Choose between "normal" or "offensive".

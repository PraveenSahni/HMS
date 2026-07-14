.. _changelog:changelog:

Changelog
=========

This is a summary of the Hospital Information System (HIS) release announcements

Since release 5.0 we don't show the patchsets, only major, minor release annoucements.
You can find a detailed Changelog per commit inside the repository at Codeberg.



5.0.0
~~~~~

``2025/06/30``

Dear community:

I am very happy to announce the release 5.0 series of the GNU Health Hospital Information System (HIS). This release it's the result of a tremendous amount of work that spanned for almost the last two years!

Series 5.0 represent a major leap in functionality, the underlying technology & project development.

Currently we have the vanilla version ready to be downloaded, via gnuhealth-control

The following paragraphs summarize the changes and features included in GNUHealth HIS 5.0. There are more features and information that has been left outside this document for the sake of brevity.
You can look consult the Changelog at Codeberg.


New Functionality Features

**Laboratory Information System (Occhiolino)**

    * New visual aids for out-of-range results
    * Create individual test directly w/o orders
    * Include testing for veterinary context
    * Analyte code harmonization
    * Test sources for patient & non-patients
    * Enhanced report formats


**Focus on Social Diseases**

    * Check for uninsured population
    * Enhanced data entry for socioeconomic status and family functionality
    * Add homeless status
    * Link with International Classification of Functionality, Health and Disability (ICF)
    * Epidemiological report takes into account the socioeconomic status of the population


**Medical Imaging**

    * Extensive package refactoring
    * health_imaging
    * health_imaging_worklist (DICOM patient worklists)
    * health_imaging_orthanc
    * Better integration with Orthanc PACS server
    * Work from Wei Thao, University of Louvain and the Orthanc community


**Patient Medication**

    * Accessible from the main menu
    * Report at population level


**Allergic status validation**

    Automatically check the patient allergic status
    Patient level
    Prescription level
    Sets 'Focus on allergy' automatically


**Demographics**

    Enhanced demographics information
    Insurance validity check
    Record Homeless status
    Ethnicity and proclaimed ethnicity
    Improved socioeconomic assessments


**Insurances**

    Enhanced demographics
    Warning on expired insurances
    Insurance policies and pricing for procedures
    Linked to medical evaluations, surgeries, ...


**Obstetrics**

    Enhanced obstetric history
    Link newborn with pregnancy result
    General population report
    Detailed information about multiple-pregnancy for each fetus


**Medical Genetics**

    * Include family history in core package
    * Patient family tab (members, history ...)
    * Mutation zygosity
    * Improved data entry and view


    * Updated genes and proteins datasets (2023 → 2025)
    * Genes: 44056 (+348)
    * UniProt Natural variants: 82581 (+1422)
    * Protein related diseases: 6740 (+300)
    * HGNC: 80 gene symbols renamed



**Summary of new features**


    * New functionality for patient procedures and medical interventions
    * Improved reporting and analytics
    * New features on patient obstetric history and pregnancy related evaluations
    * Improved ergonomics and views on demographics and patient related information.
    * Enhanced socioeconomic and family functionality assessment
    * Extensively revised Medical Imaging, DICOM worklists and Orthanc packages
    * Reorganize nursing and ambulatory care packages
    * Enhanced patient body composition and anthropometrics
    * Enhanced “Focus on” patient section, including automated settings and mental health
    * New insurance and billing features for medical interventions and insurance plans.
    * Improved patient safety and allergic conditions checks and prescription writing


Technology


**The development environment is now at Codeberg**

    Translation : 30+ language teams


**GNUHealth-Control as a single point for sysadmin tasks**

    * GNU Health control will install, update and backup the instances
    * Removed gnuhealth-setup



**GNU Health HIS 5.0 uses Tryton 7.0 LTS framework**

    * Support until end of 2028
    * Full refactoring of packages
    * Support of Python 3.13
    * Native GNU Health GTK Client
    * Development web client


**Gunicorn as WSGI server**

    * Gunicorn is now the default WSGI server for GNUHealth HIS
    * For production / large deployments
    * Can be coupled with Nginx
    * Used already in Thalamus and the GNU Health Federation
    * Replaces uWSGI


**Increased Modularity**

    * Reduced Package inter-dependency, mainly in:

        * Nursing & Ambulatory care
        * Crypto
        * Lab
        * Clinical History
        * Stock management


    * Removed health_profile


**Packages are in the GNU Health Organization at PyPI**

    * wheel and source (sdist) distributions
    * Installation of individual health packages via gnuhealth-control
    * Much lighter, simple installations and implementations
    * Specific for user and health institution needs
    * Reduced complexity
    * Improved performance and security


**Minor number / patches at individual package level**

    * The patch level version is at package level instead of the whole GNU Health. This provides greater modularity and improves system administration tasks.
    * gnuhealth-control detects which packages need to be updated, from gnuhealth and its dependencies.


**Source code of GNU Health HIS and gnuhealth-control at GNU.org**

    * GNU Health HIS sourced code will be packaged as a bundle with a date format when any of the resources is updated.
    * gnuhealth-control source will also be at GNU.org


**Migrate to Poetry**

    Poems, everybody! From release 5.0, we have migrated the package and dependency management system from setuptools to Poetry.



4.4.0
~~~~~

``2023/12/23``

Dear community:

I am very happy to announce the release of the 4.4 series from the GNU Health Hospital Management Information System (HMIS) component!


**What is new in GNUHealth Hospital Management 4.4 series**


The following is a summary of the main new features included in GH 4.4:

* Improve ergonomics on patient health condition model
* Menu for dental treatments
* Include synchronization with Orthanc server using Tryton scheduler
* Add age_str field to gnuhealth.patient.disease
* Refactor FHIR server
* Include surgery stock moves
* New packages health_surgery_protocols and health_stock_surgery
* Update documentation on existing modules
* Expand information and management of surgical protocols
* Support generate DICOM Modality Worklists
* Operating room scheduler
* QR Code bracelet / wristband in demographics. No need to enter the patient / clinical section to print the QR.
* pot template generator
* Support Stone Web Viewer and Osimis Web Viewer link.
* Add service_updated to health_services* packages
* Automatically create patient upon entering demographics
* Move samples/interfaces/* to script directory
* Add ICD-10 or ICD-11 parent to disease_categories
* Update functionality in Health Genetics packages
* Include ambulatory care reporting
* Support no-patient labtest
* Make age string returned by compute_age_from_dates function translatable.
* Add code field to GnuHealthTestCritearea and let lab interface script use it
* Write a example Interface with pandas.


**Genomics and medical genetics package**


A particular mention to the health_genetics packages because major work and significant improvements have been done for this version.
I've spent quite a bit of time on this to be ready for this new release. I am confident GNU Health genetics functionality can be a valuable tool for genomics and medical genetics, both in research and clinical practice.

The following is a summary of changes in health_genetics and health_genetics_uniprot packages:

* Rename gnuhealth.disease.gene model to gnuhealth.gene
* Rename disease_genes xml data files to human_genes
* Update views and references in related modules
* Include hgnc_id
* The primary key is now the HGNC identifier
* Add symbol aliases
* Update gene type selection
* Include locus group and type
* Update Gene form and tree view
* Include name aliases, omim, ensembl and refseq accession ids to gnuhealth.gene model
* Gene related proteins are now managed in main health_genetics package
* Update and remove obsolete references of natural variants and phenotypes
* Use human genes datafiles for Genome Reference Consortium Human build 38 (grch38) and alternative loci
* Include xrefs, protein and keywords in genetic diseases
* Improve field descriptions
* Simplify protein-related views and terms
* Use Inheritance pattern
* Include MIM reference in protein diseases tree view
* Use xrefs in tree view to broaden search
* Update protein diseases datafile
* Update variants phenotypes datafile to v 2023_03_june28 from  Uniprot


**Upgrading from GNU Health 4.2**


The GNUHealth 4.4 will benefit from the stability of using Tryton 6.0! Still, at GH level there are significant changes on the data dictionary and kernel.

As usual:

* Make a FULL BACKUP your kernel, database and attach directories !!
* Follow the instructions in the manual / Wikibooks


**Development focus**


In addition of the GH HMIS server, we will focus the development in the following  areas of the GNU Health ecosystem:

* The Documentation Portal: It's now a reality! Little by little we are integrating the information on https://docs.gnuhealth.org . We now have a dedicated server that will host the documentation for the GNUHealth ecosystem components. The docmentation portal is a read-only resource, focusing on stability and quality. Wikibooks will work as the great community wiki that has been helping us for over a decade. Wikibooks will also work for development discussion and host the latest screenshots at Wikimedia commons.
* MyGNUHealth: The GNU Health Personal Health Record app for desktop and mobile devices is now at 2.0 and on Kivy framework! We can now port it to different platforms (Android, MacOS, ..) using pretty much the same codebase.
* Thalamus and the Federation Portal. The GNU Health Federation integrates information from many health institutions and individuals from a region or country. The GH Federation portal will  allow to manage resources, as well as the main point for **analytics** and **reporting** of massive demographics and epidemiological data generated nationwide. People, health centers and research institutions will benefit from the GNU Health Federation and the GNU Health ecosystem in general.


As always, no matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, and give us your feedback via them via health@gnu.org

The community server has been already migrated to 4.4.0, so you just need to download the GNU Health HMIS client.

Happy and Healthy Hacking!
Luis

4.2.3
~~~~~

``2023/09/24``

**Priority**: High

**List of other issues and tasks related to this patchset**:

* bug #64712: Bug afer installing patcheset 4.2.2
* bug #64706: Error saving party with photo due to PIL deprecation of ANTIALIAS


4.2.2
~~~~~

```2023/09/17``

**Priority**: High

**List of bugs and tasks related to this patchset**:

* bug #64269: get_serial function of LabTest class in health_crypto_lab.py need conside add units.name
* bug #64386: Automatically update the appointment sequence when state is confirm
* bug #64432: Gestational weeks show floating point instead of weeks
* bug #64457: Patient automatic critical information entries should be unique
* bug #64530: traceback on evaluation page of life if no institution is given
* bug #64665: Product cost_price needs to be passed as an argument in stock moves


4.2.1
~~~~~

``2023/04/07``

**Priority**: High

**List of other issues and tasks related to this patchset**:

* bug #64014: Update gender identity in patient evaluations and reports
* bug #64009: Include signing health professional and avoid scrolling in patient evaluation
* bug #64007: Summary report is not using FreeFonts family
* bug #63993: Python-sql error on patient evaluation report


4.2.0
~~~~~

``2023/02/11``

Dear community:

I am excited to announce the release of series 4.2 from the GNU Health Hospital Management Information System (HMIS) component!

The 4.2 series is the result of one year of work and cooperation with the community. Many new exciting features are included, bugs fixed and new translations are now in place.

**What is new in GNUHealth Hospital Management 4.2 series**

The following is a summary of the main new features included in GH 4.2:

* Enhanced Medical Imaging functionality and ergonomics.
* Introduced GNU Health "Focus on" section on patient main form. Key health indicators that put our attention on the patient main health conditions. The main indicators are Cardiovascular (excl hbp), HBP, Nutrition, Cognitive, Social, Cancer and Immuno.
* Surgery package has been vastly revised and enhanced. Thanks to the collaboration with our colleagues from Cirugia Solidaria, the surgery package is now being used in thousands of operations and all the new functionality is available in this 4.2.
* Enhanced Insurance and billing functionality. Now, in one view we can integrate all product policies from a particular insurance company plan. The 4.2 release also allows to include a fixed prices on product or category.
* The Vital Record System (VRS) can now issue reports on birth and death certificates.
* Demographics can now accept entering estimate age / DoB.
* Health services has now the functionality of "grouping" all the tests from a single order - lab and medical imaging -. It allows automatically updating the service document directly right from the request order wizard. There a new "ungroup" checkbox that, when set, it will behave as today, ie, giving the option to the manager.
* Improved Patient encounter / evaluation. Medical interventions, DDx and secondary conditions. A new report is now available that summarizes the key information from the evaluation.
* Weblate translations holds 35 languages!
* Instance and connection information visible at the GTK client title
* On the technical side, we have improved unit testing on each package, speedup load times on large datafiles and using python-sql for most queries.
* Last but not least.... GNU Health is now REUSE (Free Software Foundation Europe) compliant! This is a great step forward, since REUSE facilitates documenting and sharing licenses of Libre projects like GNU Health. It's been quite a bit of work, but definitely worth!



**Upgrading from GNU Health 4.0**


The GNUHealth 4.2 will benefit from the stability of using Tryton 6.0! Still, at GH level there are significant changes on the data dictionary and kernel.

As usual:

* Make a FULL BACKUP your kernel, database and attach directories !!!
* Follow the instructions on the Wikibooks.



Development focus


In addition of the GH HMIS server, we will focus the development in the
following  areas of the GNU Health ecosystem:

* The Documentation Portal. We now have a dedicated server that will host the documentation for the GNUHealth ecosystem components.
  The docmentation portal is a read-only resource, focusing on stability and high-quality. We will also keep using Wikibooks as a community wiki, as well as development.
* MyGNUHealth: The GNU Health app for desktop and mobile devices
* Thalamus and the Federation Portal. The GNU Health Federation integrates information from many health institutions and individuals from a region or country. The GH Federation portal will  allow to manage resources, as well as the main point for **analytics** and **reporting** of massive demographics and epidemiological data generated nationwide. People, health centers and research institutions will benefit from the GNU Health Federation and the GNU Health ecosystem in general.


As always, no matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, and give us your feedback via them via health@gnu.org

The community server has been already migrated to 4.2.0, so you just need to download the GNU Health HMIS client.


Happy and Healthy Hacking !


4.0.5
~~~~~

``2023/01/09``


**Priority**: High

**List of other issues and tasks related to this patchset**:

* bug #63558: Fault: 'NoneType' object has no attribute 'name'
* bug #63557: Missing view architecture for ('calendar.category', None, 'tree')
* bug #63533: Model 'gnuhealth.pol' is missing a default access
* bug #63532: health_caldav misses requiremnt vobject in setup.py
* bug #63517: Fault: 'webdav' is not in list
* bug #62777: The term health prof used for both initiating and signing professional in patient evaluation
* bug #62634, Missing Spanish Translations


4.0.2 (Client)
~~~~~~~~~~~~~~

``2022/12/14``

Dear GNUHealth community:

I am happy to announce the maintenance release 4.0.2 of the Hospital Management client (GTK).

Release 4.0.2 of the GNUHealth HMIS client includes bug fixes (see the Changelog[1]) and is REUSE compliant[2].

As usual, the source code can be downloaded from the official GNU ftp site[3]. You can also install it directly via pip[4].

You can join us at Mastodon for the latest news and events around GNUHealth! (https://mastodon.social/@gnuhealth)

Happy and healthy hacking!
Luis

1.- https://hg.savannah.gnu.org/hgweb/health-hmis-client/file/5d21a06fa998/Changelog
2.- https://reuse.software/
3.- https://ftp.gnu.org/gnu/health/
4.- https://pypi.org/project/gnuhealth-client/

4.0.4
~~~~~

``2022/06/16``

**Priority**: High

**List of other issues and tasks related to this patchset**:

* bug #62598, Payment term search stops in party
* bug #62596: Traceback if there is no Account Receivable defined neither on party or default acct config
* bug #62555: Too many decimals error when generating the invoice with certain discounts
* bug #62439: Error in sequence when generating Dx Imaging order
* bug #62428: complete blood count report takes two pages
* bug #62427: Typo in health_services exceptions


4.0.3
~~~~~

``2022/04/02``

**Priority**: High

**Summary of this patchset**


**Update Python dependencies**:

* vobject: We have removed the version pinning on this library, using the current, latest version.
* Update gnuhealth-control and gnuhealth-setup
* Fixed issue on stock and nursing due to an old method on default health professional.

**List of other issues and tasks related to this patchset**:

* bug #62240: trytond-console: ValueError due to old vobject version
* bug #62235: Traceback on default health professional



4.0.1
~~~~~

``2022/03/08``

**Priority**: High

**Summary of this patchset**

**Update Python dependencies**

**We needed to pin some underlying python libraries dependencies. We also included defusedxml library, included in a trytond security patch**:

* progressbar
* defusedxml
* pycountry

GNU Health control center (gnuhealth-control) and gnuhealth-setup packages have also been updated to 4.0.1 and ready at GNU.org

**List of other issues and tasks related to this patchset**:

* bug #62154 Missing dependency: defusedxml


4.0.0
~~~~~

``2022/03/03``

Dear community:

I am very proud to announce the release of series 4.0 from the GNU Health Hospital Management Information System (HMIS) component!

Thanks to our community, GNU Health is now a leading Hospital Management Information System, with implementations in many countries around the world. The 4.0 series improves the navigation, introduces many more language teams, new packages and much better integration of evaluation, laboratory and Dx Imaging services.

**What is new in GNU Health 4.0 series**:

* Improved ergonomics on the GTK client
* New HELP command that allows offline and contextualized documentation
* WebDAV and CalDAV packages are fully integrated in GH (no links)
* Weblate now holds 34 language teams!
* Removed obsoleted binary ODT (except for some charts)
* Improved integration with OpenStreetMap (OSM)
* Improved surgery and patient evaluation flows
* New health service Dx imaging package
* Update person gender list
* Add medical evaluations to health services
* Include (optional) expiration date on the person ID
* Add context field for Dx Imaging and Lab tests



**Upgrading from GNU Health 3.8**

* Make a FULL BACKUP your kernel, database and attach directories !!!
* Follow the instructions on the Wikibooks.
* Don't forget to run the "before" and "after" sql scripts


**Development focus**

In addition of the GH HMIS server, we will focus the development in the following  areas of the GNU Health ecosystem:

* MyGNUHealth: The GNU Health app for desktop and mobile devices
* The Documentation Portal and HELP command documentation packages
* Thalamus and the Federation Portal



The GNU Health Federation integrates information from many health institutions and people from a region or country. The GH Federation portal will allow to manage resources, as well as the main point for **analytics** and **reporting** of massive demographics and epidemiological data generated nationwide. People, health centers and research institutions (eg genomics) can benefit from the GNU Health Federation and the GNU Health ecosystem in general.

As always, no matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, and give us your feedback via them via health@gnu.org

The community server has been already migrated to 4.0.0, so you just need to download the GNU Health HMIS client and enjoy it.


Happy and Healthy Hacking !

.. _changelog:changelog-versions_3.x.x:

Versions 3.x.x
--------------

3.8.0
~~~~~

``2021/02/14``

Dear community:

I am very proud to announce the release of the series 3.8 from the GNU Health Hospital Management Information System (HMIS) component!

Twelve years old, the GNU Health project has now become a Libre digital Health ecosystem, with different solutions to meet different realities, integrating them in the Federation.

The year 2020, the year of the COVID-19 pandemic, has put our societies against the ropes, and challenging the public health system of every country around the globe.
The GNU Health community responded swiftly to this formidable challenge. Within hours of the official World Health Organization announcement, we were able to deliver the new ICD-10 codes of the COVID-19 disease; Include the pathology in the person record when it was confirmed by laboratory and setting the disease as a notifiable disease so the Min. of Health could have uptodate epidemiological information.

GNU Health has played a crucial role in many public health systems, not only by providing real-time observatory of COVID-19, but also, very importantly, study the impact of the socioeconomic conditions in both the incidence and severity of the disease on the underprivileged.

Our community keeps growing! A notable example is that GNU Health is now also part of the**KDE community**! KDE has adopted MyGNUHealth, the GH Personal Health record.
We are very grateful to KDE for trusting us! Most GNU/Linux users will have in their favorite GNU/Linux distribution a Personal Health Record focused on privacy and integrated with Libre devices and trackers. MyGNUHealth also runs on the PinePhone!

**What is new in GNU Health 3.8 series**

* New Dentistry package with odontogram and dental procedures
* Enhanced Page of Life generation (PoL)
* Use FODT (Flat ODT) format for reports
* Integrated infectious diseases Contact Tracing
* Epidemiological observatory
* International Classification of diseases, 11th revision (ICD-11)
* Improved integration with Weblate (now 23 languages!)
* Updated the UNIPROT protein natural variants DB from 2020
* The HL7 FHIR server is now ported to Python3
* New repositories for the components (HMIS, client, plugins, Thalamus...)


**Development focus**


In addition of the GH HMIS server, we will focus the development in the following  areas of the GNU Health ecosystem:

* MyGNUHealth: The GNU Health application for desktop and mobile devices
* The GNU Health Federation Portal


The GH Federation Portal has already started. It is a VueJS application and provides a single point of entry for individuals, health professionals and epidemiologists to the GNU Health Information system.

The GNU Health Federation integrates information from many health institutions and people from a region or country. The GH Federation portal will allow to manage resources, as well as the main point for **analytics** and **reporting** of massive demographics and epidemiological data generated nationwide. People, health centers and research institutions can benefit from the GNU Health Federation and from the GNU Health ecosystem in general.

**Upgrading from GNU Health 3.6**

* Make a **FULL BACKUP** your kernel, database and attach directories !!!
* Follow the instructions on the Wikibooks.


As always, no matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, and give us your feedback via them via health@gnu.org

The community server has been already migrated to 3.8.0, so you just need to download the GNU Health HMIS client and enjoy it.

**Free Software day**


Finally, today is the Free Software day. We have chosen this date as the release date of the GH HMIS component, as a way to remind and stress the importance of Libre Software and Open Science in our society.

Happy and Healthy Hacking !

0.9b3 (HL7 FHIR)
~~~~~~~~~~~~~~~~

``2020/11/04``

Dear GH community

The FHIR REST server 0.9b3 is out! This new version is Python3 compatible and can interact with the GNU Health HMIS node => 3.6

The FHIR server is a Flask application, that generates HL7 FHIR messages to a number of resources in the GNU Health Hospital Management Information System (HMIS) node .

This Reversion is the continuation of the great work done by Chris Zimmerman for Python2 and older GH instances.

The current resources are now being implemented are:

* Conformance: Describes the server's FHIR capabilities.
* Patient: Patient demographic information, like email, address, SSN, etc.
* DiagnosticReport: Completed lab tests, but not the data
* Observation: Lab data, like uric acid values
* Practitioner: Health professionals and their information
* Procedure: Surgeries/operations
* Condition: Diseases/diagnoses
* FamilyHistory: Family histories of patients
* Medication: Medications (not prescriptions!)
* MedicationStatement: Medications taken by a patient
* Immunization: Immunizations
* Organization: Institutions, departments, companies, etc.


This is still a beta version. We plan to add write support in the near future.

The server is now shipped as a Python package and hosted at PyPI (https://pypi.org/project/gnuhealth-fhir-server/). It also provides two scripts to run it via Tornado or Gunicorn WSGI servers.

The latest documentation about the FHIR REST server can be found at Wikibooks (https://en.wikibooks.org/wiki/GNU_Health/Using_the_FHIR_REST_server)

We have also created an instance at the GH Federation community server, so you can try it out without the need of installing it.

The HL7 provides yet another means to interact with GNU Health HMIS nodes from other systems, besides the current existing methods that are in place.

Best
Luis

3.6.5
~~~~~

``2020/08/21``

**Priority**: High

**Summary of this patchset**

GNU Health 3.6.5 includes:

* ICD-10 package:
  The World Health Organization International Classification of Diseases, 10th revision, h  has been extensively revised and updated to the 2020 edition.
  The translation templates have been also updated, specially the German and Chinese.
  Special thanks to Dr. Edgar Hagenbichler for his excellent work on this package!

**List of other issues and tasks related to this patchset**:

* task #15733: Update ICD10 datafile


3.6.5 (Control Center)
~~~~~~~~~~~~~~~~~~~~~~

``2020/07/02``

Dear community

As you may know, GNU Health HMIS has migrated its translation server to Weblate.
(see news https://savannah.gnu.org/forum/forum.php?forum_id=9762)

Today, we have released the GH Control Center 3.6.5, which has support to Weblate for the language installation. The syntax is the same, and you won't notice any difference.

To update to the latest GH Control Center, run:

$ cdutil
$ ./gnuhealth-control update

That will fetch and install the latest version, and you're ready to go :)

Happy and Healthy hacking!
Luis

3.6.4 (Control Center)
~~~~~~~~~~~~~~~~~~~~~~

``2020/06/20``

Dear all
The GH control center (gnuhealth-control) version 3.6.4 is out, fixing some minor security issues found by the openSUSE security team[1]

You just need to to the following:

1) Login as GNU Health
2) cdutil
3) ./gnuhealth-control update

That is all. The new gnuhealth-control center is now installed. To verify, please check it with

./gnuhealth-control version

If the update reports that, in addition to the gnuhealth-control, there are other components that need to be upgraded, please re-run gnuhealth-control and update the instance, as explained in the wikibook[2]

Please remember to submit any possible vulnerabilities to security@gnuhealth.org

Have a great weekend!
1.- https://bugzilla.opensuse.org/show_bug.cgi?id=1167128#c13
2.- https://en.wikibooks.org/wiki/GNU_Health/Control_Center

3.6.4
~~~~~

``2020/05/16``

**Priority**: High

**Summary of this patchset**


GNU Health 3.6.4 includes:
The most relevant features on this version are:

* health_contact_tracing package: Allows to trace people that have been in contact with a person suspected of being positive of a infectious disease. Name, demographics, place and date of contact, sanitary region (operational sector), type of contact, exposure risk and follow-up status are some of the information that is recorded per contact.
* Epidemiological Surveillance: A new report that provides epidemiological information on an specific health condition. Data on prevalence of the disease as well as the incidence over a period of time. It produces epi curves for new confirmed cases, deaths related to the disease (both immediate cause as well as underlying conditions) from death certificates. It also shows very relevant charts on the population affected from a demographic and socioeconomic point of view (age, gender, ethnicity, socioeconomic status).
* Lab and lab crypto packages: When a disease is confirmed from a positive lab test result, GNU Health LIMS automatically includes the health condition in the patient medical history upon the validation of the lab manager.
* GH Control center and gnuhealth-setup have been updated.


**Installation Notes**

You must apply previous patchsets before installing this patchset. If your patchset level is 3.6.3, then just follow the general instructions. You can find the patchsets at GNU Health main download site at GNU.org (https://ftp.gnu.org/gnu/health/)

In most cases, GNU Health Control center (gnuhealth-control) takes care of applying the patches for you.

Pre-requisites for upgrade to 3.6.4: Matplotlib (You can skip this step if you are doing a fresh installation.)
If you are upgrading from 3.6.3, you need to install the matplotlib package:

$pip3 install --upgrade --user matplotlib

Now follow the general instructions at

* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


After applying the patches, make a full update of your GNU Health
database as explained in the documentation.

When running "gnuhealth-control" for the first time, you will see the following message: "Please restart now the update with the new control center" Please do so. Restart the process and the update will continue.

* Restart the GNU Health server


**List of other issues and tasks related to this patchset**:

* bug #58104: view_attributes() method should extend list of attributes
* bug #58358: Need current SES in main patient info
* task #15563: Assign health condition from a confirmed lab
* task #15562: ((updated)) Include coronavirus COVID-19 in ICD10 codes



3.6.8 (Client)
~~~~~~~~~~~~~~

``2020/03/01``

Dear all

The GH GTK client 3.6.8 fixes several bugs, specially related to the compatibility issues with KDE and other desktop environments.

We have moved the header bar components to the main window, so now it also allows borderless operation.

Summary :

* Removed the deprecated App Menu in favor of the Menu Bar.
* Migrate from obsolete Table to Grid
* Fix the footer
* Include accelerator for preferences (ctrl+shift+p) and fix accelerator for shortcuts (ctrl+shift+F1)
* Avoid maximizing application at startup
* Remove unused fast tabbing option from menu
* Allow setting the GH command line on the bottom again (cli_position = bottom). By default is top.


3.6.3
~~~~~

``2020/02/28``

**Priority**: High

**Summary of this patchset**

Patch 3.6.3 updates World Health Organization ICD10 with the novel coronavirus COVID-19 code (U07.1)

It also fixes an issue when creating a page of life from an encounter that has an empty main condition.
in addition, updated gnuhealth-setup and gnuhealth control center are also included.

**List of issues and tasks related to this patchset**:

* GH HMIS server. task #15562: Include coronavirus COVID-19 in ICD10 codes
* GH HMIS server. bug #57695: Traceback when creating a page of life associated to an empty evaluation
* GH HMIS server. task #15561: Werkzeug 1.0 is not compatible with Trytond 5.0


3.6.2
~~~~~

``2019/11/23``

**Summary of this patchset**

Patch 3.6.2 fixes a problem in the obstetric history (OBS command) on representing the weeks at the end of pregnancy.

**List of issues and tasks related to this patchset**:

* GH HMIS server. health_gyneco . Bug #57292: OBS command generates a traceback
* GH HMIS server. health_federation.  Enforce unicode on setup read method


3.6.1
~~~~~

``2019/11/19``

**Priority**: High

**Summary of this patchset**

Patch 3.6.1 mainly fixes crash / tracebacks on medicament computation,
which is now using the standard product location quantities. Version
3.6.1 also provides the latest gnuhealth-control center tool.

**List of issues and tasks related to this patchset**:

* bug #57267: Crash when listing the medicaments:
  https://savannah.gnu.org/bugs/?57267
* bug #57266: Remove the 2to3 conversion in updates:
  https://savannah.gnu.org/bugs/?57266


3.6.0
~~~~~

``2019/11/10``

Dear community:

I am very proud to announce the release of the GNU Health 3.6 series !

This version is the result of many developments and integration of ideas from the community.

We are now 11 years old. We should all be very proud because not only we have built the best Libre Health and Hospital Information System, but we have created a strong, committed and friendly international community around it.

**What is new in GNU Health 3.6 series**:

* Both GNU Health client and server are now in Python3
* Remove Python2 support
* GH HMIS server uses Tryton 5.0 LTS kernel (5 year support)
* Client is based on Tryton GTK client 5.2
* Automation on the GH Federation queue management
* Integration to Orthanc DICOM server
* Pages of Life models fully integrated with patient evaluation & GH Federation
* GNU Health camera plugin integrated with the latest OpenCV
* GH Client uses GI. Removed pygtkcompat.
* GH Federation HIS has been migrated from MongoDB to PostgreSQL
* New demo database downloader
* Thalamus uses now uwsgi as the default WSGI
* SSL is the default method for Thalamus and the GH Federation



**Upgrading from GNU Health 3.4**:

* Make a **FULL BACKUP** your kernel, database and attach directories !!!
* Follow the instructions on the Wikibooks
* Read specific instructions found under scripts/upgrade/3.6 of the main source installation tarball, an apply the scripts in the specified order.



**Development focus**

In addition of the GH HMIS server, we will focus the development in the following  areas of the GNU Health ecosystem:

* The GNU Health Federation Portal
* The mobile client
* Interoperability


The GH Federation Portal has already started. It is a VueJS application and provides a single point of entry for individuals, health professionals and epidemiologists to the GNU Health Information system.

The GNU Health Federation now receives information coming from many health institutions and people from a region or country. The GH Federation portal will allow to manage resources, as well as the main point for **analytics** and **reporting** of massive amount of demographics health data generated nationwide. People, health centers and research institutions (eg genomics already can enjoy the benefits from the GNU Health Federation.

The mobile client (MyGNUHealth) development will remain in QT and will be focus on KDE plasma mobile technology, and run in Libre mobile operating systems and devices (such as Pine64). We need fully libre mobile devices if we want to preserve privacy in healthcare.

As far as Interoperability goes, GNU Health is now very interoperable. It uses open coding standards, as well as open formats (XML, JSON, .. ) to exchange messages. We currently have support for read operations in HL7 FHIR for a number of resources. Needless to say, we are open to other open standard communities that are willing to integrate to GNU Health.

Last but not least....no matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, and give us your feedback via them via health@gnu.org

Happy and Healthy Hacking !

3.4.1 (Installer)
~~~~~~~~~~~~~~~~~

``2019/03/18``

Dear community

The GNU Health installer (gnuhealth-setup) has been updated to 3.4.1.

It basically fixes an issue due to the removal of the the pybarcode library from pypi (https://savannah.gnu.org/bugs/?55942)

We have also updated the documentation to always download the latest installer as the first step (https://en.wikibooks.org/wiki/GNU_Health/Installation#Downloading_and_Installing_GNU_Health)

This applies for new installations / migrations.

3.4.1
~~~~~

``2019/03/10``

**Priority**: High

**Summary of this patchset**

Patch 3.4.1 fixes issues related to the generation of the Federation Account, and it adapts the ID field on the federation objects.

The gnuhealth-control program and the documentation / man page have also been updated.

It is important to know that since 3.4.1 and Thalamus 0.9.8, the Health Information System has been migrated from MongoDB to PostgreSQL.

**List of issues and tasks related to this patchset**:

* bug #55595: Remove unimplemented functionality fields from Federation Country
* bug #55594: Traceback when creating a person without a system institution


3.4.1 (Control Center)
~~~~~~~~~~~~~~~~~~~~~~

``2019/03/02``

Dear all

We just released GNU health control center 3.4.1 !

It mainly fixes an issue with the file format of the translation files from pootle on our GNU Health translation portal, when executing the getlang command.

You can update automatically the gnuhealth control center using the command

$ gnuhealth-control update

You can also find the program at our GNU FTP site (https://ftp.gnu.org/gnu/health/)

3.4.0
~~~~~

``2018/11/27``

Dear community

We are proud to announce the release of GNU Health 3.4 series !

It's been over a year of hard work, integrating the latest in technology and Social Medicine into GNU Health.

This versions incorporates many cool features, some of them are :

* The GNU Health Federation model
* Thalamus message server
* New Health Information System (on MongoDB)
* Person Master Index
* MongoDB support (on the HIS)
* Updated UniprotKB database with over 30K protein natural variants
* Contextualized information on genetics and social determinants
* Genetic and family history and environmental factors integrated to the Page of Life and Federation
* The GNU Health Book of Life
* Tryton 4.6 integration on the HMIS node
* All GNU Health packages are natively in Python 3
* Enhanced support for Calendar and WebDAV system
* GNU LIMS improvements in views
* Pypi packages with our own name ("gnuhealth-<package>")
* Native client has a command line interface
* Over 30 new commands for the main daily tasks
* Enhanced GNU Health camera plugin, including zoom
* Activity Log window on the client
* SYSINFO command to retrieve the information about client and server
* Customize the banner on the client
* Reports are generated now in PDF format



**The GNU Health Federation**


The GNU Health Federation (aka, The Federation) is here !
This is revolutionary and ground breaking. With the Federation, we will be able to integrate heterogeneous systems and build large regional and national health networks. No more data isolation. No more silos. The GNU Health Federation is a great tool for the people, health practitioners, research institutions and public health systems.

Relevant demographics and medical information will be up-to-date, no matter where the person and patient visits. It is great tool for early detection on epidemics, improving the health promotion and disease prevention campaigns.

I am also optimist about the role of the Federation in integrative anc precision medicine. It combines Nature and Nurture, and can shed light on the diagnostic and therapeutics of devastating and elusive genetic diseases, cancer and autoimmune disorders.

The GNU Health Federation components (eg, Thalamus), will have their own development process, so they can be integrated with each of the other GNU Health projects without blocking each other.

This journey is just starting, but I trust that, as a community, we'll be able to tackle today and future issues in health.

**Derivative languages / translations**


GNU Health takes the approach of derivative languages, which will simplify the localization effort. Basically, for languages who have many strings in common, will only have to work on those strings that differ from a main source.
Let's take the example of Spanish. The new approach will work in the following way:
* One source language "es"
* Many derivative / regional languages (es_ES, es_AR, es_PE, es_VE ... ).

Until now, each derivative language had, except the local terminology, the same strings as the source. That makes localization harder to maintain,and larger in size.
The new method allow the translators to focus on the main source language, greatly improving the quality of the translation, and without duplication.

Please make sure that you focus on the generic language first, and only add local terms in the derivative language.

**Summary of Upgrade steps**:

* Make a FULL BACKUP your kernel, database and attach directories !!!
* Follow the instructions on the Wikibooks.
* Apply the SQL script "upgrade_34.sql" found under scripts/upgrade/3.4 of the main source installation tarball.
* Upgrade the instance


Last but not least....oo matter how hard we try to avoid them, there will be bugs, so please test the new system, upgrade process, languages, ... and please report them via health@gnu.org

Enjoy Freedom in Healthcare !



3.2.10
~~~~~~

``2018/06/05``

**Priority**: Medium

**Summary of this patchset**

Patch 3.2.10 fixes issues related to the CalDAV functionality, updating the calDAV event after changing an appointment.

The gnuhealth-setup program has also been updated, including numpy for the latest pytools

**List of issues and tasks related to this patchset**:

* bug #54055: Caldav event does not update after changing the appointment


3.2.9
~~~~~

``2017/12/04``

**Priority**: High

**Summary of this patchset**

Patch 3.2.9 mainly fixes issues with real time computation of fields in the evaluation, lab, and APACHE II score system

Minor view reordering on the WHR and BMI fields have been also applied.

**List of issues and tasks related to this patchset**:

* bug #52580: Removing the patient field before saving the record generates an error
* bug #52579: some on_change numeric method operations generate traceback
* bug #52578: WHR should be on the same line as hip and waist fields


3.2.7 & 3.2.8
~~~~~~~~~~~~~

``2017/11/15``

**Priority**: High

**Summary of this patchset**

Yes folks, two for the price of one :-)

* Patch 3.2.7 fixes a problem related to signing a death certificate
* Patch 3.2.8 fixes a depdendency issue related to the calendar_webdav3 package, on installations that use the python packages (setup / pip). The standard installation method is not affected.

We also updated the descriptions and URLs of trytond_calendar_webdav3 and trytond_webdav3 packages, that no longer are supported by Tryton, and that are now GNU Health developments.

**List of issues and tasks related to this patchset**:

* bug #52366: Error when signing the death certificate
* task #14626: Renaming Package names prefix ``trytond_`` from Pypi

(https://savannah.gnu.org/task/index.php?14626)

3.2.6
~~~~~

``2017/10/28``

**Priority**: High

**Summary of this patchset**

Version 3.2.6 fixes two issues , one related to the invoice discount associated to an insurance plan (health_insurance package), and the other related to free time slots in a health professional calendar (health_calendar and health_qrcodes packages)

**List of issues and tasks related to this patchset**:

* bug #52298: Traceback generating an invoice from service with an insurance policy plan
* bug #52275: Traceback when creating a free slot in appointments or work schedule


3.2.5
~~~~~

``2017/10/07``

**Priority**: High

**Summary of this patchset**

Version 3.2.5 fixes issues on reports (patient evaluation, appointment and QRCODES), mainly linked to lingering obsolete python2 unicode function that is no longer used in GNU Health 3.2 series, that uses Python 3

**List of issues and tasks related to this patchset**:

* bug #52179: Traceback due to obsolete unicode method in reports


3.2.4
~~~~~

``2017/10/04``

**Priority**: High

**Summary of this patchset**

Version 3.2.4 provides an important fix on the services model, that prevented to generate the related invoice, due to changes on the data model of Tryton 4.2 from previous versions.
Other minor bug fixes related to the prescription report have been also fixed.

**List of issues and tasks related to this patchset**:

* bug #52160: Issues related to invoice type and domain when creating the service invoice
* bug #52167: Selection field translations in prescription report are not translatable
* bug #52168: Rename Prothesis model name from Amputation


3.2.3
~~~~~

``2017/09/15``

**Priority**: High

**Summary of this patchset**:

Version 3.2.3 provides the updated gnuhealth-control and gnuhealth-setup programs, the latter including the bcrypt library. It also fixes a duplicated field on the tree view for the prescription line.

**List of issues and tasks related to this patchset**:

* bug #52020: Missing bcrypt dependency in gnuhealth-setup
* bug #52038: Field history is repeated in the tree view of the prescription line

**Additional Installation Notes**

If you are applying the patch (not a new installation) you need to install locally the bcrypt package.

Login as the "gnuhealth" admin user, and execute :

* Stop the GNU Health Tryton instance
* Install the Bcrypt package
  $ pip3 install --user bcrypt
* Restart the GNU Health Tryton server


3.2.2
~~~~~

``2017/08/27``

**Priority**: Medium

**Summary of this patchset**:

* health_imaging: Update the default health doctor retreival to the current method

**List of issues and tasks related to this patchset**:

* bug #51864: Default doctor retrieval on Dx Imaging using obsolete method


3.2.1
~~~~~

``2017/07/22``

**Priority**: High

**Summary of this patchset**:

* Fix view error on lab order.

**List of issues and tasks related to this patchset**:

* bug #51537: Missing ID on lab separator view


3.2.0
~~~~~

``2017/07/01``

Dear community

I am proud to announce the release of GNU Health 3.2 series !

It's been over a year of hard work, integrating the latest in technology and Social Medicine into GNU Health.

This versions incorporates many cool features, some of them are :

* Tryton 4.2 integration
* All GNU Health packages are now written in Python 3
* Enhanced support for Calendar and WebDAV system
* Updated Crypto packages
* Link lab orders with health services
* Better language and localization, that optimizes translation for regional languages
* Add code39 to lab tests
* Include the Domicilary Unit address in the main person information
* Improved gnuhealth-setup and gnuhealth-control programs
* Patient, Medicament and Services can now be activated / deactivated



**New Modules**:

* health_ems : Emergency and Ambulances Management
* health_insurance : Insurance management and pricelists
* health_genetics_uniprot : Uniprot DB for thousands of genetic natural variants and phenotypes
* health_crypto_lab : Digital signatures for lab orders
* health_services_lab : Integrate lab orders into services



**The GNU Health Federation**

In addition to all these new features and enhancements, probably the most revolutionary and exciting feature of the GNU Health project at this time is the GNU Health Federation.

The GNU Health Federation goal is to make a distributed network of multiple, heterogeneous nodes. The main components are :

* The GNU Health Information System (on MongoDB)
* The GNU Health Thalamus (Message and Authentication Server).
  See https://pypi.python.org/pypi/thalamus/0.0.6
* The participating nodes : GNU Health HMIS, mobile applications, research centers, etcetera.

The GNU Health Federation will produce more quality information and at a better pace. It will also separate the traditional GNU Health HMIS transactional and operational model, from the analytic model that will be taken by the GNU Health Information System on a document database (MongoDB).

The GNU Health Federation, the Health Information System will also provide a unique ID and unique history per person. No data isolation, and no data duplication.
The demographics and medical history of people will updated in realtime, and people will be able to go from one center to the other in the region or country, knowing that all the relevant information will be at timely updated in any center she or he visits.

The GNU Health Federation components (eg, Thalamus), will have
their own development process, so they can be integrated with each of the other GNU Health projects without blocking each other.

GNU Health 3.2 will be the first release where we could start focusing on the GNU Health Information

**New model for translations**


GNU Health takes the approach of derivative languages, which will simplify the localization effort. Basically, for languages who have many strings in common, will only have to work on those strings that differ from a main source.
Let's take the example of Spanish. The new approach will work in the following way:
* One source language "es"
* Many derivative / regional languages (es_ES, es_AR, es_PE, es_VE ... ).

Until now, each derivative language had, except the local terminology, the same strings as the source. That makes localization harder to maintain, and larger in size. The new method allow the translators to focus on the main source language, greatly improving the quality of the translation, and without uplication.


**Summary of Upgrade steps**:

* Make a full backup your kernel, database and attach directories !
* Follow the instructions on the Wikibooks.
* Upgrade the instance
* Apply the SQL script "upgrade_32.sql" found under scripts/upgrade/3.2 of the   main source installation tarball.


No matter how hard we try to avoid issues, there will be bugs, so please test the new system, upgrade process, languages, ... and please report them via health@gnu.org

Enjoy Freedom in Healthcare !


3.0.8
~~~~~

``2017/03/25``

Dear community

GNU Health 3.0.8 patchset has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.8.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Fix missing view declaration on module health_disability in pypi based installers (eg, SuSE, Debian). This issue does not affect to installations that used the vanilla installation method (gnuhealth-setup install)


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.7, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


List of issues and tasks related to this patchset:

* bug #50635: Missing declaration of view directory on setup.py on health_disability module


For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

For detailed information about each task, you can visit https://savannah.gnu.org/task/?group=health


3.0.7
~~~~~

``2017/03/15``

Dear community

GNU Health 3.0.7 patchset has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.7.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Fix traceback on patient critical info with non-ascii characters from health conditions in the allergy group
* Fix several issues related to the inpatient meal orders.


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.6, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues and tasks related to this patchset**:

* Bug #50464 Official given and family names not updating on party
* Bug #50460 Use of gender when using growth charts in transgender population
* Bug #50437 Missing declaration of view directory on setup.py

For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

For detailed information about each task, you can visit https://savannah.gnu.org/task/?group=health

3.0.6
~~~~~

``2017/02/12``

Dear community

GNU Health 3.0.6 patchset has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.6.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Fix traceback on patient critical info with non-ascii characters from health conditions in the allergy group
* Fix several issues related to the inpatient meal orders.


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.5, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

**Follow the general instructions at**:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues and tasks related to this patchset**:

* bug #50281: Traceback when displaying patient critical info in non-english languages
* bug #50288: Wrong widget for mealtime field on meal order tree view
* bug #50269: Traceback when assigning a new meal order

For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

For detailed information about each task, you can visit https://savannah.gnu.org/task/?group=health

3.0.5
~~~~~

``2016/12/12``

Dear community

GNU Health 3.0.5 patchset has been released !

**Priority**: Medium

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.5.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Update to the latest WHO ICD10 version 2016, update descriptions and deactivate obsolete codes.
* Fix issues on prescription reports


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.4, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues and tasks related to this patchset**:

* task #14262: Update to ICD10 - 2016 version
* bug #49414: Error when printing prescription using review dates


For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

For detailed information about each task, you can visit https://savannah.gnu.org/task/?group=health

3.0.4
~~~~~

``2016/10/22``

Dear community

GNU Health 3.0.4 patchset has been released !

**Priority**: Medium

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.4.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Fix issues on summary reports
* Fix timezone issue on patient hospitalization admission


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.3, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues related to this patchset**:

* 49405 Error on summary report when no date of birth is assigned to the person
* 49181 Check admission date with UTC

 For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

3.0.3
~~~~~

``2016/08/14``

Dear community

GNU Health 3.0.3 patchset has been released !

**Priority**: Medium

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.3.tar.gz)

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Fix issues when updating demographics on existing person


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.2, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues related to this patchset**:

* health core: bug #48695: Error when adding attribute in existing person

For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

3.0.2
~~~~~

``2016/07/13``

Dear community

GNU Health 3.0.2 patchset has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.2.tar.gz)


**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks). Don't use it if you use an alternative method or if your distribution does not follow the GNU Health packaging guidelines.

**Summary of this patchset**:

* Issues with GTK client on MS, and performance improvements
* GNU Health control now includes automatic download of security patches from its components[1]. There is always Security Advisory (SA) associated to the patch.
* New site for GNU Health translation portal is now at translate.gnusolidario.org. GNU Health control has been updated to fetch the language packs from the new URL.
* Bug fixes on reports, especially on dates, ages and date formats.
* Gnuhealth-control has been updated. These tools are also packaged separately, with their own numbering, so you can always download the latest version without the need of applying a patchset.


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.


**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.1, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues related to this patchset**:

* client: #47583: Windows client crashes rendering SVG files
* health_iss: #48491: Remove TimeDelta for age and use patient gender
* health: #47983: Performance and scalability issues on party address
* health_stock: #47739: Allow to use storage for pharmacy
* gnuhealth-control : Update to 3.0.3. Use SSL for main GNU URL. Include automatic download of security advisories. Updated URL for translation portal (translate.gnusolidario.org)
* health: #47562: Domain error when modifying a party name
* health : #47312: Use Subdivision as label in DU
* task #13904: Use user specific date format in reports. Include DoB validation
* health_socioeconomics : remove TimeDelta function and use standard GNU Health age computation in Family and Socioeconomic assessment


1.- https://savannah.gnu.org/forum/forum.php?forum_id=8482

For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

3.0.1
~~~~~

``2016/01/31``

Dear community

GNU Health 3.0.1 patchset has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Summary of this patchset
* Updating your system with the GNU Health control Center
* Installation notes
* List of issues related to this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow applying bug fixes and updates on production systems. Always try to keep your production system up-to-date with the latest patches.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

NOTE: Patchsets are applied on previously installed systems only. For new, fresh installations, download and install the whole tarball (ie, gnuhealth-3.0.1.tar.gz)

**Summary of this patchset**:

* The main issues resolved have to do with the age representation . There were issues with the generic timedelta method, so we reverted to the original relativedelta function, with deals better with ages. Timedelta (and its related Tryton fields.TimeDelta) is still used to show shorter periods of time, such as patient waiting times, duration of evaluations / surgeries, etc...
* Bug fixes on reports, especially on dates, ages and date formats.
* The gnuhealth-setup and and gnuhealth-control have been updated. These tools are also packaged separately, with their own numbering, so you can always download the latest version without the need of applying a patchset.


Refer to the List of issues related to this patchset for a comprehensive list of fixed bugs.

**Updating your system with the GNU Health control Center**


Starting GNU Health 3.x series, you can do automatic updates on the GNU Health and Tryton kernel and modules using the GNU Health control center program.

Please refer to the administration manual section ( https://en.wikibooks.org/wiki/GNU_Health/Control_Center )

The GNU Health control center works on standard installations (those done following the installation manual on wikibooks).

**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 3.0.0, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at:

* https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* https://en.wikibooks.org/wiki/GNU_Health/Control_Center


**List of issues related to this patchset**:

* #47031 gnuhealth-control status error when multiple instances are running
* #47023 Patient CAGE score not available to admin group
* #46996 vobject version name changed
* #46991 health : gnuhealth.patient has no attribute "patient_age" at immunization status report
* #46961 Use relative delta for age
* #46953 Error on creating appointment if healthprof.name.internal_user == None
* #46950 Error when generating the summary report
* #46947 Traceback when generating the invoice associated to a prescription service
* #46942 Prescription report : Age on prescription is shown in days
* #46908 Use biological sex in view attributes

For detailed information about each issue, you can visit https://savannah.gnu.org/bugs/?group=health

3.0.0
~~~~~

``2016/01/11``

Dear all

After one year of work, I am very happy and proud to announce the release of GNU Health 3.0 series !

Following is a brief summary of the release highlights

**New features**:

* Tryton 3.8 compatibility and responsive web client.
* Multiple person names, compliant with FHIR HL7, and flexible person name formats
* Automatic inclusion of medicament history from the prescription
* History of a person socioeconomic assessments
* Link to patient health conditions
* Health conditions now visible from patient main page
* Any person can be mapped to an internal user, not only the health professionals
* Add person biological sex and gender properties.
* Check all evaluations related to a person specific healh condition
* Easy change a patient appointment status from the tree view (checked in, no show, ... )
* Automatic computing of a patient evaluation waiting time
* Hospitalization and outpatient discharge reason
* Merge chronic with followups evaluations. Merge ambulatory with outpatient evaluations
* Optimize CAGE (Alcoholism status assessment) view
* Enhanced Crypto plugin and module
* Create / see all the evaluations within a hospitalization
* Health center and hospitalization meals management
* Improved surgery module (surgery team, supplies, status, wound class, post-op dx, reservation workflow)
* Health services reporting
* Automatic prescription concentration, form and route based on the med
* Enhanced functionality in patient evaluation.
* Improved reporting
* Include / Update unitests ( Thanks Cedric !)
* Improved ergonomics for patient conditions and history.
* Patient protheses and amputation history ( Thanks Lao team !)
* Automatic inclusion of prescription lines in Service document
* Updated disease groups (thanks Chris Zimmerman !)
* Improve patient clinical history report
* New installer gnuhealth-setup tool
* Improved gnuhealth-control center
* Installation of language packs in one single instruction.
* Many other additions and community contributions ...


**New Modules**:

* WHO ICD9 Volume 3 (procedural codes) (in addition to ICD10-PCS and ICPM) .( Thanks Min of Health of Morelos, Mexico !)
* Ophthalmology module ( thanks Sivadas !)
* Functioning and Disability module [1]



**Translation portal moves to Pootle**


Since GNU Health 3.0, the main translation portal is at GNU Pootle server [2]

The following languages have been requested, and they are now included:

* Arabic
* Chinese (China)
* English (United Kingdom)
* French
* German (Austria)
* Greek
* Italian
* Japanese
* Kannada
* Lao
* Portuguese (Brazil)
* Spanish (Argentina)
* Spanish (Ecuador)
* Spanish (Mexico)
* Spanish (Peru)
* Spanish (Spain)


Some of them are still in the process of migrating the translation files from Transifex to the GNU Pootle server. It will take a bit until everything is in place. Of course, you can update your server translation packs at anytime,  using the getlang command of gnuhealth-control program.

There is a new mailing list (health-i18n) dedicated to the localization and translation of GNU Health[3]

During the upcoming weeks we'll be updating the documentation,
improving the demo database, as well as working on the translations.

Of course, we'll be fixing any bugs you will find in this new
release :)

Many, many thanks to all of you who have contributed to this
release, in any way !

All the best,

| 1.- https://en.wikipedia.org/wiki/International_Classification_of_Functioning,_Disability_and_Health
| 2.- https://chapters.gnu.org/projects/health/
| 3.- https://lists.gnu.org/mailman/listinfo/health-i18n
| 4.- https://en.wikipedia.org/wiki/ICD-9-CM_Volume_3



.. _changelog:changelog-versions_2.x.x:

Versions 2.x.x
--------------

2.8.1
~~~~~

``2015/02/08``

Dear community

GNU Health patchset 2.8.1 has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Summary of this patchset
* Installation notes
* List of Bugs


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow quick bug fixes and updates for production systems.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation.

NOTE: Patchsets are applied on previously installed systems only. For new installations, download and install the whole tarball (ie, gnuhealth-2.8.1.tar.gz)

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

**Summary of this patchset**:

* Affected modules (excludes localization / typos) : health, health_lab, installer
* health : Fix traceback error when creating a company and assigning a code with non-ascii characters
* health_lab : Fix default date analysis
* Installer : In new installations, the serverpass script is called automatically.



**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 2.8.0, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

Source the GNU Health profile (source $HOME/.gnuhealthrc) to update your environment

Update your database ( trytond --all )

**List of bugs related to this patchset**:

* #44165     Subtle bug in date of analysis for lab tests
* #44182     2.8 installer fails with "TRYTOND_CONFIG variable not set"
* #44189     Ascii code Error when trying to create Institution

2.8.0
~~~~~

``2015/02/02``

Dear GNU Health community

After 7 months of intense work, I am happy to announce GNU Health 2.8 series !

Here is a partial list of the new features :

* Tryton 3.4 compatibility
* Distributed environment, data aggregation and synchronization features
* Universal Person Unique Identifier (PUID) and UUID implementation
* Country immunization schedule
* HL7 FHIR server (thank you, Chris Zimmerman !)
* Automatic person immunization status check
* Vital Records System : Birth and Death certificates
* Enhanced security for Tryton server credentials
* Injury Surveillance System (Thank you, Jamaica Ministry of Health !)
* GNU Health control program : Automatic backups and patches
* Enhanced Crypto features / GNU Privacy Guard integration
* New models including in digital signatures
* Demographics reports



There are many other improvements and bug fixes that have not been included in this summary document. You can read the Changelog for a detailed description of all the activity.


**Installation**


If you are installing GNU Health as the first time, follow the
instructions in https://en.wikibooks.org/wiki/GNU_Health/Installation


**Upgrade procedure**


If you already have a GNU Health system in your health center, you should upgrade it to 2.8.0 . As always, the upgrade path is included in GNU Health.  The upgrade for version 2.8.0 is straight forward :

Follow the Upgrade Instructions in the Wikibook
https://en.wikibooks.org/wiki/GNU_Health/Upgrade


**Official Languages**


GNU Health now includes**English, Chinese, French, Greek, Italian, Japanese, Portuguese and  Spanish**as the official languages. The language packs of the official languages are included in the GNU Health package, with all the modules, so there is no need to download.

There are **over 100 language teams for GNU Health !** If you are a
language maintainer and want to include your language for the next stable release, please send us a mail to health@gnusolidario.org .


Thanks !


A big thank you to my colleagues from GNU Health community; GNU
Solidario; Thymbra and Tryton, and to the Free Software movement.

Enjoy the new version and report any bug / issues / improvements to health@gnu.org !

T : @gnuhealth


Back to the top


2.6.4
~~~~~

``2014/10/04``

Dear community

GNU Health patchset 2.6.4 has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Summary of this patchset
* Installation notes
* List of Bugs


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow quick bug fixes and updates for production systems.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation. Some of them, and thanks to the magic of Tryton can be applied to running system.

NOTE: Patchsets are applied on previously installed systems only. For new installations, download and install the whole tarball (ie, gnuhealth-2.6.4.tar.gz)

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

**Summary of this patchset**:

* Affected modules (excludes localization / typos) : health, health_calendar
* health : Fix appointment institution link, to point now to the new Institution model.
* health_calendar : Fix Health Professional Work Schedule wizard



**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 2.6.3, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

Follow the general instructions at https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

Source the GNU Health profile (source $HOME/.gnuhealthrc) to update your environment

Update your database ( update=all )

**List of bugs related to this patchset**:

* #43347     Invalid assignment of institution in appointments ( https://savannah.gnu.org/bugs/index.php?43347 )
* #43350 Institution field in Work Schedule still points to party ( https://savannah.gnu.org/bugs/index.php?43350 )


2.6.3
~~~~~

``2014/09/09``

Dear community

GNU Health patchset 2.6.3 has been released !

**Priority**: High

**Table of Contents**:

* About GNU Health Patchsets
* Summary of this patchset
* Installation notes
* List of bugs fixed in this patchset


**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow quick bug fixes and updates for production systems.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation. Some of them, and thanks to the magic of Tryton can be applied to running system.

NOTE: Patchsets are applied on previously installed systems only. For new installations, download and install the whole tarball (ie, gnuhealth-2.6.3.tar.gz)

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

**Summary of this patchset**:

* Affected modules (excludes localization / typos) : health, health_lab, health_socioeconomics
* health : The relate action on appointments is now a wizard, to create patient evaluations from appointment (due to Tryton change on action domains); more validations and constraints on operational sectors, specialties and insurances; fix appointment report.
* health_socioeconomics : Fix Smilkstein Family APGAR (FAPGAR) on the field "help from family".


**Installation Notes**


You must apply previous patchsets before installing this patchset. If your patchset level is 2.6.2, then just follow the general instructions. You can find the patchsets at GNU Health FTP site (ftp://ftp.gnu.org/gnu/health/)

**Read** and follow the general instructions at https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets

Source the GNU Health profile (source $HOME/.gnuhealthrc) to update your environment

Update your database ( update=all )

**List of bugs fixed in this patchset**:

* #43179 The Insurance number must be unique for each insurance company ( https://savannah.gnu.org/bugs/index.php?43179 )
* #43111 Traceback when creating an evaluation from the appointment form ( https://savannah.gnu.org/bugs/index.php?43111 )
* #43092 column b.doctor does not exist (https://savannah.gnu.org/bugs/index.php?43092)
* #43090 Specialties should be unique per health professionals (https://savannah.gnu.org/bugs/index.php?43090)
* #43089 Missing unique constraint on health professionals ( https://savannah.gnu.org/bugs/index.php?43089)
* #43085 Institution Specialty should be available on existing records only ( https://savannah.gnu.org/bugs/index.php?43085 )
* #43083 Operational Sectors and Specialties for each institution must be unique ( https://savannah.gnu.org/bugs/index.php?43083 )
* #43059 Error creating specialties on institutions ( https://savannah.gnu.org/bugs/index.php?43059 )
* #43048 Assertion Error with datetime, it does not possible install health module ( https://savannah.gnu.org/bugs/index.php?43048 )
* #42938 Error on Family APGAR selections ( https://savannah.gnu.org/bugs/index.php?42938 )


2.6.2
~~~~~

``2014/08/07``

Dear community

GNU Health patchset 2.6.2 has been released !

**Priority**: Medium

Table of Contents:

* About GNU Health Patchsets
* Summary of this patchset
* Installation notes
* List of Bugs



**About GNU Health Patchsets**


We provide "patchsets" to stable releases. Patchsets allow quick bug fixes and updates for production systems.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation. Some of them, and thanks to the magic of Tryton can be applied to running system.

**NOTE**: Patchsets are applied on previously installed systems only. For new installations, download and install the whole tarball (ie, gnuhealth-2.6.2.tar.gz)

For more information about GNU Health patches and patchsets you can visit https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets


**Summary of this patchset**


This is a small patchset, related mostly to reports and wizards:

* Affected modules (excludes localization / typos) :   health, health_lab, health_imaging
* health : Fix prescription report
* health_lab :Check for health professional on test request
* health_imaging : Check for health professional on Dx imaging request


**Installation Notes**:

* You must apply patchset 2.6.1 before installing this patchset. If you have already apply 2.6.1, then just follow the general instructions. Otherwise, download and apply patchset 2.6.1 (ftp://ftp.gnu.org/gnu/health/gnuhealth_patchset-2.6.1.tar.gz)
* Follow the general instructions at https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* Source the GNU Health profile (source $HOME/.gnuhealthrc) to update your environment
* This patchset does not require a database update.


**List of bugs related to this patchset**:

* health: error in prescription report when assigining a revision date to prescription line ( https://savannah.gnu.org/bugs/?42841 )
* health_lab : Error in printing lab test result ( https://savannah.gnu.org/bugs/?42843 )
* Check for health professional when requesting tests (https://savannah.gnu.org/bugs/?42914 )


2.4.1
~~~~~

``2014/02/18``

GNU Health patchset 2.4.1 has been released !

**SUMMARY OF BUG FIXES / TASKS**


**Affected modules / functionality**:

* health_inpatient:

  * Fix health professional display on the patient discharge (changeset 1182:6b452268a2a5 )

* health_surgery:

  * Fix surgery report traceback due to date format (changeset 1177:33e45da63c55 )

* health_services:

  * Update health services wizard to be Tryton 3.0 compatible on the invoice generation (changeset 1178:83f26d207cb0)

* PIP setup.py:

  * Update setup.py to Tryton version 3.0 ( changeset 1174:3eaa6b06807f )
  * Update missing module health_stock setup.py to Tryton version 3.0 (changeset 1175:25948f16ffab)


**About GNU Health Patchsets**

We provide "patchsets" to stable releases (with even minor number). This allows quick bug fixes and updates for production systems.

Patches and Patchsets maximize uptime for production systems, and keep your system updated, without the need to do a whole installation. Some of them, and thanks to the magic of Tryton can be applied to running system.

Patchsets are installed on previously installed systems. For new
installations, download the regular package (ie, gnuhealth-latest.tar.gz)

**Installation Notes**:

* Follow the general instructions at https://en.wikibooks.org/wiki/GNU_Health/Patches_and_Patchsets
* No special instructions for this patchset


Please send your comments and suggestions to health@gnu.org

.. _changelog:changelog-versions_1.x.x:

Versions 1.x.x
--------------

1.8.0
~~~~~

``2013/02/20``

It's been a couple of weeks since the release of GNU Health **series 1.8**, and we're thrilled on the evolution of the system, and its adoption by the community.

This latest series is compatible with Tryton 2.6 and has many improvements, in the core and reporting modules, among others. As usual, the migration from previous versions are included.

The other good news is that, being compatible with Tryton 2.6 allows the connection from **mobile devices** with the Android Operating System .
Thanks to the great Tryton development framework, and to the fantastic job done by SCIL  in the development of the Android client for Tryton, GNU Health servers can now be accessed directly from your mobile device.

 You can find the Android client on Google Play . For the development process, check the SCIL page .

There are more good news on the way. The **web client** is also around the corner, and we will have 3 different ways to connect to GNU Health. From the standard GTK interface, the Android client, or your web browser.

Make sure you upgrade your database to the latest GNU Health version. The upgrade scripts and the instructions are always incorporated in the new version. The upgrade process is an integral part of GNU Health and, of course, it's completely free.

e-Health for all !

**About GNU Health**


GNU Health is a free Health and Hospital Information System that provides the following functionality :

* Electronic Medical Record (EMR)
* Hospital Information System (HIS)
* Health Information System (Epidemiology)


GNU Health has been awarded the **Best Project of Social Benefit** from the Free Software Foundation in 2012.
In 2013, GNU Health received the awards for  most revolutionary Free Software and software with the largest potential from PortalProgramas.


GNU Health is an **official GNU Package**, chosen by Richard Stallman and part of GNU Solidario. GNU Solidario is a NGO that delivers education and health to emerging economies with free software. GNU Health is the Hospital Information System chosen by the **United Nations** International Institute of Global Health.  GNU Solidario and the United Nations University, International Institute for Global Health have signed an agreement to implement and to train GNU Health globally.

Main site : http://health.gnu.org

1.6.4
~~~~~

I am happy to announce the release of GNU Health **1.6.4**!

This version brings many improvements, especially in the Obstetrics and Nursing modules. A quick summary :

**Features**

**Gynecology and Obstetrics module**

* Functionality covers pre-conception; genetic and nutrition counseling; prenatal evaluations; antenatal and intrapartum monitoring; labor and puerperium
* Improve obstetrics views and navigation
* Automatic Pregnancy due date calculation from last menstrual period (LMP)
* Pregnancies include the prenatal, antepartum and puerperium
* Automatic, functional notification of patient pregnancy
* Automatic computation of gestation age
* Improved prenatal evaluation information:

  * Include ultrasound information
  * Fetal biometry and activity
  * IUGR and its forms
  * Simplify end of birth recording, as well as maternal death information
  * Include preeclampsia, invasive placentation and other abnormalities during pregnancy


**Lifestyle**:

* Include CAGE alcoholism score


**Pediatrics**:

* Optimize Pediatric Symptoms Checklist for psychosocial risk


**Nursing**:

* New outpatient / ambulatory care functionality


-> Bug fixes


**Installation Notes**


Please follow the instructions at the Wikibook GNU Health
documentation Portal : http://en.wikibooks.org/wiki/GNU_Health

**Upgrade Notes**


There are no specific notes for this upgrade, so upgrading your previous GNU Health version should be straight forward. Of course, before any upgrade, please backup your database and follow the general upgrade instructions at the GNU Health Wikibook : http://en.wikibooks.org/wiki/GNU_Health/Upgrade


1.6.3
~~~~~

``2012/08/28``

Dear all

We are proud to announce the release of GNU Health 1.6.3, the Free Health and Hospital Information System. This version brings major improvements in the hospital information system, both from the administrative and patient management. Here is a quick summary of the main changes :

**New Features**:

* Patient Nutrition management. Complex combinations that take into account therapeutics, pre-existing conditions, surgeries, lifestyles, vegetarianism and other belief-based diets.
* Inpatient medication medication and history log.
* New nursing module
* Nursing roundings ( evaluations, procedures, medications ... )
* New user profiles (doctors, nurses, clerks, ...)
* New appointment reports
* Improved standard security profiles
* The translation project is now entirely done from Transifex, so the health center will install only the languages they need
* Revised and improved look and feel, from views to icons
* Many models datafiles ( medicaments, WHO essential meds, .. ) can be now modified from the client.
* Improve installation scripts and Archlinux / Parabola support
* Improve search patient methods
* Bugfixes


**Credits**


Thanks to all of you who have collaborated in the mailing lists and IRC channels. The end users, developers, Tryton community. Many thanks to the GNU community and to the **Free Software Foundation** ( http://www.fsf.org ) for hosting GNU Health !

Thanks to organizations like the **United Nations** International Institute for Global Health - UNU IIGH - for their commitment with GNU Health. UNU is giving GNU Health trainings and capacity building to countries in Asia and Africa.

**Upgrade Notes**


There is no specific notes for this upgrade, so upgrading your previous GNU Health version will be straight forward. Please follow the general upgrade instructions at the GNU Health Wikibook : http://en.wikibooks.org/wiki/GNU_Health/Upgrade

More information at : http://health.gnu.org

1.4.4
~~~~~

``2012/03/11``

Dear all

I'm happy to announce the new stable version of GNU Health **1.4.4**

This version has great new features, such as *Medicament Pregnancy
Categories, Prescription Decision Support and patient and newborn QR codes identification*

We have also included and updated translations for : **French, Greek, Italian, Persian (Farsi) and Spanish**

We'll be updating the documentation portal at Wikibooks with the
content of this new version. I invite you to download and test it, as usual from Savannah ( https://savannah.gnu.org/projects/health/ )

For more information please check the official homepage at http://health.gnu.org

Thanks to the GNU community contributing your time and talent to Health.

Best,
Luis Falcon


1.4.1
~~~~~

``2011/10/30``

I'm happy to announce the release of **GNU Health 1.4.1**, in which we have incorporated support for PyPI, the Python Package Index

This version is compatible with the latest Tryton release (2.2.0). Now GNU Health is also a set of python modules, fully integrated to the Python community.


Thanks to the magic of pip, and the help of the Tryton community ( Cedric Krier, et al ), installing the latest GNU Health version is as easy as running

pip install --user trytond_health_profile

This will install the requirements ( the tryton server and all the standard GNU Health modules ) automatically and in your "$HOME/.local" directory. I will be updating the installation process at the wiki today.
The main site is the GNU Savannah where all the development and discussion takes place.

There are many improvements, bug fixes and news features, some of them :

* CalDav compatibility (it allows complex calendar views and settings for appointments and hospitalizations)
* Support for JSON RPC protocol
* Fully Tryton 2.2 compatible
* Enhanced Medication form
* New Medicament categories
* Medication pregnancy category
* Included the latest WHO essential medicines (17th edition)
* New translation engine (to be used with .po format)
* Improved Laboratory model and functionality


Thanks to all of you for contributing with your code, testing, translating and documenting the project !



**About GNU Health**

GNU Health is a Free (GPL v3+) Health and Hospital Information System that provides the following functionality :

* Electronic Medical Record (EMR)
* Hospital Information System (HIS)
* Health Information System


GNU Health is an **official GNU Package**.

GNU Health is part of **GNU Solidario**. GNU Solidario is a NGO that delivers education and health to emerging economies with free software.

GNU Health is the Hospital Information System chosen by the **United Nations International Institute of Global Health**.

Main site : http://health.gnu.org

Governments hosting GNU Health through their portals :

* European Commission (EU) , OSOR
* Brazil: Portal do Software Público Brasileiro (SPB)


1.3.3
~~~~~

``2011/09/19``

I'm pleased to announce GNU Health 1.3.3

This version could be considered a milestone in itself, due the major changes and new features:

* New naming convention of modules and models. From  medical to gnuhealth
* New installation scripts (setup.py) .
* Major improvements in the Laboratory module. Now we have automatic visual alerts, possibility to exclude analytes from the analysis, qualitative and quantitative testing. Contextualize results in the patient status (gender, age, comorbidities ... ).

As in every new release, bugs are fixed, navigation improved and new features are includes.

Since Health is now part of the official GNU system, the development is hosted at GNU Savannah, where you can also download the latest version.

Last but not least...  many thanks to Cedric and Tryton community for getting involved in the GNU Health project !

**About GNU Health**

GNU Health (formerly known as "Medical") is a free (GPL v3+ license), Health and Hospital Information System that provides the following functionality :

* Electronic Medical Record (EMR)
* Hospital Information System (HIS)
* Health Information System

GNU Health is part of GNU Solidario. GNU Solidario is a NGO that delivers education and health to emerging economies with free software.

Main site : http://health.gnu.org

Governments hosting GNU Health through their portals :

* European Commission (EU) , OSOR


* Brazil: Portal do Software Público Brasileiro (SPB)


You can check the original post, with screenshots at :  http://blog.gnusolidario.org/2011/09/gnu-health-133-released.html

Project at the Savannah :
https://savannah.gnu.org/projects/health/

Thanks,

--
Luis Falcón

GNU Health

health.gnu.org

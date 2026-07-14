.. _userguide-basics-coremodule-vitalrecords:vital_records:

Vital Records
=============
.. _userguide-basics-coremodule-vitalrecords:vital_records-about_vital_records:

About Vital Records
-------------------

Since version 2.8, GNU Health also serves as a :wikipedia:`Vital Record System <Vital_record>`, allowing to create and sign birth and death certificates.

.. _userguide-basics-coremodule-vitalrecords:vital_records-birth_certificates:

Birth Certificates
------------------

The person birth certificate is part of the GNU Health Vital Record System. It links the person to an official document with the information used in most countries. The information about the date of birth is taken from the person. In addition, if your institution has the :ref:`userguide-modules-pediatrics:pediatrics` module installed, the date of birth is automatically taken from the neonatology department.


.. note::
        The best way to access and enter the birth certificate is the relate action from the people (party) model. This will fill automatically fields such as the person and birth date

Alternatively, birth certificates can be managed via *Health → Demographics → Birth certificates* section.

A birth certificate stores the following information:

* *Person:* The name of the newborn (link to a person record)
* *Date of Birth* : By default, taken from the person (party) model.
* *Mother* and *Father* (links to person records)
* *Institution:* The health institution where the birth took place (or the health institution that certifies a delivery at home)
* *Code*
* *Country* and *Subdivision*: These fields will be automatically filled as default values, with the country and subdivision (such as province) of the institution.
* *Observations*

If you create a birth certificate record it will have the *Draft* state by default. You can switch to the *Signed* state by clicking the *Sign* button. You will be prompted to confirm that you want to sign the birth certificate; please note that signing a birth certificate can not be undone. Signing a birth certificate will add the name of the certifier (the health professional) plus date and time of the signing process.

.. _userguide-basics-coremodule-vitalrecords:vital_records-death_certificates:

Death Certificates
------------------

The death certificate is a key document, since it has legal, administrative, demographic and epidemiological significance.

Death certificates work very much the same way like birth certificates, but they store more information about causes and circumstances of death. The best way to access a person death certificate is by using the related action from the Party model (refer to the birth certificate section). Alternatively, the can be accessed via *Health → Demographics → Birth certificates* section.

A death certificate stores the following information:

*Main* section:

* *Person:* The name of the dead person (link to a person record)
* *Date*: Date of Death, including hour and minute.

*Place* section:

* *Place:* Details about where the person died (at home, at work, in a public place, in a health institution)
* *Details* about the place
* *DU:* The exact building/address (link to a :ref:`userguide-basics-coremodule-domiciliaryunits:domiciliary_units` record)
* *Institution:* The health institution where the person died (or the health institution that certifies a death which occurred at home, at work, or in a public place)
* *Op. Sector*: Operational Sector where the death occurred.
* *Country* and *Subdivision*, such as province. These two fields are automatically filled with the address information from the health institution.

*Cause* section:

* *Cause:* The immediate cause of death (link to a *Disease* record)
* *Underlying conditions:* Medical conditions that lead to death, in chronological order.

*Other* section:

* *Type of death:* Choose between "Natural", "Suicide", "Homicide", "Undetermined", or "Pending Investigation"
* *Autopsy:* Check if an autopsy has been performed
* *Code*: Unique identifier to the certificate. The format / nomenclature is country-dependent.
* *Observations*

If you create a death certificate record it will have the Draft state by default. You can switch to the Signed state by clicking the Sign button. You will be prompted to confirm that you want to sign the death certificate; please note that signing a death certificate can not be undone. Signing a death certificate will add the name of the certifier (the health professional) plus date and time of the signing process.

.. _userguide-basics-coremodule-vitalrecords:vital_records-digital_signatures:

Digital Signatures
------------------

It is highly recommended that you use digital signatures to sign the death certificate. The GNU Health Cryptography module :code:`health_crypto` has the functionality to verify any change to the document. It also allows you to use your private key to sign the document, giving it legal value in many countries. Once signed, the document can be verify against the person who ultimately signed the certificate.

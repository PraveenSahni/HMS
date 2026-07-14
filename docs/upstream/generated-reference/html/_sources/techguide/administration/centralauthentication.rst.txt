.. _techguide-administration-centralauthentication:central_authentication:

Central Authentication
======================
.. _techguide-administration-centralauthentication:central_authentication-introduction:

Introduction
------------

For large, distributed GNU Health installations, such a network of public hospitals, you might want to consider a central user authentication model.

Under this method, the users and their login credentials are managed centrally, so it's easy to create, modify, and/or revoke them when necessary.

The central authentication model in GNU Health is quite flexible, allowing different roles per health facility. For example, a health professional can work in two different health centers. *Dr. Cameron Cordara* works in the morning as a family medicine physician at *GNU SOLIDARIO Hospital*, and in the afternoon, she cooperates with the social workers, meeting with the community at the local primary care facility. Two different roles in two different centers, yet one single person and one single login.

**Note:** This documentation is based on a installation under :wikipedia:`FreeBSD` and :wikipedia:`OpenLDAP`, but it should work fine on other Free/Libre Operating Systems, such as :wikipedia:`GNU/Linux` . There are also many configuration and deployment options, such as Public Key Infrastructure (PKI), LDAP replication, etc... that are not covered in this introductory, conceptual document.

.. _techguide-administration-centralauthentication:central_authentication-introduction-components:

Components
^^^^^^^^^^

* **OpenLDAP** server (slapd)
* Tryton server modules : :code:`trytond_ldap_authentication`

.. _techguide-administration-centralauthentication:central_authentication-introduction-central_authentication_workflow:

Central Authentication Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. The health professional enters the username / password at the login prompt.
#. The credentials are checked against the OpenLDAP server.

    * **Scenario 1**: The user exists in the OpenLDAP database. If the password provides is correct, then she logins with her local authorization profiles. If she enters an incorrect password, she will be get the login prompt again.
    * **Scenario 2**: The user does not exist in the OpenLDAP database. The credentials are checked against the local GNU Health database at the health facility.
    * **Scenatio 3**: The OpenLDAP server is unreachable (network outage, server down, ... ). Same rule as in Scenario 2 applies.

.. _techguide-administration-centralauthentication:central_authentication-installation:

Installation
------------

.. _techguide-administration-centralauthentication:central_authentication-installation-creating_the_organization_and_users_on_the_ldap_server:

Creating the Organization and Users on the LDAP Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After you installed OpenLDAP, you need to create the organization, the roles and the users, so the LDAP client and GNU Health can interact with the server.

The following :wikipedia:`LDIF` file to  the basic organization and users, just for demonstration purposes.

Sample LDIF file

.. code-block:: yaml


    # The GNU Health Organization
    dn: dc=gnuhealth,dc=org
    objectclass: dcObject
    objectclass: organization
    o: GNU Health Nation
    dc: gnuhealth

    dn: cn=Manager,dc=gnuhealth,dc=org
    objectclass: organizationalRole
    cn: Manager

    # PEOPLE Organizational UNIT (first level hierchy)
    dn: ou=people, dc=gnuhealth,dc=org
    ou: people
    description: All people in organisation
    objectclass: organizationalunit

    # Actual users
    dn: cn=Cameron Cordara,ou=People,dc=gnuhealth,dc=org
    objectClass: inetorgperson
    cn: Cameron Cordara
    sn: Cordara
    uid: cameroncordara
    userPassword: SecretPass


You can now populate the initial OpenLDAP database uploading your newly created LDIF, for instance

.. code-block:: console


    $ slapadd -l <your_ldif_file>

.. _techguide-administration-centralauthentication:central_authentication-installation-configuring_ldap_in_gnu_health:

Configuring LDAP in GNU Health
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


After you have configured the OpenLDAP server and created your users, you need to configure your GNU Health Tryton instance to communicate with it.

* **Install the following Tryton module**

    * :code:`trytond_ldap-authentication`
* **Create a new LDAP connection** (Administration → LDAP → Connections)

    * Fill in the information to meet your LDAP server specification.
    * Save the connection
* **Create a user in GNU Health** (Administration → Users → Users)

You can now create a user matching the uid on the LDIF file, and assign local roles to her. In this case, we would match the "login" name on he screen, with the uid of the user on your Organization. In the case of our Doctor Cameron Cordara, the login name would be *cameroncordara*. Again, this is just for demo purposes. In real-life scenarios you would use unique identifiers for login names.

Note: You will notice that the password field is already "filled in". This is because the actual user password resides now in the LDAP server, and not in your local instance database.

If everything went right, you now have GNU Health enable for central authentication. Try to login as "cameroncordara". Her credentials will be checked on the LDAP server.

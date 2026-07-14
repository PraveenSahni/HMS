.. _techguide-administration-patches:about_gnu_health_package_bundles:

About GNU Health package bundles
================================

Since release 5.0 patchsets are included in the GNU Health HIS **server bundles**.
The new approach in GNU Health software development is to provide each package
with its own release patch number. To avoid confusion between the whole bundle and
each invidual component, the GNU Health software bundle has the following nomenclature:

gnuhealth-his-server-<major_number>.<minor_number>-bundle-yyyy.n


For example:

*gnuhealth-his-server-5.0-bundle-2025.1* will include all the patches from the
individual packages in the server.

Again, each component has its own version. For instance, gnuhealth-his-server-7.0-bundle-2027.3 can have the core health package "health" with version 7.0.2 and the he health-pediatrics with version 7.0.1, all bundled on 7.0-bundle-2027.3.

Our organization in PyPI contains the 50+ individual packages. The best way to
install them is using **gnuhealth-control** :ref:`techguide-administration-controlcenter:the_gnu_health_control_center`


.. _techguide-administration-patches:about_gnu_health_package_bundles-updating_the_packages:

Updating the packages
---------------------

GNU Health control center facilitates common administration tasks, such as backups or system updates.
To check the status of your Tryton and GNU Health kernel and modules, as well
as to keep your system uptodate, please visit the section :ref:`techguide-administration-controlcenter:the_gnu_health_control_center`

Go to :ref:`techguide-administration-controlcenter:the_gnu_health_control_center` for the documentation on how to install the patchsets.



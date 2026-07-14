.. _appendix-errata:errata:

Errata
======
In GNU Health we work hard to minimize issues and bugs.

The errata section shows issues that emerged after the release of the documentation of a particular version, that
might impair the installation or upgrade process. For each issue, we try to document the context and the solution.

.. _appendix-errata:errata-version_5.0:

VERSION 5.0
-----------

Issue: Database connection using TCP instead of UNIX socket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default database connection configuration URI was configured with TCP (eg, uri = postgresql://localhost:5432)
instead of local UNIX socket,and depending on the current postgreSQL configuration, the instance creation might produce an error.

**Context**: Installation (ghcontrol)

**Solution**:

 Verify that the uri entry in *trytond.conf* on [database] section is using sockets. The problem is fixed in gnuhealth-control (>= 5.0.1).
 The URI entry to use UNIX sockets for the database connection should be (uri = postgresql://)

 .. code-block:: cfg

        [database]
        uri = postgresql://


Issue: Loglevel too low for production servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default loglevel for the GNU Health server has been shipped to INFO, which is a bit of an overkill for production
servers due to the verbosity it produces, impacting to the log file. Since gnuhealth-control 5.0.1, the server loglevel has been
set to WARNING by default.

**Context**: Logger


**Solution**:

 You can raise the loglevel of the GNU Health Tryton server from INFO to WARNING , editing the file *server_log.conf* .

 .. code-block:: cfg

        [logger_root]
        level=WARNING



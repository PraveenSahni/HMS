.. _techguide-development-scheduler:scheduler:

Scheduler
=========

In order to run scheduled and repeated actions in the background you can use Tryton Cron.

It is located under *Administration -> Scheduler -> Scheduled Actions*:

.. thumbnail:: ../../images/Scheduler.png
    :title: Scheduling actions in the client

The available ``Methods`` have to be added by developers.
They will run in the given frequency on the given ``Companies``.
For enabling or disabling it you can toggle the ``Active`` Field.
If you want to run the method right now click the ``Run Once`` Button.

.. todo:: Add example (maybe from Orthanc module)

If you want to put more methods refer to the documentation of Tryton:

https://docs.tryton.org/7.0/server/topics/cron.html

Note that the Scheduler only works if Tryton Cron itself is running.
If you followed the Vanilla installation, change to the executable directory
and start it like this:

.. code-block:: console

    $ cdexe
    $ trytond-cron

The Ansible installation has a systemd service prepared.
If you set the boolean *gh_cron* to true before executing the playbook
you will get this service started and enabled.
To do so change it to true inside your inventory in
*group_vars/gnuhealth/vars.yml* or pass it as flag when running the playbook (-e gh_cron=1).

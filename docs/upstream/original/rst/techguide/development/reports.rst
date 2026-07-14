.. _techguide-development-reports:reports:

Reports
=======

.. _techguide-development-reports:reports-template_guidelines:

Template Guidelines
-------------------

Read tryton reports document
############################

GNU Health HIS is based on tryton service, so should read it first.

https://docs.tryton.org/7.0/server/topics/reports/index.html


Libreoffice setup
#################

.. _techguide-administration-reports:1._libreoffice_setup-1)_remove_user_data:

#. Remove user data

   - Open: *(File → Properties)*
   - Uncheck: *Apply user data*
   - Uncheck: *Save preview image with this document*
   - Click on: *Reset Properties*

#. Set some parameters

   - Check *(View > Field Names)* and let field only show
     *Placeholder* label, which will be more conducive to observing
     the layout effect.
   - Use English (USA) UI, so the name of table or figure in document will be
     English.

     *(Options → Language Settings → Languages → User Interface)*

   - Disable table number recognition

     *(Options → Libreoffice Write → Table → Number recognition)*


Edit report template file
#########################

#. Do not use direct (or manual) formatting.
#. Do not use character style unless absolutely necessary.
#. Prefer use paragraph styles, but suggest style number < 20.
#. Use *GNU FreeFont* as English font, for example: *FreeSerif*, *FreeSans* and *FreeMono*.
#. Hide all unused styles.
#. User custom styles suggest prefix with *GH-*, which means *GNU Health*.
#. Be careful of spaces of label strings.

   Suggest *PUID* or *PUID:*, instead of *PUID<SPC>:*.

#. Do not add extra spaces between two words.

   Using *hello<SPC>world* instead of *hello<SPC><SPC>world*.

#. The name of table, figure and other things suggest use ascii.
#. Reconfigure table properties after table layout is changed.

#. Should we use *and/or/not* or *if directive* ?

   #. In most situation, we prefer *and/or/not*, for it is not disrupt
      report layout and make grep work well.

      .. code-block:: python

         appointment.patient and appointment.patient.name and appointment.patient.name.ref or ''

      Using Python Conditional Expressions is a good idea too:

      .. code-block:: python

         <value_if_true> if <expression> else <value_if_false>


   #. if string will be translated by other languages, and *if
      directive* do not disrupt report layout too much, we suggest
      use *if directive*.

      .. code-block:: console

         if test='appointment.patient'
         appointment.patient.name.ref
         /if

   #. if *if directive* seriously affects the report structure, we
      suggest to add a method to model and use this method in
      template, for example, we use *get_report_pain_and_level()* in
      report template of health_nursing modules.

      .. code-block:: python

         # Use by round_report template
         def get_report_pain_and_level(self):
              if self.pain and self.pain_level:
                  return gettext('health_nursing.msg_report_pain_level',
                                 pain_level=str(self.pain_level))
              elif self.pain:
                  return gettext('health_nursing.msg_report_pain_yes')
              else:
                  return gettext('health_nursing.msg_report_pain_no')


#. How to keep ratio when add a image to report?

   We have added *ImageReportMixin* class and register to *Report*
   class with the help of *Pool.register_mixin*, user can use its
   methods in report template, for example:

   - patient_card.fodt: *image: image_crop(patient.photo, 2.5, 3.5)*
   - labtest_report.fodt: *image: image_resize(image.data, 5, 5)*

#. How to add 'yes' or 'no' string to report and let them translatable.

   A simple way is using *yes_str* and *no_str* variable in report
   template, for example:

   .. code-block:: python

      death_cert.autopsy and yes_str or no_str

   User can use gettext in report template if wish, for example:

   .. code-block:: python

      death_cert.autopsy and gettext('health.msg_yes_str') or gettext('health.msg_no_str')


#. The functions and variables which can be used directly in report template.

   Grep *get_context* in Trytond sources and GNU Health sources, you
   will find like below:

   .. code-block:: python

      @classmethod
      def get_context(cls, records, header, data):
          context = super(GettextReportMixin, cls).get_context(
              records, header, data)

          context['yes_str'] = gettext('health.msg_yes_str')
          context['no_str'] = gettext('health.msg_no_str')
          context['gettext'] = gettext

          return context


   #. Tryton

      - header
      - data
      - context
      - user
      - records
      - record
      - format_date
      - format_datetime
      - format_timedelta
      - format_currency
      - format_number
      - datetime

   #. GNU Health

      - image_crop
      - image_resize
      - image_keep_size
      - yes_str
      - no_str
      - gettext


Save and check report template file
###################################

- Clean Direct Formatting.

  #. *(Edit → Select All)*
  #. *(Format → Clean Direct Formatting)*

  NOTE: This step is very useful, which can solve most *Abnormal
  string fragmentation* issues describe below.

- Check 'Abnormal string fragmentation' issue.

  Save file to fodt format, then open fodt file with a text editor to
  check “PU” + “ID” style issues *(Abnormal string fragmentation)*, if
  found, edit template file again.

  .. code-block:: console

     <text:span text:style-name="T4">PU</text:span><text:span text:style-name="T3">ID</text:span>

  .. code-block:: console

     <text:p text:style-name="P11">Hello <text:s/>world</text:p>


- Check po or pot files.

  Finally, user can use below command to update pot files (see:
  :ref:`techguide-localization-index:localization-update_po_and_pot_files`),
  then check diff with hg command, make sure no *PU + ID* style
  issues.

  .. code-block:: console

     bash his-utils/script/po-export/po-export.sh --fast-export --his-dir <your-his-repo> --pot

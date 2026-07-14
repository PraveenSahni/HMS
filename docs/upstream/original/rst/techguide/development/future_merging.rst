.. _techguide-development-future_merging:future_merging_script:

Future Merging Script
=====================

This section might be added in the future and is still subject to discussion:

https://codeberg.org/gnuhealth/his/issues/10

In current HIS branching strategy, we will merge **main** branch to
**devel** branch frequently, during the merge process, we may need
to skip some commits, for example:

1. Version bump commits in main branch.
2. Backport commits with cherry-pick from **devel**.
3. Other changes, which is meanless to merge to **devel**.

In practice, developers will add some fixed tag strings to commit
messages, such as: **Bump version to**, **Backport:**, **cherry picked
from**, **no need to merge**, **do not merge** and so on, to indicate
these commits need to be skipped when merging from **main** to
**devel**.

It is recommended to use **gitmerge4gh.el** in this situation, it is a
fork of **gitmerge.el** of Emacs, which has been used by emacser many
years.

1. https://codeberg.org/gnuhealth/his-utils/src/branch/devel/scripts/gitmerge4gh/gitmerge4gh.el
2. https://codeberg.org/gnuhealth/his-utils/src/branch/devel/scripts/gitmerge4gh/README.org

If you really want to, you can do the merge manually, but make
absolutely sure that you **always** use the 'merge' command to
transport commits from the **main** branch to **devel** branch.
**Never** use 'cherry-pick'! If you don't know why, then you shouldn't
manually do the merge in the first place, just use **gitmerge4gh.el**
instead.

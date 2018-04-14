Miscellaneous tips
==================

Some useful snippets and things in the Crimson codebase.

Memory-heavy database migrations
--------------------------------

Database migration `0003_auto_20150406_2103.py <https://github.com/harvard-crimson/crimsononline/blob/b2e95e372c5b7732b15699d2cf4f3a6af011407b/crimsononline/content/migrations/0003_auto_20150406_2103.py>`__
under content has a snippet for doing more memory-efficient iteration
over large QuerySets. If you have a database query that's using lots of
RAM, try ``queryset_iterator`` from that file.

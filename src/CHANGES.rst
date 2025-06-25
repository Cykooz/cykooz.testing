..  Changelog format guide.
    - Before make new release of core egg you MUST add here a header for new version with name "Next release".
    - After all headers and paragraphs you MUST add only ONE empty line.
    - At the end of sentence which describes some changes SHOULD be identifier of task from our task manager.
      This identifier MUST be placed in brackets. If a hot fix has not the task identifier then you
      can use the word "HOTFIX" instead of it.
    - At the end of sentence MUST stand a point.
    - List of changes in the one version MUST be grouped in the next sections:
        - Features
        - Changes
        - Bug Fixes
        - Docs

CHANGELOG
*********

2.0 (2025-06-26)
================

Features
--------

- Added ``CiStr`` to compare strings case-insensitively.
- Added ``RoundFloat`` to compare float numbers rounded to given precision
  in decimal digits.
- Added ``DictCi`` to compare with another dict object
  without regard to keys that did not present in the ``DictCi`` instance
  and with case-insensitive comparison of string keys.

Breaking Changes
----------------

- Dropped support Python versions less than 3.9.

1.2 (2021-08-27)
================

Changes
-------

- Added argument ``ignore_order`` into ``List`` helper to
  comparing of lists without regard of ordering of items.

1.1.2 (2020-04-14)
==================

Bug Fixes
---------

- Added new helper into ``__all__``.

1.1 (2020-04-14)
================

Features
--------

- Added new helper ``Json``.

1.0.3 (2020-03-20)
==================

Bug Fixes
---------

- Fixed namespace declaration.

1.0.1 (2019-07-12)
==================

Bug Fixes
---------

- Fixed "Development Status" of package.

1.0 (2019-07-12)
================

Features
--------

- Initial release.

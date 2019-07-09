Release History
===============

0.1.3 (2019-07-10)
------------------

**Improvements**

- Added a new `proxies` argument in the `get_*` functions, and a global `proxies` option (#2)
- Return an explicit error message when an indicator is not found (#7)
- Package tested with Python 3.8


0.1.2 (2019-04-13)
------------------

**BugFixes**

- Fix _Unable to download the data in full_ error on `get_indicators`

0.1.1 (2019-04-09)
------------------

**BugFixes**

- Fixed `simplify_index` when the data is a scalar
- Non-WDI indicators can now be loaded (#4)
- Package also works under Python 2.7 (#1)

0.1.0 (2019-04-06)
------------------

Initial release

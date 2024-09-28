0.1.4 (2024-09-28)
------------------

**Fixed**
- We now use HTTPS as required by the world bank API ([#18](https://github.com/mwouts/world_bank_data/pull/18)) - thanks to [John Cant](https://github.com/johncant) for fixing this!

**Added**
- Added `__version__`
- We use GitHub Actions for CI
- We use `pre-commit` for code formatting

**Changed**
- The package can be used with Python 3.7 to 3.12


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

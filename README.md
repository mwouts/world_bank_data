# The World Bank Data in Python

[![CI](https://github.com/mwouts/world_bank_data/actions/workflows/continuous-integration.yml/badge.svg?branch=main)](https://github.com/mwouts/world_bank_data/actions)
[![codecov.io](https://codecov.io/github/mwouts/world_bank_data/coverage.svg?branch=main)](https://codecov.io/github/mwouts/world_bank_data?branch=main)
[![Language grade: Python](https://img.shields.io/badge/lgtm-A+-brightgreen.svg)](https://lgtm.com/projects/g/mwouts/world_bank_data/context:python)
[![Pypi](https://img.shields.io/pypi/v/world_bank_data.svg)](https://pypi.python.org/pypi/world_bank_data)
[![pyversions](https://img.shields.io/pypi/pyversions/world_bank_data.svg)](https://pypi.python.org/pypi/world_bank_data)
[![Jupyter Notebook](https://img.shields.io/badge/Binder-Notebook-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/world_bank_data/main?filepath=examples%2FA%20sunburst%20plot%20of%20the%20world%20population.ipynb)
[![JupyterLab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/world_bank_data/main?urlpath=lab)

This is an implementation of the [World Bank API v2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview) in Python. Use this package to explore the [World Development Indicators](http://datatopics.worldbank.org/world-development-indicators/) published by the [World Bank](http://www.worldbank.org/).

# Quick tutorial

## Installation

Install or update the _World Bank Data_ python package with

```bash
pip install world_bank_data --upgrade
```

## Get the list of sources, topics, countries, regions

```python
import pandas as pd
import world_bank_data as wb
pd.set_option('display.max_rows', 6)
```

The list of topics is available with

```python
wb.get_topics()
```

Sources are returned by

```python
wb.get_sources()
```

And finally, the list of countries is accessible with

```python
wb.get_countries()
```

In addition, give a try to
- `get_regions`
- `get_incomelevels`
- `get_lendingtypes`

to retrieve more information about country classifiers.

## Get the list of indicators

This is done with the `get_indicators` function. You may query only the indicators for a specific source or topic as below. If you input no arguments, the `get_indicator` function will return the description of all the 16,000+ indicators.

```python
wb.get_indicators(topic=3, source=2)  # topic and source id are from get_topics/get_sources
```

Requesting all indicators may take a few seconds, but no worries, the result is cached, so next time this will be instantaneous.

## Searching for one country or indicator

Use the functions `search_countries`, `search_source`, `search_indicators`. Or, if you want to search in a existing dataframe, simply use `search`.

```python
wb.search_indicators('mathematics')
```

## Get the values of an indicator

The function `get_series` returns the value of a single indicator. The World Bank API accepts quite a few arguments, including:
- `mrv`, integer: one or more _most recent values_
- `date`, string: either one year, or two years separated with a colon, like '2010:2018'
- `gapfill`, string: 'Y' or 'N' (the default): forward fills missing values.

For instance, the call below returns the most recent estimate for the World Population:

```python
wb.get_series('SP.POP.TOTL', mrv=1)
```

The result above has a 3-dimensional index. Use the argument `simplify_index` to ignore the dimensions that take a single value (here: `year` and `series`). Also, use the argument `id_or_value='id'` if you prefer your data to be indexed by the codes rather than labels:

```python
wb.get_series('SP.POP.TOTL', date='2016', id_or_value='id', simplify_index=True)
```

## Ready for an interative tutorial?

Go to our [Binder](https://mybinder.org/v2/gh/mwouts/world_bank_data/main) and run either this [README](https://github.com/mwouts/world_bank_data/blob/main/README.md), or our other [tutorial](https://github.com/mwouts/world_bank_data/blob/main/examples/) with the code required to produce this plot of the World Population:

[![World Population 2017](https://gist.githubusercontent.com/mwouts/ec3a88f1d97e36a062f69d4072b91e39/raw/79211a09957c6934fabf738a59c2c9b8df943696/world_population.gif)](https://nbviewer.jupyter.org/github/mwouts/world_bank_data/blob/main/examples/A%20sunburst%20plot%20of%20the%20world%20population.ipynb)

# References

## The World Bank

The [World Bank](https://www.worldbank.org/) has a [Data Catalog](https://datacatalog.worldbank.org/), and an interactive [data explorer](https://data.worldbank.org/indicator/sp.pop.totl).

Third party applications that allow to access the data from various languages are listed [here](https://data.worldbank.org/products/third-party-apps).

## Google's Public Data Explorer

The World Bank data is also available in Google's [Data Explorer](https://data.worldbank.org/products/third-party-apps).

## Python

Alternatively to `world_bank_data`, Python users may find useful the following packages:
- [`wbpy`](https://github.com/mattduck/wbpy/), nicely documented and recently updated to Python 3 and the World Bank API v2.
- [`wbdata`](https://github.com/oliversherouse/wbdata/), which works well.
- [`pandas_datareader`](https://pandas-datareader.readthedocs.io/en/latest/readers/world-bank.html)

The reason for which I wrote `world_bank_data` is mostly speed, e.g. I wanted to use the lastest version of the World Bank API (v2) and benefit from significant speed improvements. Reimplementing the API also gave me a finer control on the mapping of options.

## R

R users can use two packages to access the World Bank data:
- [`WDI`](https://github.com/vincentarelbundock/WDI/blob/master/README.md)
- [`wbstats`](https://github.com/GIST-ORNL/wbstats/blob/master/README.md)

See also the [Introduction to the wbstats R-package](https://cran.r-project.org/web/packages/wbstats/vignettes/Using_the_wbstats_package.html), or this [quick review](https://cengel.github.io/gearup2016/worldbank.html) of the two packages.

# FAQ

## Country and indicator description in non-English languages

The World Bank describes their sources and indicators in other languages than English. Use either the `language` argument in each of `get_countries`, `get_indicators`, etc, or change the default globally:

```python
wb.options.language = 'vi'
wb.get_indicators('SP.POP.TOTL')
```

```python
wb.options.language = 'en'
```

## Caching

All requests, except `get_series`, are cached using a _least recently used_ cache from the `cachetools` package.

## Using behind a proxy

Using the package behind an http proxy is possible. Use either the `proxies` argument in the `get_*` functions, or set the proxy globally with e.g.:

```python
wb.options.proxies = {'http': 'http://example.com:3128'}
```

## License

This python package is licenced under the MIT License.

Please also read the World Bank [Terms of Use](https://data.worldbank.org/summary-terms-of-use) relative to the conditions that apply to the data downloaded with this package.

# The World Bank Data in Python

[![Build Status](https://travis-ci.com/mwouts/world_bank_data.svg?branch=master)](https://travis-ci.com/mwouts/world_bank_data)
[![codecov.io](https://codecov.io/github/mwouts/world_bank_data/coverage.svg?branch=master)](https://codecov.io/github/mwouts/world_bank_data?branch=master)
[![Language grade: Python](https://img.shields.io/badge/lgtm-A+-brightgreen.svg)](https://lgtm.com/projects/g/mwouts/world_bank_data/context:python)
[![Jupyter Notebook](https://img.shields.io/badge/Binder-Notebook-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/world_bank_data/master?filepath=examples%2FA%20sunburst%20plot%20of%20the%20world%20population.ipynb)
[![JupyterLab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/world_bank_data/master?urlpath=lab)


This is an implementation of the [World Bank API v2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview) in Python.

# Install

Install or update the _World Bank Data_ python package with

```bash
pip install world_bank_data --upgrade
```

# Quick tutorial

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

to see how the World countries are classified.


## Get the list of available indicators

This is done with the `get_indicators` function. You may query only the indicators for a specific source or topic: use the index for that source or topic from `get_source` and `get_topic`. If you input no arguments, the `get_indicator` function will return the description of all the 16,000 indicators.

```python
wb.get_indicators(topic=3, source=2)
```

## Searching for one country or indicator


Use the functions `search_countries`, `search_source`, `search_indicators`, or simply call `search` on your existing dataframe.

```python
wb.search_indicators('mathematics')
```

## Get indicator value

The function `get_series` will return the value of a single indicator. The World Bank API accepts quite a few arguments, including:
- `mrv`, integer: one or more _most recent values_
- `date`, string: either one year, or two years separated with a colon, like '2010:2018'
- `gapfill`, string: 'Y' or 'N' (the default): forward fills missing values.

```python
wb.get_series('SP.POP.TOTL', mrv=1)
```

By default, the `get_series` function returns the full index given by the World bank, even if there is a single series and a single year. Use the argument `simplify_index` to ignore these dimensions. Also, use the argument `id_or_value='id'` if you prefer your data to be indexed by the codes rather than labels.

```python
wb.get_series('SP.POP.TOTL', date='2016', id_or_value='id', simplify_index=True)
```

## Ready for an interative tutorial?

Go to our Binder and run either this [README](https://mybinder.org/v2/gh/mwouts/world_bank_data/master?filepath=README.md), or our other [tutorial](https://mybinder.org/v2/gh/mwouts/world_bank_data/master?filepath=examples%2FA%20sunburst%20plot%20of%20the%20world%20population.ipynb) on how to produce this plot of the World Population:

![World Population 2017](https://gist.githubusercontent.com/mwouts/ec3a88f1d97e36a062f69d4072b91e39/raw/b0d4a76e185cac48d4253df8792cac4b91e746f2/world_population.png)

# References

## The World Bank

This package eases the access to the [World Bank](https://www.worldbank.org/) Data. You can also explore the [Data Catalog](https://datacatalog.worldbank.org/), and the data itself directly on the [site](https://data.worldbank.org/indicator/sp.pop.totl).

Third party applications that allow to access the data from various languages are listed [here](https://data.worldbank.org/products/third-party-apps).

## Google's Public Data Explorer

The World Bank data can be visualized in Google's [Data Explorer](https://data.worldbank.org/products/third-party-apps).

## R

R users can use two packages to access the World Bank data:
- [`WDI`](https://github.com/vincentarelbundock/WDI/blob/master/README.md) 
- [`wbstats`](https://github.com/GIST-ORNL/wbstats/blob/master/README.md)

See here for an [Introduction to the wbstats R-package](https://cran.r-project.org/web/packages/wbstats/vignettes/Using_the_wbstats_package.html). For a quick comparison of the two packages, see [here](https://cengel.github.io/gearup2016/worldbank.html).

## Python

Python users can also use, alternatively to `world_bank_data`, the following two packages:
- [`wbpy`](https://github.com/mattduck/wbpy/blob/master/README.rst), nicely documented but last released in 2013.
- [`wbdata`](https://github.com/oliversherouse/wbdata/blob/master/README.rst), which works well.

The reason for which I wrote `world_bank_data` is mostly speed, e.g. I wanted to use the lastest version of the World Bank API (v2) and benefit from significant speed improvements. Reimplementing the API also gave me a finer control on the mapping of options.


# FAQ



## Using another language

The World Bank describes their sources and indicators in a few other languages than English. Use either the `language` argument in each function, or change the default globally:

```python
wb.options.language = 'vi'
wb.get_indicators('SP.POP.TOTL')
```

```python
wb.options.language = 'en'
```

## Caching

All requests, except `get_series`, are cached using a _least recently used_ cache from the `cachetools` package.

## License

This python package is licenced under the MIT License.

Please also read the World Bank [Terms of Use](https://data.worldbank.org/summary-terms-of-use) relative to the conditions that apply to the data downloaded with this package.

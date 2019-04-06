# The World Bank Data in Python

This is an implementation of the [World Bank API v2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview) in Python.

# Install

Install or update the _World Bank Data_ python package with

# ```bash
pip install world_bank_data --upgrade
# ```

# Quick tutorial

## Get the list of available indicators

```python
import pandas as pd
pd.set_option('display.max_rows', 6)
```

```python
import world_bank_data as wb
wb.get_indicators()
```

# Indicators in another language

```python
wb.get_indicators('SP.POP.TOTL', language='fr')
```

# Get indicator value

```python
wb.get_series('SP.POP.TOTL', mrv=1)
```

```python
wb.get_series('SP.POP.TOTL', mrv=1, field='id', drop_constant_index=True)
```

# FAQ

## Caching

All requests, except `get_series`, are cached for up to one hour using a _least recently used_ cache of size 128 from the `cachetools` package.

## Terms of Use

Please read the World Bank [Terms of Use](https://data.worldbank.org/summary-terms-of-use) relative to the conditions that apply to the data downloaded with this package.

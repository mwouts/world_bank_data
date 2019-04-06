"""Request the world bank API"""
from copy import copy
from requests import get, HTTPError
import pandas as pd

WORLD_BANK_URL = 'http://api.worldbank.org/v2'


class WBRequestError(HTTPError):
    """An error occured when downloading the WB data"""


def collapse(country_list):
    """Collapse multiple countries to a colon-separated list of countries"""
    return country_list if isinstance(country_list, str) else ';'.join(country_list) if country_list else 'all'


def extract_preferred_field(data, field):
    """In case the preferred representation of data when the latter has multiple representations"""
    if isinstance(data, dict):
        if field in data:
            return data[field]
        return ''

    if isinstance(data, list):
        return ','.join([extract_preferred_field(i, field) for i in data])

    return data


def wb_get(*args, language='en', data_format='json', **kwargs):
    """Request the World Bank for the desired information"""
    params = copy(kwargs)
    params['format'] = data_format

    # collapse the list of countries to a single str
    if len(args) > 1:
        args = list(args)
        args[1] = collapse(args[1])

    if language != 'en':
        args = [language] + args

    url = '/'.join([WORLD_BANK_URL, *args])

    response = get(url=url, params=params)
    response.raise_for_status()
    data = response.json()

    # Redo the request and get the full information when the first response is incomplete
    if data_format == 'json' and isinstance(data, list):
        page_information, data = data
        if int(page_information['pages']) > 1:
            params['per_page'] = page_information['total']
            response = get(url=url, params=params)
            response.raise_for_status()
            page_information, data = response.json()

            if int(page_information['pages']) > 1:
                raise WBRequestError('Unable to download the data in full')

    return data


def wb_get_table(name, only=None, language=None, **params):
    """Request data and return it in the form of a data frame"""
    data = wb_get(name, only, language=language, **params)

    columns = data[0].keys()
    table = {}

    for col in columns:
        table[col] = [cnt[col] for cnt in data]

    table = pd.DataFrame(table, columns=columns)

    if table['id'].any():
        return table.set_index('id')

    table.pop('id')
    return table.set_index('code')

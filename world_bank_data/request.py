"""Request the world bank API"""
from copy import copy
from requests import get, HTTPError
import pandas as pd
from cachetools import cached, TTLCache
import world_bank_data.options as options

WORLD_BANK_URL = 'http://api.worldbank.org/v2'


class WBRequestError(HTTPError):
    """An error occured when downloading the WB data"""


def collapse(values):
    """Collapse multiple values to a colon-separated list of values"""
    if isinstance(values, str):
        return values
    if values is None:
        return 'all'
    if isinstance(values, list):
        return ';'.join([collapse(v) for v in values])
    return str(values)


def extract_preferred_field(data, id_or_value):
    """In case the preferred representation of data when the latter has multiple representations"""
    if not id_or_value:
        return data

    if not data:
        return ''

    if isinstance(data, dict):
        if id_or_value in data:
            return data[id_or_value]

    if isinstance(data, list):
        return ','.join([extract_preferred_field(i, id_or_value) for i in data])

    return data


def wb_get(*args, **kwargs):
    """Request the World Bank for the desired information"""
    params = copy(kwargs)
    language = params.pop('language') if 'language' in params else 'en'
    params.setdefault('format', 'json')

    # collapse the list of countries to a single str
    if len(args) > 1:
        args = list(args)
        args[1] = collapse(args[1])

    if 'topic' in params:
        args = ['topic', str(params.pop('topic'))] + args

    if language != 'en':
        args = [language] + args

    url = '/'.join([WORLD_BANK_URL] + args)

    response = get(url=url, params=params)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and data and 'message' in data[0]:
        try:
            msg = data[0]['message'][0]['value']
        except (KeyError, IndexError):
            msg = str(msg)

        raise ValueError("{msg}\nurl={url}\nparams={params}".format(msg=msg, url=url, params=params))

    # Redo the request and get the full information when the first response is incomplete
    if params['format'] == 'json' and isinstance(data, list):
        page_information, data = data
        if int(page_information['pages']) > 1:
            params['per_page'] = page_information['total']
            response = get(url=url, params=params)
            response.raise_for_status()
            page_information, data = response.json()

            if int(page_information['pages']) > 1:
                raise WBRequestError('Unable to download the data in full')

    if not data:
        raise RuntimeError("The request returned no data:\nurl={url}\nparams={params}"
                           .format(url=url, params=params))

    return data


@cached(TTLCache(128, 3600))
def _wb_get_table_cached(name, only=None, language=None, id_or_value=None, **params):
    if language:
        params['language'] = language
    data = wb_get(name, only, **params)

    # We get a list (countries) of dictionary (properties)
    columns = data[0].keys()
    table = {}

    for col in columns:
        table[col] = [extract_preferred_field(cnt[col], id_or_value) for cnt in data]

    table = pd.DataFrame(table, columns=columns)

    if table['id'].any():
        return table.set_index('id')

    table.pop('id')
    return table.set_index('code')


def wb_get_table(name, only=None, language=None, id_or_value=None, expected=None, **params):
    """Request data and return it in the form of a data frame"""
    only = collapse(only)
    id_or_value = id_or_value or options.id_or_value

    if expected and id_or_value not in expected:
        raise ValueError("'id_or_value' should be one of '{}'".format("', '".join(expected)))

    return _wb_get_table_cached(name, only, language or options.language, id_or_value, **params)

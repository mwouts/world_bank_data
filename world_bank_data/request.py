"""Request the world bank API"""
from copy import copy
from requests import get, HTTPError

WORLD_BANK_URL = 'http://api.worldbank.org/v2/'


class WBRequestError(HTTPError):
    """An error occured when downloading the WB data"""


def collapse(country_list):
    """Collapse multiple countries to a colon-separated list of countries"""
    return country_list if isinstance(country_list, str) else ';'.join(country_list) if country_list else 'all'


def wb_get(*args, format='json', **kwargs):
    """Request the World Bank for the desired information"""
    params = copy(kwargs)
    params['format'] = format

    # collapse the list of countries to a single str
    if len(args) > 1:
        args = list(args)
        args[1] = collapse(args[1])

    url = '/'.join([WORLD_BANK_URL, *args])

    response = get(url=url, params=params)
    response.raise_for_status()
    data = response.json()

    # Redo the request and get the full information when the first response is incomplete
    if format == 'json' and isinstance(data, list):
        page_information, data = data
        if int(page_information['pages']) > 1:
            params['per_page'] = page_information['total']
            response = get(url=url, params=params)
            response.raise_for_status()
            page_information, data = response.json()

            if int(page_information['pages']) > 1:
                raise WBRequestError('Unable to download the data in full')

    return data

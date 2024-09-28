# -*- coding: utf-8 -*-

"""Request the world bank API"""
import json
import re
from copy import copy

import pandas as pd
from cachetools import TTLCache, cached, keys
from requests import HTTPError, get

import world_bank_data.options as options

WORLD_BANK_URL = "https://api.worldbank.org/v2"


class WBRequestError(HTTPError):
    """An error occured when downloading the WB data"""


def collapse(values):
    """Collapse multiple values to a colon-separated list of values"""
    if isinstance(values, str):
        return values
    if values is None:
        return "all"
    if isinstance(values, list):
        return ";".join([collapse(v) for v in values])
    return str(values)


def extract_preferred_field(data, id_or_value):
    """In case the preferred representation of data when the latter has multiple representations"""
    if not id_or_value:
        return data

    if not data:
        return ""

    if isinstance(data, dict):
        if id_or_value in data:
            return data[id_or_value]

    if isinstance(data, list):
        return ",".join([extract_preferred_field(i, id_or_value) for i in data])

    return data


def wb_get(*args, **kwargs):
    """Request the World Bank for the desired information"""
    params = copy(kwargs)
    language = params.pop("language", "en")
    proxies = params.pop("proxies", options.proxies)
    params.setdefault("format", "json")
    params.setdefault("per_page", 20000)

    # collapse the list of countries to a single str
    if len(args) > 1:
        args = list(args)
        args[1] = collapse(args[1])

    if "topic" in params:
        args = ["topic", str(params.pop("topic"))] + args

    if language != "en":
        args = [language] + args

    url = "/".join([WORLD_BANK_URL] + args)

    response = get(url=url, params=params, proxies=proxies)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError:  # simplejson.errors.JSONDecodeError derives from ValueError
        raise ValueError(
            "{msg}\nurl={url}\nparams={params}".format(
                msg=_extract_message(response.text), url=url, params=params
            )
        )
    if isinstance(data, list) and data and "message" in data[0]:
        try:
            msg = data[0]["message"][0]["value"]
        except (KeyError, IndexError):
            msg = str(msg)

        raise ValueError(
            "{msg}\nurl={url}\nparams={params}".format(msg=msg, url=url, params=params)
        )

    # Redo the request and get the full information when the first response is incomplete
    if params["format"] == "json" and isinstance(data, list):
        page_information, data = data
        if "page" not in params:
            current_page = 1
            while current_page < int(page_information["pages"]):
                params["page"] = current_page = int(page_information["page"]) + 1
                response = get(url=url, params=params)
                response.raise_for_status()
                page_information, new_data = response.json()
                data.extend(new_data)

    if not data:
        raise RuntimeError(
            "The request returned no data:\nurl={url}\nparams={params}".format(
                url=url, params=params
            )
        )

    return data


def _extract_message(msg):
    """'ï»¿<?xml version="1.0" encoding="utf-8"?>
    <wb:error xmlns:wb="http://www.worldbank.org">
      <wb:message id="175" key="Invalid format">The indicator was not found. It may have been deleted or archived.</wb:message>
    </wb:error>'"""
    if "wb:message" not in msg:
        return msg
    return re.sub(
        re.compile(".*<wb:message[^>]*>", re.DOTALL),
        "",
        re.sub(re.compile("</wb:message>.*", re.DOTALL), "", msg),
    )


def _robust_key(*args, **kwargs):
    if "proxies" in kwargs:
        kwargs["proxies"] = json.dumps(kwargs["proxies"])
    return keys.hashkey(*args, **kwargs)


@cached(TTLCache(128, 3600), key=_robust_key)
def _wb_get_table_cached(name, only=None, language=None, id_or_value=None, **params):
    if language:
        params["language"] = language
    data = wb_get(name, only, **params)

    # We get a list (countries) of dictionary (properties)
    columns = data[0].keys()
    table = {}

    for col in columns:
        table[col] = [extract_preferred_field(cnt[col], id_or_value) for cnt in data]

    table = pd.DataFrame(table, columns=columns)

    if table["id"].any():
        return table.set_index("id")

    table.pop("id")
    return table.set_index("code")


def wb_get_table(
    name, only=None, language=None, id_or_value=None, expected=None, **params
):
    """Request data and return it in the form of a data frame"""
    only = collapse(only)
    id_or_value = id_or_value or options.id_or_value

    if expected and id_or_value not in expected:
        raise ValueError(
            "'id_or_value' should be one of '{}'".format("', '".join(expected))
        )

    return _wb_get_table_cached(
        name, only, language or options.language, id_or_value, **params
    )

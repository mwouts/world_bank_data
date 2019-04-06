"""Get regions, topics, sources, etc"""

from .request import wb_get_table
from .options import default_language


def get_regions(region=None, language=default_language, **params):
    """Return a DataFrame that describes one, multiple or all regions, indexed by the region id.
    :param region: None (all regions), the id of a region, or a list of multiple ids
    :param language: Desired language"""
    return wb_get_table('region', region, language, **params)


def get_sources(source=None, language=default_language, **params):
    """Return a DataFrame that describes one, multiple or all sources, indexed by the source id.
    :param source: None (all sources), the id of a source, or a list of multiple ids
    :param language: Desired language"""
    return wb_get_table('source', source, language, **params)


def get_topics(topic=None, language=default_language, **params):
    """Return a DataFrame that describes one, multiple or all sources, indexed by the source id.
    :param topic: None (all topics), the id of a topic, or a list of multiple ids
    :param language: Desired language"""
    return wb_get_table('topic', topic, language, **params)


def get_incomelevels(incomelevel=None, language=default_language, **params):
    """Return a DataFrame that describes one, multiple or all income levels, indexed by the IL id.
    :param incomelevel: None (all income levels), the id of an income level, or a list of multiple ids
    :param language: Desired language"""
    return wb_get_table('incomelevel', incomelevel, language, **params)


def get_lendingtypes(lendingtype=None, language=default_language, **params):
    """Return a DataFrame that describes one, multiple or all lending types, indexed by the LT id.
    :param lendingtype: None (all lending types), the id of a lending type, or a list of multiple ids
    :param language: Desired language"""
    return wb_get_table('lendingtype', lendingtype, language, **params)

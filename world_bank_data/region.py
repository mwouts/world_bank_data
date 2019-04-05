import pandas as pd
from .request import wb_get


def regions(region_list=None, **params):
    """Return a DataFrame that describes one, multiple or all regions, indexed by the region id.
    :param region_list: None (all regions), the id of a region, or a list of multiple ids"""

    region_data = wb_get('region', region_list, **params)

    # 'id' is always empty
    columns = [col for col in region_data[0].keys() if col != 'id']
    df = {}

    for col in columns:
        df[col] = [cnt[col] for cnt in region_data]

    return pd.DataFrame(df, columns=columns).set_index('code')

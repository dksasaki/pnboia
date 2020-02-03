"""These simple functions were only tested for the itaguai buoy"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dtt

def _get_time(df):
    """Get time from the columns of year, month, day, hour and minute of
    the PNBOIA dataframe

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    Pandas dataframe

    """
    yyyy = df['yyyy'].values
    mm = df['mm'].values
    dd = df['dd'].values
    hour = df['hour'].values
    minu = df['min'].values

    tm = [dtt.datetime(*t) for t in  zip(yyyy,mm,dd,hour,minu)]
    return tm


def _rectify_column(df):
    """remove string spaces from the column names of the PNBOIA dataframe

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    Pandas dataframe
    """
    df1 = df.copy(deep=True)
    k = {i: i.replace(' ', '') for i in df.keys()}
    df1 = df1.rename(columns=k)
    return df1

def organize_dataframe(df):
    """ Set datetime as the index of the dataframe

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    Pandas dataframe
    """
    df1 = _rectify_column(df)
    t1 = _get_time(df1)
    df1['time'] = t1
    df1 = df1.set_index('time')
    return df1


if __name__ == '__main__':
    df = pd.read_csv('Bitaguai_argos.csv')

    # flag (1,2) para (vento, ondas)
    i = [np.where(df['flag']==j) for j in [1,2] ]

    data = {'wave': organize_dataset(df.iloc[i[1]]),
            'wind': organize_dataset(df.iloc[i[0]])}

    datanc = {i: data[i].to_xarray() for i in ['wave', 'wind']}

    for i in ['wave', 'wind']:
        datanc[i].to_netcdf(f'{i}.nc')

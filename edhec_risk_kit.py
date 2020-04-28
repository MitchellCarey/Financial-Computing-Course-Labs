import pandas as pd

def drawdown(return_series: pd.Series):
    """
    Takes a time series of asset returns
    Computes and returns a dateaframe that contains:
    the wealth index
    previous peaks
    percent dropdown
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks =wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({
        'Wealth':wealth_index,
        "Peaks": previous_peaks,
        "Drawdown": drawdowns
    })

def get_ffme_returns():
    """
    Load the Fama-French Dataset for the returns of the top and bottom deciles by marketcap
    """
    me_m = pd.read_csv("data/Portfolios_Formed_on_ME_monthly_EW.csv", 
                       header=0, index_col=0, na_values=-99.99)
    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets/100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period('M')
    return rets

def get_hfi_returns():
    """
    Load and format the EDHEC hedge fund index returns
    """
    hfi = pd.read_csv("data/edhec-hedgefundindices.csv",
                     header=0, index_col=0, parse_dates=True)
    hfi = hfi/100
    hfi.index = hfi.index.to_period('M')
    return hfi

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied series or dataframe
    returns a float or series 
    """
    demeaned_r = r-r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied series or dataframe
    returns a float or series 
    """
    demeaned_r = r-r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

import scipy.stats
def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine is a series is normal or not
    Test is applied at the 1% level by default
    returns true if the hypothesis of the normality is accepted, False otherwise
    """
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level









import math
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from greykite.framework.templates.autogen.forecast_config import (
    ForecastConfig,MetadataParam)

metadata=MetadataParam(
    time_col="date",
    value_col="turnover_rate",
    freq="D"
)
df=pd.read_csv('temp.csv')
df=df.dropna()
df=df[['date','turnover_rate']]
df=df.loc[:, ~df.columns.str.contains('^Unnamed')]
turnover_rate=df['turnover_rate']
train=turnover_rate[:400]
test=turnover_rate[400:]
df.to_csv('a.csv')
import warnings
from greykite.framework.templates.forecaster import Forecaster
from greykite.framework.templates.model_templates import ModelTemplateEnum

forecaster=Forecaster()
warnings.filterwarnings("ignore",category=UserWarning)
result=forecaster.run_forecast_config(
    df=df.reset_index(),
    config=ForecastConfig(
        model_template=ModelTemplateEnum.SILVERKITE_DAILY_1.name,
        forecast_horizon=1,
        coverage=0.95,
        metadata_param=metadata
    )
)
forecast=result.forecast
forecast.plot().show()

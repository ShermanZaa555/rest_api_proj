import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def preprocessing():
    df = pd.read_csv('../rest_api_proj/heart/data/raw data/heart.csv')
    df_clean = data_cleasing(df)
    df_wrag = data_wrangling(df_clean)
    return df_wrag

def data_cleasing(df):
    df_clean = df.copy()
    df_clean = clean_outlier(df_clean)
    return df_clean

def clean_outlier(df):
    df_num = [i for i in df.dtypes.index if df.dtypes[i] == 'int64' or df.dtypes[i] == 'float64']
    df_num_out = [i for i in df_num if len(find_outliers_IQR(df[i])) > 0]

    if len(df_num_out) == 0:
        return df
    else:
        for i in df_num_out:
            tenth_q = df[i].quantile(0.10)
            ninth_q = df[i].quantile(0.90)
            df[i] = np.where(df[i] < tenth_q, tenth_q, df[i])
            df[i] = np.where(df[i] > ninth_q, ninth_q, df[i])

    return df

def find_outliers_IQR(df):
  Q1 = df.quantile(0.25)
  Q3 = df.quantile(0.75)
  IQR = Q3-Q1
  outliers = df[((df < (Q1 - 1.5*IQR)) | (df > (Q3 + 1.5*IQR)))]
  return outliers

def data_wrangling(df):
    df_wrag = df.copy()
    df_str = [i for i in df_wrag.dtypes.index if df_wrag.dtypes[i] == 'object']

    df_bin = [i for i in df_str if len(df_wrag[i].unique()) == 2]
    df_category = [i for i in df_str if len(df_wrag[i].unique()) > 2]

    label_encode(df_bin, df_wrag)
    mean_encode(df_category, df_wrag)

    df_wrag.to_csv('../rest_api_proj/heart/data/processed data/heart_clean.csv', index=False)

    return df_wrag


def label_encode(df_bin, df):
    label_encoder = LabelEncoder()
    for i in df_bin:
        df[i] = label_encoder.fit_transform(df[i])

def mean_encode(df_cate, df):
    for i in df_cate:
        mean_encoded = df.groupby(i)['HeartDisease'].mean().to_dict()
        df[i] = df[i].map(mean_encoded)
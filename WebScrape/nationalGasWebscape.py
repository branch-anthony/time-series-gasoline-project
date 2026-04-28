import pandas as pd
import requests
from io import StringIO
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_national_gas_data():
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GASREGW"

    response = requests.get(url, verify=False, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    df = df.rename(columns={
        "observation_date": "date",
        "GASREGW": "national_gas_price"
    })

    df["date"] = pd.to_datetime(df["date"])
    df["national_gas_price"] = pd.to_numeric(df["national_gas_price"], errors="coerce")

    df = df.dropna().sort_values("date").reset_index(drop=True)

    os.makedirs("Data", exist_ok=True)
    df.to_csv("Data/National_Gas_Weekly.csv", index=False)

    return df


if __name__ == "__main__":
    df = get_national_gas_data()
    print(df.head())
    print(df.tail())
    print(df.shape)
import requests
import pandas as pd

url = "https://fuelinsights.gasbuddy.com/api/HighChart/GetHighChartRecords/"

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://fuelinsights.gasbuddy.com",
    "referer": "https://fuelinsights.gasbuddy.com/charts",
    "user-agent": "Mozilla/5.0",
    "x-requested-with": "XMLHttpRequest",
}

payload = {
    "regionID": [1883231],   # Austin
    "fuelType": 3,
    "timeWindow": [13],      # 5 years
    "frequency": 1
}

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

data = response.json()
records = data[0]["USList"]

df = pd.DataFrame(records)

df["datetime"] = pd.to_datetime(df["datetime"])
df = df.rename(columns={
    "datetime": "date",
    "price": "gas_price"
})

df = df.sort_values("date").reset_index(drop=True)

print("rows:", len(df))
print("first:", df["date"].min())
print("last:", df["date"].max())

df.to_csv("Data/austin_gas_full.csv", index=False)
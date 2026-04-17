import requests
import pandas as pd
import os

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
    "regionID": [500000],
    "fuelType": 3,
    "timeWindow": [4],
    "frequency": 1
}

print("script started")

response = requests.post(url, headers=headers, json=payload)
print("status code:", response.status_code)

response.raise_for_status()

data = response.json()
print("top-level type:", type(data))
print("top-level length:", len(data))

records = data[0]["USList"]
print("number of records:", len(records))

df = pd.DataFrame(records)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.rename(columns={"datetime": "date", "price": "gas_price"})
df = df.sort_values("date").reset_index(drop=True)

output_path = os.path.join("Data", "gasbuddy_gasdata.csv")
print("saving to:", output_path)

df.to_csv(output_path, index=False)

print("saved successfully")
print(df.head())
print(df.tail())
print(df.shape)
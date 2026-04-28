import os
import requests
import pandas as pd

MASTER_FILE = "Data/austin_gas_full.csv"

url = "https://fuelinsights.gasbuddy.com/api/HighChart/GetHighChartRecords/"

payload = {
    "regionID": [1883231],
    "fuelType": 3,
    "timeWindow": [13],
    "frequency": 1
}

headers = {
    "content-type": "application/json",
    "referer": "https://fuelinsights.gasbuddy.com/charts",
    "origin": "https://fuelinsights.gasbuddy.com",
    "user-agent": "Mozilla/5.0",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
response.raise_for_status()

data = response.json()
records = data[0]["USList"] if isinstance(data, list) else data["USList"]

new_df = pd.DataFrame(records)
new_df = (
    new_df.rename(columns={"datetime": "date", "price": "gas_price"})
    .assign(date=lambda x: pd.to_datetime(x["date"]))
    [["date", "gas_price"]]
)

old_df = pd.read_csv(MASTER_FILE)
old_df["date"] = pd.to_datetime(old_df["date"])

combined = (
    pd.concat([old_df, new_df], ignore_index=True)
    .drop_duplicates(subset="date", keep="last")
    .sort_values("date")
    .reset_index(drop=True)
)

combined.to_csv(MASTER_FILE, index=False)

print("Updated master file:", MASTER_FILE)
print("Old rows:", len(old_df))
print("New scrape rows:", len(new_df))
print("Final rows:", len(combined))
print(combined.tail())
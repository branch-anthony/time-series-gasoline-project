import pandas as pd

gas = pd.read_csv("Data/austin_gas_full.csv")
wti = pd.read_csv("Data/DCOILWTICO.csv")
nat = pd.read_csv("Data/National_Gas_Price_Weekly.csv")

# Convert dates
gas["date"] = pd.to_datetime(gas["date"])
wti["date"] = pd.to_datetime(wti["date"])
nat["date"] = pd.to_datetime(nat["date"])

# Weekly aggregation
gas_w = gas.set_index('date').resample("W-MON").mean().reset_index()
wti_w = wti.set_index('date').resample("W-MON").mean().reset_index()

# Merge
df = gas_w.merge(wti_w, on="date", how="inner") \
          .merge(nat, on="date", how="inner")
         
df = df.sort_values("date").reset_index(drop=True)

df.to_csv("Data/combinedWeekly_dataset.csv", index=False)
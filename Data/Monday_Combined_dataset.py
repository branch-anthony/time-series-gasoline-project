import pandas as pd

gas = pd.read_csv("Data/austin_gas_full.csv")
wti = pd.read_csv("Data/DCOILWTICO.csv")
nat = pd.read_csv("Data/National_Gas_Price_Weekly.csv")

gas["date"] = pd.to_datetime(gas["date"])
wti["date"] = pd.to_datetime(wti["date"])
nat["date"] = pd.to_datetime(nat["date"])

gas = gas.sort_values("date").set_index("date")
wti = wti.sort_values("date").set_index("date")
nat = nat.sort_values("date").set_index("date")

# Monday snapshot style: use last available observation up to each Monday
gas_monday = gas.resample("W-MON").ffill().reset_index()
wti_monday = wti.resample("W-MON").ffill().reset_index()
nat_monday = nat.resample("W-MON").ffill().reset_index()

df_monday = (
    gas_monday
    .merge(wti_monday, on="date", how="inner")
    .merge(nat_monday, on="date", how="inner")
    .sort_values("date")
    .reset_index(drop=True)
)

df_monday.to_csv("Data/Monday_Combined_dataset.csv", index=False)

print(df_monday.head())
print(df_monday.tail())
print(df_monday.shape)
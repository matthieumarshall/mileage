import pandas as pd

df = pd.read_csv(
    "./data/mileage.csv"
)
df.drop("coloured scale of moving sum", axis=1, inplace=True)
df.fillna(0, inplace=True)
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df.set_index("Date", inplace=True)

df["miles"] = df["km per day"] * 0.62137119
df["kilometres"] = df["km per day"]

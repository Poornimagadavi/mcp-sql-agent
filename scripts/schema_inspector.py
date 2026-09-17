import pandas as pd
import glob
import os

for file in glob.glob("data/*.csv"):
    df = pd.read_csv(file, nrows=100)
    table = os.path.splitext(os.path.basename(file))[0]

    print(f"\nTABLE: {table}")
    for col, dtype in df.dtypes.items():
        print(f"{col}: {dtype}")
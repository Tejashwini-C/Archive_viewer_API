import pandas as pd
import os
import numpy as np


def get_test_data(sheet_name):
    file_path = os.path.join("data", "API_DATA.xlsx")

    # Read Excel normally
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Replace only NaN (empty Excel cells) with ""
    df = df.replace({np.nan: ""})

    headers = df.columns.tolist()
    data = df.values.tolist()

    return headers, data

import pandas as pd
import numpy as np

# Original DataFrame
df = pd.DataFrame({0: [np.nan, '01', '02'], 1: [np.nan, np.nan, '12'], 2: [np.nan, np.nan, np.nan]})

# Transpose the DataFrame
df_transposed = df.T

# Combine the original and transposed DataFrame
df_combined = df.combine_first(df_transposed)

print(df_combined)

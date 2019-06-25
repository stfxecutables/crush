import sys
import numpy as np
import pandas as pd

arr = np.random.randn(6)
print(arr)
print(arr.std())

print("##########")
data = {'x':[1.5,1.7,3.6,2.4,2.9,3.2]}
df = pd.DataFrame(data)
print(df.loc[:'x'].std())
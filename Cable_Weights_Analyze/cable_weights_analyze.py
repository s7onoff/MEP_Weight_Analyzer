import pandas
import math
from matplotlib import pyplot as plt
import numpy as np

with open('Cable_Types_Weights.txt', 'r', encoding='utf-8') as file:
    cables_df = pandas.read_csv(file, sep=';')

cables_df['Cable Type'] = pandas.Categorical(cables_df['Cable Type'])
cables_df['D'] = cables_df['D'].apply(lambda x: float(str(x).replace(',', '.')))
cables_df['Weight'] = cables_df['Weight'].apply(lambda x: float(str(x).replace(',', '.')))
# Area (effective) of cable section, mm2
cables_df['Area_mm2'] = cables_df['D'] ** 2
# Weight in input table is in t/m. To kg/m:
cables_df['Weight'] = cables_df['Weight'].apply(lambda x: float(x)/1000)
cables_df.rename(columns={'Weight': 'Weight_kg/m'}, inplace=True)
cables_df['W/A_kg/m3'] = cables_df['Weight_kg/m']/(cables_df['Area_mm2'] / 10 ** 6)
cables_df.sort_values(by=['W/A_kg/m3'], ascending=True, ignore_index=True, inplace=True)

# bins for histogram (Sturges' rule):
k_sturges = 1+math.log2(cables_df.shape[0]).__ceil__()

cables_df['W/A_kg/m3'].hist(bins=k_sturges)
cables_df.plot(kind='scatter', x='Area_mm2', y='Weight_kg/m', c='Cable Type', cmap='jet', s=10)
# cables_df.groupby('Cable Type')['W/A_kg/m3'].hist(histtype='barstacked', bins=10, zorder=-1)
x = np.linspace(cables_df['Area_mm2'].min(), cables_df['Area_mm2'].max())
y95 = (cables_df['Weight_kg/m'] / cables_df['Area_mm2']).quantile(.95) * x
y50 = (cables_df['Weight_kg/m'] / cables_df['Area_mm2']).quantile(.5) * x
plt.plot(x, y95, "r--")
plt.plot(x, y50, "b:")

import pandas
import math
from matplotlib import pyplot as plt

with open('Cable_Types_Weights.txt', 'r', encoding='utf-8') as file:
    cables_df = pandas.read_csv(file, sep=';')

cables_df['Cable Type'] = pandas.Categorical(cables_df['Cable Type'])
cables_df['Area'] = cables_df['Area'].apply(lambda x: float(str(x).replace(',','.')))
cables_df['Weight/Area'] = cables_df['Weight']/cables_df['Area']
cables_df.sort_values(by=['Weight/Area'], ascending=True, ignore_index=True, inplace=True)

# bins for histogram (Sturges' rule):
k_sturges = 1+math.log2(cables_df.shape[0]).__ceil__()

cables_df['Weight/Area'].hist(bins=k_sturges)
cables_df.plot.scatter(x='Area', y='Weight', c='Cable Type', cmap='tab20b')
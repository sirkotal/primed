import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sb

df_medicine = pd.read_json('../dataset/medicine_details.json')
new_df_medicine = df_medicine.transpose()
new_df_medicine.head()

new_df_medicine['Medicine Name'].value_counts()
new_df_medicine.info()

new_df_medicine.isna().sum()
new_df_medicine = new_df_medicine.astype({'Excellent Review %':'int', 'Average Review %':'int', 'Poor Review %':'int'})
new_df_medicine.info()

percentages = new_df_medicine['Manufacturer'].value_counts() / new_df_medicine['Manufacturer'].value_counts().sum() * 100

new_df_medicine['Manufacturer'].value_counts().plot(kind='pie', labels=[label if i < 5 else '' for i, label in enumerate(new_df_medicine['Manufacturer'].value_counts().index)], autopct=lambda p: f'{p:.1f}%' if p >= percentages.nlargest(5).min() else '')
plt.ylabel('')
plt.title('Medicine Manufacturers')
plt.show()

numerical_summary = new_df_medicine.select_dtypes(include=['int32']).describe()

formatted_summary = numerical_summary.map(lambda n: f'{int(n)}' if n.is_integer() else f'{n:.2f}')

print(formatted_summary)

new_df_medicine.select_dtypes(include=['int32']).mean()
new_df_medicine.select_dtypes(include=['int32']).median()

numerical = new_df_medicine.select_dtypes(include=['int32']).columns.tolist()

fig, axes = plt.subplots(math.ceil(len(numerical) / 4), 4, figsize=(25, 25))
fig.subplots_adjust(hspace=0.5, wspace=0.5)
axes = axes.ravel()

for col, axis in zip(numerical, axes):
    sb.boxplot(data=new_df_medicine[col], ax=axis)

for i in range(len(numerical), len(axes)):
    fig.delaxes(axes[i])

plt.show()
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sb
from wordcloud import WordCloud
from processing import convert_json_to_sql

df_medicine = pd.read_json('../dataset/output/drug_details.json')
df_company = pd.read_json('../dataset/output/pharmaceutical_companies.json')

new_df_medicine = df_medicine.transpose()
new_df_company = df_company.transpose()

new_df_medicine.reset_index(inplace=True)
new_df_medicine.rename(columns={'index': 'Medicine Name'}, inplace=True)

new_df_medicine.head()

new_df_medicine['Medicine Name'].value_counts()
new_df_medicine.info()

new_df_medicine.isna().sum()
new_df_medicine = new_df_medicine.astype({'Excellent Review %':'int', 'Average Review %':'int', 'Poor Review %':'int'})
new_df_medicine.info()

percentages = new_df_medicine['Manufacturer'].value_counts() / new_df_medicine['Manufacturer'].value_counts().sum() * 100

plt.figure(figsize=(10, 6))
new_df_medicine['Manufacturer'].value_counts().nlargest(5).plot(kind='bar', color='purple')

plt.ylabel('Number of Medicines')
plt.title('Top 5 Medicine Manufacturers')
plt.xticks(rotation=45, ha='right')

for index, value in enumerate(new_df_medicine['Manufacturer'].value_counts().nlargest(5)):
    plt.text(index, value + 50, str(value), ha='center')

plt.tight_layout()
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


abbreviations = {
    'Hypertension (high blood pressure)': 'Hypertension', 
    'Pain relief': 'Pain Relief',
    'Treatment of Gastroesophageal reflux disease (Acid reflux)Treatment of Peptic ulcer disease': 'Gastroesophageal reflux disease',
    'Brain tumor': 'Brain tumor',
    'Treatment of Bacterial infections': 'Bacterial infections',
    'Treatment of Fungal infections': 'Fungal infections',
    'Treatment of Fungal skin infections': 'Fungal skin infections',
    'Breast cancer': 'Breast cancer',
    'Back pain': 'Back pain',
    'Pain reliefTreatment of Fever': 'Fever',
    'Treatment of Neuropathic pain': 'Neuropathic pain',
    'Treatment of Type 2 diabetes mellitus': 'Diabetes',
    'Treatment of Hypertension (high blood pressure)': 'Hypertension Prevention of Angina', 
}

new_df_medicine['Uses'] = new_df_medicine['Uses'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
new_df_medicine['Uses'] = new_df_medicine['Uses'].replace(abbreviations)

top_uses = new_df_medicine['Uses'].value_counts().nlargest(10).index
new_df_medicine_filtered = new_df_medicine[new_df_medicine['Uses'].isin(top_uses)]

category_summary = new_df_medicine_filtered.groupby('Uses')[['Excellent Review %', 'Average Review %', 'Poor Review %']].mean()

category_summary.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.xticks(rotation=45, ha='right')
plt.title('Mean of Review Percentages by Use Category')
plt.ylabel('Review Percentage')
plt.show()


all_side_effects = ' '.join([' '.join(effect) if isinstance(effect, list) else effect for effect in new_df_medicine['Uses'].dropna()])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_side_effects)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Common Uses')
plt.show()


new_df_medicine['Side_effects'] = new_df_medicine['Side_effects'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    
side_effects_flat = new_df_medicine['Side_effects'].str.split(', ').explode()

top_side_effects = side_effects_flat.value_counts().nlargest(10)

plt.figure(figsize=(12, 8))
top_side_effects.plot(kind='bar', color='steelblue')
plt.xlabel('Side Effects')
plt.ylabel('Number of Medicines')
plt.title('Distribution of Medicines by Number of Common Side Effects')
plt.xticks(rotation=45, ha='right')
plt.show()


abbreviations = {
    "Levocetirizine (5mg) + Montelukast (10mg)": "Levocetirizine + Montelukast",
    "Luliconazole (1% w/w)": "Luliconazole",
    "Telmisartan (40mg)": "Telmisartan",
    "Ketoconazole (2% w/w)": "Ketoconazole",
    "Domperidone (30mg) + Rabeprazole (20mg)": "Domperidone + Rabeprazole"
}

top_compositions = new_df_medicine['Composition'].value_counts().nlargest(5)
    
top_compositions.index = [abbreviations.get(comp, comp) for comp in top_compositions.index]
    
plt.figure(figsize=(10, 8))
plt.pie(top_compositions, labels=top_compositions.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Top 5 Most Common Medicine Compositions')
plt.show()


year_counts = new_df_company['Year Start'].dropna().value_counts().sort_values(ascending=False)

top_years = year_counts.head(5).sort_index()

plt.figure(figsize=(10, 6))
top_years.plot(kind='bar', color='orange')
plt.xlabel('Year of Foundation')
plt.ylabel('Number of Companies')
plt.title('Years with the Most Company Foundations')
plt.yticks(range(0, int(top_years.max()) + 1))
plt.show()


convert_json_to_sql(new_df_medicine)

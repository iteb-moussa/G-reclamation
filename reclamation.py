import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Charger les données JSON
with open("data.json", 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Créer un DataFrame à partir des données JSON
df = pd.DataFrame(data)

# Normaliser les noms de colonnes en minuscules
df.columns = df.columns.str.lower()

# Supprimer les espaces avant et après le nom de colonne
df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) and x.strip() != x else x)

# Fusionner les colonnes ayant le même nom
df = df.groupby(level=0, axis=1).first()

# Supprimer la colonne 'B'
df.drop(columns=['type_assurance'], inplace=True)
# Supprimer les doublons
df = df.drop_duplicates()

# Lire le fichier Excel
df_excel = pd.read_excel('C:/Users/ACER/stage/motif.xlsx')

# Remplacer les valeurs NaN dans la colonne "type d'assurance" par la valeur précédente
df_excel['Assurance'].fillna(method='ffill', inplace=True)
# Supprimez les lignes contenant des valeurs NaN
df_excel = df_excel.dropna()
df_excel.rename(columns={'Motifs': 'motif'}, inplace=True)

# Fonction pour obtenir le type d'assurance
def get_type_assurance(row):
    motif = row['motif']
    sujet_demande = row['sujet_demande']
    # Vérification dans df2 pour le motif
    if motif in df_excel['motif'].values:
        return df_excel.loc[df_excel['motif'] == motif, 'Assurance'].iloc[0]
    # Vérification dans df2 pour le sujet de la demande
    elif sujet_demande in df_excel['motif'].values:
        return df_excel.loc[df_excel['motif'] == sujet_demande, 'Assurance'].iloc[0]
    else:
        return "Non spécifié"

# Application de la fonction pour obtenir le type d'assurance pour chaque ligne de df1
df['type_assurance'] = df.apply(get_type_assurance, axis=1)

# Affichage du résultat
import matplotlib.pyplot as plt

# Créer un histogramme pour l'âge
df['age'].plot.hist(bins=20)
plt.xlabel('Âge')
plt.ylabel('Fréquence')
plt.title('Distribution de l\'âge')
plt.show()
from matplotlib import cm

# Count the number of demands by type
demandes_par_type = df["type_demande"].value_counts()

# Choose a color palette
palette = cm.get_cmap("tab10")  # Example palette (adjust as needed)

# Create a list of colors (one for each type)
colors = [palette(i / (len(demandes_par_type) - 1)) for i in range(len(demandes_par_type))]

# Create the horizontal bar chart
plt.barh(demandes_par_type.index, demandes_par_type.values, color=colors)

# Set chart title and labels (adjust for horizontal layout)
plt.title("Répartition des demandes par type")
plt.xlabel("Nombre de demandes")
plt.ylabel("Type de demande")

# Display the chart
plt.show()

# Créer un dictionnaire pour stocker les totaux par région
demande_par_region = {}
for region in df["region"].unique():
    demande_par_region[region] = df[df["region"] == region].shape[0]

# Créer un DataFrame à partir du dictionnaire
df_demande = pd.DataFrame.from_dict(demande_par_region, orient="index", columns=["Total"])

# Définir le nom d'index
df_demande.index.name = "Région"

# Créer un graphique à secteurs (pie chart)
plt.figure(figsize=(8, 8))
plt.pie(df_demande["Total"], labels=df_demande.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)

# Ajouter un titre
plt.title("Répartition des demandes par région")

# Afficher le graphique
plt.show()
# Compter le nombre de chaque genre
genre_counts = df['genre'].value_counts()

# Créer un graphique à secteurs
plt.figure(figsize=(6, 6))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', colors=['pink', 'lightblue'])
plt.title('Répartition des genres')

# Afficher le graphique
plt.show()
# Compter le nombre de chaque profession
profession_counts = df['profession'].value_counts()

# Créer un diagramme à barres horizontales
plt.figure(figsize=(8, 6))
plt.barh(profession_counts.index, profession_counts.values, color='purple')
plt.xlabel('Nombre de personnes')
plt.ylabel('Profession')
plt.title('Répartition des professions')

# Afficher le graphique
plt.show()

# Count the number of demands by type
demandes_par_type = df["type_assurance"].value_counts()

# Choose a color palette
palette = cm.get_cmap("tab10")  # Example palette (adjust as needed)

# Create a list of colors (one for each type)
colors = [palette(i / (len(demandes_par_type) - 1)) for i in range(len(demandes_par_type))]

# Create the horizontal bar chart
plt.barh(demandes_par_type.index, demandes_par_type.values, color=colors)

# Set chart title and labels (adjust for horizontal layout)
plt.title("Répartition des demandes par type")
plt.xlabel("Nombre de demandes")
plt.ylabel("Type de demande")

# Display the chart
plt.show()

# Moyenne, médiane et autres statistiques pour chaque type de demande
demandes_stats = df.groupby('type_demande')['age'].agg(['mean', 'median', 'std', 'min', 'max', 'count'])
print(demandes_stats)
# Moyenne, médiane et autres statistiques pour chaque type d'assurance
assurance_stats = df.groupby('type_assurance')['age'].agg(['mean', 'median', 'std', 'min', 'max', 'count'])
print(assurance_stats)



# Calculer le z-score pour l'âge
df['z_score_age'] = (df['age'] - df['age'].mean()) / df['age'].std()

# Identifier les valeurs avec un z-score élevé (par exemple, supérieur à 2)
anomalies = df[df['z_score_age'] > 2]

# Visualiser les anomalies
plt.scatter(df['age'], df['z_score_age'], label='Données')
plt.scatter(anomalies['age'], anomalies['z_score_age'], color='r', label='Anomalies')
plt.xlabel('Âge')
plt.ylabel('Z-score')
plt.title('Détection des anomalies dans l\'âge')
plt.legend()
plt.show()
# Créer un sous-ensemble de données pour chaque type de demande
demandes_par_date = df.groupby(['date', 'type_demande']).size().unstack(fill_value=0)

# Créer un graphique de ligne pour chaque type de demande
demandes_par_date.plot(kind='line', figsize=(10, 6))
plt.xlabel('Date')
plt.ylabel('Nombre de demandes')
plt.title('Nombre de demandes en fonction de la date et du type de demande')
plt.legend(title='Type de demande')
plt.show()
# Par exemple, vous pouvez utiliser des diagrammes en barres pour voir la distribution des réclamations par type d'assurance
df['type_assurance'].value_counts().plot(kind='bar', title='Distribution des réclamations par type d\'assurance')
plt.xlabel('Type d\'assurance')
plt.ylabel('Nombre de réclamations')
plt.show()

# Vous pouvez également comparer les âges moyens des demandeurs pour chaque type d'assurance
age_mean_by_type = df.groupby('type_assurance')['age'].mean()
print(age_mean_by_type)

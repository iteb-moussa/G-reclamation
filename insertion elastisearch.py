import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Chemin vers votre fichier CSV
csv_file_path = 'C:/Users/ACER/stage/assurance.csv'

# Nom de l'index Elasticsearch dans lequel vous souhaitez importer les données
index_name = 'kpi'

# Initialiser une connexion Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Charger le fichier CSV dans un DataFrame pandas
df = pd.read_csv(csv_file_path)

# Convertir le DataFrame en liste d'actions pour Elasticsearch
actions = [
    {
        '_index': index_name,
        '_source': row.to_dict()  # Convertir chaque ligne en un dictionnaire
    }
    for _, row in df.iterrows()
]

# Utiliser elasticsearch.helpers.bulk pour insérer les données dans Elasticsearch
success, _ = bulk(es, actions)

print(f"Importé {success} documents dans Elasticsearch")

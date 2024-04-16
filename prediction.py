import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Charger les données
data = pd.read_csv("assurance.csv")
# Convertir la colonne 'date' en format datetime
data['date'] = pd.to_datetime(data['date'])

# Extraire le mois et l'année à partir de la colonne 'date'
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year

# Regrouper les réclamations par mois, type_demande et compter le nombre de réclamations
monthly_claims_by_type = data.groupby(['year', 'month', 'type_demande']).size().reset_index(name='claims_count')

# Utiliser ARIMA pour ajuster un modèle à chaque série temporelle de réclamations
for type_demande, group in monthly_claims_by_type.groupby('type_demande'):
    # Créer une série temporelle à partir du nombre de réclamations
    ts = pd.Series(group['claims_count'].values, index=pd.to_datetime(group[['year', 'month']].assign(day=1)))

    # Ajuster le modèle ARIMA
    model = ARIMA(ts, order=(1, 1, 1))  # Vous pouvez ajuster l'ordre de l'ARIMA selon vos besoins
    arima_result = model.fit()

    # Faire des prédictions pour les 12 prochains mois
    predictions = arima_result.forecast(steps=12)

    # Tracer les résultats
    plt.figure(figsize=(15, 7))
    plt.plot(ts.index, ts, label='Observations')
    plt.plot(predictions.index, predictions, color='r', label='Prévisions')
    plt.title(f'Prévisions des réclamations mensuelles pour le type de demande : {type_demande}')
    plt.xlabel('Date')
    plt.ylabel('Nombre de réclamations')
    plt.legend()
    plt.show()
import os
import requests
import pandas as pd
import pickle
from dash import html
from dotenv import load_dotenv
load_dotenv()

def calculate_rolling_performance(df, team_column, result_column, rolling_window=5):
    # Create a copy to avoid modifying the original data
    performance = df[[team_column, result_column]].copy()
    performance['is_win'] = performance[result_column].apply(lambda x: 1 if x == 1 else 0)
    
    # Group by team and calculate rolling win rate
    rolling_performance = performance.groupby(team_column)['is_win'].rolling(window=rolling_window, min_periods=1).mean().reset_index(0, drop=True)
    
    return rolling_performance

def get_base():

    brasileirao_data = pd.read_csv('model/mundo_transfermarkt_competicoes_brasileirao_serie_a.csv')

    columns_to_drop = [
        'arbitro', 'publico', 'publico_max', 'chutes_bola_parada_mandante', 
        'chutes_bola_parada_visitante', 'defesas_mandante', 'defesas_visitante',
        'impedimentos_mandante', 'impedimentos_visitante', 'chutes_mandante', 
        'chutes_visitante', 'chutes_fora_mandante', 'chutes_fora_visitante'
    ]

    cleaned_data = brasileirao_data.drop(columns=columns_to_drop)

    cleaned_data['resultado'] = cleaned_data.apply(
        lambda row: 1 if row['gols_mandante'] > row['gols_visitante'] else (-1 if row['gols_mandante'] < row['gols_visitante'] else 0),
        axis=1
    )

    # Add rolling performance for both home and away teams
    cleaned_data['mandante_rolling_performance'] = calculate_rolling_performance(cleaned_data, 'time_mandante', 'resultado')
    cleaned_data['visitante_rolling_performance'] = calculate_rolling_performance(cleaned_data, 'time_visitante', 'resultado')

    return cleaned_data

def get_model():
    with open('model/modelo.pkl', 'rb') as arquivo:
        model = pickle.load(arquivo)

    return model

def get_team_info(team_name):

    # Cabeçalho com a chave de API
    headers = {
        'X-Auth-Token': os.environ.get("PI_FOOTBALL_KEY")
    }

    # URL do endpoint de times para uma competição (por exemplo, Brasileirão Série A)
    url = "https://api.football-data.org/v4/competitions/BSA/teams"

    # Fazer a requisição
    response = requests.get(url, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        
        data = response.json()
        teams = data['teams']
        filtered_team = [team for team in teams if team_name.lower() in team['name'].lower()]
        
        if filtered_team:
            return html.Img(
                id='result-img',
                src=filtered_team[0]['crest'],
                className='img-fluid d-flex justify-content-center result-img',
            )
        
    else:
        print(f"Erro: {response.status_code}")
        print(response)
    
    return html.Label(
        'Não foi possivel encontrar uma imagem para esse time',
        className="d-flex justify-content-center",
    )

def prediction_teams(model, cleaned_data, mandante, visitante):

    mandante_performance = cleaned_data[cleaned_data['time_mandante'] == mandante]['mandante_rolling_performance'].mean()
    visitante_performance = cleaned_data[cleaned_data['time_visitante'] == visitante]['visitante_rolling_performance'].mean()

    # Creating a DataFrame for the São Paulo x Corinthians match
    match_data = pd.DataFrame({
        'mandante_rolling_performance': [mandante_performance],
        'visitante_rolling_performance': [visitante_performance]
    })

    # Making a prediction using the trained model
    match_prediction = model.predict(match_data)

    # Mapping the prediction to the result
    result_map = {1: mandante, 0: 'Empate', -1: visitante}
    predicted_result = result_map[match_prediction[0]]

    return predicted_result
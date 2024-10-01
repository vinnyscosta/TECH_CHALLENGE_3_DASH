import dash
from dash import html, Output, Input, State
from utils import *
from config import *

def register_callbacks(app):

    @app.callback(
        [
            Output('possivel-resultado', 'children'),
            Output('possivel-resultado-icon', 'children'),
            Output('mandante-container', 'children'),
            Output('visitante-container', 'children'),
        ],
        Input('mandante-dropdown', 'value'),
        Input('visitante-dropdown', 'value'),
        State('mandante-container', 'children'),
        State('visitante-container', 'children'),
    )
    def predict(
        mandante, 
        visitante,
        mandante_img,
        visitante_img,
        ):

        trigger_id = dash.callback_context.triggered[0]['prop_id']

        not_found = html.I(className="fas fa-times fa-lg")

        prediction = html.Label(
            'Selecione os times para que a predição possa ser realizada.',
            className="d-flex justify-content-center mt-2",
        )

        prediction_icon = html.I(className="fas fa-futbol fa-lg")

        if mandante:
            if 'mandante' in trigger_id:
                mandante_img = get_team_info(mandante)
        else:
            mandante_img = not_found

        if visitante:
            if 'visitante' in trigger_id:
                visitante_img = get_team_info(visitante)
        else:
            visitante_img = not_found

        if mandante and visitante:
            prediction = prediction_teams(model, cleaned_data, mandante, visitante)
            prediction = [
                html.P(
                    f'Em um possivel jogo entre {mandante} X {visitante} o resultado possível é: {prediction}',
                    className="d-flex justify-content-center"
                )
            ]

            if prediction == mandante:
                prediction_icon = mandante_img
            
            elif prediction == visitante:
                prediction_icon = visitante_img

            elif prediction == 'Empate':
                prediction_icon = html.I(className="fas fa-equals fa-lg")

        return [
            prediction,
            prediction_icon,
            mandante_img,
            visitante_img,
        ]

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import *

def card_team_choice(type:str):

    return dbc.Card(
        dbc.CardBody(
            [
                html.H2(
                    f'Time {type.title()}',
                    className="d-flex justify-content-center"
                ),
                dcc.Dropdown(
                    options=teams,
                    placeholder="Escolha um time...",
                    id=f'{type}-dropdown',
                ),
                html.Div(
                    [
                        html.I(className="fas fa-times fa-lg")
                    ],
                    id=f"{type}-container",
                    className="m-5 d-flex justify-content-center"
                )
            ]
        ),
        color="dark",
        # style={"width": "18rem"},
    )

def result_area():
    return [
        html.H2(
            'Possivel Resultado',
            className="d-flex justify-content-center",
        ),
        html.Div(
            [],
            id="possivel-resultado",
            className="m-5 d-flex justify-content-center"
        ),
        html.Div(
            [
                html.I(className="fas fa-futbol fa-lg")
            ],
            id="possivel-resultado-icon",
            className="m-5 d-flex justify-content-center"
        ),
    ]
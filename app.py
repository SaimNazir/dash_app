import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_vtk

from pydoc import classname
from dash import dash_table, Dash, dcc, html
from dash.dependencies import Input, Output


from index import app, df
from portfolio import portfolio_layout
from individual_tab import individual_layout
from model_performance import model_perf_layout

# from xAI import xAI_layout


app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Portfolio Overview",
                    tab_id="tab_portfolio",
                    labelClassName="text-success font-weigth",
                ),
                dbc.Tab(
                    label="Individual Overview",
                    tab_id="tab_individual",
                    labelClassName="text-success font-weigth",
                ),
                # dbc.Tab(
                #     label="xAI",
                #     tab_id="tab_xAI",
                #     labelClassName="text-success font-weigth",
                # ),
                dbc.Tab(
                    label="Model Performance",
                    tab_id="tab_model_perf",
                    labelClassName="text-success font-weigth",
                ),
            ],
            id="tabs",
            active_tab="tab_portfolio",
        ),
    ],
    className="mt-3",
)


app.layout = dbc.Container(
    [
        # Title
        dbc.Row(
            dbc.Col(html.H3("Dashboard"), width={"size": 6, "offset": 5},),
            justify="start",
        ),
        html.Hr(),
        dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
        html.Div(id="content", children=[]),
        html.Br(),
        dcc.Store(id="stored_data", data=df.to_dict("records")),
        dcc.Store(id="slider1", data=None),
    ]
)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(tab_chosen):
    if tab_chosen == "tab_individual":
        return individual_layout
    elif tab_chosen == "tab_portfolio":
        return portfolio_layout
    # elif tab_chosen == "tab_xAI":
    #     return xAI_layout
    elif tab_chosen == "tab_model_perf":
        return model_perf_layout


# RUN
# -------------------------------------------------------#
if __name__ == "__main__":
    app.run_server(debug=False)


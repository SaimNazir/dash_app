import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_vtk

from pydoc import classname
from dash import dash_table, Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from index import app, df
#from vizzes import default_histogram, income_histogram, age_hist, revolve_hist



def prob_default(dataframe):
    fig = (
        px.histogram(
            dataframe,
            x="Probability of Default",
            histnorm="probability",
            opacity=0.8,
            hover_data=dataframe.columns,
        )
        .update_layout(
            xaxis_title="Probability of Default", yaxis_title="Probability Density"
        )
        .update_traces(marker=dict(color="#1f77b4"))
    )

    return fig


default_histogram = prob_default(df)


def monthly_histogram(dataframe):
    fig = (
        px.histogram(
            dataframe,
            x="MonthlyIncome",
            # histnorm="probability",
            opacity=0.8,
            hover_data=dataframe.columns,
        )
        .update_layout(xaxis_title="Monthly Income", yaxis_title=None)
        .update_traces(marker=dict(color="#ff7f0e"))
    )
    return fig


income_histogram = monthly_histogram(df)


def age_histogram(dataframe):
    fig = (
        px.histogram(
            df,
            x="age",
            # histnorm="probability",
            opacity=0.8,
            hover_data=df.columns,
        )
        .update_layout(xaxis_title="Age", yaxis_title=None)
        .update_traces(marker=dict(color="#17becf"))
    )

    return fig


age_hist = age_histogram(df)


def revolver_histogram(dataframe):
    fig = (
        px.histogram(
            df,
            x="RevolvingUtilizationOfUnsecuredLines",
            # histnorm="probability",
            opacity=0.8,
            hover_data=df.columns,
        )
        .update_layout(xaxis_title="Revolving Use of Credit", yaxis_title=None)
        .update_traces(marker=dict(color="#2ca02c"))
    )

    return fig


revolve_hist = revolver_histogram(df)




# LAYOUT
# -------------------------------------------------------#
portfolio_layout = html.Div(
    [
        # PD slider title
        dbc.Row(
            [
                dbc.Col(html.H6("PD Slider"), width={"size": 2, "offset": 1},),
                dbc.Col(html.H6("Debt Ratio Slider"), width={"size": 2, "offset": 2},),
                dbc.Col(html.H6("Open Credit Slider"), width={"size": 2, "offset": 2},),
            ],
            align="stretch",
        ),
        # Sliders
        dbc.Row(
            [
                dbc.Col(
                    dcc.RangeSlider(
                        0, 1, 0.1, value=[0, 1], id="pd_slider", persistence=True
                    ),
                    width={"size": 4, "offset": 0},
                ),
                dbc.Col(
                    dcc.RangeSlider(
                        0, 1, 0.1, value=[0, 1], id="debt_slider", persistence=True
                    ),
                    width={"size": 4, "offset": 0},
                ),
                dbc.Col(
                    dcc.RangeSlider(
                        0,
                        60,
                        5,
                        value=[0, 60],
                        id="open_credit_slider",
                        persistence=True,
                    ),
                    width={"size": 4, "offset": 0},
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Probability of Default Distribution"),
                    width={"size": 6, "offset": 4},
                ),
            ],
            align="start",
        ),
        dbc.Row(dbc.Col(dcc.Graph(id="hist", figure=default_histogram),)),
        # income, age andxx charts
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="hist_income", figure=income_histogram),
                    width={"size": 4},
                ),
                dbc.Col(dcc.Graph(id="hist_age", figure=age_hist), width={"size": 4},),
                dbc.Col(
                    dcc.Graph(id="revolving", figure=revolve_hist), width={"size": 4},
                ),
            ]
        ),
    ]
)


# CALBACKS
# -------------------------------------------------------#

# pd filtering
@app.callback(
    # Output('datatable_id', 'children'),
    Output("hist", "figure"),
    [
        Input("open_credit_slider", "value"),
        Input("pd_slider", "value"),
        Input("debt_slider", "value"),
    ],
)
def update_graph(slice1, slice2, slice3):
    print(slice1)

    dff = df[
        (df["NumberOfOpenCreditLinesAndLoans"] >= slice1[0])
        & (df["NumberOfOpenCreditLinesAndLoans"] <= slice1[1])
        & (df["Probability of Default"] >= slice2[0])
        & (df["Probability of Default"] <= slice2[1])
        & (df["DebtRatio"] >= slice3[0])
        & (df["DebtRatio"] <= slice3[1])
    ]

    fig = (
        px.histogram(
            dff,
            x="Probability of Default",
            histnorm="probability",
            opacity=0.8,
            hover_data=dff.columns,
        )
        .update_layout(
            xaxis_title="Probability of Default", yaxis_title="Probability Density"
        )
        .update_traces(marker=dict(color="#1f77b4"))
    )

    return fig


# monthlyIncome filtering
@app.callback(
    Output("hist_income", "figure"),
    [
        Input("open_credit_slider", "value"),
        Input("pd_slider", "value"),
        Input("debt_slider", "value"),
    ],
)
def update_income(slice1, slice2, slice3):

    dff = df[
        (df["NumberOfOpenCreditLinesAndLoans"] >= slice1[0])
        & (df["NumberOfOpenCreditLinesAndLoans"] <= slice1[1])
        & (df["Probability of Default"] >= slice2[0])
        & (df["Probability of Default"] <= slice2[1])
        & (df["DebtRatio"] >= slice3[0])
        & (df["DebtRatio"] <= slice3[1])
    ]

    fig = (
        px.histogram(
            dff,
            x="MonthlyIncome",
            # histnorm="probability",
            opacity=0.8,
            hover_data=dff.columns,
        )
        .update_layout(xaxis_title="Monthly Income", yaxis_title=None)
        .update_traces(marker=dict(color="#ff7f0e"))
    )
    return fig


# age filtering
@app.callback(
    Output("hist_age", "figure"),
    [
        Input("open_credit_slider", "value"),
        Input("pd_slider", "value"),
        Input("debt_slider", "value"),
    ],
)
def update_age(slice1, slice2, slice3):

    dff = df[
        (df["NumberOfOpenCreditLinesAndLoans"] >= slice1[0])
        & (df["NumberOfOpenCreditLinesAndLoans"] <= slice1[1])
        & (df["Probability of Default"] >= slice2[0])
        & (df["Probability of Default"] <= slice2[1])
        & (df["DebtRatio"] >= slice3[0])
        & (df["DebtRatio"] <= slice3[1])
    ]

    fig = (
        px.histogram(
            dff,
            x="age",
            # histnorm="probability",
            opacity=0.8,
            hover_data=df.columns,
        )
        .update_layout(xaxis_title="Age", yaxis_title=None)
        .update_traces(marker=dict(color="#17becf"))
    )

    return fig


# revolver filtering
@app.callback(
    Output("revolving", "figure"),
    [
        Input("open_credit_slider", "value"),
        Input("pd_slider", "value"),
        Input("debt_slider", "value"),
    ],
)
def update_revolver(slice1, slice2, slice3):

    dff = df[
        (df["NumberOfOpenCreditLinesAndLoans"] >= slice1[0])
        & (df["NumberOfOpenCreditLinesAndLoans"] <= slice1[1])
        & (df["Probability of Default"] >= slice2[0])
        & (df["Probability of Default"] <= slice2[1])
        & (df["DebtRatio"] >= slice3[0])
        & (df["DebtRatio"] <= slice3[1])
    ]

    fig = (
        px.histogram(
            dff,
            x="RevolvingUtilizationOfUnsecuredLines",
            # histnorm="probability",
            opacity=0.8,
            hover_data=df.columns,
        )
        .update_layout(xaxis_title="Revolving Use of Credit", yaxis_title=None)
        .update_traces(marker=dict(color="#2ca02c"))
    )

    return fig

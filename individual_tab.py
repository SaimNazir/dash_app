from pydoc import classname
import pandas as pd

pd.options.plotting.backend = "plotly"

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_vtk
import json

from dash import dash_table, Dash, dcc, html
from dash.dependencies import Input, Output
from index import app, df


shap_df = pd.read_csv(r"/home/saim/Desktop/dash/shap_df.csv")


def shap_initial(shap_dataframe):
    fig = shap_dataframe.iloc[0].plot(kind="bar")

    fig.for_each_trace(
        lambda t: t.update(marker_color=t.y, marker_coloraxis="coloraxis")
    ).update_layout(
        coloraxis_cmin=-1,
        coloraxis_cmax=1,
        coloraxis_colorscale=px.colors.sequential.Bluered,
        showlegend=False,
    ).update_yaxes(
        title="Feature Importance for PD", title_font_size=12
    )

    return fig


inital_bar = shap_initial(shap_df)


initial_active_cell = {"row": 0, "column": 0, "column_id": "Name", "row_id": 0}

# LAYOUT
# -------------------------------------------------------#
individual_layout = html.Div(
    [
        html.Br(),
        dbc.Row(
            [dbc.Col(html.H4("Customer Table"), width={"size": 6, "offset": 5},),],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        columns=[
                            {"name": i, "id": i}
                            for i in df.loc[
                                :,
                                [
                                    "Name",
                                    "age",
                                    "DebtRatio",
                                    "MonthlyIncome",
                                    "isRetired",
                                    "Probability of Default",
                                ],
                            ]
                        ],
                        data=df.to_dict("records"),
                        filter_action="native",
                        sort_action="native",
                        sort_mode="single",
                        # row_selectable="single",
                        style_data={
                            "whiteSpace": "normal",
                            "height": "auto",
                            "lineHeight": "1px",
                        },
                        fill_width=True,
                        style_table={"overflowX": "auto"},
                        page_size=10,
                        selected_rows=[],
                        active_cell=initial_active_cell,
                        id="tbl_out",
                        persistence=True,
                    ),
                    width={"size": 10, "offset": 1},
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Feature Explainability"), width={"size": 6, "offset": 4},
                ),
            ],
            align="start",
        ),
        # dbc.Row(
        #     dbc.Col(html.Img(src="/assets/shap.png"), width={"size": 3, "offset": 0}),
        # ),
        dbc.Row(dbc.Col(dcc.Graph(id="chart", figure=inital_bar),)),
    ]
)


# CALBACKS
# -------------------------------------------------------#


@app.callback(
    Output(component_id="chart", component_property="figure"),
    Input(component_id="tbl_out", component_property="active_cell"),
)
def cell_clicked(active_cell):

    row = active_cell["row"]
    fig = shap_df.iloc[row].plot(kind="bar")

    fig.for_each_trace(
        lambda t: t.update(marker_color=t.y, marker_coloraxis="coloraxis")
    ).update_layout(
        coloraxis_cmin=-1,
        coloraxis_cmax=1,
        coloraxis_colorscale=px.colors.sequential.Bluered,
        showlegend=False,
    ).update_yaxes(
        title="Feature Importance for PD", title_font_size=12
    )

    return fig

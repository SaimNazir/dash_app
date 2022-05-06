from pydoc import classname
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_vtk
import plotly.express as px
import plotly.figure_factory as ff


from dash import dash_table, Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from sklearn import metrics


from index import app, df, clf, X_test, y_test
from index import app, df, X_test, y_test, clf, y_train, X_train
from sklearn.metrics import confusion_matrix, accuracy_score


def evaluation(model, model_name):
    prediction = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    fpr, tpr, thresh = metrics.roc_curve(y_test, probabilities[:, 1])
    roc_auc = metrics.auc(fpr, tpr)
    class_report = metrics.classification_report(y_test, prediction)

    return prediction, probabilities, roc_auc, tpr, fpr, class_report


lgbm_pred, lgbm_proba, lgbm_roc_auc, lgbm_tpr, lgbm_fpr, lgbm_report = evaluation(
    clf, "Light GBM"
)


train_pred = clf.predict(X_train)

train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, lgbm_pred)

# graph components


def roc_curve(false_pr, true_pr):

    fig = px.area(
        x=false_pr,
        y=true_pr,
        labels=dict(x="False Positive Rate", y="True Positive Rate"),
        width=700,
        height=400,
    )

    fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)
    fig.update_layout(
        title_text="<i><b>ROC Curve </b></i> "
        + f"(AUC={metrics.auc(false_pr, true_pr):.2f})",
    )

    return fig


roc_auc_fig = roc_curve(lgbm_fpr, lgbm_tpr)


def grouped_barchart(dataframe):

    # slices report to columns precision, recall and f1 and rows 0, 1 and puts in list
    not_default_ls = dataframe.iloc[0, :].values.tolist()
    default_ls = dataframe.iloc[1, :].values.tolist()

    # rounds elements in lists
    rounded_NDL = [round(i, 2) for i in not_default_ls]
    rounded_DL = [round(i, 2) for i in default_ls]

    # plotting
    values = ["precision", "recall", "f1-score"]

    fig = go.Figure(
        data=[
            go.Bar(
                name="Non-Default Class",
                x=values,
                y=not_default_ls,
                text=rounded_NDL,
                textposition="auto",
            ),
            go.Bar(
                name="Default Class",
                x=values,
                y=default_ls,
                text=rounded_DL,
                textposition="auto",
            ),
        ]
    )

    fig.update_layout(
        title_text="<i><b>Classification Report</b></i>", barmode="group", height=450,
    )  # .update_traces(color="#2ca02c")

    return fig


# input is a df of the classification report as created by sklearn
report = pd.DataFrame(
    metrics.classification_report(y_test, lgbm_pred, output_dict=True)
).transpose()

classi = grouped_barchart(report)


ls_true = y_test["SeriousDlqin2yrs"].tolist()
cm = confusion_matrix(ls_true, list(lgbm_pred))
z = cm.tolist()
z = z[::-1]

# confusion matrix
# z = [[589, 2047], [19166, 1860]]


def confusion_matrix(z):
    x = ["Not-default", "Default"]
    y = x[::-1].copy()

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure
    fig = ff.create_annotated_heatmap(z, colorscale="blues",)

    # add title
    fig.update_layout(title_text="<i><b>Confusion matrix</b></i>")

    # add custom xaxis title
    fig.add_annotation(
        dict(
            font=dict(color="black", size=14),
            x=0.5,
            y=-0.15,
            showarrow=False,
            text="Predicted",
            xref="paper",
            yref="paper",
        )
    )

    # add custom yaxis title
    fig.add_annotation(
        dict(
            font=dict(color="black", size=14),
            x=-0.1,
            y=0.5,
            showarrow=False,
            text="True",
            textangle=-90,
            xref="paper",
            yref="paper",
        )
    )

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=50, l=100))

    # add colorbar
    fig["data"][0]["showscale"] = True

    return fig


heat = confusion_matrix(z)


# LAYOUT
# -------------------------------------------------------#
model_perf_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H2(f"{train_acc*100:.2f}%", className="card-title"),
                            html.P("Model Training Accuracy", className="card-text"),
                        ],
                        body=True,
                        color="light",
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H2(f"{test_acc*100:.2f}%", className="card-title"),
                            html.P("Model Test Accuracy", className="card-text"),
                        ],
                        body=True,
                        color="dark",
                        inverse=True,
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H2(
                                f"{X_train.shape[0]} / {X_test.shape[0]}",
                                className="card-title",
                            ),
                            html.P("Train / Test Split", className="card-text"),
                        ],
                        body=True,
                        color="primary",
                        inverse=True,
                    ),
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="conf", figure=heat),
                    width={"size": 6, "offset": 0, "order": 1},
                ),
                dbc.Col(
                    dcc.Graph(id="grouped_bar", figure=classi),
                    width={"size": 6, "offset": 0, "order": 0},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="roc", figure=roc_auc_fig),
                    width={"size": 12, "offset": 0, "order": 1},
                ),
            ]
        ),
    ]
)


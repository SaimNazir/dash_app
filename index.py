import dash
import dash_bootstrap_components as dbc
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split


# INIT
# -------------------------------------------------------#
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    title="My app",
    external_stylesheets=[dbc.themes.LUX],
)

server = app.server

### load ML model ###########################################
with open("lgbm_model.pickle", "rb") as f:
    clf = pickle.load(f)


csv = pd.read_csv(r"/home/saim/Desktop/clen.csv")


X = csv.iloc[:, 1:]
y = csv.iloc[:, 0:1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)


probabilities_lgbm = clf.predict_proba(X)
lgbDF = pd.DataFrame({"Probability of Default": probabilities_lgbm[:, 1]})


df_proba = lgbDF.reset_index(drop=True)
df_rest = csv.reset_index(drop=True)

df = df_rest.join(df_proba)
df = df.round(2)

names = ["Winston Smith"] * len(df)
df["Name"] = names


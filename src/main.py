import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import mlflow
import numpy as np
import os

# Establecer la URI de la base de datos SQLite
os.environ['MLFLOW_TRACKING_URI'] = 'sqlite:///mlruns.db'

# Configuración de MLflow
mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
mlflow.set_experiment("arboles")

# Carga de datos
df = pd.read_parquet(r"C:\Users\Usuario\Downloads\Datos_la_liga_preparados_entrenamiento.parquet", engine='pyarrow')
df.reset_index(drop=True, inplace=True)
df = df.drop(['año', 'Player', 'index'], axis=1)

# Codificación One-Hot
variables = ['Equipo', 'position', 'nationality']

# Codificación One-Hot sin sparse=False
one_hot_encoder = OneHotEncoder()
one_hot_encoded = one_hot_encoder.fit_transform(df[variables])

# Convertir de matriz dispersa a densa
one_hot_encoded_dense = one_hot_encoded.toarray()

# Crear DataFrame con los nombres de las nuevas columnas
one_hot_encoded_names = one_hot_encoder.get_feature_names_out(variables)
one_hot_encoded_df = pd.DataFrame(one_hot_encoded_dense, columns=one_hot_encoded_names)
df = pd.concat([df, one_hot_encoded_df], axis=1)
df = df.drop(variables, axis=1)

# Selección de características
c = ['Mins', 'Goals', 'Assists', 'Yel', 'Red', 'SpG', 'PS%', 'AerialsWon', 'MotM', 'Tackles', 'Inter',
     'Fouls', 'Offsides', 'Clear', 'DeffDrb', 'Blocks', 'OwnG', 'KeyP', 'OffDrb', 'Fouled', 'Off',
     'Disp', 'UnsTch', 'AvgP', 'Crosses', 'LongB', 'ThrB', 'age', 'height', 'Año_natural', 'Titularidades',
     'Suplencias', 'Equipo_pos', '1_año_anterior', '2_año_anterior', '3_año_anterior', '4_año_anterior',
     '5_año_anterior', 'Equipo_Athletic Bilbao', 'Equipo_Atlético de Madrid', 'Equipo_CA Osasuna',
     'Equipo_CD Leganés', 'Equipo_Celta de Vigo', 'Equipo_Cádiz CF', 'Equipo_Deportivo Alavés',
     'Equipo_Elche CF', 'Equipo_FC Barcelona', 'Equipo_Getafe CF', 'Equipo_Girona FC', 'Equipo_Granada CF',
     'Equipo_Levante UD', 'Equipo_RCD Espanyol Barcelona', 'Equipo_RCD Mallorca', 'Equipo_Rayo Vallecano',
     'Equipo_Real Betis Balompié', 'Equipo_Real Madrid', 'Equipo_Real Sociedad', 'Equipo_Real Valladolid CF',
     'Equipo_SD Eibar', 'Equipo_SD Huesca', 'Equipo_Sevilla FC', 'Equipo_UD Almería', 'Equipo_Valencia CF',
     'Equipo_Villarreal CF', 'position_Attacking Midfield', 'position_Central Midfield', 'position_Centre-Back',
     'position_Centre-Forward', 'position_Defensive Midfield', 'position_Goalkeeper', 'position_Left Midfield',
     'position_Left Winger', 'position_Left-Back', 'position_Right Winger', 'position_Right-Back',
     'position_Second Striker', 'nationality_Albania', 'nationality_Algeria', 'nationality_Angola',
     'nationality_Argentina', 'nationality_Armenia', 'nationality_Australia', 'nationality_Austria',
     'nationality_Belgium', 'nationality_Bosnia-Herzegovina', 'nationality_Brazil', 'nationality_Cameroon',
     'nationality_Canada', 'nationality_Cape Verde', 'nationality_Central African Republic', 'nationality_Chile',
     'nationality_Colombia', 'nationality_Costa Rica', 'nationality_Cote d\'Ivoire', 'nationality_Croatia',
     'nationality_Czech Republic', 'nationality_DR Congo', 'nationality_Denmark', 'nationality_Dominican Republic',
     'nationality_Ecuador', 'nationality_England', 'nationality_Equatorial Guinea', 'nationality_France',
     'nationality_Gabon', 'nationality_Georgia', 'nationality_Germany', 'nationality_Ghana', 'nationality_Greece',
     'nationality_Guadeloupe', 'nationality_Guinea', 'nationality_Guinea-Bissau', 'nationality_Ireland',
     'nationality_Israel', 'nationality_Italy', 'nationality_Japan', 'nationality_Kosovo', 'nationality_Mali',
     'nationality_Martinique', 'nationality_Mauritania', 'nationality_Mexico', 'nationality_Montenegro',
     'nationality_Morocco', 'nationality_Netherlands', 'nationality_Nigeria', 'nationality_North Macedonia',
     'nationality_Norway', 'nationality_Paraguay', 'nationality_Peru', 'nationality_Poland', 'nationality_Portugal',
     'nationality_Romania', 'nationality_Russia', 'nationality_Scotland', 'nationality_Senegal', 'nationality_Serbia',
     'nationality_Slovakia', 'nationality_Slovenia', 'nationality_Spain', 'nationality_Sweden',
     'nationality_Switzerland',
     'nationality_The Gambia', 'nationality_Türkiye', 'nationality_Ukraine', 'nationality_United States',
     'nationality_Uruguay', 'nationality_Venezuela', 'nationality_Wales', 'nationality_Zambia', 'nationality_Zimbabwe',
     'marketValue']

datos = df[c]
datos = datos.reset_index()
datos = datos.drop('index', axis=1)
X = datos.iloc[:, :-1]
Y = datos.iloc[:, -1]

# Partición de datos
RANDOM_STATE = 83
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=RANDOM_STATE)

# Definición del modelo
param_grid = {
    'max_depth': range(1, 18),
    'min_samples_split': range(2, 18),
    'min_samples_leaf': range(1, 18),
    'max_features': ['auto', 'sqrt', 'log2'],
    'criterion': ['absolute_error', 'poisson', 'squared_error', 'friedman_mse'],
    'splitter': ['best', 'random']
}

clf = DecisionTreeRegressor(random_state=RANDOM_STATE)
grid_search = GridSearchCV(clf, param_grid, cv=10, scoring='neg_mean_absolute_error')

# Registro de parámetros y métricas en MLflow
with mlflow.start_run():
    mlflow.log_params({"random_state": RANDOM_STATE})
    mlflow.log_params({"n_samples": len(X_train)})

    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    best_score = -grid_search.best_score_
    mlflow.log_params(best_params)
    mlflow.log_metric("mean_absolute_error", best_score)

    print("Mejores parámetros encontrados:")
    print(best_params)
    print("Mejor puntuación de error absoluto medio negativo:")
    print(best_score)

    # Guardar el dataset
    mlflow.log_artifact(r"C:\Users\Usuario\Downloads\Datos_la_liga_preparados_entrenamiento.parquet", "dataset")

    # Guardar el modelo
    model_path = "decision_tree_model"
    mlflow.sklearn.save_model(grid_search.best_estimator_, model_path)

    # Registro del modelo en MLflow
    mlflow.sklearn.log_model(grid_search.best_estimator_, model_path)

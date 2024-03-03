import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv(r"C:\Users\Usuario\Documents\Alvaro\Carrera\2-Segundo\Segundo Cuatrimestre\Proyecto de Datos 1\proyecto\src\02limpieza\Datos finales LaLiga.csv",)
# Visualizar las primeras filas del DataFrame
print(df.head())

# Seleccionar solo columnas numéricas
numeric_cols = df.select_dtypes(include=[np.number])
# Análisis Descriptivo
descriptive_stats = df.describe()
display(descriptive_stats)

# Visualización de la Distribución y Boxplot para cada variable
for col in numeric_cols.columns:
    plt.figure(figsize=(6, 4))
    
    # Histograma
    plt.subplot(1, 2, 1)
    sns.histplot(df[col], kde=True)
    plt.title(f'Distribución de {col}')
    
    # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot de {col}')
    
    plt.tight_layout()
    plt.show()

# Matriz de Correlación (Heatmap) mejorado
plt.figure(figsize=(16, 12))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title('Matriz de Correlación')
plt.show()

# Normalidad (QQ Plot) para cada variable
for col in numeric_cols.columns:
    sm.qqplot(df[col], line='s')
    plt.title(f'QQ Plot de {col}')
    plt.show()






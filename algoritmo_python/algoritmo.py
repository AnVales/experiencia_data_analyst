# analizamos las compras
# A producto 1
# B producto 2
# A B comprados juntos

# soporte: probabilidad de que se compren ambos con las compras que tenemos
# soporte = P(A y B) = P(A ∩ B)

# soporte = P(A) 
# soporte del antecedente para fomentar los menos vistos

# confianza= probabilidad de que un cliente agrege B una vez que ya ha agregado A
# confianza = P(B|A) = P(A∩B) / P(A)

# lift = cuantificar cuantas veces es superior la probabilidad de ambos juntos sobre 
# la compra de cada uno de manera independiente
# Lift = P(A∩B) / P(A) * P(B)
# Lift = 1, sucesos independientes
# Lift > 1, más esperable que por azar, tienen relación

import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite
conexion = sqlite3.connect(r"C:\Users\yayau\Downloads\data_science_4_bus\analisis_insights_sql\sanoyfresco.db")

# Cargar una tabla completa en un DataFrame
df = pd.read_sql_query("SELECT * FROM tickets", conexion)

# Mostrar los primeros registros del DataFrame
print(df)

# Cerrar la conexión a la base de datos
conexion.close()

# resumen de datos, columnas, tipo de datos
df.info()

# nos detecta la fecha como texto
df['fecha'] = pd.to_datetime(df['fecha'])

# no necesitamos todo, hacemos un mini dataframe con los datos de interés
df_cesta = df[['id_pedido','nombre_producto']]
print(df_cesta)

# Agrupar los productos por id_pedido
df_agrupado = df_cesta.groupby('id_pedido')['nombre_producto'].apply(lambda producto: ','.join(producto))
print(df_agrupado)

# Aplicar pd.get_dummies() para transformar los productos en columnas con 0/1
df_transacciones = df_agrupado.str.get_dummies(sep=',')
print(df_transacciones)

# Soporte para cada producto
# soporte del antecendente, prob indv de comprar cada producto
soporte = df_transacciones.mean(axis=0) * 100
# con esto miramos las compras de cada producto
print(soporte.sort_values(ascending=False))

# Función para calcular la confianza entre dos productos en la muestra
def confianza(antecedente, consecuente):
    # Casos donde se compraron ambos productos
    conjunto_ac = df_transacciones[(df_transacciones[antecedente] == 1) &
                                   (df_transacciones[consecuente] == 1)]
    # Confianza = compras conjuntas / compras de producto A
    return len(conjunto_ac) / df_transacciones[antecedente].sum()

# Función para calcular el lift entre dos productos en la muestra
def lift(antecedente, consecuente):
    soporte_a = df_transacciones[antecedente].mean()
    soporte_c = df_transacciones[consecuente].mean()
    conteo_ac = len(df_transacciones[(df_transacciones[antecedente] == 1) &
                                   (df_transacciones[consecuente] == 1)])
    soporte_ac = conteo_ac / len(df_transacciones)
    return soporte_ac / (soporte_a * soporte_c)

from itertools import combinations

# Definir un umbral para la confianza mínima
umbral_confianza = 0.05
asociaciones = []

# Generar combinaciones de productos y calcular confianza y lift
for antecedente, consecuente in combinations(df_transacciones.columns, 2):

    # Soporte del antecedente
    soporte_a = df_transacciones[antecedente].mean()

    # Calcular confianza
    conf = confianza(antecedente, consecuente)
    if conf > umbral_confianza:
        asociaciones.append({
            'antecedente': antecedente,
            'consecuente': consecuente,
            'soporte_a': round(soporte_a * 100,1),
            'confianza': round(conf * 100,1),
            'lift': round(lift(antecedente, consecuente),1)
        })


# Convertir las asociaciones en un DataFrame
df_asociaciones = pd.DataFrame(asociaciones)

# Ordenar las asociaciones por confianza de mayor a menor
df_asociaciones.sort_values(by='lift', ascending=False, inplace=True)

print(df_asociaciones)
from pymongo import MongoClient


def valores_años_anteriores(row, db):
    iden = str(row.name)  # Obtiene el valor del índice
    anio = row['Año_natural']

    años = [int(anio - 1), int(anio - 2), int(anio - 3), int(anio - 4), int(anio - 5)]

    for p, año in enumerate(años):
        meses = ['Jun', 'Jul', 'Aug', 'May', 'Apr', 'Mar', 'Oct', 'Feb', 'Nov', 'Jan', 'Dec']
        encontrado = False
        i = 0

        while not encontrado and i < len(meses):
            s = meses[i] + r'\s\d{1,2},\s' + str(año)

            resultados = db.Futbolistas.find(
                {
                    'id': iden,
                    'marketValueHistory.date': {'$regex': s}
                },
                {'marketValueHistory.$': 1, '_id': 0}
            )
            for resultado in resultados:
                try:
                    valor = resultado['marketValueHistory'][0]['value']
                    if p == 1:
                        row['1_año_anterior'] = valor
                    elif p == 2:
                        row['2_año_anterior'] = valor
                    elif p == 3:
                        row['3_año_anterior'] = valor
                    elif p == 4:
                        row['4_año_anterior'] = valor
                    else:
                        row['5_año_anterior'] = valor
                    encontrado = True

                except Exception as e:

                    if p == 1:
                        row['1_año_anterior'] = '€0.0k'
                    elif p == 2:
                        row['2_año_anterior'] = '€0.0k'
                    elif p == 3:
                        row['3_año_anterior'] = '€0.0k'
                    elif p == 4:
                        row['4_año_anterior'] = '€0.0k'
                    else:
                        row['5_año_anterior'] = '€0.0k'

                    encontrado = True

            i += 1
            if (i == len(meses) and not encontrado):
                if p == 1:
                    row['1_año_anterior'] = '€0.0k'
                elif p == 2:
                    row['2_año_anterior'] = '€0.0k'
                elif p == 3:
                    row['3_año_anterior'] = '€0.0k'
                elif p == 4:
                    row['4_año_anterior'] = '€0.0k'
                else:
                    row['5_año_anterior'] = '€0.0k'
    return row

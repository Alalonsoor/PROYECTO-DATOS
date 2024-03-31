from pymongo import MongoClient

def eliminar_valores_duplicados(db):
    ids_duplicados = db.Futbolistas.aggregate([
        {
            '$group': {
                '_id': '$id',
                'ids_duplicados': {'$addToSet': '$_id'},
                'total': {'$sum': 1}
            }
        },
        {
            '$match': {
                'total': {'$gt': 1}
            }
        }
    ])

    # Eliminar los documentos duplicados
    for id_duplicado in ids_duplicados:
        documentos_duplicados = id_duplicado['ids_duplicados'][1:]
        db.Futbolistas.delete_many({'_id': {'$in': documentos_duplicados}})

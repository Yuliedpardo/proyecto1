from fastapi import FastAPI
import pandas as pd
 
app = FastAPI()

@app.get('/')
def hola():
    return {'Bienvenidos a mi api'}

consulta1= pd.read_csv(r"consulta1.csv", low_memory=False)
# Lee el archivo Parquet en un DataFrame de pandas
Modelo = pd.read_parquet(r'Modelo.parquet')

@app.get('/userdata/{user_id}')
def userdata(user_id):
    # Filtrar el DataFrame user_total por el user_id especificado
    user_data = consulta1[consulta1['user_id'] == user_id]

    # Obtener la cantidad de dinero gastado por el usuario
    money_spent = user_data['price'].values[0]

    # Obtener el porcentaje de recomendación
    recommend_percentage = user_data['porcentaje'].values[0]

    # Obtener la cantidad de items del usuario
    items_count = user_data['items_count'].values[0]

    return money_spent, recommend_percentage, items_count

@app.get("/recomendacion_juego/{id_producto}")
def recomendacion_juego(id_producto: int):
    recomendaciones = Modelo[Modelo['id'] == id_producto]['recomendaciones'].iloc[0]
    
    # Verificar si la lista de recomendaciones no está vacía
    if len(recomendaciones) > 0:
        recomendaciones_dict = {i + 1: juego for i, juego in enumerate(recomendaciones)}
        return recomendaciones_dict
    else:
        # Si no se encontraron recomendaciones para el ID, devolver un mensaje de error
        error_data = {'error': 'No se encontraron recomendaciones para el ID proporcionado'}
        return JSONResponse(content=error_data, status_code=404)
    
# @app.get('/userdata/{user_id}')
# def userdata(user_id):
#     # leer archivos csv 
#     #leemos el documento guardado en csv
#     outputsin= pd.read_csv(r"outputsin.csv", low_memory=False)
#     #leemos el documento guardado en csv
#     review_desanidado= pd.read_csv(r"review_desanidado.csv")
#     #leemos el documento guardado en csv
#     output_desanidado= pd.read_csv(r"output_desanidado.csv")
#     #leemos el documento guardado en csv
#     items_desanidadas= pd.read_csv(r"items_desanidadas.csv")
#     #leemos el documento guardado en csv
#     # Calcular la cantidad de dinero gastado por el usuario
#     user_purchases = output_desanidado[output_desanidado['user_id'] == user_id]['price'].sum()

#     # Calcular el porcentaje de recomendación basado en las reviews
#     user_reviews = review_desanidado[review_desanidado['user_id'] == user_id]
#     recommend_count = user_reviews['recommend'].sum()
#     total_reviews = len(user_reviews)
#     recommendation_percentage = (recommend_count / total_reviews) * 100 if total_reviews > 0 else 0

#     # Obtener la cantidad de items que el usuario posee (sin necesidad de suma)
#     user_items_count = items_desanidadas.loc[items_desanidadas['user_id'] == user_id, 'items_count'].values[0]

#     return {
#         'money_spent': user_purchases,
#         'recommendation_percentage': recommendation_percentage,
#         'item_count': user_items_count
#     }

# # Llamada a la función para un user_id específico
# user_id_to_check = '--000--'  # Cambiar al valor que desees verificar
# user_data = userdata(user_id_to_check)
# print(user_data)

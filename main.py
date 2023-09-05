from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

@app.get('/')
def hola():
    return {'Bienvenidos a mi api'}

consulta1= pd.read_csv(r"consulta1.csv", low_memory=False)
# Lee el archivo Parquet en un DataFrame de pandas
Modelo = pd.read_parquet(r'Modelo.parquet')
consulta2= pd.read_csv(r"consulta2.csv", low_memory=False)
consulta5= pd.read_csv(r"consulta5.csv", low_memory=False)

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
    
    # @app.get("/countreview/{start_date: str, end_date: str}")
    # def countreviews(start_date: str, end_date: str):
    # # Convertir la columna 'porcentaje' a números flotantes, ignorando los valores no válidos
    # consulta2['porcentaje'] = pd.to_numeric(consulta2['porcentaje'], errors='coerce')

    # # Filtrar el DataFrame para obtener las reseñas dentro del rango de fechas
    # filtered_df = consulta2[(consulta2['posted'] >= start_date) & (consulta2['posted'] <= end_date)]

    # # Calcular la cantidad de usuarios que realizaron reseñas en ese período
    # users_count = len(filtered_df['user_id'].unique())

    # # Calcular el porcentaje de recomendación promedio en base a las reseñas
    # recommendation_percentage = filtered_df['porcentaje'].mean()

    # result = {
    #     "Cantidad de usuarios que realizaron reseñas": users_count,
    #     "Porcentaje de recomendación promedio": recommendation_percentage
    # }   
    # # Serializar el resultado como JSON con comillas dobles
    # return json.dumps(result)
    # except Exception as e:
    # return {"error": str(e)}

@app.get("/countreview/{start_date: str}/{end_date: str}")
def countreviews(start_date: str, end_date: str):
    try:
        # Convertir la columna 'porcentaje' a números flotantes, ignorando los valores no válidos
        consulta2['porcentaje'] = pd.to_numeric(consulta2['porcentaje'], errors='coerce')
        
        # Filtrar el DataFrame para obtener las reseñas dentro del rango de fechas
        filtered_df = consulta2[(consulta2['posted'] >= start_date) & (consulta2['posted'] <= end_date)]
        
        # Calcular la cantidad de usuarios que realizaron reseñas en ese período
        users_count = len(filtered_df['user_id'].unique())
        
        # Calcular el porcentaje de recomendación promedio en base a las reseñas
        recommendation_percentage = filtered_df['porcentaje'].mean()
        
        # Crear un diccionario con los resultados
        result = {
            "Cantidad de usuarios que realizaron reseñas": users_count,
            "Porcentaje de recomendación promedio": recommendation_percentage
        }
        
        # Serializar el resultado como JSON con comillas dobles
        # return json.dumps(result)
        return result
    except Exception as e:
        return {"error": str(e)}

from fastapi.responses import JSONResponse

@app.get('/developer/{year}')
def developer(year):
    try:
        # Paso 1: Filtrar las filas para el año especificado
        filtered_output = consulta5[consulta5['release_year'] == year]

        # Paso 2: Agrupar por desarrollador y calcular la cantidad total de ítems para cada uno
        developer_items_count = filtered_output.groupby('developer')['item_id'].count().reset_index()

        # Paso 3: Calcular la cantidad de ítems con precio igual a 0 (contenido gratuito) por desarrollador
        developer_free_items_count = filtered_output[filtered_output['price'] == 0].groupby('developer')['item_id'].count().reset_index()

        # Paso 4: Fusionar los DataFrames para tener la información completa
        developer_info = pd.merge(developer_items_count, developer_free_items_count, on='developer', how='left')

        # Paso 5: Calcular el porcentaje de contenido gratuito y reemplazar los NaN con 0%
        developer_info['Contenido Free'] = (developer_info['item_id_y'] / developer_info['item_id_x'] * 100).fillna(0).astype(int).astype(str) + '%'

        # Paso 6: Renombrar las columnas para obtener el formato de salida deseado
        developer_info.rename(columns={'developer': 'Empresa Desarrolladora', 'item_id_x': 'Cantidad de Ítems', 'item_id_y': 'Contenido Free'}, inplace=True)

        # Crear un diccionario con los resultados
        result = {
            "Año": year,
            "Información de Desarrolladores": developer_info.to_dict(orient='records')
        }
        return result
        # Devolver el resultado en formato JSON usando JSONResponse
        # return JSONResponse(content=result, status_code=200)
       
    except Exception as e:
        # Si ocurre una excepción, devolver un mensaje de error en formato JSON con código de estado 500 (Error interno del servidor)
        error_data = {'error': str(e)}
        return JSONResponse(content=error_data, status_code=500)

    
# @app.get('/developer/{year}')
# def developer(year):
#     # Paso 1: Filtrar las filas para el año especificado
#     filtered_output = consulta5[consulta5['release_year'] == year]

#     # Paso 2: Agrupar por desarrollador y calcular la cantidad total de ítems para cada uno
#     developer_items_count = filtered_output.groupby('developer')['item_id'].count().reset_index()

#     # Paso 3: Calcular la cantidad de ítems con precio igual a 0 (contenido gratuito) por desarrollador
#     developer_free_items_count = filtered_output[filtered_output['price'] == 0].groupby('developer')['item_id'].count().reset_index()

#     # Paso 4: Fusionar los DataFrames para tener la información completa
#     developer_info = pd.merge(developer_items_count, developer_free_items_count, on='developer', how='left')

#     # Paso 5: Calcular el porcentaje de contenido gratuito y reemplazar los NaN con 0%
#     developer_info['Contenido Free'] = (developer_info['item_id_y'] / developer_info['item_id_x'] * 100).fillna(0).astype(int).astype(str) + '%'

#     # Paso 6: Renombrar las columnas para obtener el formato de salida deseado
#     developer_info.rename(columns={'developer': 'Empresa Desarrolladora', 'item_id_x': 'Cantidad de Ítems', 'item_id_y': 'Contenido Free'}, inplace=True)

#     return year, developer_info
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

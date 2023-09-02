from fastapi import FastAPI
import pandas as pd
 
app = FastAPI()

@app.get('/')
def hola():
    return {'Bienvenidos a mi api'}

@app.get('/userdata/{user_id}')
def userdata(user_id):
    # leer archivos csv 
    #leemos el documento guardado en csv
    outputsin= pd.read_csv(r"outputsin.csv", low_memory=False)
    #leemos el documento guardado en csv
    review_desanidado= pd.read_csv(r"review_desanidado.csv")
    #leemos el documento guardado en csv
    output_desanidado= pd.read_csv(r"output_desanidado.csv")
    #leemos el documento guardado en csv
    items_desanidadas= pd.read_csv(r"items_desanidadas.csv")
    #leemos el documento guardado en csv
    # Calcular la cantidad de dinero gastado por el usuario
    user_purchases = output_desanidado[output_desanidado['user_id'] == user_id]['price'].sum()

    # Calcular el porcentaje de recomendación basado en las reviews
    user_reviews = review_desanidado[review_desanidado['user_id'] == user_id]
    recommend_count = user_reviews['recommend'].sum()
    total_reviews = len(user_reviews)
    recommendation_percentage = (recommend_count / total_reviews) * 100 if total_reviews > 0 else 0

    # Obtener la cantidad de items que el usuario posee (sin necesidad de suma)
    user_items_count = items_desanidadas.loc[items_desanidadas['user_id'] == user_id, 'items_count'].values[0]

    return {
        'money_spent': user_purchases,
        'recommendation_percentage': recommendation_percentage,
        'item_count': user_items_count
    }

# Llamada a la función para un user_id específico
user_id_to_check = '--000--'  # Cambiar al valor que desees verificar
user_data = userdata(user_id_to_check)
print(user_data)

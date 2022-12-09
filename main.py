from fastapi import File, UploadFile, FastAPI
import pandas as pd
import uvicorn
from starlette.responses import RedirectResponse
#Creación de una aplicación FasAPI
app = FastAPI(title='Consultas de películas en las plataformas: Amazón, Disney, Hulu y Netflix')

@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs/")

if __name__== '__main__':
     uvicorn.run("main:app", port=8000, reload=True, access_log=False)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "Hubo un error al subir el archivo"}
    finally:
        file.file.close()

    return {"message": f"El archivo cargo con éxito {file.filename}"}


# vamos a escribir las funciones para las consultas deseadas.

# 1) Máxima duración según tipo de film (película/serie), por plataforma y por año: 
# El request debe ser: get_max_duration(año, plataforma, [min o season])

movies_df=pd.read_csv('movies_titles.csv')

@app.get("/max_duration")
async def get_max_duration(Año: int, Plataforma: str , Min_or_Season: str):
  
    resultado=movies_df[(movies_df.Año_lanzamiento == Año) & (movies_df.Plataforma == Plataforma) & (movies_df.unidad_tiempo== Min_or_Season)].Duracion.max()
    resultado
    return {"Para el año": f"{Año}, la máxima duración de la película/serie por la plataforma {Plataforma} es de {resultado}, {Min_or_Season}"}


# 2) Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)

@app.get("/count_plataform")
async def get_count_plataform( Plataforma: str):
    resutado_2=movies_df[(movies_df.Plataforma == Plataforma)].Tipo.value_counts()
    return {"La cantidad de peliculas y series para la plataforma": f"{Plataforma} es de {resutado_2['Movie']} películas y {resutado_2['Tv Show']} series." }


# 3) Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
# Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.

@app.get("/Frequency_by_plataform")
async def get_listedin(genero : str):
    #separamos los generos en un df
    lista_df=movies_df['Listada_en'].str.split(',', n=4, expand=True)

    #creamos una funcion para buscar la frecuencia
    def frecuencia (lista):
        frecuenciadicc = dict()
        repetidos = set()
        for element in lista:
            if element in repetidos:
                frecuenciadicc[element] = frecuenciadicc[element] + 1
            else:
                frecuenciadicc[element] = 1
                repetidos.add(element)
        return frecuenciadicc


    dic_1=frecuencia(lista_df[0])
    dic_2=frecuencia (lista_df[1])
    dic_3=frecuencia (lista_df[2])
    dic_4=frecuencia (lista_df[3])
    dic_5=frecuencia (lista_df[4])

    dic_6 = {i: dic_1.get(i, 0) + dic_2.get(i, 0)
	for i in set(dic_1).union(dic_2)}

    dic_7 = {i: dic_6.get(i, 0) + dic_3.get(i, 0)
        for i in set(dic_6).union(dic_3)}

    dic_8 = {i: dic_7.get(i, 0) + dic_4.get(i, 0)
        for i in set(dic_7).union(dic_4)}

    dic_9 = {i: dic_8.get(i, 0) + dic_5.get(i, 0)
        for i in set(dic_8).union(dic_5)}

    lista_values =dic_9.values()
    lista_keys =dic_9.keys()
    lista_values=list(lista_values)
    lista_keys=list(lista_keys)

    #creamos un df con las dos listas
    df_genero =pd.DataFrame({'Genero':lista_keys, 
                            'Frecuencia': lista_values})

    # borramos los null
    df_genero=df_genero.drop(150)
    
    resultado3=int(df_genero[(df_genero.Genero== genero)].Frecuencia)

    return {"El número de veces que se repite el genero" : f"{genero} es de {resultado3} veces"}


# 4) funcion
# Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

@app.get("/get_actor")
async def get_actor(plataforma: str, año: int):
    pass
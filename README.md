# Predicción del Valor de Mercado de Jugadores de LaLiga

## Descripción del proyecto

## Objetivo

El propósito de este proyecto es realizar predicciones sobre el valor de mercado de los futbolistas de La Liga (liga española) al final de la temporada 22-23. 

## Fuentes de datos
El modelo se entrena utilizando estadísticas de los jugadores de las últimas 4 temporadas. La fuente de datos proviene de Transfermarkt y de  [WhoScored](https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/PlayerStatistics/Spain-LaLiga-2023-2024).

### TransferMarket

Esta fuente de datos nos aportará información acerca del valor de mercado que queremos predecir, e información sobre el precio del jugador en los últimos años. Se hará a través de la API de TransferMarket, hay información en el siguiente [enlace](https://github.com/felipeall/transfermarkt-api?tab=readme-ov-file), que muestra la instalación de la API, en cuanto a la interfaz de la misma, tendrá la siguiente pinta:

  **De forma general tenemos los siguientes apartados:**

  ![image](https://github.com/Alalonsoor/PROYECTO-DATOS/assets/127221222/b91c653c-3fb7-4b63-a96d-f77e2d29f401)

  **Dentro de cada apartado:**

  ![image](https://github.com/Alalonsoor/PROYECTO-DATOS/assets/127221222/1443f536-fbbd-44bb-99f7-2401d8d884e3)

  **En nuestro caso:**
  Sacaremos primero según el id del equipo los equipos, y dentro de los equipos sacaremos a cada jugador, para obtener todos los jugadores.

  ![image](https://github.com/Alalonsoor/PROYECTO-DATOS/assets/127221222/4f3178c5-131c-4b74-9967-29fa25ceb5ae)

  Una vez tenemos todos los jugadores, sacaremos el valor de mercado con el siguiente apartado:

  ![image](https://github.com/Alalonsoor/PROYECTO-DATOS/assets/127221222/937fd441-90c5-4f2a-9cd9-dc09e2b00870)

  Todo este proceso se encuentra en el siguiente [enlace](https://github.com/Alalonsoor/PROYECTO-DATOS/tree/main/src/01adquisicion/modulos_adq/TRANSFERMARKET%20API).


### WhoScored

Este apartado, lo sacaremos a través de la técnica de webScrapping, del que sacaremos todos los datos de las estadísticas de los jugadores para posteriormente hacer el análisis:

Lo primero es inicializar el navegador, una vez inicializado, en caso de la presencia de un aviso para aceptar las cookies, tenemos una función que las acepta nada más iniciar la web, haciendo click en el botón correspondiente. 

Una vez pasadas las cookies leemos la cabecera de la tabla del primer año seleccionado.

Tenemos un bucle encargado de tomar todas las celdas de cada página de la tabla, a partir de aquí solo queda avanzar página por página de la tabla sacando sus datos hasta la última. 

Todo esto dentro de dos bucles: uno que se encarga de sacar todas las tablas pertinentes al año actual (Summary, Deffensive, Offensive y Passing), y uno que recorre todos los años de los que queremos sacar la información.


## Entrenamiento de los modelos

Para la predicción de los datos, procederemos a entrenar los modelos según varias técnicas, ajustando lo mejor posible tanto los hiperparámetros como la selección de variables según sea necesario:

1. Regresión Lineal
2. Árboles
3. Redes Neuronales

Hay hecho un profundo análisis para elegir la mejor combinación de los datos, todo junto, separado en posiciones o separado entre años.

#### Evaluación de Modelos

Las pruebas realizadas con cada modelo se guardarán en MLFlow, teniendo registrados los diferentes modelos a utilizar, y para cada uno de ellos las pruebas realizadas. Estas pruebas se guardará en una base de datos de SQLite.

El servidor se levantará con el siguiente comando: mlflow ui --port 5000 --backend-store-uri sqlite:///mlruns.db. 

A partir de aquí, abriendo la siguiente URL: http://127.0.0.1:5000, se podrá acceder a las pruebas realizadas.

## Estructura del Proyecto

- **`src/`**: Contiene el código fuente del proyecto.
  - **`adquisicion/`**: Módulo para la adquisición de datos.
  - **`limpieza/`**: Módulo para la limpieza y preprocesamiento de datos.
  - **`exploracion/`**: Módulo para la exploración de datos.
  - **`entrenamiento/`**: Módulo con las pruebas realizadas para entrenar cada modelo.
- **`.gitignore`**: Especifica los archivos y directorios que Git debe ignorar.
- **`requirements.txt`**: Lista las librerías con sus versiones

## Colaboradores

- [Álvaro Alonso Ortega](https://github.com/Alalonsoor)
- [Óscar Marin Esteban](https://github.com/Oscmarin715)
- [Carlos Mantilla Mateos](https://github.com/c123qw)

# **Descarga del proyecto** 
 Para clonar el proyecto actual, deberás utilizar el siguiente [enlace](https://github.com/Alalonsoor/PROYECTO-DATOS).

# **Instrucciones de trabajo**

  #### Proyectos
  En la sección de [proyectos](https://github.com/users/Alalonsoor/projects/5), se encontrará el trabajo general que hay que hacer.
  #### Issues
  En el apartado de [issues](https://github.com/Alalonsoor/PROYECTO-DATOS/issues), se publicará un poco más el día a día 
  del proyecto, problemas que se vayan teniendo, o pequeñas tareas que se vayan haciendo para completar un apartado de la sección proyectos.

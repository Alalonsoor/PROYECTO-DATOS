# PROYECTO-DATOS
Nuestro proyecto de datos 


Instrucciones para usar la API de TransferMarket

En esta url se pudee ver la informacion de la api https://transfermarkt-api.vercel.app/docs#/

  # Clone the repository
  $ git clone https://github.com/felipeall/transfermarkt-api.git
  
  # Go to the project's root folder
  $ cd transfermarkt-api
  
  # Instantiate a Poetry virtual env
  $ poetry shell
  
  # Install the dependencies
  $ poetry install --no-root

  set PYTHONPATH=%PYTHONPATH%;%cd%

  # Start the API server
  python app/main.py

# Access the API local page
  open http://localhost:8000/

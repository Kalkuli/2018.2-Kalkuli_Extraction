[![Build Status](https://travis-ci.org/Kalkuli/2018.2-Kalkuli_Interpretation.svg?branch=master
)](https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Interpretation)

# 2018.2-Kalkuli_Extraction
Microsserviço para a extração de texto de notas fiscais escaneadas.

## Instalação

    sudo docker-compose -f docker-compose-dev.yml build
  
## Uso
    sudo docker-compose -f docker-compose-dev.yml up
    
As rotas estarão disponíveis através de localhost:5001

## Testes

    ```docker-compose -f docker-compose-dev.yml run base python3.6 manage.py test```

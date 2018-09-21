[![Build Status](https://travis-ci.org/Kalkuli/2018.2-Kalkuli_Interpretation.svg?branch=master
)](https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Interpretation)

# 2018.2-Kalkuli_Extraction
Microsserviço para a extração de texto de notas fiscais escaneadas.

## Instalação

    sudo docker-compose -f docker-compose-dev.yml build
  
## Uso
    sudo docker-compose -f docker-compose-dev.yml up
    
As rotas estarão disponíveis através de localhost:5001

## Testando

Para rodar os testes utilize o comando:

```docker-compose -f docker-compose-dev.yml run base python3.6 manage.py test```

E para saber a cobertura dos testes utilize:

```docker-compose -f docker-compose-dev.yml run base python3.6 manage.py cov```

Para acessar a visualização do HTML coverage no browser, acesse a pasta htmlcov e abra o arquivo index.html no navegador, ou utilize o comando:

```google-chrome ./htmlcov/index.html```

# Serviço de Extração de Texto de Notas Fiscais  

<div style="text-align: center"> 

<a href="https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Extraction"><img src="https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Extraction.svg?branch=master" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Extraction/test_coverage"><img src="https://api.codeclimate.com/v1/badges/6a9fd127ec7d6c8f6a1e/test_coverage" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Extraction/maintainability"><img src="https://api.codeclimate.com/v1/badges/6a9fd127ec7d6c8f6a1e/maintainability" /></a>
<a href="https://opensource.org/licenses/GPL-3.0"><img src="https://img.shields.io/badge/license-GPL-%235DA8C1.svg"/></a>

</div> 


# Configurando o ambiente
Para instruções de como instalar o _Docker_ e o _Docker-compose_ clique [aqui](https://github.com/Kalkuli/2018.2-Kalkuli_Front-End/blob/master/README.md). 


## Colocando no ar
Com o _Docker_ e _Docker-Compose_ instalados, basta apenas utilizar os comandos:

```
docker-compose -f docker-compose-dev.yml build
```

e

```
docker-compose -f docker-compose-dev.yml up
```
    

As rotas estarão disponíveis através de [localhost:5001](http://localhost:5001/).

## Testando

Para rodar os testes utilize o comando:

```
docker-compose -f docker-compose-dev.yml run base python3.6 manage.py test
```

E para saber a cobertura dos testes utilize:

```
docker-compose -f docker-compose-dev.yml run base python3.6 manage.py cov
```

Para acessar a visualização do _HTML coverage_ no _browser_, acesse a pasta htmlcov e abra o arquivo index.html no navegador, ou utilize o comando:

```
google-chrome ./htmlcov/index.html
```
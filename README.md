# Desafio Técnico JusBrasil

Olá, pessoal da JusBrasil!! Para fazer a parte do scraping desse projeto utilizei o ```Playwright``` para navegar nas páginas e ```BeautifulSoup``` para extrair as informações. Além disso, utilizei o ```Flask``` para criação da API.

## Estrutura do Projeto

```bash
desafio_tecnico_jusBrasil/
│
├── src/
│   ├── API/
│   │   ├── __init__.py
│   │   ├── Routes/
│   │   │   ├── __init__.py
│   │   │   ├── process_routes.py
│   │
│   ├── Crawlers/
│   │   ├── __init__.py
│   │   ├── tjal_tjce_scraper.py
│   │   └── tjal_tjce_level2_scraper.py
│   └── run.py
│
├── tests/
│   ├── __init__.py
│   ├── test_process_routes.py
│
├── requirements.txt
└── .gitignore
└── README.md
```

## Configuração do Ambiente
### 1. Clone o Repositório
```git clone https://github.com/sstephanyy/desafio_tecnico_jusBrasil.git```

```cd desafio_tecnico_jusBrasil```

### 2. Crie um Ambiente Virtual
```python -m venv venv```

### 3. Ative o Ambiente Virtual
No Windows:
```venv\Scripts\activate```

No macOS/Linux:
```source venv/bin/activate```

### 4. Instale as Dependências
```pip install -r requirements.txt```

## Rodando os Projeto
### 1. Vá até a pasta src
```cd src```

### 2. Em seguida, digite o seguinte comando no terminal:
```python run.py ```

## Estrutura da Requisição
Endpoint da API: ```/api/processo```

Método HTTP: **GET**

### Corpo da Requisição (JSON):
```
{
  "process_number": "123456789",
  "tribunal_name": "TJAL"
}
```
-> **Atenção**: O número do processo precisa ser válido e o nome do tribunal só aceita "**TJAL**" ou "**TJCE**". 

## Rodando os Testes
### 1. Executar Todos os Testes
Para rodar todos os testes do projeto, use o comando:
```pytest```



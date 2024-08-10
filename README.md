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

### 5. Instalando o Playwright
Instale os navegadores necessários:

```playwright install```

## Rodando o Projeto
### 1. Primeiro, vá até a pasta src
```cd src```

### 2. Em seguida, digite o seguinte comando no terminal para iniciar seu servidor do Flask:
```python run.py ```

## Estrutura da Requisição
Endpoint da API: ```/api/processo```

Método HTTP: **GET**

### Corpo da Requisição (JSON):
Esse é o input esperado que o usuário coloque.
```
{
  "process_number": "0710802-55.2018.8.02.0001",
  "tribunal_name": "TJAL"
}
```
-> **Atenção**: O número do processo precisa ser válido e no nome do tribunal, só é aceito "**TJAL**" ou "**TJCE**". 

### Output esperado dos processos:
● classe

● área

● assunto

● data de distribuição

● juiz

● valor da ação

● partes do processo

● lista das movimentações (data e movimento)

## Rodando os Testes
### 1. Executar Todos os Testes
Para rodar todos os testes do projeto, use o comando:
```pytest```



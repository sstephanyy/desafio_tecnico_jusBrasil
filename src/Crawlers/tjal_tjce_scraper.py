from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class Tribunal(ABC):
    @abstractmethod
    def scrape(self, process_number):
        pass

    def extract_parts(self, soup):
        parts = {}
        possible_ids = ["tableTodasPartes", "tablePartesPrincipais"]
        
        table = None
        for table_id in possible_ids:
            table = soup.find("table", {"id": table_id})
            if table:
                break
        
        if not table:
            print("Nenhuma tabela de partes encontrada.")
            return parts
        
        rows = table.find_all("tr")
        for row in rows:
            label = row.find("span", {"class": "mensagemExibindo tipoDeParticipacao"})
            if label:
                role = label.text.strip().replace(" ", "").replace(":", "").lower()
                names_cell = row.find("td", class_="nomeParteEAdvogado")
                if names_cell:
                    names = names_cell.get_text(separator="\n").split("\n")
                    names = [name.strip() for name in names if name.strip()]
                    if role in parts:
                        parts[role].extend(names)
                    else:
                        parts[role] = names
        
        return parts


    def extract_movements(self, soup):
        movimentacoes = []
        table = soup.find("tbody", {"id": "tabelaTodasMovimentacoes"})
        if not table:
            return movimentacoes
        
        rows = table.find_all("tr", class_="containerMovimentacao")
        for row in rows:
            data = row.find("td", class_="dataMovimentacao").text.strip() if row.find("td", class_="dataMovimentacao") else "Data não encontrada"
            descricao = row.find("td", class_="descricaoMovimentacao").text.strip() if row.find("td", class_="descricaoMovimentacao") else "Descrição não encontrada"
            
            removing_spaces_descricao = ' '.join(descricao.split())
            movimentacoes.append({"data": data, "descricao": removing_spaces_descricao})

        return movimentacoes

class TJAL(Tribunal):
    def scrape(self, process_number):
        url = "https://www2.tjal.jus.br/cpopg/show.do"
        params = {"processo.numero": process_number}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar o TJAL: Status {response.status_code}")
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        data = {
            "classe": soup.find("span", {"id": "classeProcesso"}).text.strip() if soup.find("span", {"id": "classeProcesso"}) else "Classe não foi encontrada ou não existe",
            "area": soup.find("div", {"id": "areaProcesso"}).text.strip() if soup.find("div", {"id": "areaProcesso"}) else "Área não foi encontrada ou não existe",
            "assunto": soup.find("span", {"id": "assuntoProcesso"}).text.strip() if soup.find("span", {"id": "assuntoProcesso"}) else "Assunto não foi encontrado ou não existe",
            "data_distribuicao": soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}).text.split(" às ")[0] if soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}) else "Data de distribuição não foi encontrada ou não existe",
            "juiz": soup.find("span", {"id": "juizProcesso"}).text.strip() if soup.find("span", {"id": "juizProcesso"}) else "Juiz não foi encontrado ou não existe",
            "valor_acao": soup.find("div", {"id": "valorAcaoProcesso"}).text.strip() if soup.find("div", {"id": "valorAcaoProcesso"}) else "Valor da ação não foi encontrado ou não existe",
            "parte_do_processo": self.extract_parts(soup),
            "movimentacoes": self.extract_movements(soup)
        }
        return data

class TJCE(Tribunal):
    def scrape(self, process_number):
        url = f"https://esaj.tjce.jus.br/cpopg/show.do?processo.numero={process_number}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            content = page.content()
            browser.close()
        
        soup = BeautifulSoup(content, "html.parser")
        data = {
            "classe": soup.find("span", {"id": "classeProcesso"}).text.strip() if soup.find("span", {"id": "classeProcesso"}) else "Classe não foi encontrada ou não existe",
            "area": soup.find("div", {"id": "areaProcesso"}).find("span").text.strip() if soup.find("div", {"id": "areaProcesso"}) else "Área não foi encontrada ou não existe",
            "assunto": soup.find("span", {"id": "assuntoProcesso"}).text.strip() if soup.find("span", {"id": "assuntoProcesso"}) else "Assunto não foi encontrado ou não existe",
            "data_distribuicao": soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}).text.split(" às ")[0] if soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}) else "Data de distribuição não foi encontrada ou não existe",
            "juiz": soup.find("span", {"id": "juizProcesso"}).text.strip() if soup.find("span", {"id": "juizProcesso"}) else "Juiz não encontrado ou não existe",
            "valor_acao": soup.find("div", {"id": "valorAcaoProcesso"}).text.strip() if soup.find("div", {"id": "valorAcaoProcesso"}) else "Valor não encontrado ou não existe",
            "parte_do_processo": self.extract_parts(soup),
            "movimentacoes": self.extract_movements(soup)
        }
        return data

def get_process_data(process_number, tribunal_name):
    tribunals = {
        "TJAL": TJAL(),
        "TJCE": TJCE(),
    }
    
    if tribunal_name in tribunals:
        return tribunals[tribunal_name].scrape(process_number)
    else:
        raise ValueError("Nome do Tribunal não foi encontrado ou não existe!")

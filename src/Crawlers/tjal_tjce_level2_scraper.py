from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class TribunalGrau2(ABC):
    BASE_URL_SEARCH = None
    BASE_URL_PROCESS = None

    def format_num_processo(self, num_processo):
        partes = num_processo.split('.')
        if len(partes) > 2:
            return f"{partes[0]}-{partes[1]}.{partes[2]}"
        return num_processo

    def get_foro_numero_unificado(self, num_processo):
        return num_processo[-4:]

    @abstractmethod
    def get_urls(self):
        pass

    def navigate_and_get_soup(self, page, num_processo):
        formatted_num_processo = self.format_num_processo(num_processo)
        foro_numero_unificado = self.get_foro_numero_unificado(num_processo)

        page.type('input[name="numeroDigitoAnoUnificado"]', formatted_num_processo)
        page.wait_for_timeout(3000)
        page.type('input[name="foroNumeroUnificado"]', foro_numero_unificado)

        with page.expect_navigation(timeout=60000):
            page.click('input[type="submit"]#pbConsultar')

        return BeautifulSoup(page.content(), "html.parser")

    def extract_movements(self, soup):
        movimentacoes = []
        table = soup.find("tbody", {"id": "tabelaTodasMovimentacoes"})
        if not table:
            return movimentacoes
        
        rows = table.find_all("tr", class_="movimentacaoProcesso")
        for row in rows:
            data = row.find("td", class_="dataMovimentacaoProcesso").text.strip() if row.find("td", class_="dataMovimentacaoProcesso") else "Data não encontrada ou não existe."
            descricao = row.find("td", class_="descricaoMovimentacaoProcesso").text.strip() if row.find("td", class_="descricaoMovimentacaoProcesso") else "Descrição não encontrada ou não existe."
            
            removing_spaces_descricao = ' '.join(descricao.split())
            movimentacoes.append({"data": data, "descricao": removing_spaces_descricao})
            
        return movimentacoes

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
                    parts.setdefault(role, []).extend(names)
        
        return parts

    def scrape(self, num_processo):
        urls = self.get_urls()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.goto(urls['search'])
            soup = self.navigate_and_get_soup(page, num_processo)
            
            process_code = soup.find('input', {'id': 'processoSelecionado'})
            if not process_code:
                return {"error": "Desculpe, processo de grau 2 não existe ou não foi encontrado."}

            process_value = process_code.get('value')
            page.goto(f"{urls['process']}{process_value}")

            process_content = page.content()
            soup = BeautifulSoup(process_content, "html.parser")

            juiz = "Juiz não encontrado ou não existe"
            tr_element = soup.find('tr', class_='fundoClaro')

            if tr_element:
                tds = tr_element.find_all('td')
                if len(tds) >= 4:
                    juiz = tds[3].get_text(strip=True) or "Juiz não encontrado ou não existe"

            data = {
                "classe": soup.find("div", {"id": "classeProcesso"}).text.strip() if soup.find("div", {"id": "classeProcesso"}) else "Classe não foi encontrada ou não existe.",
                "area": soup.find("div", {"id": "areaProcesso"}).find("span").text.strip() if soup.find("div", {"id": "areaProcesso"}) else "Área não foi encontrada ou não existe.",
                "assunto": soup.find("div", {"id": "assuntoProcesso"}).text.strip() if soup.find("div", {"id": "assuntoProcesso"}) else "Assunto não foi encontrado ou não existe.",
                "data_distribuicao": soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}).text.split(" às ")[0] if soup.find("div", {"id": "dataHoraDistribuicaoProcesso"}) else "A data não foi encontrada ou não existe.",
                "juiz": juiz,
                "valor_acao": soup.find("div", {"id": "valorAcaoProcesso"}).text.strip() if soup.find("div", {"id": "valorAcaoProcesso"}) else "Valor não encontrado ou não existe.",
                "parte_do_processo": self.extract_parts(soup),
                "movimentacoes": self.extract_movements(soup)
            }

            return data

class TJALGrau2(TribunalGrau2):
    def get_urls(self):
        return {
            "search": "https://www2.tjal.jus.br/cposg5/search.do",
            "process": "https://www2.tjal.jus.br/cposg5/show.do?processo.codigo="
        }

class TJCEGrau2(TribunalGrau2):
    def get_urls(self):
        return {
            "search": "https://esaj.tjce.jus.br/cposg5/search.do",
            "process": "https://esaj.tjce.jus.br/cposg5/show.do?processo.codigo="
        }

def get_process_data_grau2(process_number, tribunal_name):
    tribunals = {
        "TJAL": TJALGrau2(),
        "TJCE": TJCEGrau2(),
    }
    
    if tribunal_name in tribunals:
        return tribunals[tribunal_name].scrape(process_number)
    else:
        raise ValueError("Nome do Tribunal não foi encontrado ou não existe!")

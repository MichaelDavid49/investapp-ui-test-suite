from playwright.sync_api import Page


class PortfolioPage:
    """Page Object da carteira e do formulário de aportes (US02)."""

    def __init__(self, page: Page):
        self.page = page
        self.select_ativo = page.get_by_test_id("select-asset-name")
        self.input_quantidade = page.get_by_test_id("input-asset-amount")
        self.input_preco_compra = page.get_by_test_id("input-asset-price")
        self.input_dias_investidos = page.get_by_test_id(
            "input-asset-days-invested"
        )
        self.input_dias_planejados = page.get_by_test_id(
            "input-asset-planned-days"
        )
        self.botao_adicionar = page.get_by_test_id("btn-add-asset")
        self.tabela_carteira = page.get_by_test_id("table-portfolio")
        self.linhas_tabela = self.tabela_carteira.locator("tbody tr")
        self.linhas_de_ativos = self.linhas_tabela.filter(
            has_not_text="Nenhum ativo cadastrado"
        )
        self.alerta_erro = page.get_by_test_id("portfolio-error")

    def cadastrar_aporte(
        self,
        ativo: str,
        quantidade: str,
        preco: str,
        dias_inv: str,
        dias_plan: str,
    ):
        """Preenche e submete um aporte pela interface da carteira."""
        self.select_ativo.wait_for(state="visible")
        try:
            self.select_ativo.select_option(label=ativo)
        except Exception:
            self.select_ativo.select_option(value=ativo)
        self.input_quantidade.fill(quantidade)
        self.input_preco_compra.fill(preco)
        self.input_dias_investidos.fill(dias_inv)
        self.input_dias_planejados.fill(dias_plan)
        self.botao_adicionar.click()

    def obter_linha_por_ativo(self, nome_ativo: str):
        """Retorna a última linha da tabela que corresponde ao ativo."""
        return self.linhas_tabela.filter(has_text=nome_ativo).last

    def obter_alerta_erro(self):
        """Expõe o alerta da carteira para asserções do teste."""
        return self.alerta_erro

    def total_de_ativos_listados(self) -> int:
        """Conta registros reais, ignorando a mensagem de carteira vazia."""
        self.tabela_carteira.wait_for(state="visible")
        return self.linhas_de_ativos.count()

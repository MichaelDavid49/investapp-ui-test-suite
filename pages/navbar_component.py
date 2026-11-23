
class NavbarComponent:
    """Componente responsável pela navegação principal do InvestApp."""

    def __init__(self, page):
        self.page = page

        self.botao_portfolio = page.get_by_test_id("nav-portfolio")
        self.botao_simulador_rentabilidade = page.get_by_test_id(
            "nav-yield-sim"
        )
        self.botao_simulador_imposto = page.get_by_test_id(
            "nav-tax-sim"
        )
        self.botao_gerenciar_taxas = page.get_by_test_id(
            "nav-asset-rates"
        )
        self.botao_sair = page.get_by_test_id("btn-logout")

    def acessar_portfolio(self):
        self.botao_portfolio.click()

    def acessar_simulador_rentabilidade(self):
        self.botao_simulador_rentabilidade.click()

    def acessar_simulador_imposto(self):
        self.botao_simulador_imposto.click()

    def acessar_gerenciar_taxas(self):
        self.botao_gerenciar_taxas.click()

    def realizar_logout(self):
        self.botao_sair.click()


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

    def navegar_para_carteira(self):
        """Abre a carteira e aguarda a carga inicial dos investimentos."""
        with self.page.expect_response(
            lambda resposta: (
                "/api/investments" in resposta.url
                and resposta.request.method == "GET"
            ),
            timeout=20000,
        ) as resposta_info:
            self.acessar_portfolio()

        resposta = resposta_info.value
        if resposta.status != 200:
            raise AssertionError(
                f"Falha ao carregar a carteira: HTTP {resposta.status}"
            )

        # Aguarda a SPA aplicar os dados da resposta à tabela antes das asserções.
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_test_id("table-portfolio").wait_for(
            state="visible"
        )
        investimentos = resposta.json()
        if not isinstance(investimentos, list):
            raise AssertionError(
                "A resposta da carteira não contém uma lista de investimentos."
            )
        return len(investimentos)

    def acessar_simulador_rentabilidade(self):
        self.botao_simulador_rentabilidade.click()

    def acessar_simulador_imposto(self):
        self.botao_simulador_imposto.click()

    def acessar_gerenciar_taxas(self):
        self.botao_gerenciar_taxas.click()

    def realizar_logout(self):
        self.botao_sair.click()

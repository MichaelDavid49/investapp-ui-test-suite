from pages.base_page import BasePage


class YieldSimulatorPage(BasePage):
    """Page Object do Simulador de Rentabilidade."""

    def __init__(self, page):
        super().__init__(page)

        # Campo de quantidade de meses
        self.campo_meses = page.get_by_test_id(
            "input-sim-months"
        )

        # Botão para calcular a evolução
        self.botao_calcular = page.get_by_test_id(
            "btn-calc-monthly"
        )

        # Tabela de evolução mês a mês
        self.grid_mensal = page.get_by_test_id(
            "table-monthly-projection"
        )

        # Tabela consolidada por tipo de ativo
        self.tabela_consolidada = page.get_by_test_id(
            "table-type-summary"
        )

        # Linhas de resultados das tabelas
        self.linhas_meses = self.grid_mensal.locator(
            "tbody tr"
        )

        self.linhas_resumo = self.tabela_consolidada.locator(
            "tbody tr"
        )

    def definir_meses(self, meses: int):
        """Define a quantidade de meses da projeção."""
        self.campo_meses.fill(str(meses))

    def calcular_evolucao(self):
        """Executa o cálculo da projeção mensal."""
        self.botao_calcular.click()

    def obter_rotulo_mes(self, indice: int):
        """Obtém o rótulo do mês em uma linha do grid."""
        return self.linhas_meses.nth(indice).locator(
            "td"
        ).first

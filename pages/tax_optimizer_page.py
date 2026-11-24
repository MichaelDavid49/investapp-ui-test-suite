"""Page Object do Otimizador Fiscal de Resgate - Integrante 6."""

import re

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class TaxOptimizerPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.campo_valor_resgate = page.get_by_role("spinbutton")

        self.botao_analisar = page.get_by_role(
            "button",
            name="Simular Otimização"
        )

        self.melhor_opcao = page.get_by_text(
            re.compile(r"Melhor\s+Opção", re.IGNORECASE)
        ).first

    def preencher_valor_resgate(self, valor: str):
        expect(self.campo_valor_resgate).to_be_visible(timeout=10000)
        self.campo_valor_resgate.fill(valor)

    def submeter_analise_fiscal(self):
        expect(self.botao_analisar).to_be_visible(timeout=10000)
        self.botao_analisar.click()

    def analisar_resgate(self, valor: str):
        self.preencher_valor_resgate(valor)
        self.submeter_analise_fiscal()

from playwright.sync_api import Dialog, Locator, Page


class PortfolioPage:
    def __init__(self, page: Page):
        self.page = page
        self.card_patrimonio_total = page.get_by_test_id(
            "summary-current-val"
        )
        self.linhas_tabela_carteira = page.get_by_test_id(
            "table-portfolio"
        ).locator("tbody tr")

    def excluir_aporte(self, linha: Locator) -> None:
        def tratar_dialogo(dialogo: Dialog) -> None:
            if dialogo.type == "confirm":
                dialogo.accept()
            else:
                dialogo.dismiss()

        botao_excluir = linha.locator(
            "[data-testid^='btn-delete-asset-']"
        )

        self.page.on("dialog", tratar_dialogo)
        try:
            botao_excluir.click()
        finally:
            self.page.remove_listener("dialog", tratar_dialogo)
    def cadastrar_aporte(
        self,
        ativo: str,
        quantidade: str,
        preco: str,
        dias_investidos: str,
        dias_planejados: str,
    ) -> None:
        menu_ativos = self.page.get_by_test_id("select-asset-name")
        opcao = menu_ativos.get_by_role("option", name=f"{ativo} (")
        menu_ativos.select_option(label=opcao.inner_text(timeout=5000))
        self.page.get_by_test_id("input-asset-amount").fill(quantidade)
        self.page.get_by_test_id("input-asset-price").fill(preco)
        self.page.get_by_test_id("input-asset-days-invested").fill(
            dias_investidos
        )
        self.page.get_by_test_id("input-asset-planned-days").fill(
            dias_planejados
        )
        self.page.get_by_test_id("btn-add-asset").click() 

    def obter_linha_por_ativo_e_prazo(
        self,
        ativo: str,
        dias_investidos: str,
        dias_planejados: str,
    ) -> Locator:
        prazo = f"{dias_investidos} / {dias_planejados} dias"
        return self.linhas_tabela_carteira.filter(
            has_text=ativo
        ).filter(has_text=prazo)
"""US04 — UI do Otimizador Fiscal de Resgate. Integrante 6: Sabrina Custodio Brito."""

from playwright.sync_api import Page, expect

from pages.navbar_component import NavbarComponent
from pages.tax_optimizer_page import TaxOptimizerPage


def test_otimizador_fiscal_exibe_melhor_opcao(
    logged_page: Page,
    navbar: NavbarComponent,
):
    """Ao analisar um resgate, exibe a melhor alternativa (menor IR).

    Pré-condição: usuário de homologação autenticado, com investimentos
    disponíveis para resgate na carteira.
    """
    navbar.acessar_simulador_imposto()
    otimizador = TaxOptimizerPage(logged_page)

    otimizador.analisar_resgate("1")

    expect(otimizador.melhor_opcao).to_be_visible(timeout=15000)

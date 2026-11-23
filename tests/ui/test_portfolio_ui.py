from playwright.sync_api import expect

from pages.portfolio_page import PortfolioPage


def test_remover_ativo_recalcula_patrimonio(logged_page, navbar):
    carteira = PortfolioPage(logged_page)
    navbar.acessar_portfolio()

    card = carteira.card_patrimonio_total
    expect(card).to_be_visible()
    patrimonio_inicial = card.inner_text()

    ativo = "Poupança"
    dias_investidos = "0"
    dias_planejados = "417"

    linha = carteira.obter_linha_por_ativo_e_prazo(
        ativo, dias_investidos, dias_planejados
    )
    expect(linha).to_have_count(0)

    carteira.cadastrar_aporte(
        ativo=ativo,
        quantidade="1000.00",
        preco="1.00",
        dias_investidos=dias_investidos,
        dias_planejados=dias_planejados,
    )

    expect(linha).to_have_count(1, timeout=10000)
    expect(card).not_to_have_text(patrimonio_inicial, timeout=10000)

    carteira.excluir_aporte(linha)

    expect(linha).to_have_count(0, timeout=10000)
    expect(card).to_have_text(patrimonio_inicial, timeout=10000)
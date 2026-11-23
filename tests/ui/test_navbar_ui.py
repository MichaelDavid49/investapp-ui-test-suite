
from playwright.sync_api import expect


def test_exibir_opcoes_do_menu(logged_page, navbar):
    expect(navbar.botao_portfolio).to_be_visible()
    expect(navbar.botao_simulador_rentabilidade).to_be_visible()
    expect(navbar.botao_simulador_imposto).to_be_visible()
    expect(navbar.botao_gerenciar_taxas).to_be_visible()
    expect(navbar.botao_sair).to_be_visible()

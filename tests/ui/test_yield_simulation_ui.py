
import pytest
from playwright.sync_api import expect

from pages.navbar_component import NavbarComponent
from pages.yield_simulator_page import YieldSimulatorPage


@pytest.mark.parametrize("meses", [1, 3, 60])
def test_projetar_rendimento_mensal(logged_page, meses):
    """Verifica a projeção para diferentes quantidades de meses."""

    navbar = NavbarComponent(logged_page)
    simulador = YieldSimulatorPage(logged_page)

    navbar.acessar_simulador_rentabilidade()

    simulador.definir_meses(meses)
    simulador.calcular_evolucao()

    expect(simulador.grid_mensal).to_be_visible()
    expect(simulador.linhas_meses).to_have_count(meses)

    expect(
        simulador.obter_rotulo_mes(0)
    ).to_contain_text("Mês 1")

    expect(
        simulador.obter_rotulo_mes(meses - 1)
    ).to_contain_text(f"Mês {meses}")

    expect(simulador.tabela_consolidada).to_be_visible()


def test_exibir_tabela_consolidada_por_tipo_ativo(logged_page):
    """Verifica a exibição da tabela consolidada."""

    navbar = NavbarComponent(logged_page)
    simulador = YieldSimulatorPage(logged_page)

    navbar.acessar_simulador_rentabilidade()

    simulador.definir_meses(3)
    simulador.calcular_evolucao()

    expect(simulador.tabela_consolidada).to_be_visible()

    expect(
        simulador.tabela_consolidada
    ).to_contain_text("Tipo de Ativo")

    expect(
        simulador.tabela_consolidada
    ).to_contain_text("Total Investido")

    expect(
        simulador.tabela_consolidada
    ).to_contain_text("Valor Final Projetado")

    expect(
        simulador.tabela_consolidada
    ).to_contain_text("Rendimento Total (%)")

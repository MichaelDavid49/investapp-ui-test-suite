import csv
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.navbar_component import NavbarComponent
from pages.portfolio_page import PortfolioPage


def carregar_dados_investimentos_csv():
    """Carrega os cenários de UI do CSV com caminho independente do CWD."""
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "dados_investimentos_ui.csv"
    )
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não localizado em: {caminho}")

    with caminho.open(mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas_obrigatorias = {
            "asset_name",
            "amount",
            "purchase_price",
            "days_invested",
            "planned_days",
            "deve_ter_sucesso",
        }
        if not colunas_obrigatorias.issubset(leitor.fieldnames or []):
            raise ValueError("O CSV não contém todas as colunas obrigatórias.")

        return [
            (
                linha["asset_name"],
                linha["amount"],
                linha["purchase_price"],
                linha["days_invested"],
                linha["planned_days"],
                linha["deve_ter_sucesso"].strip().lower() == "true",
            )
            for linha in leitor
        ]


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, deve_sucesso",
    carregar_dados_investimentos_csv(),
    ids=["poupanca-valida", "cdb-valido", "acoes-validas", "aporte-negativo"],
)
def test_cadastro_aporte_ddt_pom(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
    asset: str,
    amount: str,
    price: str,
    days: str,
    planned: str,
    deve_sucesso: bool,
):
    """Valida aportes orientados por CSV usando somente ações do POM."""
    quantidade_carregada = navbar.navegar_para_carteira()
    total_inicial = portfolio_page.total_de_ativos_listados(
        quantidade_esperada=quantidade_carregada
    )

    portfolio_page.cadastrar_aporte(
        ativo=asset,
        quantidade=amount,
        preco=price,
        dias_inv=days,
        dias_plan=planned,
    )

    if deve_sucesso:
        expect(portfolio_page.linhas_de_ativos).to_have_count(
            total_inicial + 1, timeout=60000
        )
        expect(portfolio_page.obter_linha_por_ativo(asset)).to_be_visible()
    else:
        expect(portfolio_page.linhas_de_ativos).to_have_count(
            total_inicial, timeout=5000
        )
        expect(portfolio_page.obter_alerta_erro()).to_be_visible(timeout=5000)

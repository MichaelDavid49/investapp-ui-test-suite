
import os

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.navbar_component import NavbarComponent


@pytest.fixture(scope="session")
def base_url():
    """Disponibiliza a URL principal da aplicação."""
    url = os.getenv("UI_BASE_URL")

    if not url:
        pytest.fail("UI_BASE_URL não configurada no arquivo .env")

    return url


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configura o navegador usando as variáveis do .env."""
    headless = os.getenv(
        "HEADLESS_MODE", "true"
    ).strip().lower() == "true"

    slow_mo = int(os.getenv("SLOW_MO", "0"))

    return {
        "headless": headless,
        "slow_mo": slow_mo
    }


@pytest.fixture
def login_page(page: Page):
    """Disponibiliza o Page Object da tela de login."""
    return LoginPage(page)


@pytest.fixture
def logged_page(
    page: Page,
    base_url: str,
    login_page: LoginPage
):
    """
    Abre a aplicação e realiza o login.

    Entrega aos testes uma página já autenticada.
    """
    usuario = os.getenv("TEST_USER")
    senha = os.getenv("TEST_PASSWORD")

    if not usuario or not senha:
        pytest.fail(
            "TEST_USER e TEST_PASSWORD devem estar configurados no .env"
        )

    page.goto(base_url)

    login_page.abrir_modal_login()
    login_page.preencher_credenciais(usuario, senha)
    login_page.realizar_login()

    expect(login_page.campo_usuario).not_to_be_visible(
        timeout=10000
    )

    return page


@pytest.fixture
def navbar(page: Page):
    """Disponibiliza o componente de navegação para os testes."""
    return NavbarComponent(page)

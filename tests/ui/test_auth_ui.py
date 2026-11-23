
import os

from pages.login_page import LoginPage


def test_abrir_e_fechar_modal_login(page):
    url = os.getenv("UI_BASE_URL")

    page.goto(url)

    login_page = LoginPage(page)

    # Abre o modal
    login_page.abrir_modal_login()

    # Verifica se os campos estão visíveis
    assert login_page.campo_usuario.is_visible()
    assert login_page.campo_senha.is_visible()

    # Fecha o modal
    login_page.fechar_modal()

    # Verifica se o modal foi fechado
    assert not login_page.campo_usuario.is_visible()


def test_login_com_credenciais_validas(page):
    import os

    url = os.getenv("UI_BASE_URL")
    usuario = os.getenv("TEST_USER")
    senha = os.getenv("TEST_PASSWORD")

    assert usuario, "TEST_USER não configurado no .env"
    assert senha, "TEST_PASSWORD não configurado no .env"

    page.goto(url)

    login_page = LoginPage(page)
    login_page.abrir_modal_login()

    login_page.preencher_credenciais(usuario, senha)

    with page.expect_response(
        lambda response: "/api/login" in response.url
    ) as response_info:
        login_page.realizar_login()

    response = response_info.value

    assert response.status == 200

    resultado = response.json()

    assert resultado.get("access_token")
    assert resultado.get("token_type")

    assert not login_page.campo_usuario.is_visible()


def test_login_com_credenciais_invalidas(page):
    import os

    page.goto(os.getenv("UI_BASE_URL"))

    login_page = LoginPage(page)
    login_page.abrir_modal_login()

    login_page.preencher_credenciais(
        os.getenv("TEST_USER"),
        "SenhaIncorreta123!"
    )

    with page.expect_response(
        lambda response: "/api/login" in response.url
    ) as response_info:
        login_page.realizar_login()

    response = response_info.value

    assert response.status == 400

    resultado = response.json()

    assert resultado.get("detail") == "Usuário ou senha incorretos"

    mensagem_erro = page.get_by_text(
        "Usuário ou senha incorretos",
        exact=True
    )

    assert mensagem_erro.is_visible()
    assert login_page.campo_usuario.is_visible()
    assert login_page.campo_senha.is_visible()
    
    

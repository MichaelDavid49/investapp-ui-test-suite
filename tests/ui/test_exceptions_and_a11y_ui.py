from playwright.sync_api import expect
from pages.exceptions_page import ExceptionsPage


def test_formulario_login_vazio(page, base_url):
    """CT-08-01: Verifica a rejeicao do formulario vazio."""

    page.goto(base_url)

    exceptions_page = ExceptionsPage(page)
    exceptions_page.abrir_formulario_login()

    usuario, senha = exceptions_page.obter_campos_login()

    expect(usuario).to_be_visible()
    expect(senha).to_be_visible()

    exceptions_page.preencher_login_vazio()
    exceptions_page.enviar_login()

    expect(usuario).to_be_visible()
    expect(senha).to_be_visible()

    expect(exceptions_page.obter_botao_logout()).not_to_be_visible()

    assert (
        exceptions_page.campo_login_invalido()
    ), "Os campos vazios nao apresentaram invalidade HTML."


def test_diagnostico_validacao_html_aporte_negativo(logged_page):
    """
    CT-08-02: Diagnostico HTML de quantidade negativa.

    Nao cadastra investimentos e nao comprova rejeicao.
    """
    tela = ExceptionsPage(logged_page)

    tela.acessar_carteira_e_aguardar()
    tela.preencher_aporte_negativo()

    expect(tela.obter_campo_quantidade()).to_have_value("-10")

    resultado = tela.verificar_validade_quantidade()

    print("VALOR TESTADO:", resultado["valor"])
    print("VALIDO HTML:", resultado["valido"])
    print("MENSAGEM HTML:", resultado["mensagem"])

    assert resultado["valor"] == "-10"


def calcular_luminancia(cor):
    """Calcula luminancia relativa para cores RGB."""

    componentes = [
        int(valor)
        for valor in cor.replace("rgb(", "").replace(")", "").split(",")
    ]

    valores = []

    for componente in componentes:
        canal = componente / 255

        if canal <= 0.04045:
            valores.append(canal / 12.92)
        else:
            valores.append(((canal + 0.055) / 1.055) ** 2.4)

    return 0.2126 * valores[0] + 0.7152 * valores[1] + 0.0722 * valores[2]


def test_contraste_botao_adicionar(logged_page, navbar):
    """CT-08-04: Verifica contraste do botao Adicionar."""

    navbar.acessar_portfolio()

    exceptions_page = ExceptionsPage(logged_page)
    cores = exceptions_page.obter_cores_botao_adicionar()

    luminancia_texto = calcular_luminancia(cores["texto"])
    luminancia_fundo = calcular_luminancia(cores["fundo"])

    maior = max(luminancia_texto, luminancia_fundo)
    menor = min(luminancia_texto, luminancia_fundo)

    contraste = (maior + 0.05) / (menor + 0.05)

    print(f"CONTRASTE CALCULADO: {contraste:.2f}:1")

    assert contraste >= 4.5, f"Contraste insuficiente: {contraste:.2f}:1"

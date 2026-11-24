from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.navbar_component import NavbarComponent


class ExceptionsPage:
    """Page Object dos cenarios negativos."""

    def __init__(self, page: Page):
        self.page = page
        self.login = LoginPage(page)
        self.navbar = NavbarComponent(page)

    def abrir_formulario_login(self):
        self.login.abrir_modal_login()

    def preencher_login_vazio(self):
        self.login.campo_usuario.fill("")
        self.login.campo_senha.fill("")

    def enviar_login(self):
        self.login.realizar_login()

    def obter_campos_login(self):
        return self.login.campo_usuario, self.login.campo_senha

    def obter_botao_logout(self):
        return self.navbar.botao_sair

    def campo_login_invalido(self):
        usuario_invalido = self.login.campo_usuario.evaluate(
            "(element) => !element.checkValidity()"
        )
        senha_invalida = self.login.campo_senha.evaluate(
            "(element) => !element.checkValidity()"
        )
        return usuario_invalido or senha_invalida

    def preencher_aporte_negativo(self):
        """Preenche um aporte com quantidade negativa."""
        self.page.get_by_test_id("input-asset-amount").fill("-10")

        self.page.get_by_test_id("input-asset-price").fill("1")

    def obter_campo_quantidade(self):
        return self.page.get_by_test_id("input-asset-amount")

    def obter_botao_adicionar(self):
        return self.page.get_by_test_id("btn-add-asset")

    def obter_total_linhas_carteira(self):
        """Conta somente investimentos reais."""

        tabela = self.page.get_by_test_id("table-portfolio")
        tabela.wait_for(state="visible")

        linhas = tabela.locator("tbody tr")

        linhas_reais = linhas.filter(has_not_text="Nenhum ativo cadastrado")

        return linhas_reais.count()

    def obter_atributos_quantidade(self):
        """Consulta os atributos HTML do campo quantidade."""
        campo = self.page.get_by_test_id("input-asset-amount")

        return {
            "type": campo.get_attribute("type"),
            "min": campo.get_attribute("min"),
            "max": campo.get_attribute("max"),
            "required": campo.get_attribute("required"),
            "disabled": campo.get_attribute("disabled"),
            "readonly": campo.get_attribute("readonly"),
            "aria-disabled": campo.get_attribute("aria-disabled"),
        }

    def obter_cores_botao_adicionar(self):
        """Consulta as cores CSS do botao Adicionar."""
        botao = self.page.get_by_test_id("btn-add-asset")

        return botao.evaluate("""(elemento) => {
                const estilo = getComputedStyle(elemento);
                return {
                    texto: estilo.color,
                    fundo: estilo.backgroundColor
                };
            }""")

    def verificar_validade_quantidade(self):
        """Consulta a validade HTML do campo de quantidade."""

        campo = self.page.get_by_test_id("input-asset-amount")

        return campo.evaluate("""(elemento) => ({
                valor: elemento.value,
                valido: elemento.checkValidity(),
                mensagem: elemento.validationMessage
            })""")

    def acessar_carteira_e_aguardar(self):
        """Acessa a carteira e aguarda a resposta da API."""

        with self.page.expect_response(
            lambda resposta: (
                "/api/investments" in resposta.url
                and resposta.request.method == "GET"
            ),
            timeout=20000,
        ) as resposta_info:
            self.navbar.acessar_portfolio()

        resposta = resposta_info.value

        assert (
            resposta.status == 200
        ), f"Erro ao carregar investimentos: HTTP {resposta.status}"

        self.page.get_by_test_id("table-portfolio").wait_for(state="visible")

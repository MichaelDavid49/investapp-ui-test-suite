from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page, base_url=""):
        super().__init__(page, base_url)

        # Botões para abrir o modal
        self.botao_entrar_sistema = page.get_by_test_id("btn-open-login")
        self.botao_fazer_login = page.get_by_test_id("hero-login-btn")

        # Campos de autenticação
        self.campo_usuario = page.get_by_test_id("input-username")
        self.campo_senha = page.get_by_test_id("input-password")

        # Botões do modal
        self.botao_entrar = page.get_by_test_id("btn-submit-login")
        self.botao_cancelar = page.get_by_role("button", name="Cancelar")
        self.botao_fechar = page.locator(".btn-close-modal")

        # Mensagem de erro
        self.mensagem_erro = page.get_by_text(
            "Usuário ou senha incorretos",
            exact=True
        )

    def abrir_modal_login(self):
        self.botao_fazer_login.click()

    def preencher_credenciais(self, usuario, senha):
        self.campo_usuario.fill(usuario)
        self.campo_senha.fill(senha)

    def realizar_login(self):
        self.botao_entrar.click()

    def cancelar_login(self):
        self.botao_cancelar.click()

    def fechar_modal(self):
        self.botao_fechar.click()

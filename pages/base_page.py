
class BasePage:
    """Classe base para os Page Objects do projeto."""

    def __init__(self, page, base_url=""):
        self.page = page
        self.base_url = base_url

    def navegar(self, path=""):
        """Navega para a URL principal ou para um caminho informado."""
        url_destino = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url_destino)

    def obter_titulo(self):
        """Retorna o título da página atual."""
        return self.page.title()

    def recarregar(self):
        """Recarrega a página atual."""
        self.page.reload()

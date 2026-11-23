
# InvestApp - UI Test Suite

Projeto de automação de testes de interface web da aplicação InvestApp, desenvolvido com Python, Pytest e Playwright.

## Tecnologias

- Python
- Pytest
- Playwright
- pytest-playwright
- pytest-dotenv
- pytest-cov
- pytest-html
- Flake8

## Pré-requisitos

- Python instalado
- Git instalado
- Visual Studio Code (recomendado)

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/MichaelDavid49/investapp-ui-test-suite.git
cd investapp-ui-test-suite
```

### 2. Criar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Instalar o navegador do Playwright

```powershell
playwright install chromium
```

### 5. Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Preencha o arquivo `.env` com as credenciais individuais de teste.

Não compartilhe esse arquivo e não o envie ao GitHub.

## Executar os testes

Executar toda a suíte:

```powershell
python -m pytest tests/ui -v
```

Executar somente os testes de autenticação:

```powershell
python -m pytest tests/ui/test_auth_ui.py -v
```

Executar somente os testes de navegação:

```powershell
python -m pytest tests/ui/test_navbar_ui.py -v
```

## Estrutura do projeto

```text
investapp-ui-test-suite/
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── navbar_component.py
│
├── tests/
│   └── ui/
│       ├── test_auth_ui.py
│       ├── test_home_ui.py
│       └── test_navbar_ui.py
│
├── .env.example
├── .gitignore
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Padrão de desenvolvimento

O projeto utiliza Page Object Model (POM).

- Os seletores e ações da interface devem ficar dentro de `pages/`.
- Os testes devem ficar dentro de `tests/ui/`.
- Os testes devem validar comportamentos e resultados, sem implementar seletores diretamente.
- As fixtures compartilhadas devem ser centralizadas no `conftest.py`.

## Regras para contribuição

1. Atualize sua branch antes de iniciar alterações.
2. Desenvolva somente os arquivos atribuídos a você.
3. Execute os testes antes de enviar suas alterações.
4. Não envie arquivos `.env`, ambientes virtuais ou credenciais.
5. Utilize commits com mensagens claras.
6. Não altere arquivos de outro integrante sem alinhamento com a equipe.

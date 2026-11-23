import os


def test_abrir_aplicacao(page):
    url = os.getenv("UI_BASE_URL")

    response = page.goto(url)

    assert response is not None
    assert response.status == 200
    assert page.url == url

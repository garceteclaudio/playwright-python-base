import time
from behave import given, when, then

URL = "https://www.saucedemo.com/"

@given("el usuario abre la página de login")
def step_abrir_pagina(context):
    print("--------- El user abre la pagina para logear")
    context.page.goto(URL)

@when('ingresa el usuario "{username}" y contraseña "{password}"')
def step_ingresar_credenciales(context, username, password):
    print("--------- Se ingresa usuario y contraseña")
    context.page.fill("#user-name", username)
    context.page.fill("#password", password)
    context.page.click("#login-button")
    time.sleep(1)  # pequeña espera para que cargue

@then("debería ver la página de inventario")
def step_validar_inventario(context):
    print("--------- Validar home")
    assert context.page.url.endswith("/inventory.html"), f"URL actual: {context.page.url}"

@then('debería ver un error que contiene "{mensaje}"')
def step_validar_error(context, mensaje):
    error = context.page.locator("h3[data-test='error']")
    assert mensaje.lower() in error.text_content().lower()

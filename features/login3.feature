Feature: Login en SauceDemo
  Como usuario de la app
  Quiero poder iniciar sesión
  Para acceder al inventario

  @login
  Scenario: Login3
    Given el usuario abre la página de login
    When ingresa el usuario "standard_user" y contraseña "secret_sauce"
    Then debería ver la página de inventario


  @login
  Scenario: Login3.1
    Given el usuario abre la página de login
    When ingresa el usuario "standard_user" y contraseña "secret_sauce"
    Then debería ver la página de inventario


Feature: Login en SauceDemo
  Como usuario de la app
  Quiero poder iniciar sesión
  Para acceder al inventario

  @login @test12345
  Scenario: Login exitoso con usuario válido
    Given el usuario abre la página de login
    When ingresa el usuario "standard_user" y contraseña "secret_sauce"
    Then debería ver la página de inventario
  @login
  Scenario: Login fallido con usuario bloqueado
    Given el usuario abre la página de login
    When ingresa el usuario "locked_out_user" y contraseña "secret_sauce"
    Then debería ver un error que contiene "locked out"
  @login
  Scenario: Login fallido con credenciales incorrectas
    Given el usuario abre la página de login
    When ingresa el usuario "fake_user" y contraseña "bad_pass"
    Then debería ver un error que contiene "username and password do not match"

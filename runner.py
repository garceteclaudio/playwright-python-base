from behave.__main__ import main as behavemain
import subprocess
import sys
import shutil
import os

# ===============================
# Limpiar reportes anteriores
# ===============================
folders_to_remove = ["reports", "allure-html", "output"]
for folder in folders_to_remove:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Se eliminó la carpeta: {folder}")

# ===============================
# Configuración de tags
# ===============================
tags_value = "@login"  # Cambiar según necesidad
behave_command = f"--tags={tags_value} -f allure_behave.formatter:AllureFormatter -o reports/ features"

# ===============================
# Ejecutar Behave
# ===============================
print("🚀 Ejecutando tests con Behave...")
exit_code = behavemain(behave_command.split())

if exit_code != 0:
    print(f"❌ Tests fallaron con exit code {exit_code}. Se omite generación de reporte.")
    sys.exit(exit_code)

print("✅ Tests completados. Generando reporte Allure HTML...")
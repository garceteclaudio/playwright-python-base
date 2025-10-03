import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import allure

# ============================
# Función para limpiar nombres
# ============================
def clean_filename(name: str) -> str:
    # Reemplaza cualquier carácter que no sea alfanumérico, guion o guion bajo
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# ============================
# Hooks de Behave
# ============================

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)

def before_scenario(context, scenario):
    context.page = context.browser.new_page()
    context.screenshot_dir = Path(f"reports/screenshots/{clean_filename(scenario.name)}")
    context.screenshot_dir.mkdir(parents=True, exist_ok=True)
    context.step_counter = 1

def after_step(context, step):
    filename = f"step_{context.step_counter}_{clean_filename(step.name)}.png"
    screenshot_path = context.screenshot_dir / filename
    context.page.screenshot(path=str(screenshot_path))

    # Adjuntar a Allure
    with open(screenshot_path, "rb") as image_file:
        allure.attach(image_file.read(), name=step.name, attachment_type=allure.attachment_type.PNG)

    context.step_counter += 1

def after_scenario(context, scenario):
    context.page.close()

def after_all(context):
    context.browser.close()
    context.playwright.stop()

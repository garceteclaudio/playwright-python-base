import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import allure
import os

# ============================
# Función para limpiar nombres
# ============================
def clean_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?* ]+', '_', name)

# ============================
# Hooks de Behave / BehaveX
# ============================

def before_all(context):
    context.playwright = sync_playwright().start()

def before_scenario(context, scenario):
    # Lanzar el browser por proceso → más estable con BehaveX
    context.browser = context.playwright.chromium.launch(headless=True)
    context.page = context.browser.new_page()

    # Carpeta de screenshots por escenario
    pid = os.getpid()
    folder_name = f"{clean_filename(scenario.name)}_{pid}"
    context.screenshot_dir = Path(f"reports/screenshots/{folder_name}")
    context.screenshot_dir.mkdir(parents=True, exist_ok=True)

    context.step_counter = 1

def after_step(context, step):
    filename = f"step_{context.step_counter}_{clean_filename(step.name)}.png"
    screenshot_path = context.screenshot_dir / filename
    context.page.screenshot(path=str(screenshot_path))

    # Adjuntar a ALLURE (forma compatible)
    allure.attach(
        body=open(screenshot_path, "rb").read(),
        name=f"Step {context.step_counter}: {step.name}",
        attachment_type=allure.attachment_type.PNG
    )
    context.step_counter += 1

def after_scenario(context, scenario):
    context.page.close()
    context.browser.close()

def after_all(context):
    context.playwright.stop()

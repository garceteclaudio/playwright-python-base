import os
import shutil
import subprocess
from pathlib import Path
import platform

ROOT_DIR = Path("reports")
MERGED_DIR = Path("allure-generated-merged-results")
OUTPUT_DIR = Path("allure-report")

# =====================================
# Detectar ruta de Allure (multiplataforma)
# =====================================
def find_allure_command():
    system = platform.system()
    home = Path.home()

    possible_paths = ["allure"]  # intentar primero en PATH

    if system == "Windows":
        possible_paths += [
            "allure.bat",
            r"C:\Program Files\Allure\bin\allure.bat",
            home / "scoop" / "apps" / "allure" / "current" / "bin" / "allure.bat",
        ]

    if system in ("Linux", "Darwin"):  # Darwin = macOS
        possible_paths += [
            "/usr/local/bin/allure",
            "/opt/homebrew/bin/allure",   # macOS M1/M2/M3
            "/usr/bin/allure",
        ]

    for cmd in possible_paths:
        try:
            subprocess.run(
                [str(cmd), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"✔ Allure encontrado: {cmd}")
            return str(cmd)
        except Exception:
            pass

    raise FileNotFoundError(
        "❌ No se encontró Allure.\n"
        "Instalar:\n"
        "Windows → scoop install allure\n"
        "macOS → brew install allure\n"
        "Linux → instalar manualmente desde GitHub"
    )

# =====================================
# Manejo de carpetas
# =====================================
def clean_and_create_dir(directory: Path):
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)

def merge_allure_results():
    print(f"🔍 Buscando carpetas dentro de: {ROOT_DIR}")
    clean_and_create_dir(MERGED_DIR)

    for subfolder in ROOT_DIR.iterdir():
        if subfolder.is_dir():
            print(f"📁 Copiando resultados desde: {subfolder}")
            for item in subfolder.rglob("*"):
                if item.is_file():
                    target_path = MERGED_DIR / item.relative_to(subfolder)
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_path)

    print("✅ Merge completado.")

# =====================================
# Generar reporte final
# =====================================
def generate_allure_report():
    allure_cmd = find_allure_command()

    print("⚙️ Generando reporte Allure...")

    base_cmd = [
        allure_cmd,
        "generate",
        str(MERGED_DIR),
        "-o",
        str(OUTPUT_DIR),
        "--clean"
    ]

    # intentar single-file
    try:
        subprocess.run(base_cmd + ["--single-file"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ --single-file no soportado. Generando reporte normal...")
        subprocess.run(base_cmd, check=True)

    print(f"🎉 Reporte generado en: {OUTPUT_DIR}/index.html")

# =====================================
def main():
    merge_allure_results()
    generate_allure_report()

if __name__ == "__main__":
    main()

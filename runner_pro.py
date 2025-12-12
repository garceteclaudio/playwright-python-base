import os
import sys
import shutil
import subprocess
import datetime
import multiprocessing
from pathlib import Path
from functools import partial
from concurrent.futures import ProcessPoolExecutor, as_completed

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn

console = Console()

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
TAGS = "@test12345"
FEATURES_DIR = "features"

# Timeout por ejecución en segundos
FEATURE_TIMEOUT = 600   # 10 minutos

# Reportes con timestamp (mantener histórico)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_ROOT = Path(f"reports_{timestamp}")

REPORTS_DIR = REPORT_ROOT / "reports"
OUTPUT_DIR = REPORT_ROOT / "output"
JUNIT_DIR = REPORT_ROOT / "Reportes" / "reportXML"


# ==========================================================
# Función: limpieza de directorios (solo main)
# ==========================================================
def clean_and_prepare_folders():
    console.print("[yellow]🧹 Limpiando reportes anteriores...[/]")

    if REPORT_ROOT.exists():
        shutil.rmtree(REPORT_ROOT, ignore_errors=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JUNIT_DIR.mkdir(parents=True, exist_ok=True)

    console.print(f"[green]✔ Directorios preparados en:[/] {REPORT_ROOT}")


# ==========================================================
# Buscar features que contienen el tag
# ==========================================================
def find_features_with_tag(directory, tag):
    matching = []

    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".feature"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                if tag in content:
                    matching.append(path)

    return matching


# ==========================================================
# Ejecutar una feature
# ==========================================================
def run_feature(feature_file, tags):
    feature_name = os.path.splitext(os.path.basename(feature_file))[0]

    report_folder = REPORTS_DIR / feature_name
    report_folder.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{feature_name}.behave.output"

    behave_command = [
        "behave",
        feature_file,
        "--tags", tags,
        "--summary",
        "--show-timings",
        "--verbose",
        "--format", "pretty",
        "--outfile", str(output_file),
        "--junit",
        "--junit-directory", str(JUNIT_DIR),
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", str(report_folder)
    ]

    try:
        result = subprocess.run(
            behave_command,
            timeout=FEATURE_TIMEOUT
        )
        return (feature_file, result.returncode)

    except subprocess.TimeoutExpired:
        return (feature_file, -9)  # código custom de timeout

    except Exception as e:
        return (feature_file, -99)


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    console.print("\n[bold cyan]🚀 RUNNER PRO · Ejecución Paralela de Features[/]\n")

    # limpiar / preparar
    clean_and_prepare_folders()

    # buscar solo features que tienen el tag
    features = find_features_with_tag(FEATURES_DIR, TAGS)

    if not features:
        console.print(f"[red]⚠ No se encontraron features con el tag {TAGS}[/]")
        sys.exit(1)

    # Tabla inicial
    table = Table(title="Features seleccionadas")
    table.add_column("Feature")
    table.add_column("Ruta completa")
    for f in features:
        table.add_row(Path(f).name, f)
    console.print(table)

    console.print(f"\n[green]✔ {len(features)} features serán ejecutadas[/] con el tag [bold]{TAGS}[/]\n")

    # Configurar procesos según CPU
    max_workers = max(1, multiprocessing.cpu_count() - 1)
    workers_to_use = min(max_workers, len(features))

    console.print(f"[cyan]🌐 Ejecutando con {workers_to_use} workers paralelos[/]\n")

    run_with_tags = partial(run_feature, tags=TAGS)

    results = []

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        task = progress.add_task("Procesando features…", total=len(features))

        with ProcessPoolExecutor(max_workers=workers_to_use) as executor:
            futures = {executor.submit(run_with_tags, f): f for f in features}

            for future in as_completed(futures):
                feature_file = futures[future]
                result = future.result()
                results.append(result)

                progress.update(task, advance=1)

    # ==========================================================
    # RESULTADOS
    # ==========================================================

    console.print("\n\n[bold cyan]📊 RESULTADOS[/]\n")

    result_table = Table(title="Resumen de ejecución")
    result_table.add_column("Feature", style="white")
    result_table.add_column("Estado", style="white")

    failed = 0

    for feature, code in results:
        name = Path(feature).name

        if code == 0:
            result_table.add_row(name, "[green]✔ OK")
        elif code == -9:
            result_table.add_row(name, "[yellow]⏳ Timeout")
            failed += 1
        else:
            result_table.add_row(name, "[red]❌ Error")
            failed += 1

    console.print(result_table)

    if failed == 0:
        console.print("[bold green]\n🎉 TODAS LAS FEATURES PASARON CORRECTAMENTE[/]\n")
        sys.exit(0)
    else:
        console.print(f"[bold red]\n❌ {failed} features fallaron o tuvieron errores.[/]\n")
        sys.exit(1)

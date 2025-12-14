import os
import sys
import shutil
import subprocess
from multiprocessing import Pool
from functools import partial

# ============================================
# CONFIGURACIÓN
# ============================================
TAGS = "@test12345"
FEATURES_DIR = "features"
MAX_PROCESSES = 3


# ============================================
# 1) LIMPIAR CARPETAS (solo proceso principal)
# ============================================
def clean_folders():
    folders_to_remove = ["allure-report","reports", "allure-html", "output", "Reportes", "allure-generated-merged-results"]
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f"🧹 Se eliminó la carpeta: {folder}")

    os.makedirs("reports", exist_ok=True)
    os.makedirs("output", exist_ok=True)


# ============================================
# 2) BUSCAR .feature QUE CONTENGAN EL TAG
# ============================================
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


# ============================================
# 3) EJECUTAR UN ARCHIVO FEATURE
# ============================================
def run_feature(feature_file, tags):
    feature_name = os.path.splitext(os.path.basename(feature_file))[0]
    report_folder = os.path.join("reports", feature_name)
    os.makedirs(report_folder, exist_ok=True)

    output_file = os.path.join("output", f"{feature_name}.behave.output")

    behave_command = [
        "behave",
        feature_file,
        "--tags", tags,
        "--summary",
        "--show-timings",
        "--verbose",
        "--format", "pretty",
        "--outfile", output_file,
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", report_folder
    ]

    print(f"🚀 Ejecutando: {feature_file}")

    result = subprocess.run(behave_command)

    if result.returncode != 0:
        print(f"❌ Falló: {feature_file}")
    else:
        print(f"✅ Completado: {feature_file} → {output_file}")

    return result.returncode


# ============================================
# 4) MAIN (solo proceso principal)
# ============================================
if __name__ == "__main__":
    clean_folders()

    # Obtener solo features con el tag
    features = find_features_with_tag(FEATURES_DIR, TAGS)

    if not features:
        print(f"⚠️ No se encontraron features con el tag {TAGS}")
        sys.exit(1)

    print(f"📂 Ejecutando {len(features)} features con el tag {TAGS}")

    run_with_tags = partial(run_feature, tags=TAGS)
    num_processes = min(len(features), MAX_PROCESSES)

    with Pool(processes=num_processes) as pool:
        results = [pool.apply_async(run_with_tags, args=(feature,)) for feature in features]
        pool.close()
        pool.join()

        exit_codes = [r.get() for r in results]

    if any(code != 0 for code in exit_codes):
        print("❌ Algunas pruebas fallaron.")
        sys.exit(1)

    print("✅ Todas las pruebas finalizaron correctamente.")

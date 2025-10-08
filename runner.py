import os
import sys
import shutil
import subprocess
from multiprocessing import Pool
from functools import partial

# ===============================
# Limpiar reportes anteriores
# ===============================
folders_to_remove = ["reports", "allure-html", "output", "Reportes"]
for folder in folders_to_remove:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"🧹 Se eliminó la carpeta: {folder}")

os.makedirs("reports", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("Reportes/reportXML", exist_ok=True)

# ===============================
# Configuración de tags
# ===============================
TAGS = "@login"  # Cambiar según necesidad
FEATURES_DIR = "features"

# ===============================
# Buscar archivos .feature
# ===============================
def get_feature_files(directory):
    feature_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".feature"):
                feature_files.append(os.path.join(root, f))
    return feature_files

# ===============================
# Función para ejecutar un archivo .feature
# ===============================
def run_feature(feature_file, tags):
    feature_name = os.path.splitext(os.path.basename(feature_file))[0]
    report_folder = os.path.join("reports", feature_name)
    os.makedirs(report_folder, exist_ok=True)

    # Archivo behave.output único por feature
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
        "--junit",
        "--junit-directory", "Reportes/reportXML",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", report_folder
    ]

    print(f"🚀 Ejecutando en paralelo: {feature_file}")
    # 🟢 Ejecutar Behave en tiempo real mostrando logs en consola
    result = subprocess.run(behave_command)

    if result.returncode != 0:
        print(f"❌ Falló: {feature_file}")
    else:
        print(f"✅ Completado: {feature_file} → {output_file}")

    return result.returncode

# ===============================
# Ejecutar en paralelo
# ===============================
if __name__ == "__main__":
    features = get_feature_files(FEATURES_DIR)

    if not features:
        print("⚠️ No se encontraron archivos .feature.")
        sys.exit(1)

    print(f"📂 Se encontraron {len(features)} archivos .feature.")
    run_with_tags = partial(run_feature, tags=TAGS)

    # Máximo 3 procesos en paralelo
    num_processes = min(len(features), 3)

    with Pool(processes=num_processes) as pool:
        results = [pool.apply_async(run_with_tags, args=(feature,)) for feature in features]
        pool.close()
        pool.join()

        exit_codes = [r.get() for r in results]

    # ===============================
    # Verificar resultados
    # ===============================
    if any(code != 0 for code in exit_codes):
        print("❌ Algunas pruebas fallaron.")
        sys.exit(1)

    print("✅ Todas las pruebas finalizaron correctamente.")

FROM ubuntu:24.04

# -------------------------------
# Dependencias del sistema
# -------------------------------
RUN apt update && apt install -y \
    software-properties-common \
    wget unzip curl gnupg default-jre \
    python3.12 python3.12-venv python3-pip \
    apt-transport-https \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 \
    libpango-1.0-0 libglib2.0-0 libxshmfence1 libgbm1 \
    libasound2t64 libx11-xcb1 libxtst6 libdrm2 \
    libxcb-dri3-0 libxfixes3 libffi8 libwoff1 \
    libharfbuzz-icu0 \
    && apt clean

RUN ln -sf /usr/bin/python3.12 /usr/bin/python3

# -------------------------------
# Node.js 20 (requerido por Playwright)
# -------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt install -y nodejs && apt clean

# -------------------------------
# Workdir de la aplicación
# -------------------------------
WORKDIR /app

# -------------------------------
# Copiar requirements e instalar dependencias Python
# -------------------------------
COPY requirements.txt .
RUN pip install --break-system-packages -r requirements.txt

# Asegurar que Behave esté instalado
RUN pip install --break-system-packages behave

# Instalar Playwright únicamente
RUN pip install --break-system-packages playwright

# -------------------------------
# Copiar el proyecto completo
# -------------------------------
COPY . .

# -------------------------------
# Instalar navegadores de Playwright
# -------------------------------
RUN playwright install --with-deps chromium firefox webkit

# -------------------------------
# Instalar Allure CLI
# -------------------------------
RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip && \
    unzip allure-2.29.0.zip && mv allure-2.29.0 /opt/allure && \
    ln -sf /opt/allure/bin/allure /usr/local/bin/allure && \
    rm allure-2.29.0.zip

# -------------------------------
# Variables de entorno
# -------------------------------
ENV PLAYWRIGHT_HEADLESS=1
ENV USERNAME=testing
ENV PASSWORD=testing

# -------------------------------
# Comando por defecto
# -------------------------------
CMD ["python3", "runner.py"]
